import os
import sys
import platform
import shutil
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

def build_windows_package():
    """建立 Windows 安裝程式"""
    print("正在建立 Windows 安裝程式...")
    
    # 檢查必要檔案
    required_files = [
        '../src/app.py',
        '../src/literature_analysis.py',
        '../requirements.txt',
        '../resources/app_icon.ico',
        '../.env.example',
        '../README.md',
        'installer.nsi'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"錯誤：找不到必要檔案 {file}")
            sys.exit(1)
    
    # 建立輸出目錄
    os.makedirs('dist', exist_ok=True)
    
    # 執行 NSIS 編譯
    print("正在編譯安裝程式...")
    result = os.system('makensis installer.nsi')
    
    if result == 0:
        print("Windows 安裝程式已建立完成！")
        print("安裝檔案位於：dist/windows_installer.exe")
    else:
        print("錯誤：無法建立安裝程式")
        print("請確認是否已安裝 NSIS，並將其加入系統 PATH")
        sys.exit(1)

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
            build_windows_package()
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
    else:
        build_package('current') 