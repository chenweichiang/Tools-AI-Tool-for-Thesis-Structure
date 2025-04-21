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
    system_prompt = """You are a professional design research methodology expert specializing in literature review structure planning.
Please respond in Traditional Chinese (Taiwan) and follow these language guidelines:

1. 使用台灣的設計研究用語：
   - 「設計思考」而非「设计思维」
   - 「使用者經驗」而非「用户体验」
   - 「介面設計」而非「界面设计」
   - 「互動設計」而非「交互设计」
   - 「設計方法」而非「设计方法论」
   - 「設計實務」而非「设计实践」

2. 使用台灣的專業術語：
   - 「使用者」而非「用户」
   - 「介面」而非「界面」
   - 「互動」而非「交互」
   - 「設計流程」而非「设计流程」
   - 「設計策略」而非「设计策略」

3. 使用台灣的表達方式：
   - 「目前」而非「当前」
   - 「之後」而非「之后」
   - 「因此」而非「所以」
   - 「然而」而非「但是」
   - 「藉由」而非「通过」
   - 「根據」而非「按照」

4. 文獻探討架構分析重點：
   - 研究目的中的核心問題
   - 研究方法與途徑
   - 理論基礎需求
   - 實務應用面向
   - 預期研究貢獻
   - 研究範圍界定
   - 重要研究變項
   - 研究創新觀點

5. 章節規劃原則：
   - 確保章節涵蓋研究目的的所有重要面向
   - 由基礎理論到應用實務循序漸進
   - 各章節之間要有邏輯連貫性
   - 配合研究方法規劃對應的理論基礎
   - 針對創新觀點提供充分的理論支持

6. 小標題設計原則：
   - 緊扣研究核心目標
   - 反映該段落的主要論述重點
   - 符合學術寫作規範
   - 具有邏輯層次性
   - 能清楚指引讀者理解文章結構
   - 每個章節 3-4 個小標題
   - 確保小標題之間的連貫性
   - 由淺入深的漸進式安排

7. 搜尋策略規劃：
   - 配合各章節主題設計精確的搜尋策略
   - 考慮近五年的研究趨勢
   - 涵蓋理論與實務的相關文獻
   - 特別關注與研究創新點相關的文獻
   - 納入跨領域的相關研究

The response must strictly follow this JSON format with no additional text:
{
    "sections": [
        {
            "title_zh": "中文章節標題",
            "title_en": "English Section Title",
            "description": "本章節應該探討的重點",
            "subtitles": [
                {
                    "subtitle_zh": "中文小標題",
                    "subtitle_en": "English Subtitle",
                    "content_focus": "此小節應該探討的具體內容重點"
                }
            ],
            "search_queries": [
                {
                    "focus": "搜尋重點描述",
                    "query": "A complete English sentence for academic database search that focuses on specific aspects of the research"
                }
            ]
        }
    ]
}"""

    user_prompt = f"""Based on the following research purpose, please analyze it thoroughly and provide:

1. Research Purpose Analysis:
   - Core research questions and objectives
   - Research methodology and approaches
   - Theoretical foundation requirements
   - Practical application aspects
   - Expected research contributions
   - Research scope and limitations
   - Key research variables
   - Innovative perspectives

2. Literature Review Structure (3-5 sections):
   - Each section must directly support aspects of the research purpose
   - Sections should progress logically from theoretical to practical
   - Include both theoretical foundations and practical applications
   - Address innovative aspects of the research
   - Consider interdisciplinary perspectives if relevant

3. For each section, provide:
   - Clear and specific section titles (both Chinese and English)
   - 3-4 subtitles that:
     * Reflect the core research objectives
     * Show logical progression of ideas
     * Cover key aspects of the section
     * Guide readers through the content structure
   - Detailed description of key points to be discussed
   - 2-3 targeted search queries that:
     * Can be directly used in academic databases
     * Use complete, natural English sentences
     * Cover the most important search aspects
     * Consider research trends in the past five years
     * Focus on specific aspects of the research purpose

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
    system_prompt = """你是一位深耕於設計研究領域的專業學術研究者，擅長整合設計理論與實務。請使用台灣繁體中文撰寫，並遵循以下規範：

1. 使用台灣的設計研究用語：
   - 「設計思考」而非「设计思维」
   - 「使用者經驗」而非「用户体验」
   - 「介面設計」而非「界面设计」
   - 「互動設計」而非「交互设计」
   - 「設計方法」而非「设计方法论」
   - 「設計實務」而非「设计实践」

