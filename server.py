from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import torch

from summarimer import Summarimer

from config_log import get_logger
import os
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()
BASE_MODEL = os.getenv("BASE_MODEL")
PEFT_MODEL = os.getenv("PEFT_MODEL")

logger = get_logger(__name__)


app = FastAPI()


class Request(BaseModel):
    """
    Request model for the summarization API.
    
    Attributes:
        thread_id (str): The ID of the thread.
        message (str): The text to summarize.
    """
    thread_id: str
    message: str

class Response(BaseModel):
    """
    Response model for the summarization API.
    
    Attributes:
        role (str): The role of the response (e.g., 'machine').
        content (str): The summarized text.
    """
    role: str
    content: str

device = "cuda" if torch.cuda.is_available() else "cpu"
logger.info(f"Using device: {device}")
# Load the summarization model
summarizer = Summarimer(
    base_model=BASE_MODEL,
    mmodel_name=PEFT_MODEL,
    framework="pt",
    device=device
)
logger.info("Model loaded successfully")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/summary")
def summarize_text(request: Request) -> Response:
    """
    Summarizes the given text using the loaded model.
    
    Args:
        text (str): The text to summarize.
    
    Returns:
        str: The summarized text.
    """
    summary = summarizer.summarize(
        request.message,
        )
    return Response(content=summary, role='machine')

@app.post("/summary_stream")
def summarize_text_stream(request: Request):
    """
    Summarizes the given text using the loaded model with streaming response.
    
    Args:
        request (Request): The request containing the text to summarize.
    
    Returns:
        StreamingResponse: A streaming response with the summarized text.
    """
    def generate():
        for token in summarizer.summarize_stream(request.message):
            yield f"data: {token}\n\n"

    return StreamingResponse(
        generate(), 
        media_type="text/event-stream"
    )