FROM ubuntu:22.04

# 避免安裝過程中的交互式提示
ENV DEBIAN_FRONTEND=noninteractive

# 安裝必要的工具
RUN dpkg --add-architecture i386 && \
    apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    gcc \
    g++ \
    mingw-w64 \
    && rm -rf /var/lib/apt/lists/*

# 設置工作目錄
WORKDIR /app

# 複製必要文件
COPY requirements.txt .
COPY app.py .
COPY build_installer.py .
COPY .env.example .
COPY README.md .

# 安裝 Python 依賴
RUN pip3 install -r requirements.txt
RUN pip3 install pyinstaller

# 設置環境變數
ENV PATH="/usr/x86_64-w64-mingw32/bin:${PATH}"

# 運行打包命令
CMD ["python3", "build_installer.py", "--windows"] 