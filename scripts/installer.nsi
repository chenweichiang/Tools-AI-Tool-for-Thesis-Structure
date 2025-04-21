; 安裝程式設定
Unicode true
SetCompressor /SOLID lzma

; 基本資訊
!define VERSION "1.0.0"
Name "研究寫作工具 ${VERSION}"
OutFile "dist\windows_installer_${VERSION}.exe"
InstallDir "$LOCALAPPDATA\研究寫作工具"
RequestExecutionLevel admin

; 安裝介面設定
!include "MUI2.nsh"
!include "LogicLib.nsh"
!define MUI_ICON "..\resources\app_icon.ico"
!define MUI_UNICON "..\resources\app_icon.ico"
!define MUI_ABORTWARNING

; 介面頁面
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "..\README.md"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; 解除安裝頁面
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; 語言設定
!insertmacro MUI_LANGUAGE "TradChinese"

Section "MainSection" SEC01
    SetOutPath "$INSTDIR"
    SetOverwrite try
    
    ; 檢查是否有足夠的磁碟空間（至少需要 500MB）
    ${If} $INSTDIR != ""
        System::Call 'kernel32::GetDiskFreeSpaceEx(t "$INSTDIR", *l .r1, *l .r2, *l .r3) i .r0'
        ${If} $r1 < 524288000 ; 500MB in bytes
            MessageBox MB_OK|MB_ICONSTOP "安裝目錄的可用空間不足，至少需要 500MB 的可用空間。"
            Abort
        ${EndIf}
    ${EndIf}
    
    ; 複製主程式檔案
    File "..\src\app.py"
    File "..\src\literature_analysis.py"
    File "..\requirements.txt"
    File "..\resources\app_icon.ico"
    File "..\env.example"
    File "..\README.md"
    
    ; 下載並安裝 Python
    DetailPrint "檢查 Python 安裝..."
    nsExec::ExecToLog 'python --version'
    Pop $0
    ${If} $0 != 0
        DetailPrint "正在下載 Python..."
        NSISdl::download "https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe" "$TEMP\python-installer.exe"
        Pop $0
        ${If} $0 == "success"
            DetailPrint "正在安裝 Python..."
            ExecWait '"$TEMP\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0' $0
            ${If} $0 != 0
                MessageBox MB_OK|MB_ICONSTOP "Python 安裝失敗，錯誤代碼: $0"
                Abort
            ${EndIf}
            Delete "$TEMP\python-installer.exe"
        ${Else}
            MessageBox MB_OK|MB_ICONSTOP "無法下載 Python，請檢查網路連線後重試。錯誤: $0"
            Abort
        ${EndIf}
    ${EndIf}
    
    ; 建立虛擬環境
    DetailPrint "正在建立 Python 虛擬環境..."
    nsExec::ExecToLog 'python -m venv "$INSTDIR\venv"'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONSTOP "建立虛擬環境失敗，錯誤代碼: $0"
        Abort
    ${EndIf}
    
    ; 安裝必要套件
    DetailPrint "正在安裝必要套件..."
    nsExec::ExecToLog '"$INSTDIR\venv\Scripts\python" -m pip install --upgrade pip'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONSTOP "更新 pip 失敗，錯誤代碼: $0"
        Abort
    ${EndIf}
    
    nsExec::ExecToLog '"$INSTDIR\venv\Scripts\pip" install -r "$INSTDIR\requirements.txt"'
    Pop $0
    ${If} $0 != 0
        MessageBox MB_OK|MB_ICONSTOP "安裝必要套件失敗，錯誤代碼: $0"
        Abort
    ${EndIf}
    
    ; 建立啟動腳本
    FileOpen $0 "$INSTDIR\start_research_writer.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 'cd /d "$INSTDIR"$\r$\n'
    FileWrite $0 'call venv\Scripts\activate.bat$\r$\n'
    FileWrite $0 'if not exist .env ($\r$\n'
    FileWrite $0 '    echo 找不到 .env 檔案，請確認是否已設定 OpenAI API 金鑰$\r$\n'
    FileWrite $0 '    pause$\r$\n'
    FileWrite $0 '    exit /b 1$\r$\n'
    FileWrite $0 ')$\r$\n'
    FileWrite $0 'start "" streamlit run app.py$\r$\n'
    FileClose $0
    
    FileOpen $0 "$INSTDIR\start_literature_analysis.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 'cd /d "$INSTDIR"$\r$\n'
    FileWrite $0 'call venv\Scripts\activate.bat$\r$\n'
    FileWrite $0 'if not exist .env ($\r$\n'
    FileWrite $0 '    echo 找不到 .env 檔案，請確認是否已設定 OpenAI API 金鑰$\r$\n'
    FileWrite $0 '    pause$\r$\n'
    FileWrite $0 '    exit /b 1$\r$\n'
    FileWrite $0 ')$\r$\n'
    FileWrite $0 'start "" streamlit run literature_analysis.py$\r$\n'
    FileClose $0
    
    ; 建立桌面捷徑
    CreateShortCut "$DESKTOP\研究寫作工具.lnk" "$INSTDIR\start_research_writer.bat" "" "$INSTDIR\app_icon.ico"
    CreateShortCut "$DESKTOP\文獻分析工具.lnk" "$INSTDIR\start_literature_analysis.bat" "" "$INSTDIR\app_icon.ico"
    
    ; 建立開始選單捷徑
    CreateDirectory "$SMPROGRAMS\研究寫作工具"
    CreateShortCut "$SMPROGRAMS\研究寫作工具\研究寫作工具.lnk" "$INSTDIR\start_research_writer.bat" "" "$INSTDIR\app_icon.ico"
    CreateShortCut "$SMPROGRAMS\研究寫作工具\文獻分析工具.lnk" "$INSTDIR\start_literature_analysis.bat" "" "$INSTDIR\app_icon.ico"
    CreateShortCut "$SMPROGRAMS\研究寫作工具\解除安裝.lnk" "$INSTDIR\uninstall.exe"
    
    ; 提示輸入 API 金鑰
    MessageBox MB_OK "請在接下來的視窗中輸入您的 OpenAI API 金鑰$\n您可以從 https://platform.openai.com/account/api-keys 獲取"
    nsDialogs::Create 1018
    Pop $0
    ${NSD_CreateLabel} 0 0 100% 12u "OpenAI API 金鑰:"
    Pop $1
    ${NSD_CreateText} 0 13 100% 12u ""
    Pop $2
    nsDialogs::Show
    ${NSD_GetText} $2 $3
    
    ; 驗證 API 金鑰不為空
    ${If} $3 == ""
        MessageBox MB_OK|MB_ICONEXCLAMATION "API 金鑰不能為空。您可以之後在 .env 檔案中手動設定。"
    ${EndIf}
    
    FileOpen $0 "$INSTDIR\.env" w
    FileWrite $0 "OPENAI_API_KEY=$3"
    FileClose $0
    
    ; 寫入解除安裝資訊
    WriteUninstaller "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具" "DisplayName" "研究寫作工具 ${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具" "DisplayIcon" "$INSTDIR\app_icon.ico"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具" "DisplayVersion" "${VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具" "Publisher" "研究寫作工具"
SectionEnd

Section "Uninstall"
    ; 移除檔案
    Delete "$INSTDIR\app.py"
    Delete "$INSTDIR\literature_analysis.py"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\app_icon.ico"
    Delete "$INSTDIR\.env"
    Delete "$INSTDIR\.env.example"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\start_research_writer.bat"
    Delete "$INSTDIR\start_literature_analysis.bat"
    Delete "$INSTDIR\uninstall.exe"
    
    ; 移除虛擬環境
    RMDir /r "$INSTDIR\venv"
    
    ; 移除桌面捷徑
    Delete "$DESKTOP\研究寫作工具.lnk"
    Delete "$DESKTOP\文獻分析工具.lnk"
    
    ; 移除開始選單捷徑
    Delete "$SMPROGRAMS\研究寫作工具\研究寫作工具.lnk"
    Delete "$SMPROGRAMS\研究寫作工具\文獻分析工具.lnk"
    Delete "$SMPROGRAMS\研究寫作工具\解除安裝.lnk"
    RMDir "$SMPROGRAMS\研究寫作工具"
    
    ; 移除安裝目錄
    RMDir "$INSTDIR"
    
    ; 移除註冊表項目
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\研究寫作工具"
SectionEnd 