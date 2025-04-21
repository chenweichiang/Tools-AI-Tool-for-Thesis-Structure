# 研究寫作輔助工具

這是一個基於 AI 的研究寫作輔助工具，可以幫助研究者：
- 生成研究主題和關鍵詞
- 產生研究題目建議
- 自動生成研究目的內容
- 協助進行文獻探討

## 功能特色

- 智能關鍵詞生成
- 多方向研究題目建議
- 自動生成研究目的
- 文獻探討架構建議
- 整合 SciSpace 文獻搜尋

## 安裝說明

1. 複製專案：
```bash
git clone https://github.com/[您的GitHub帳號]/research-writing-assistant.git
cd research-writing-assistant
```

2. 建立虛擬環境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\activate  # Windows
```

3. 安裝相依套件：
```bash
pip install -r requirements.txt
```

4. 設定環境變數：
- 複製 `.env.example` 為 `.env`
- 在 `.env` 中填入您的 OpenAI API 金鑰：
```
OPENAI_API_KEY=您的API金鑰
```

## 使用方法

1. 啟動應用程式：
```bash
streamlit run src/app.py
```

2. 在瀏覽器中開啟顯示的網址（預設為 http://localhost:8501）

3. 依照介面指示進行操作：
   - 輸入研究主題
   - 填寫研究內容
   - 選擇關鍵詞
   - 選擇研究題目
   - 生成研究目的
   - 進行文獻探討

## 注意事項

- 需要有效的 OpenAI API 金鑰
- 建議使用 Python 3.8 或以上版本
- 請確保網路連線穩定

## 授權

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案 