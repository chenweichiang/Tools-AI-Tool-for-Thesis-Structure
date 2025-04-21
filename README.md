# 研究寫作工具

這是一個協助研究者撰寫論文的工具，能夠根據文獻資料自動生成研究目的和相關內容。

## 系統需求

### Windows 版本
- Windows 10 或更新版本
- 不需要安裝 Python 環境
- 需要有效的 OpenAI API Key

### macOS 版本
- macOS 10.15 或更新版本
- Python 3.8 或更新版本
- 需要有效的 OpenAI API Key

## 安裝說明

### Windows 使用者（推薦方式）

1. 從 [Releases](../../releases) 頁面下載最新的 `研究寫作工具-windows.zip`
2. 解壓縮下載的檔案到任意位置
3. 執行解壓縮後的 `install.bat`
4. 根據提示輸入您的 OpenAI API Key
5. 安裝程式會自動：
   - 在 `%LOCALAPPDATA%\ResearchWriter` 創建安裝目錄
   - 複製必要檔案
   - 在桌面創建快捷方式 "Research Writing Tool"
   - 設置環境變數

### Windows 使用者（開發者方式）

1. 安裝 Python 3.8 或更新版本
2. 下載或克隆此專案
3. 在命令提示字元中進入專案目錄
4. 執行以下命令：
   ```batch
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```
5. 複製 `.env.example` 為 `.env` 並填入您的 OpenAI API Key
6. 執行程式：
   ```batch
   streamlit run app.py
   ```

### macOS 使用者（推薦方式）

1. 下載或克隆此專案
2. 開啟終端機（Terminal）並進入專案目錄
3. 執行安裝腳本：
   ```bash
   chmod +x install.sh
   ./install.sh
   ```
4. 根據提示輸入您的 OpenAI API Key
5. 安裝程式會自動：
   - 在 `~/Applications/ResearchWriter` 創建安裝目錄
   - 複製必要檔案
   - 在桌面創建快捷方式
   - 設置環境變數

### macOS 使用者（開發者方式）

1. 確保已安裝 Python 3.8 或更新版本
2. 下載或克隆此專案
3. 在終端機中進入專案目錄
4. 執行以下命令：
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. 複製 `.env.example` 為 `.env` 並填入您的 OpenAI API Key
6. 執行程式：
   ```bash
   streamlit run app.py
   ```

### 提升效能（選擇性）
如果要提升程式效能，可以安裝 Watchdog 模組：

macOS：
```bash
xcode-select --install
pip install watchdog
```

Windows：
```batch
pip install watchdog
```

## 使用說明

1. 啟動程式後，您會在瀏覽器中看到應用程式介面：
   - 本地網址：http://localhost:8501
   - 如果要從其他裝置存取：http://<您的IP地址>:8501
2. 依照介面提示，輸入您的文獻摘要資料
3. 系統會自動：
   - 分析文獻內容
   - 生成研究主題建議
   - 產生完整的研究目的內容
   - 提供參考文獻引用

## 注意事項

- 請確保您有有效的 OpenAI API Key
- 建議輸入至少 3-5 篇相關文獻的摘要，以獲得更好的生成結果
- 生成的內容僅供參考，請根據您的研究需求進行適當的修改和調整

## 問題回報

如果您遇到任何問題或有改進建議，請：
1. 在 GitHub Issues 頁面提出問題
2. 提供詳細的問題描述和重現步驟
3. 如果可能，附上相關的錯誤訊息或截圖

## 授權說明

本工具僅供學術研究使用。使用本工具時，請遵守相關的學術倫理規範。 