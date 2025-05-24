from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
from peft import PeftModel

from transformers import TextIteratorStreamer
import threading

from config_log import get_logger
logger = get_logger(__name__)



class Summarimer:
    def __init__(self, base_model: str, mmodel_name : str, device: str , framework : str = 'pt'):
        self.base_model = AutoModelForSeq2SeqLM.from_pretrained(base_model)
        self.model = PeftModel.from_pretrained(self.base_model, mmodel_name)
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(mmodel_name)
        self.summarizer = pipeline(   
                task="summarization",
                model= self.model,
                tokenizer= self.tokenizer,
                framework = framework,
                )
    
    def estimate_max_length(self, text: str, max_cap: int, ratio: float ) -> int:
        """
        Estimates the maximum length of the text.
        
        Args:
            text (str): The text to estimate the length for.
        
        Returns:
            int: The estimated maximum length.
        """
        length_text = int(len(text.split()) * 1.5 * ratio) if int(len(text.split()) * 1.5 * ratio) else int(len(text.split()) * 1.5 )
        return min(length_text, max_cap)

    def split_into_chunks(self, text: str, max_tokens: int) -> list:
        """
        Splits the text into chunks based on the maximum number of tokens.
        parameters:
            text (str): The text to split.
            max_tokens (int): The maximum number of tokens per chunk.
        returns:
            list: A list of text chunks.
        """
        sentences = text.split('. ')
        chunks, current_chunk = [], []

        current_len = 0
        for sentence in sentences:
            token_len = int(len(sentence.split())  * 1.5 )
            if current_len + token_len > max_tokens:
                chunks.append('. '.join(current_chunk))
                current_chunk = [sentence]
                current_len = token_len
            else:
                current_chunk.append(sentence)
                current_len += token_len
        if current_chunk:
            chunks.append('. '.join(current_chunk))
        return chunks

    def join_summaries(self, summaries: list) -> str:
        """
        Joins the summaries into a single string.
        parameters:
            summaries (list): A list of summaries to join.
        returns:
            str: The joined summaries.
        """
        return ' '.join(summaries)

    def summarize(self, text: str, max_cap: int = 512 , ratio : float = 0.7) -> str:
        """
        Summarizes the given text using the loaded model.
        
        Args:
            text (str): The text to summarize.
        
        Returns:
            str: The summarized text.
        """
        tokenized_len  = len(text.split()) * 1.5
        if tokenized_len < 100:
            logger.info(f"Text is too short to summarize, returning original text.")
            return text
        elif 100 <= tokenized_len <= 1024:
            logger.info(f"Text is within the summarization range, proceeding with summarization.")
            max_length = self.estimate_max_length(text, max_cap= max_cap, ratio= ratio)
            if max_length <= 0:
                raise ValueError("max_length must be greater than 0")
            summary = self.summarizer(
                text,
                max_new_tokens= max_length,
                do_sample= True,
                temperature= 0.3,
                repetition_penalty=1.2,
                top_p=0.9,
            )
            return summary[0]['summary_text']
        else:
            logger.info(f"Text is too long, splitting into chunks for summarization.")
            # Nếu quá dài, nên chia nhỏ trước
            chunks = self.split_into_chunks(text, max_tokens=1024)
            summaries = [self.summarizer(chunk, max_new_tokens= 256, do_sample= True, temperature= 0.5, repetition_penalty= 1.2, top_p= 0.9)[0]['summary_text'] for chunk in chunks]
            return self.join_summaries(summaries)

    def summarize_stream(self, text: str, max_cap: int = 512, ratio: float = 0.7):
        """
        Trả về generator streaming các token tóm tắt.
        """
        tokenized_len = len(text.split()) * 1.5
        if tokenized_len < 100:
            logger.info(f"Text is too short to summarize, returning original text.")
            for token in text.split():
                yield token + " "
            return
        elif 100 <= tokenized_len <= 1024:
            logger.info(f"Text is within the summarization range, proceeding with streaming summarization.")
            # estimate độ dài tối đa
            max_length = self.estimate_max_length(text, max_cap, ratio)
            if max_length <= 0:
                raise ValueError("max_length phải > 0")
            
            # chuẩn hóa đầu vào thành tokens
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # khởi tạo streamer
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
            
            # prepare generate kwargs
            gen_kwargs = dict(
                **inputs,
                max_new_tokens=max_length,
                do_sample=True,
                temperature=0.3,
                repetition_penalty=1.2,
                top_p=0.9,
                streamer=streamer,
            )
            
            # chạy generate trên một thread riêng
            thread = threading.Thread(target=self.model.generate, kwargs=gen_kwargs)
            thread.start()
            
            # yield dần từng token
            for chunk in streamer:
                yield chunk

            thread.join()
        else:
            logger.info(f"Text is too long, splitting into chunks for streaming summarization.")
            # Nếu quá dài, chia nhỏ trước
            chunks = self.split_into_chunks(text, max_tokens=1024)
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                # Xử lý từng chunk và stream kết quả
                inputs = self.tokenizer(chunk, return_tensors="pt").to(self.device)
                streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
                
                gen_kwargs = dict(
                    **inputs,
                    max_new_tokens=256,
                    do_sample=True,
                    temperature=0.5,
                    repetition_penalty=1.2,
                    top_p=0.9,
                    streamer=streamer,
                )
                
                thread = threading.Thread(target=self.model.generate, kwargs=gen_kwargs)
                thread.start()
                
                # Stream kết quả của chunk hiện tại
                for chunk_result in streamer:
                    yield chunk_result
                
                thread.join()
                
                # Thêm khoảng trắng giữa các chunk nếu không phải chunk cuối
                if i < len(chunks) - 1:
                    yield " "