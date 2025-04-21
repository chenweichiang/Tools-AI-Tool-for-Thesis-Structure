#!/bin/bash

# 切換到腳本所在目錄
cd "$(dirname "$0")"

# 檢查是否已安裝 NSIS
if ! command -v makensis &> /dev/null; then
    echo "錯誤：找不到 NSIS。請先安裝 NSIS。"
    echo "在 macOS 上可以使用 Homebrew 安裝："
    echo "brew install makensis"
    exit 1
fi

# 執行建置腳本
python3 build_installer.py --windows

# 建立 Docker 映像
docker build -t research-writer-builder .

# 運行容器並將打包結果複製到本地
docker run --name research-writer-build research-writer-builder
docker cp research-writer-build:/app/dist/windows ./dist/windows
docker rm research-writer-build

echo "Windows 版本打包完成！安裝包位於 dist/windows 目錄中。" 