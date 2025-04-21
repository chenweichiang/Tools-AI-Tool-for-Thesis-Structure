# 研究寫作工具

![版本](https://img.shields.io/badge/版本-1.1.0-blue)
![更新日期](https://img.shields.io/badge/更新日期-2025.04.22-green)

這是一個協助研究者撰寫論文的工具，能夠根據文獻資料自動生成研究目的、文獻探討架構和內容。

## 版本更新說明

### v1.1.0 (2025.04.22)
- 新增文獻探討架構分析工具
- 支援多篇文獻的批量分析
- 自動生成文獻探討內容
- 提供研究趨勢和缺口分析
- 改進文獻引用的整合方式

### v1.0.0 (2025.04.21)
- 初始版本發布
- 支援根據文獻資料生成研究目的
- 提供 Windows 和 macOS 安裝包
- 加入自動化安裝腳本
- 優化使用者介面和提示訊息

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
3. 執行以下命令生成安裝檔：
   ```bash
   python3 build_installer.py
   ```
4. 執行安裝腳本：
   ```bash
   bash install.sh
   ```
5. 根據提示輸入您的 OpenAI API Key
6. 安裝程式會自動：
   - 在指定目錄創建安裝目錄
   - 複製必要檔案
   - 設置環境變數

### macOS 使用者（開發者方式）

1. 確保已安裝 Python 3.8 或更新版本
2. 下載或克隆此專案
3. 在終端機中進入專案目錄
4. 執行以下命令：
   ```bash
   python3 -m venv venv
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

### 研究目的生成工具 (app.py)

1. 啟動程式後，您會在瀏覽器中看到應用程式介面：
   - 本地網址：http://localhost:8501
   - 如果要從其他裝置存取：http://<您的IP地址>:8501
2. 依照介面提示，輸入您的文獻摘要資料
3. 系統會自動：
   - 分析文獻內容
   - 生成研究主題建議
   - 產生完整的研究目的內容
   - 提供參考文獻引用

### 文獻探討分析工具 (literature_analysis.py)

1. 在終端機中執行：
   ```bash
   streamlit run literature_analysis.py
   ```
2. 工具功能包括：
   - 根據研究目的生成文獻探討架構
   - 提供適合的英文搜尋字串
   - 支援多篇文獻的批量分析
   - 自動生成完整的文獻探討內容
   - 提供研究趨勢和缺口分析

3. 使用步驟：
   - 輸入研究目的內容
   - 獲取建議的文獻探討架構
   - 使用提供的搜尋字串在 SciSpace 搜尋文獻
   - 複製文獻的引用格式和摘要
   - 系統自動分析並整合文獻內容
   - 生成完整的文獻探討段落

## 注意事項

- 請確保您有有效的 OpenAI API Key
- 建議每個章節收集 3-5 篇相關文獻，以獲得更好的分析結果
- 生成的內容僅供參考，請根據您的研究需求進行適當的修改和調整
- 使用 SciSpace 搜尋文獻時，建議使用提供的英文搜尋字串以獲得更好的搜尋結果

## 問題回報

如果您遇到任何問題或有改進建議，請：
1. 在 GitHub Issues 頁面提出問題
2. 提供詳細的問題描述和重現步驟
3. 如果可能，附上相關的錯誤訊息或截圖

## 授權說明

本工具僅供學術研究使用。使用本工具時，請遵守相關的學術倫理規範。

# 研究文獻架構分析工具

這是一個協助研究者規劃和撰寫文獻探討的工具，能夠根據研究目的自動產生文獻探討架構，並提供適當的文獻搜尋建議。

## 功能特色

1. **文獻探討架構規劃**
   - 根據研究目的自動產生 3-5 個適合的文獻探討章節
   - 為每個章節提供詳細的重點說明
   - 產生適合的英文搜尋字串，方便在學術資料庫中搜尋

2. **文獻分析與整理**
   - 自動分析並整理文獻的 APA 引用格式和摘要
   - 分析文獻與研究主題的相關性
   - 提供文獻引用建議
   - 整合多篇文獻的重要發現

3. **文獻探討撰寫**
   - 自動產生結構完整的文獻探討內容
   - 自然地融入文獻引用
   - 突顯重要研究發現
   - 指出研究缺口與未來方向

4. **台灣繁體中文規範**
   - 完全符合台灣學術用語習慣
   - 使用正確的台灣標點符號
   - 採用台灣的表達方式
   - 套用台灣的專業術語

## 安裝說明

1. 確認已安裝 Python 3.8 或更新版本
2. 複製專案到本機：
   ```bash
   git clone [專案網址]
   ```
3. 進入專案目錄：
   ```bash
   cd [專案目錄]
   ```
4. 建立虛擬環境：
   ```bash
   python -m venv venv
   ```
5. 啟動虛擬環境：
   - Windows：`venv\Scripts\activate`
   - macOS/Linux：`source venv/bin/activate`
6. 安裝相依套件：
   ```bash
   pip install -r requirements.txt
   ```
7. 設定環境變數：
   - 複製 `.env.example` 為 `.env`
   - 在 `.env` 中填入您的 OpenAI API 金鑰

## 使用說明

1. 啟動應用程式：
   ```bash
   streamlit run literature_analysis.py
   ```

2. 在網頁介面中：
   - 輸入您的研究目的
   - 點選「產生文獻探討架構」
   - 依照產生的架構收集文獻
   - 使用提供的搜尋字串在 SciSpace 搜尋相關文獻
   - 將找到的文獻資料貼到對應章節
   - 點選「分析並新增文獻」
   - 收集足夠文獻後，點選「產生文獻探討」

## 注意事項

1. 建議每個章節至少收集 3-5 篇相關文獻
2. 文獻內容請包含 APA 引用格式和摘要
3. 貼入多篇文獻時，每篇文獻之間請空一行
4. 產生的內容會自動套用台灣繁體中文的用字規範

## 系統需求

- Python 3.8+
- OpenAI API 金鑰
- 網際網路連線
- 現代化網頁瀏覽器

## 授權資訊

本專案採用 MIT 授權條款。詳細內容請參閱 LICENSE 檔案。 