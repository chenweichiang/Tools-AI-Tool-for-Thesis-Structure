@echo off
echo 安裝研究寫作工具...

:: 創建目標目錄
set INSTALL_DIR=%LOCALAPPDATA%\ResearchWriter
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 複製文件
xcopy /E /I /Y .\* "%INSTALL_DIR%"

:: 創建桌面快捷方式
set SHORTCUT="%USERPROFILE%\Desktop\研究寫作工具.lnk"
powershell "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut(%SHORTCUT%); $SC.TargetPath = '%INSTALL_DIR%\研究寫作工具.exe'; $SC.Save()"

:: 提示輸入 OpenAI API Key
set /p OPENAI_API_KEY="請輸入您的 OpenAI API Key: "
echo OPENAI_API_KEY=%OPENAI_API_KEY% > "%INSTALL_DIR%\.env"

echo 安裝完成！
echo 您可以從桌面上的快捷方式啟動應用程序。
pause
