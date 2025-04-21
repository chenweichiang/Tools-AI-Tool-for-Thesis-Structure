FROM python:3.11-slim

WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製必要檔案
COPY requirements.txt .
COPY src/ ./src/
COPY .env.example .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 設定環境變數
ENV PYTHONPATH=/app
ENV PORT=8501

# 開放 Streamlit 端口
EXPOSE 8501

# 啟動命令
CMD ["streamlit", "run", "src/app.py", "--server.address", "0.0.0.0", "--server.port", "8501"] 