import streamlit as st
import os
from dotenv import load_dotenv
import json
import re
from openai import OpenAI

# 載入環境變數
load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_json_from_response(content):
    """從回應中擷取 JSON 內容"""
    # 嘗試找出 JSON 內容的開始和結束
    try:
        # 找出第一個 { 和最後一個 } 的位置
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != -1:
            json_str = content[start:end]
            return json.loads(json_str)
    except:
        pass
    return None

def analyze_research_purpose(research_purpose):
    """分析研究目的並產生文獻探討架構"""
    system_prompt = """You are a professional research methodology expert specializing in literature review structure planning.
Please respond in Traditional Chinese for all content except search queries.
For search queries, provide complete English sentences that are effective for academic database searches.

The response must strictly follow this JSON format with no additional text:
{
    "sections": [
        {
            "title_zh": "中文章節標題",
            "title_en": "English Section Title",
            "description": "本章節應該探討的重點",
            "search_queries": [
                {
                    "focus": "搜尋重點描述",
                    "query": "A complete English sentence for academic database search that focuses on specific aspects of the research"
                }
            ]
        }
    ]
}"""

    user_prompt = f"""Based on the following research purpose, please provide:
1. 3-5 appropriate literature review section titles (in both Chinese and English)
2. Description of key points for each section
3. 2-3 search queries for each section that:
   - Can be directly used in academic databases
   - Use complete, natural English sentences
   - Cover the most important search aspects
   - Consider research trends in the past five years

Research Purpose:
{research_purpose}

Please strictly follow the JSON format specified in the system message, with no additional explanation."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        
        # 嘗試直接解析
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # 如果直接解析失敗，嘗試擷取 JSON 部分
            result = extract_json_from_response(content)
            if result:
                return result
            else:
                st.error("無法解析回應為 JSON 格式")
                st.text_area("原始回應內容", content, height=200)
                return None
    except Exception as e:
        st.error(f"發生錯誤：{str(e)}")
        return None

def analyze_multiple_literature(section_title, literature_texts):
    """分析多篇文獻內容並產生摘要分析"""
    system_prompt = """您是一位專業的文獻分析專家，請協助分析輸入的多篇文獻內容。
請使用台灣繁體中文的用字習慣撰寫分析內容，注意：
- 使用台灣的學術用語和專業術語
- 使用台灣的標點符號習慣（如：使用「」引號）
- 使用台灣的語氣詞和表達方式
- 避免使用中國大陸的用語習慣
從輸入的文字中識別出每篇文獻的 APA 引用格式和摘要內容，並進行分析整理。
每篇文獻之間應該是用連續兩個換行符號分隔。"""

    user_prompt = f"""請分析以下多篇文獻內容，並按照以下格式整理每一篇：
1. 識別並擷取每篇文獻的 APA 引用格式
2. 擷取每篇文獻的摘要內容
3. 分析每篇文獻與「{section_title}」章節的相關性
4. 提供每篇文獻對該章節的主要貢獻
5. 建議在文獻回顧中如何引用每篇文獻

輸入內容：
{literature_texts}

