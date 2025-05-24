# Vietnamese News Summarization

Vietnamese News Summarization là một dự án mã nguồn mở sử dụng AI để tóm tắt tin tức tiếng Việt một cách tự động, nhanh chóng và chính xác. Dự án này ứng dụng các mô hình ngôn ngữ tiên tiến (transformers, LoRA, PEFT) để tạo ra các bản tóm tắt ngắn gọn, súc tích từ các bài báo dài, giúp người dùng tiết kiệm thời gian đọc và nắm bắt thông tin chính.

## 🚀 Tính năng nổi bật
- **Tóm tắt tin tức tiếng Việt**: Nhập văn bản tin tức, hệ thống sẽ trả về bản tóm tắt ngắn gọn.
- **Giao diện web thân thiện**: Sử dụng Streamlit để tương tác trực quan, dễ sử dụng.
- **API mạnh mẽ**: Triển khai FastAPI cho phép tích hợp dễ dàng vào các hệ thống khác.
- **Hỗ trợ mô hình tùy chỉnh**: Dễ dàng thay đổi mô hình nền và mô hình PEFT qua file `.env`.
- **Streaming kết quả**: Nhận kết quả tóm tắt theo dạng stream, phù hợp cho ứng dụng thời gian thực.

## 🛠️ Công nghệ sử dụng
- [Transformers](https://huggingface.co/docs/transformers/index)
- [PEFT (Parameter-Efficient Fine-Tuning)](https://github.com/huggingface/peft)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

## 📦 Cài đặt
1. **Clone repository**
   ```bash
   git clone https://github.com/trong269/Vietnamese_News_Summarization.git
   cd Vietnamese_News_Summarization
   ```
2. **Tạo môi trường ảo và cài đặt dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # hoặc
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```
3. **Cấu hình mô hình**
   - Tạo file `.env` dựa trên `.env.example` và điền tên mô hình nền, mô hình PEFT:
     ```env
     BASE_MODEL = ...
     PEFT_MODEL = ...
     ```

## 🚦 Sử dụng
### Chạy server API
```bash
uvicorn server:app --reload
```
- API docs: Truy cập [http://localhost:8000/docs](http://localhost:8000/docs)

### Chạy giao diện web (Streamlit)
```bash
streamlit run client.py
```

## 📝 Ví dụ sử dụng API
**POST** `/summary`
```json
{
  "thread_id": "abc123",
  "message": "Nội dung bài báo tiếng Việt cần tóm tắt..."
}
```
**Response:**
```json
{
  "role": "machine",
  "content": "Bản tóm tắt ngắn gọn..."
}
```

## 📁 Cấu trúc thư mục
```
├── client.py           # Giao diện người dùng (Streamlit)
├── server.py           # API FastAPI
├── summarimer.py       # Lớp xử lý tóm tắt
├── config_log.py       # Cấu hình logging
├── requirements.txt    # Thư viện phụ thuộc
├── .env.example        # Mẫu file cấu hình môi trường
└── README.md           # Tài liệu dự án
```

## 💡 Đóng góp
Chúng tôi hoan nghênh mọi đóng góp! Hãy tạo pull request hoặc mở issue nếu bạn có ý tưởng hoặc phát hiện lỗi.


---
**Vietnamese News Summarization** - Tóm tắt tin tức, tiết kiệm thời gian, nâng tầm trải nghiệm!