import streamlit as st
import sys
import os

# 將 src 目錄加入 Python 路徑
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

# 導入主應用程式
from app import main

if __name__ == "__main__":
    main() 