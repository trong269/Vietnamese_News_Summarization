from __future__ import annotations

import uuid
import requests
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title='Vietnamese News Summarizer',
    page_icon='📰',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Apply custom CSS for better styling
st.markdown(
    """
<style>
    /* Main layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    /* Header styling */
    .header-container {
        display: flex;
        align-items: center;
        background: linear-gradient(to right, #1e3c72, #2a5298);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .header-logo {
        font-size: 2rem;
        margin-right: 1rem;
    }
    .header-title {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0;
    }
    .header-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        margin: 0;
    }
    
    /* Document container */
    .document-section {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .document-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    
    .document-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e3c72;
        margin: 0;
    }
    
    .document-content {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e9ecef;
        max-height: 40vh;
        overflow-y: auto;
    }
    
    .summary-section {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #1e3c72;
    }
    
    .summary-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        border-bottom: 1px solid #e9ecef;
        padding-bottom: 0.5rem;
    }
    
    .summary-title {
        font-size: 1.2rem;
        font-weight: bold;
        color: #1e3c72;
        margin: 0;
    }
    
    .summary-content {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 1.5rem;
        border: 1px solid #e9ecef;
        max-height: 40vh;
        overflow-y: auto;
    }
    
    .summary-placeholder {
        color: #6c757d;
        text-align: center;
        padding: 2rem;
        font-style: italic;
    }
    
    /* Input area */
    .input-container {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stTextArea textarea {
        border-radius: 8px;
        padding: 0.75rem;
        border: 1px solid #e9ecef;
        font-size: 1rem;
        min-height: 150px;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .sidebar-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1e3c72;
    }
    .sidebar-button {
        background-color: #1e3c72;
        color: white;
        border-radius: 8px;
        padding: 0.75rem;
        text-align: center;
        margin: 1rem 0;
        cursor: pointer;
        transition: background-color 0.3s;
    }
    .sidebar-button:hover {
        background-color: #2a5298;
    }
    .sidebar-info {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        border-left: 4px solid #1e3c72;
    }
    
    /* Stats section */
    .stats-container {
        display: flex;
        justify-content: space-between;
        margin-top: 1rem;
        gap: 1rem;
    }
    
    .stat-card {
        background-color: white;
        border-radius: 8px;
        padding: 1rem;
        flex: 1;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
        border-top: 3px solid #1e3c72;
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1e3c72;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Set API endpoint
API_ENDPOINT = 'http://127.0.0.1:8000/summary/'
API_STREAM_ENDPOINT = 'http://127.0.0.1:8000/summary_stream/'

# Add headers for CORS if needed
HEADERS = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
}

# Initialize session state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
if 'original_text' not in st.session_state:
    st.session_state.original_text = ""
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'streaming' not in st.session_state:
    st.session_state.streaming = False
if 'use_streaming' not in st.session_state:
    st.session_state.use_streaming = True
if 'word_count_original' not in st.session_state:
    st.session_state.word_count_original = 0
if 'word_count_summary' not in st.session_state:
    st.session_state.word_count_summary = 0
if 'reduction_percentage' not in st.session_state:
    st.session_state.reduction_percentage = 0

# Create header
st.markdown("""
<div class="header-container">
    <div class="header-logo">📰</div>
    <div>
        <h1 class="header-title">Vietnamese News Summarizer</h1>
        <p class="header-subtitle">Công cụ tóm tắt tin tức tiếng Việt tự động</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create two columns layout for input and output
col1, col2 = st.columns([1, 1])

# Input column
with col1:
    st.markdown('<div class="document-section">', unsafe_allow_html=True)
    st.markdown('<div class="document-header"><h3 class="document-title">Nội dung gốc</h3></div>', unsafe_allow_html=True)
    
    # Input area for news content
    st.text_area(
        label="",
        value=st.session_state.original_text,
        placeholder="Nhập hoặc dán nội dung tin tức cần tóm tắt vào đây...",
        height=300,
        key="input_text"
    )
      # Submit button
    if st.button("Tóm tắt nội dung", key="submit_button"):
        if st.session_state.input_text.strip():
            st.session_state.original_text = st.session_state.input_text
            st.session_state.processing = True
            st.session_state.summary = ""
            
            # Calculate word count for original text
            st.session_state.word_count_original = len(st.session_state.original_text.split())
            
            # Prepare data for API call
            data = {
                "message": st.session_state.original_text,
                "thread_id": st.session_state.thread_id,
            }
            
            if st.session_state.use_streaming:
                # Sử dụng stream mode nếu người dùng đã bật
                st.session_state.streaming = True
                try:
                    st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi chuẩn bị streaming: {str(e)}")
                    st.session_state.processing = False
                    st.session_state.streaming = False
            else:
                # Sử dụng normal mode nếu người dùng đã tắt streaming
                try:
                    # API call to get summary
                    response = requests.post(API_ENDPOINT, json=data, headers=HEADERS)
                    
                    if response.status_code == 200:
                        response_data = response.json()
                        st.session_state.summary = response_data['content']
                        
                        # Calculate word count for summary
                        st.session_state.word_count_summary = len(st.session_state.summary.split())
                        
                        # Calculate reduction percentage
                        if st.session_state.word_count_original > 0:
                            st.session_state.reduction_percentage = round(
                                (1 - (st.session_state.word_count_summary / st.session_state.word_count_original)) * 100
                            )
                        
                        st.session_state.processing = False
                        st.rerun()
                    else:
                        st.error(f"Lỗi: {response.status_code} - {response.text}")
                        st.session_state.processing = False
                except Exception as e:
                    st.error(f"Không thể kết nối với máy chủ: {str(e)}")
                    st.session_state.processing = False
        else:
            st.warning("Vui lòng nhập nội dung tin tức để tóm tắt.")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Output column
with col2:
    st.markdown('<div class="summary-section">', unsafe_allow_html=True)
    st.markdown('<div class="summary-header"><h3 class="summary-title">Bản tóm tắt</h3></div>', unsafe_allow_html=True)
    
    if st.session_state.processing:
        if st.session_state.streaming:
            # Hiển thị streaming content
            st.markdown('<div class="summary-content">', unsafe_allow_html=True)
            summary_placeholder = st.empty()
            
            # Gọi API streaming
            try:
                with requests.post(API_STREAM_ENDPOINT, json={
                    "message": st.session_state.original_text,
                    "thread_id": st.session_state.thread_id
                }, headers=HEADERS, stream=True) as response:
                    
                    complete_summary = ""
                    
                    for line in response.iter_lines():
                        if line:
                            # Xử lý format SSE (Server-Sent Events)
                            line_text = line.decode('utf-8')
                            if line_text.startswith('data: '):
                                token = line_text[6:]  # Bỏ 'data: ' phía trước
                                complete_summary += token
                                summary_placeholder.markdown(complete_summary)
                    
                    # Lưu kết quả cuối cùng
                    st.session_state.summary = complete_summary
                    
                    # Calculate word count for summary
                    st.session_state.word_count_summary = len(st.session_state.summary.split())
                    
                    # Calculate reduction percentage
                    if st.session_state.word_count_original > 0:
                        st.session_state.reduction_percentage = round(
                            (1 - (st.session_state.word_count_summary / st.session_state.word_count_original)) * 100
                        )
                    
                    st.session_state.processing = False
                    st.session_state.streaming = False
                    st.rerun()
            except Exception as e:
                st.error(f"Lỗi khi streaming: {str(e)}")
                st.session_state.processing = False
                st.session_state.streaming = False
        else:
            st.markdown('<div class="loading-spinner">', unsafe_allow_html=True)
            st.spinner("Đang xử lý tóm tắt...")
            st.markdown('</div>', unsafe_allow_html=True)
    elif st.session_state.summary:
        st.markdown('<div class="summary-content">', unsafe_allow_html=True)
        st.write(st.session_state.summary)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Statistics about the summary
        st.markdown('<div class="stats-container">', unsafe_allow_html=True)
        
        # Original word count
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.word_count_original}</div>
            <div class="stat-label">Từ trong bản gốc</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Summary word count
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.word_count_summary}</div>
            <div class="stat-label">Từ trong bản tóm tắt</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Reduction percentage
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{st.session_state.reduction_percentage}%</div>
            <div class="stat-label">Tỷ lệ rút gọn</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="summary-placeholder">
            Nhập nội dung tin tức và nhấn nút "Tóm tắt nội dung" để xem kết quả tóm tắt ở đây.
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Add a sidebar with options
with st.sidebar:
    st.markdown('<div class="sidebar-header">Tùy chọn</div>', unsafe_allow_html=True)
    
    # New document button
    if st.button('🔄 Tài liệu mới', key='new_document_button'):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.original_text = ""
        st.session_state.summary = ""
        st.session_state.word_count_original = 0
        st.session_state.word_count_summary = 0
        st.session_state.reduction_percentage = 0
        st.rerun()  
    
    # Copy to clipboard button (limited functionality due to Streamlit limitations)
    st.button('📋 Sao chép tóm tắt', key='copy_summary_button')
    
    # Streaming toggle switch
    st.markdown('---')
    st.markdown('<p><strong>Cài đặt tóm tắt</strong></p>', unsafe_allow_html=True)
    streaming_enabled = st.toggle(
        'Hiển thị tóm tắt theo thời gian thực',
        value=st.session_state.use_streaming,
        key='streaming_toggle'
    )
    # Update session state when toggle changes
    if 'streaming_toggle' in st.session_state:
        st.session_state.use_streaming = st.session_state.streaming_toggle
    
    st.markdown('---')
    st.markdown(
        f"""
        <div class="sidebar-info">
            <p><strong>ID tài liệu:</strong></p>
            <p style="font-family: monospace; word-break: break-all;">{st.session_state.thread_id}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown('---')
    st.markdown("""
    <div class="sidebar-info">
        <p><strong>Hướng dẫn sử dụng:</strong></p>
        <p>1. Dán nội dung tin tức vào khung bên trái</p>
        <p>2. Nhấn nút "Tóm tắt nội dung" để xử lý</p>
        <p>3. Xem bản tóm tắt hiển thị ở khung bên phải</p>
        <p>4. Tạo tài liệu mới bằng cách nhấn "Tài liệu mới"</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('---')
    st.markdown("""
    <div class="sidebar-info">
        <p><strong>Về công cụ này:</strong></p>
        <p>Công cụ tóm tắt tin tức tiếng Việt sử dụng trí tuệ nhân tạo để tạo ra các bản tóm tắt ngắn gọn, đầy đủ ý chính từ nội dung tin tức gốc.</p>
    </div>
    """, unsafe_allow_html=True)
