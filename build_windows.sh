#!/bin/bash

# 建立 Docker 映像
docker build -t research-writer-builder .

# 運行容器並將打包結果複製到本地
docker run --name research-writer-build research-writer-builder
docker cp research-writer-build:/app/dist/windows ./dist/windows
docker rm research-writer-build

echo "Windows 版本打包完成！安裝包位於 dist/windows 目錄中。" 