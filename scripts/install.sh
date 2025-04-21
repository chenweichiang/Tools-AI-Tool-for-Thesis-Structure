#!/bin/bash

# 切換到腳本所在目錄
cd "$(dirname "$0")"
cd ..

# 檢查 Python 版本
if ! command -v python3 &> /dev/null; then
    echo "錯誤：找不到 Python 3。請先安裝 Python 3。"
    exit 1
fi

# 建立虛擬環境
python3 -m venv venv

# 啟動虛擬環境
source venv/bin/activate

# 更新 pip
python -m pip install --upgrade pip

# 安裝必要套件
pip install -r requirements.txt

# 提示輸入 OpenAI API Key
read -p "請輸入您的 OpenAI API Key: " OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > .env

echo "安裝完成！"
echo "您可以使用以下指令啟動應用程式："
echo "source venv/bin/activate && streamlit run src/app.py"
echo "或是："
echo "source venv/bin/activate && streamlit run src/literature_analysis.py"
