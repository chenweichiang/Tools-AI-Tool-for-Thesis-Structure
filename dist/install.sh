#!/bin/bash
echo "安裝研究寫作工具..."

# 創建安裝目錄
INSTALL_DIR="$HOME/Applications/ResearchWriter"
mkdir -p "$INSTALL_DIR"

# 複製文件
cp -R dist/* "$INSTALL_DIR/"

# 創建桌面快捷方式
DESKTOP_FILE="$HOME/Desktop/研究寫作工具.command"
echo '#!/bin/bash' > "$DESKTOP_FILE"
echo "cd \"$INSTALL_DIR\"" >> "$DESKTOP_FILE"
echo "./研究寫作工具" >> "$DESKTOP_FILE"
chmod +x "$DESKTOP_FILE"

# 提示輸入 OpenAI API Key
read -p "請輸入您的 OpenAI API Key: " OPENAI_API_KEY
echo "OPENAI_API_KEY=$OPENAI_API_KEY" > "$INSTALL_DIR/.env"

echo "安裝完成！"
echo "您可以從桌面上的快捷方式啟動應用程序。"