2. 使用台灣的專業術語：
   - 「使用者」而非「用户」
   - 「介面」而非「界面」
   - 「互動」而非「交互」
   - 「設計流程」而非「设计流程」
   - 「設計策略」而非「设计策略」

3. 使用台灣的表達方式：
   - 「目前」而非「当前」
   - 「之後」而非「之后」
   - 「因此」而非「所以」
   - 「然而」而非「但是」
   - 「藉由」而非「通过」
   - 「根據」而非「按照」

4. 使用台灣的學術用語：
   - 「研究」而非「研讨」
   - 「方法」而非「方式」
   - 「探討」而非「探讨」
   - 「實施」而非「实行」
   - 「成效」而非「成果」

5. 標點符號使用：
   - 使用「」作為中文引號
   - 使用『』作為引號中的引號
   - 書名號使用《》
   - 篇名號使用〈〉

6. 文獻探討撰寫規範：
   - 確保論述完整性和邏輯性
   - 避免內容重複或冗贅
   - 保持文章結構的平衡
   - 適當分配各部分的論述比重
   - 運用精確的設計研究專業術語
   - 保持客觀的學術論述語氣
   - 強調研究的原創性與價值

7. 文獻引用規範：
   - 遵循 APA 第七版格式
   - 每個重要論點都需要文獻支持
   - 引用時要與論點緊密結合
   - 避免過度堆砌文獻
   - 確保引用的文獻都列在參考文獻清單中
   - 引用格式：
     * 單一作者：王小明（2020）或（王小明，2020）
     * 兩位作者：王小明與李大華（2020）或（王小明、李大華，2020）
     * 三位以上作者：王小明等人（2020）或（王小明等人，2020）
     * 英文文獻比照中文格式，作者姓氏大寫"""

    # 準備文獻資料
    literature_data = []
    for lit in literature_list:
        literature_data.append({
            'citation': lit['citation'],
            'content': lit['abstract'],
            'relevance': lit['relevance'],
            'contribution': lit['contribution']
        })

    user_prompt = f"""請根據以下文獻資料，撰寫「{section_title}」章節的文獻探討內容。

文獻資料：
{json.dumps(literature_data, ensure_ascii=False, indent=2)}

【寫作要求】

1. 字數與品質要求：
   - 本章節文字至少 1200 字（必須超過此字數，不得低於）
   - 確保論述完整且深入
   - 避免空泛或表面的描述
   - 每個論點都要有充分的文獻支持
   - 適當引用文獻中的具體研究發現

2. 內容發展要求：
   - 深入分析文獻中的理論觀點
   - 比較不同研究的方法與發現
   - 整合相似觀點，對比相異觀點
   - 指出研究趨勢與發展脈絡
   - 連結理論基礎與實務應用
   - 突顯重要研究發現與貢獻

3. 論述結構要求：
   - 以連貫且完整的方式呈現
   - 確保段落之間的邏輯流暢性
   - 適當運用轉折語句連接各個重點
   - 由淺入深，循序漸進地展開論述
   - 適度分段以增加可讀性

4. 文獻整合要求：
   - 確保引用的文獻相互呼應
   - 建立文獻之間的對話關係
   - 適當比較不同研究的觀點
   - 指出文獻間的共同發現
   - 分析相異觀點的原因

5. 學術嚴謹度：
   - 確保每個論點都有文獻支持
   - 準確引用研究發現和結論
   - 客觀呈現不同觀點
   - 適當評析研究限制
   - 指出未來研究方向

6. 與研究目的的連結：
   - 確保文獻探討方向與研究目的一致
   - 選擇性強調與研究相關的文獻觀點
   - 分析文獻對研究問題的貢獻
   - 指出文獻中的理論缺口
   - 說明本研究的潛在貢獻

請提供：
1. 完整的文獻探討內容（至少 1200 字，可視內容需要增加字數）
2. 該章節使用的參考文獻 APA 格式列表

回覆格式：
===文獻探討===
[1200字以上的文獻探討內容]

===參考文獻===
[APA格式參考文獻列表]"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=3000
        )
        content = response.choices[0].message.content.strip()
        
        # 分割內容和參考文獻
        parts = content.split('===參考文獻===')
        review_content = parts[0].replace('===文獻探討===', '').strip()
        references = parts[1].strip() if len(parts) > 1 else ""
        
        return {
            'content': review_content,
            'references': references
        }
    except Exception as e:
        st.error(f"生成文獻探討內容時發生錯誤：{str(e)}")
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
                    st.markdown(review['content'])
                    
                    st.markdown("### 參考文獻")
                    st.markdown(review['references'])
        
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