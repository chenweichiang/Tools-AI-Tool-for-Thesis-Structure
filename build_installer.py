import os
import sys
import platform
import shutil
from pathlib import Path

def create_spec_file(target_platform='current'):
    """創建 PyInstaller 規格文件"""
    is_windows = target_platform == 'windows'
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
        ('requirements.txt', '.'),
    ],
    hiddenimports=['streamlit', 'openai'],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='研究寫作工具{"" if not is_windows else ".exe"}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    {'target_platform="windows",' if is_windows else ''}
)
"""
    spec_filename = 'research_writer_windows.spec' if is_windows else 'research_writer.spec'
    with open(spec_filename, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    return spec_filename

def create_windows_installer():
    install_script = '''@echo off
chcp 65001
echo Installing Research Writing Tool...

:: Create target directory
set INSTALL_DIR=%LOCALAPPDATA%\\ResearchWriter
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: Copy files
xcopy /E /I /Y .\\* "%INSTALL_DIR%"

:: Create desktop shortcut
set SHORTCUT="%USERPROFILE%\\Desktop\\Research Writing Tool.lnk"
powershell "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut(%SHORTCUT%); $SC.TargetPath = '%INSTALL_DIR%\\研究寫作工具.exe'; $SC.Save()"

:: Prompt for OpenAI API Key
set /p OPENAI_API_KEY="Please enter your OpenAI API Key: "
echo OPENAI_API_KEY=%OPENAI_API_KEY% > "%INSTALL_DIR%\\.env"

echo Installation completed!
echo You can start the application from the desktop shortcut.
pause
'''
    with open('dist/windows/install.bat', 'w', encoding='utf-8') as f:
        f.write(install_script)

def create_macos_installer():
    install_script = '''#!/bin/bash
echo "安裝研究寫作工具..."

# 創建安裝目錄
INSTALL_DIR="$HOME/Applications/ResearchWriter"
mkdir -p "$INSTALL_DIR"

# 複製文件
cp -R ./* "$INSTALL_DIR/"

# 創建桌面快捷方式
DESKTOP_FILE="$HOME/Desktop/研究寫作工具.command"
echo '#!/bin/bash' > "$DESKTOP_FILE"
echo "cd \\"$INSTALL_DIR\\"" >> "$DESKTOP_FILE"
echo "./研究寫作工具" >> "$DESKTOP_FILE"
chmod +x "$DESKTOP_FILE"

# 提示輸入 OpenAI API Key
read -p "請輸入您的 OpenAI API Key: " OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > "$INSTALL_DIR/.env"

echo "安裝完成！"
echo "您可以從桌面上的快捷方式啟動應用程序。"
'''
    with open('dist/macos/install.sh', 'w', encoding='utf-8') as f:
        f.write(install_script)
    os.chmod('dist/macos/install.sh', 0o755)

def build_package(target_platform='current'):
    """建立安裝包"""
    try:
        # 建立打包目錄
        if target_platform == 'windows':
            os.makedirs('dist/windows', exist_ok=True)
        else:
            os.makedirs('dist/macos', exist_ok=True)
        
        # 創建規格文件
        spec_file = create_spec_file(target_platform)
        
        # 使用 PyInstaller 打包
        os.system(f'pyinstaller {spec_file}')
        
        # 移動文件到對應平台目錄
        if target_platform == 'windows':
            # 移動文件到 windows 目錄
            if os.path.exists('dist/研究寫作工具.exe'):
                shutil.move('dist/研究寫作工具.exe', 'dist/windows/')
            create_windows_installer()
        else:
            # 移動文件到 macos 目錄
            if os.path.exists('dist/研究寫作工具'):
                shutil.move('dist/研究寫作工具', 'dist/macos/')
            create_macos_installer()
        
        # 複製必要文件
        for file in ['.env.example', 'README.md', 'requirements.txt']:
            if os.path.exists(file):
                shutil.copy2(file, f'dist/{"windows" if target_platform == "windows" else "macos"}/')
        
        print("Build completed!")
        print(f"Package has been generated in dist/{target_platform} directory.")
        
    except Exception as e:
        print(f"Error during build process: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # 檢查命令行參數
    if len(sys.argv) > 1 and sys.argv[1] == '--windows':
        build_package('windows')
    else:
        build_package('current') 