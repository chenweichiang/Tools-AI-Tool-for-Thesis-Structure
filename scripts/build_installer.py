import os
import sys
import platform
import shutil
import subprocess
from pathlib import Path
import PyInstaller.__main__

def create_spec_file(target_platform='current'):
    """創建 PyInstaller 規格文件"""
    is_windows = target_platform == 'windows'
    
    spec_content = f"""# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../.env.example', '.'),
        ('../README.md', '.'),
        ('../requirements.txt', '.'),
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

def clean_dist_directory():
    """清理舊的建置檔案"""
    print("清理舊的建置檔案...")
    if os.path.exists('dist'):
        shutil.rmtree('dist')
    if os.path.exists('build'):
        shutil.rmtree('build')

def build_windows_installer():
    """建立 Windows 安裝程式"""
    print("開始建立 Windows 安裝程式...")
    
    # 建立暫存目錄
    build_dir = Path("build")
    dist_dir = Path("dist")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    build_dir.mkdir(exist_ok=True)
    dist_dir.mkdir(exist_ok=True)
    
    # 複製必要檔案
    print("複製檔案...")
    files_to_copy = [
        "src/app.py",
        "src/literature_analysis.py",
        "requirements.txt",
        ".env.example",
        "README.md",
        "LICENSE"
    ]
    
    for file in files_to_copy:
        src = Path(file)
        if src.exists():
            dst = build_dir / src.name
            shutil.copy2(src, dst)
            print(f"已複製: {src} -> {dst}")
    
    # 建立安裝腳本
    print("建立安裝腳本...")
    installer_script = """@echo off
echo 安裝研究寫作工具...

:: 檢查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 未安裝 Python，正在下載並安裝...
    curl -o python-installer.exe https://www.python.org/ftp/python/3.11.8/python-3.11.8-amd64.exe
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    del python-installer.exe
)

:: 建立虛擬環境
python -m venv venv
call venv\\Scripts\\activate

:: 安裝相依套件
pip install -r requirements.txt

:: 設定 OpenAI API 金鑰
set /p OPENAI_API_KEY="請輸入您的 OpenAI API 金鑰: "
echo OPENAI_API_KEY=%OPENAI_API_KEY% > .env

:: 建立桌面捷徑
echo Set oWS = WScript.CreateObject("WScript.Shell") > CreateShortcut.vbs
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\研究寫作工具.lnk" >> CreateShortcut.vbs
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> CreateShortcut.vbs
echo oLink.TargetPath = "%~dp0venv\\Scripts\\streamlit.exe" >> CreateShortcut.vbs
echo oLink.Arguments = "run app.py" >> CreateShortcut.vbs
echo oLink.WorkingDirectory = "%~dp0" >> CreateShortcut.vbs
echo oLink.Save >> CreateShortcut.vbs
cscript CreateShortcut.vbs
del CreateShortcut.vbs

echo 安裝完成！
echo 您可以從桌面的捷徑啟動程式。
pause
"""
    
    with open(build_dir / "install.bat", "w", encoding="utf-8") as f:
        f.write(installer_script)
    
    # 建立壓縮檔
    print("建立壓縮檔...")
    shutil.make_archive(
        str(dist_dir / "研究寫作工具-windows"),
        "zip",
        build_dir
    )
    
    print("Windows 安裝程式建立完成！")
    print(f"安裝檔位置: {dist_dir}/研究寫作工具-windows.zip")

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

def build_macos_installer():
    """建立 macOS 安裝程式"""
    print("開始建立 macOS 安裝程式...")
    # macOS 安裝程式建立邏輯...
    pass

def build_macos_package():
    """建立 macOS 安裝包"""
    print("正在建立 macOS 安裝包...")
    
    # 清理舊的建置檔案
    clean_dist_directory()
    
    # 建立 spec 檔案
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['../src/app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('../.env.example', '.'),
        ('../README.md', '.'),
        ('../requirements.txt', '.'),
    ],
    hiddenimports=['streamlit', 'openai'],
    hookspath=[],
    hooksconfig={},
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
    [],
    exclude_binaries=True,
    name='研究寫作工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='研究寫作工具',
)

app = BUNDLE(
    coll,
    name='研究寫作工具.app',
    icon='../resources/app_icon.icns',
    bundle_identifier='com.research.writer',
    info_plist={
        'CFBundleName': '研究寫作工具',
        'CFBundleDisplayName': '研究寫作工具',
        'CFBundleExecutable': '研究寫作工具',
        'CFBundlePackageType': 'APPL',
        'CFBundleInfoDictionaryVersion': '6.0',
        'CFBundleIconFile': 'app_icon.icns',
        'NSHighResolutionCapable': True,
    }
)
'''
    
    with open('research_writer.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    # 使用 spec 檔案打包
    PyInstaller.__main__.run(['research_writer.spec'])
    
    # 準備安裝程式目錄
    installer_dir = 'dist/研究寫作工具-installer'
    os.makedirs(installer_dir, exist_ok=True)
    
    # 複製應用程式檔案
    shutil.copytree('dist/研究寫作工具.app', os.path.join(installer_dir, '研究寫作工具.app'))
    
    # 複製其他必要檔案
    for file in ['../.env.example', '../README.md', '../requirements.txt']:
        if os.path.exists(file):
            shutil.copy2(file, installer_dir)
    
    # 建立安裝腳本
    create_macos_installer_script(installer_dir)
    
    # 建立說明文件
    create_readme(installer_dir)
    
    # 建立 ZIP 檔案
    print('正在建立安裝檔案...')
    zip_path = 'dist/研究寫作工具-macos'
    if os.path.exists(f'{zip_path}.zip'):
        os.remove(f'{zip_path}.zip')
    shutil.make_archive(zip_path, 'zip', 'dist/研究寫作工具-installer')
    
    print('macOS 安裝程式已建立完成！')
    print(f'安裝檔案位於：{zip_path}.zip')

def build_package(target_platform='current'):
    """建立安裝包"""
    try:
        # 清理舊的建置檔案
        clean_dist_directory()
        
        # 建立打包目錄
        if target_platform == 'windows':
            os.makedirs('dist/windows', exist_ok=True)
        else:
            os.makedirs('dist/macos', exist_ok=True)
        
        # 創建規格文件
        spec_file = create_spec_file(target_platform)
        
        if target_platform == 'windows':
            build_windows_installer()
        else:
            build_macos_package()
        
        print("Build completed!")
        print(f"Package has been generated in dist/{target_platform} directory.")
        
    except Exception as e:
        print(f"Error during build process: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    # 檢查命令行參數
    if len(sys.argv) > 1 and sys.argv[1] == '--windows':
        build_package('windows')
    elif len(sys.argv) > 1 and sys.argv[1] == '--macos':
        build_package('macos')
    else:
        print("請指定要建立的安裝程式類型：")
        print("  --windows : 建立 Windows 安裝程式")
        print("  --macos   : 建立 macOS 安裝程式") 