請使用以下 JSON 格式回覆，包含所有文獻的分析結果：
{{
    "literature": [
        {{
            "citation": "APA引用格式",
            "abstract": "摘要內容",
            "relevance": "與章節的相關性分析",
            "contribution": "對章節的主要貢獻",
            "usage_suggestion": "在文獻回顧中的引用建議"
        }}
    ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        
        try:
            result = json.loads(content)
            if 'literature' in result:
                return result['literature']
            return None
        except json.JSONDecodeError:
            result = extract_json_from_response(content)
            if result and 'literature' in result:
                return result['literature']
            else:
                st.error("無法解析文獻分析結果")
                st.text_area("原始回應內容", content, height=200)
                return None
    except Exception as e:
        st.error(f"分析文獻時發生錯誤：{str(e)}")
        return None

def generate_literature_review(section_title, literature_list):
    """產生文獻探討內容"""
    system_prompt = """您是一位深耕於研究領域的專業學術研究者，擅長整合文獻並撰寫具有深度的文獻探討。

【用字規範】
1. 使用台灣繁體中文的學術用語：
   - 「研究」而非「研讨」
   - 「歷程」而非「过程」
   - 「方法」而非「方式」
   - 「探討」而非「探讨」
   - 「實施」而非「实行」
   - 「成效」而非「成果」
   - 「議題」而非「课题」
   - 「建議」而非「建议」

2. 使用台灣的標點符號：
   - 使用「」作為中文引號
   - 使用『』作為引號中的引號
   - 破折號使用「──」
   - 書名號使用《》
   - 篇名號使用〈〉

3. 使用台灣的表達方式：
   - 「目前」而非「当前」
   - 「之後」而非「之后」
   - 「因此」而非「所以」
   - 「然而」而非「但是」
   - 「藉由」而非「通过」
   - 「根據」而非「按照」
   - 「顯示」而非「表明」

4. 使用台灣的專業術語：
   - 「資訊科技」而非「信息技术」
   - 「電腦」而非「计算机」
   - 「演算法」而非「算法」
   - 「人工智慧」而非「人工智能」
   - 「資料庫」而非「数据库」
   - 「網際網路」而非「互联网」

在撰寫時：
1. 根據研究主題調整專業術語和論述方式
2. 自然地融入研究者的觀察與經驗
3. 展現深入的思考過程和邏輯推演
4. 維持學術嚴謹性和創新思維
5. 確保文章結構完整且論述流暢"""

    user_prompt = f"""請根據以下文獻資料，為「{section_title}」章節撰寫文獻探討內容。

文獻資料：
{json.dumps(literature_list, ensure_ascii=False, indent=2)}

【撰寫要求】
1. 文章風格：
   - 運用第一人稱敘述，展現研究者的專業洞察
   - 保持學術嚴謹性的同時，融入個人觀點和經驗
   - 段落之間要有自然的邏輯推展
   - 避免過於制式化的表達方式

2. 論述方式：
   - 從文獻回顧中找出研究趨勢和缺口
   - 結合不同文獻的觀點進行比較和整合
   - 展現思考的深度與廣度
   - 適度融入領域專業術語

3. 語言表達：
   - 使用流暢且專業的學術用語
   - 避免過度堆砌文獻
   - 保持論述的連貫性和邏輯性
   - 適時使用轉折語句增加文章流暢度

【內容架構】（至少 800 字）：

1. 研究脈絡與趨勢分析（約 300 字）：
   - 分析該領域的研究發展脈絡
   - 指出主要研究方向和趨勢
   - 整合不同學者的觀點
   - 突顯重要的研究發現

2. 理論與實務的整合（約 300 字）：
   - 分析理論基礎和實務應用
   - 比較不同研究的方法和發現
   - 討論研究結果的實務意涵
   - 指出理論與實務的連結

3. 研究缺口與未來方向（約 200 字）：
   - 歸納目前研究的限制
   - 指出值得深入探討的議題
   - 提出可能的研究方向
   - 說明研究價值和重要性

請使用以下 JSON 格式回覆：
{{
    "literature_review": "完整的文獻探討內容",
    "references": [
        "APA格式的參考文獻列表"
    ],
    "key_findings": [
        "重要發現1",
        "重要發現2"
    ],
    "research_gaps": [
        "研究缺口1",
        "研究缺口2"
    ]
}}

注意事項：
1. 文獻引用要自然地融入論述中（使用 APA 格式）
2. 確保不同段落之間的邏輯連貫性
3. 適當使用轉折語句增加文章流暢度
4. 在保持客觀性的同時，也要展現個人的專業判斷"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )
        content = response.choices[0].message.content.strip()
        
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            result = extract_json_from_response(content)
            if result:
                return result
            else:
                st.error("無法解析文獻探討產生結果")
                st.text_area("原始回應內容", content, height=200)
                return None
    except Exception as e:
        st.error(f"產生文獻探討時發生錯誤：{str(e)}")
        return None

def load_research_purpose():
    """讀取儲存的研究目的內容"""
    try:
        with open('.research_purpose.tmp', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('research_purpose', '')
    except (FileNotFoundError, json.JSONDecodeError):
        return ''

def main():
    st.title("📚 研究文獻架構分析工具")
    st.write("本工具可以協助您根據研究目的規劃文獻探討架構，並提供適合的搜尋關鍵字。")
    
    # 初始化 session state
    if 'sections' not in st.session_state:
        st.session_state.sections = None
    if 'literature_data' not in st.session_state:
        st.session_state.literature_data = {}
    if 'literature_reviews' not in st.session_state:
        st.session_state.literature_reviews = {}
    
    # 讀取先前產生的研究目的
    saved_purpose = load_research_purpose()
    
    # 輸入區域
    research_purpose = st.text_area(
        "請貼入您的研究目的內容",
        value=saved_purpose,  # 使用儲存的內容作為預設值
        height=200,
        help="將您撰寫的研究目的內容貼在這裡"
    )
    
    if st.button("產生文獻探討架構"):
        if not research_purpose:
            st.error("請先輸入研究目的內容")
            return
            
        with st.spinner("正在分析研究目的並產生架構..."):
            result = analyze_research_purpose(research_purpose)
            if result and 'sections' in result:
                st.session_state.sections = result['sections']
                st.session_state.literature_data = {
                    section['title_zh']: {'literature': []}
                    for section in result['sections']
                }
    
    # 顯示結果和收集文獻
    if st.session_state.sections:
        for section in st.session_state.sections:
            st.markdown("---")
            st.markdown(f"## {section['title_zh']}")
            st.markdown(f"**重點說明：**\n{section['description']}")
            
            st.markdown("**建議搜尋字串：**")
            for search in section['search_queries']:
                st.markdown(f"- {search['focus']}:")
                st.code(search['query'], language="text")
            
            # 文獻收集區域
            st.markdown("### 📑 文獻收集")
            
            # 文獻輸入
            new_literature = st.text_area(
                "請貼入多篇文獻的 APA 引用格式與摘要（每篇文獻之間請空一行）",
                key=f"literature_{section['title_zh']}",
                height=400,
                help="從 SciSpace 複製多篇文獻的 APA 引用格式和摘要，每篇文獻之間請空一行"
            )
            
            col1, col2 = st.columns(2)
            
            # 新增文獻按鈕
            with col1:
                if st.button(f"分析並新增文獻到「{section['title_zh']}」", key=f"add_{section['title_zh']}"):
                    if new_literature.strip():
                        with st.spinner("正在分析文獻內容..."):
                            analysis_results = analyze_multiple_literature(section['title_zh'], new_literature)
                            if analysis_results:
                                st.session_state.literature_data[section['title_zh']]['literature'].extend(analysis_results)
                                st.success(f"已成功分析並新增 {len(analysis_results)} 篇文獻")
            
            # 產生文獻探討按鈕
            with col2:
                if st.button(f"產生「{section['title_zh']}」的文獻探討", key=f"review_{section['title_zh']}"):
                    if st.session_state.literature_data[section['title_zh']]['literature']:
                        with st.spinner("正在產生文獻探討內容..."):
                            review_result = generate_literature_review(
                                section['title_zh'],
                                st.session_state.literature_data[section['title_zh']]['literature']
                            )
                            if review_result:
                                st.session_state.literature_reviews[section['title_zh']] = review_result
                                st.success("已成功產生文獻探討內容")
                    else:
                        st.warning("請先新增文獻再產生文獻探討")
            
            # 顯示已收集的文獻
            if st.session_state.literature_data[section['title_zh']]['literature']:
                st.markdown("#### 已收集的文獻")
                for i, lit in enumerate(st.session_state.literature_data[section['title_zh']]['literature']):
                    with st.expander(f"文獻 {i+1}"):
                        st.markdown("**引用格式：**")
                        st.markdown(lit['citation'])
                        st.markdown("**摘要：**")
                        st.markdown(lit['abstract'])
                        st.markdown("**與本章節的相關性：**")
                        st.markdown(lit['relevance'])
                        st.markdown("**主要貢獻：**")
                        st.markdown(lit['contribution'])
                        st.markdown("**建議引用方式：**")
                        st.markdown(lit['usage_suggestion'])
            
            # 顯示文獻探討內容
            if section['title_zh'] in st.session_state.literature_reviews:
                review = st.session_state.literature_reviews[section['title_zh']]
                with st.expander("📝 文獻探討內容", expanded=True):
                    st.markdown("### 文獻探討")
                    st.markdown(review['literature_review'])
                    
                    st.markdown("### 重要發現")
                    for finding in review['key_findings']:
                        st.markdown(f"- {finding}")
                    
                    st.markdown("### 研究缺口")
                    for gap in review['research_gaps']:
                        st.markdown(f"- {gap}")
                    
                    st.markdown("### 參考文獻")
                    for ref in review['references']:
                        st.markdown(f"- {ref}")
        
        # 提供實用連結
        st.markdown("---")
        st.markdown("""
        ### 📖 操作提示
        1. 使用上方的搜尋字串在 [SciSpace](https://typeset.io/) 搜尋相關文獻
        2. 從搜尋結果中複製多篇文獻的 APA 引用格式和摘要
        3. 將複製的內容直接貼到對應章節的輸入框中（每篇文獻之間請空一行）
        4. 點選「分析並新增文獻」按鈕，系統會自動分析並整理所有文獻內容
        5. 收集足夠文獻後，點選「產生文獻探討」按鈕產生該章節的文獻探討內容
        6. 建議每個章節至少收集 3-5 篇相關文獻
        """)

if __name__ == "__main__":
    main() 