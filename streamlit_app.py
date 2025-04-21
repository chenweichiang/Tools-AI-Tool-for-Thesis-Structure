import streamlit as st
import sys
import os

# 將 src 目錄加入 Python 路徑
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.append(src_path)

# 導入應用程式
from app import main as app_main
from literature_analysis import main as literature_main

# 設定頁面配置
st.set_page_config(
    page_title="研究寫作工具",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 在側邊欄添加頁面選擇
page = st.sidebar.radio(
    "選擇功能",
    ["研究目的生成", "文獻分析工具"]
)

if page == "研究目的生成":
    app_main()
else:
    literature_main() 