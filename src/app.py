import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import time
import subprocess

# 載入環境變數
load_dotenv()

# 初始化 OpenAI 客戶端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_keywords(topic, content):
    """使用 OpenAI 生成關鍵字"""
    try:
        # 使用新版 API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """你是一個專業的設計研究助手，專門負責從研究主題和內容中提取核心關鍵字。

規則：
1. 只回傳關鍵字清單，每行一個關鍵字
2. 每個關鍵字必須包含中英文對照，使用 / 分隔
3. 不要包含任何其他說明文字或標點符號
4. 關鍵字應該要能反映研究的核心概念
5. 英文關鍵字使用學術資料庫常見的用詞
6. 每個關鍵字的格式必須是：中文關鍵字 / English Keyword
7. 總數限制在 5-7 個最重要的關鍵字

範例格式：
設計思考 / Design Thinking
使用者經驗 / User Experience
介面設計 / Interface Design"""},
                {"role": "user", "content": f"請從以下研究主題和內容中提取最核心的關鍵字（中英對照）：\n\n研究主題：{topic}\n\n研究內容：{content}"}
            ],
            temperature=0.3
        )
        
        # 從回應中提取內容並過濾空行
        keywords = [line.strip() for line in response.choices[0].message.content.strip().splitlines() if line.strip()]
        return keywords
    except Exception as e:
        st.error(f"生成關鍵字時發生錯誤：{str(e)}")
        return []

def generate_search_query(selected_keywords):
    """生成搜尋查詢字串"""
    try:
        # 使用 OpenAI 生成完整的英文搜尋句子
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a research assistant helping to create academic search queries. Create natural, complete English sentences that would be effective for academic database searches."},
                {"role": "user", "content": f"Create a comprehensive academic search query using these keywords: {', '.join(selected_keywords)}. The query should be a complete English sentence suitable for academic database searches."}
            ],
            temperature=0.3
        )
        
        # 從回應中提取搜尋句子
        search_query = response.choices[0].message.content.strip()
        return search_query
    except Exception as e:
        st.error(f"生成搜尋查詢時發生錯誤：{str(e)}")
        # 如果 API 呼叫失敗，退回到簡單的關鍵字組合
        english_keywords = [k.split(' / ')[-1].strip() for k in selected_keywords]
        return ' '.join(english_keywords)

def generate_titles(topic, content, literature_summary):
    """使用 OpenAI 生成研究題目選項"""
    if not client:
        st.error("OpenAI API 金鑰未設置！")
        return None

    prompt = f"""你是一位深耕於設計研究領域的專業學術研究者，請根據以下所有資訊，生成三個符合學術規範的研究題目選項。請特別注意整合所有提供的資訊，確保題目緊密連結研究主題與內容：

研究主題：
{topic}

研究內容：
{content}

文獻資料：
{literature_summary}

【題目生成要求】

1. 資料整合原則：
   - 完整分析研究主題的核心問題
   - 參考研究內容規劃的方向
   - 整合文獻資料的理論基礎
   - 確保題目反映研究重點
   - 納入關鍵概念與專業術語

2. 題目類型要求：
   A. 理論導向題目：
      - 基於文獻中的理論框架
      - 聚焦於設計理論的發展
      - 強調理論創新或整合
      - 反映文獻中的理論缺口
      - 使用理論相關的專業術語

   B. 實務導向題目：
      - 針對實際設計問題
      - 強調解決方案的開發
      - 連結設計實務需求
      - 體現應用價值
      - 使用實務相關的專業術語

   C. 整合導向題目：
      - 結合理論與實務觀點
      - 強調創新的整合方法
      - 平衡理論與應用
      - 展現研究的獨特性
      - 使用跨領域的專業術語

3. 題目格式規範：
   - 清晰準確的用詞
   - 適當的研究範圍界定
   - 符合學術寫作規範
   - 中英文對照
   - 點出研究方法或取向

4. 品質要求：
   - 確保題目的原創性
   - 維持學術的嚴謹性
   - 反映研究的可行性
   - 展現研究的價值
   - 符合設計研究領域慣例

請依照以下格式回覆：

===建議研究題目===
1. 理論導向：
[中文題目] / [English Title]
（基於文獻分析，聚焦於[具體理論框架]的研究）

2. 實務導向：
[中文題目] / [English Title]
（針對[具體實務問題]，提出解決方案）

3. 整合導向：
[中文題目] / [English Title]
（結合[理論基礎]與[實務應用]的創新研究）

每個題目後請附上 2-3 句說明：
- 如何整合了前述資料
- 研究重點為何
- 預期貢獻"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """你是一位深耕於設計研究領域的專業學術研究者，擅長整合設計理論與實務。請使用台灣繁體中文撰寫，並遵循以下規範：

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
   - 「因此」而非「所以」
   - 「然而」而非「但是」
   - 「藉由」而非「通过」
   - 「根據」而非「按照」

4. 標點符號使用：
   - 使用「」作為中文引號
   - 使用『』作為引號中的引號
   - 書名號使用《》
   - 篇名號使用〈〉

5. 研究題目命名原則：
   - 清楚表達研究主題
   - 點出研究方法或途徑
   - 說明研究對象或範圍
   - 展現研究的創新性
   - 符合學術寫作規範"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"生成研究題目時發生錯誤：{str(e)}")
        return None

def generate_full_content(research_topic, research_content, literature_summary, selected_title):
    """生成完整的研究目的和參考文獻"""
    try:
        # 構建提示詞
        prompt = f"""你是一位具有豐富設計研究與實務經驗的學者，請根據以下所有資訊，以自然且專業的學術論述方式，生成一份完整的研究目的和參考文獻。請特別注意整合所有提供的資訊，確保論述完整且字數充足：

研究主題：{research_topic}

研究內容：{research_content}

文獻摘要：{literature_summary}

選定標題：{selected_title}

【內容整合要求】
1. 資料運用：
   - 完整分析研究主題中提出的問題意識
   - 整合研究內容規劃的方法與步驟
   - 參考文獻摘要中的理論基礎
   - 呼應選定題目的研究方向
   - 確保關鍵字概念在文中得到充分討論

2. 內容發展：
   - 從研究主題發展出問題意識
   - 利用文獻摘要支持論點
   - 結合研究內容規劃說明方法
   - 根據前述資料推導出預期貢獻
   - 適當引用文獻支持各項論述

【研究目的撰寫要求】（至少1000字，可視內容需要增加字數）

1. 論述風格：
   - 以專業設計學術研究者的視角撰寫
   - 運用第一人稱敘述，展現研究者的專業洞察
   - 避免過於口語化或制式化的表達
   - 確保論述的學術性和專業性

2. 內容要素：
   - 從設計領域的理論缺口或實務問題切入
   - 整合並分析相關文獻的觀點
   - 清楚說明研究動機和重要性
   - 具體描述研究目標和方法
   - 闡述預期的理論與實務貢獻

3. 論述結構：
   - 以連貫且完整的方式呈現（不分小標題）
   - 確保段落之間的邏輯流暢性
   - 適當運用轉折語句連接各個重點
   - 由淺入深，循序漸進地展開論述

4. 論述重點：
   第一部分（至少350字）：
   - 從設計領域現況切入問題
   - 指出研究缺口或實務需求
   - 引用文獻支持問題的重要性
   - 整合研究主題的核心觀點

   第二部分（至少400字）：
   - 說明研究目標和研究問題
   - 解釋研究方法的選擇
   - 描述研究的具體步驟
   - 結合研究內容的規劃說明

   第三部分（至少250字）：
   - 闡述研究的創新觀點
   - 說明預期的理論貢獻
   - 討論實務應用價值
   - 點出研究限制與建議

5. 文獻引用規範：
   - 必須引用文獻摘要中提供的文獻
   - 每個重要論點都需要文獻支持
   - 遵循 APA 第七版引用格式：
     * 單一作者：王小明（2020）或（王小明，2020）
     * 兩位作者：王小明與李大華（2020）或（王小明、李大華，2020）
     * 三位以上作者：王小明等人（2020）或（王小明等人，2020）
     * 英文文獻比照中文格式，作者姓氏大寫
   - 引用時要與論點緊密結合
   - 避免過度堆砌文獻
   - 確保引用的文獻都列在參考文獻清單中

6. 寫作規範：
   - 運用精確的設計研究專業術語
   - 保持客觀的學術論述語氣
   - 強調研究的原創性與價值
   - 適當融入文獻觀點以支持論述

【字數與品質控制】
1. 字數要求：
   - 總字數必須超過1000字
   - 可視內容需要適度增加字數
   - 各部分字數可依實際需求調整，但不得低於建議字數

2. 品質要求：
   - 確保論述完整性和邏輯性
   - 避免內容重複或冗贅
   - 保持文章結構的平衡
   - 適當分配各部分的論述比重

【參考文獻要求】
1. 格式規範：
   - 嚴格遵循 APA 第七版格式
   - 依照字母順序排列
   - 中文文獻在前，英文文獻在後
   - 同一作者的多篇文獻依年代排序

2. 引用規則：
   - 只列出在內文中實際引用過的文獻
   - 確保每個引用都有對應的參考文獻
   - 每個重要論點都需要有文獻支持
   - 引用時要標明年份，必要時標明頁碼

3. 文獻類型：
   - 學術期刊論文
   - 研討會論文
   - 專書或專書章節
   - 博碩士論文（如適用）

請以以下格式回覆：

===研究目的===
[至少1000字完整研究目的論述，包含適當的文獻引用，並整合所有提供的資訊]

===參考文獻===
[APA格式參考文獻列表]"""

        # 使用 OpenAI API 生成內容
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """你是一位經驗豐富的設計研究學者，擅長整合設計理論與實務。請使用台灣繁體中文撰寫，並遵循以下規範：

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

5. APA 參考文獻格式：
   - 中文文獻：
     期刊：作者（年代）。文章標題。期刊名稱，卷（期），頁碼。
     專書：作者（年代）。書名。出版社。
   - 英文文獻：
     期刊：Author, A. A. (Year). Title. Journal Name, Volume(Issue), pages.
     專書：Author, A. A. (Year). Book title. Publisher.
   - 中文作者姓名完整列出
   - 英文作者姓氏加名字縮寫"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )

        # 提取生成的內容
        generated_text = response.choices[0].message.content.strip()
        
        # 分割研究目的和參考文獻
        parts = generated_text.split('===參考文獻===')
        purpose_content = parts[0].replace('===研究目的===', '').strip()
        references_content = parts[1].strip() if len(parts) > 1 else ""

        return purpose_content, references_content

    except Exception as e:
        st.error(f"生成過程中發生錯誤：{str(e)}")
        return None, None

def save_research_purpose(content):
    """將研究目的內容儲存到暫存檔案"""
    with open('.research_purpose.tmp', 'w', encoding='utf-8') as f:
        json.dump({'research_purpose': content}, f, ensure_ascii=False)

def main():
    st.title("研究目的與文獻探討生成助手")
    st.write("此工具將協助您以專業學術用語撰寫研究目的陳述與文獻探討，整合理論架構與實務應用。")
    
    # 檢查 API 金鑰
    if not client:
        st.error("請設置 OPENAI_API_KEY 環境變數！")
        st.stop()
    
    # 初始化 session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'keywords' not in st.session_state:
        st.session_state.keywords = []
    if 'research_topic' not in st.session_state:
        st.session_state.research_topic = ""
    if 'research_content' not in st.session_state:
        st.session_state.research_content = ""
    if 'selected_keywords' not in st.session_state:
        st.session_state.selected_keywords = []
    if 'literature_summary' not in st.session_state:
        st.session_state.literature_summary = ""
    if 'generated_result' not in st.session_state:
        st.session_state.generated_result = None
    if 'selected_title' not in st.session_state:
        st.session_state.selected_title = None
    if 'generated_purpose' not in st.session_state:
        st.session_state.generated_purpose = None
    if 'references' not in st.session_state:
        st.session_state.references = None
    if 'collected_literature' not in st.session_state:
        st.session_state.collected_literature = {}
    
    # 顯示當前進度
    if st.session_state.step > 1:
        with st.expander("已完成的內容", expanded=False):
            if st.session_state.research_topic:
                st.markdown("### 研究主題")
                st.markdown(st.session_state.research_topic)
            if st.session_state.selected_title:
                st.markdown("### 選定的研究題目")
                st.markdown(st.session_state.selected_title['title'])
            if st.session_state.generated_purpose:
                st.markdown("### 研究目的")
                st.markdown(st.session_state.generated_purpose)

    # 第一步：輸入研究主題
    st.header("第一步：研究主題界定")
    st.markdown("*請闡述您的研究主題，可包含研究動機、問題意識或理論探討方向。*")
    research_topic = st.text_area("研究主題：", 
                                value=st.session_state.research_topic,
                                height=100,
                                key="topic_input",
                                help="建議從理論缺口或實務問題出發，說明研究價值")
    
    # 第二步：輸入研究想要探討的內容
    st.header("第二步：研究內容規劃")
    st.markdown("*請詳述您的研究規劃，包含研究方法、理論架構、研究對象等要素。*")
    research_content = st.text_area("研究內容：",
                                  value=st.session_state.research_content,
                                  height=150,
                                  key="content_input",
                                  help="可包含：理論基礎、研究方法、研究對象、預期貢獻")
    
    # 生成關鍵字按鈕
    if st.button("產生關鍵詞", key="generate_keywords_button"):
        if research_topic and research_content:
            st.session_state.research_topic = research_topic
            st.session_state.research_content = research_content
            with st.spinner("正在產生關鍵詞..."):
                keywords = generate_keywords(research_topic, research_content)
                if keywords:
                    st.session_state.keywords = keywords
                    st.session_state.step = 2
        else:
            st.error("請完整填寫研究主題與研究內容！")
    
    # 顯示關鍵字選擇（如果已生成）
    if st.session_state.step >= 2 and st.session_state.keywords:
        st.header("第三步：關鍵詞選擇")
        st.markdown("*請選擇最能代表您研究核心概念的關鍵詞。*")
        selected_keywords = st.multiselect(
            "關鍵詞選擇：",
            st.session_state.keywords,
            default=st.session_state.keywords[:5],
            key="keyword_selector",
            help="建議選擇 5-7 個最具代表性的關鍵詞"
        )
        
        if selected_keywords:
            st.session_state.selected_keywords = selected_keywords
            search_query = generate_search_query(selected_keywords)
            
            st.header("第四步：文獻檢索")
            st.markdown("*使用系統生成的檢索字串在 SciSpace 進行文獻搜尋。*")
            st.write("檢索字串：")
            st.code(search_query)
            
            # 提供 SciSpace 連結
            scispace_url = f"https://scispace.com/search?q={search_query}"
            st.markdown(f"[前往 SciSpace 搜尋相關文獻]({scispace_url})")
            
            # 第五步：文獻摘要輸入
            st.header("第五步：文獻回顧彙整")
            st.markdown("*請依序輸入文獻的 APA 格式引用資訊，以及文獻的重要內容摘要。*")
            literature_summary = st.text_area(
                "文獻資料：",
                height=300,
                key="literature_input",
                help="""請依照以下格式輸入：

1. APA 格式引用：
[請貼上完整的 APA 格式文獻資訊]

2. 文獻重要內容：
- 研究目的
- 重要發現
- 研究方法
- 理論架構
- 研究貢獻
                """
            )
            
            # 生成研究題目按鈕
            if st.button("生成研究題目", key="generate_titles_button"):
                if literature_summary:
                    st.session_state.literature_summary = literature_summary
                    with st.spinner("正在生成研究題目選項..."):
                        titles_result = generate_titles(
                            st.session_state.research_topic,
                            st.session_state.research_content,
                            literature_summary
                        )
                        if titles_result:
                            st.session_state.generated_titles = titles_result
                            st.session_state.step = 6
                            st.rerun()

    # 顯示題目選擇
    if st.session_state.step == 6 and st.session_state.get('generated_titles'):
        st.header("第六步：選擇研究題目")
        titles_section = st.session_state.generated_titles.split('===建議研究題目===')
        if len(titles_section) > 1:
            titles_content = titles_section[1].strip()
            titles = []
            current_title = {"type": "", "title": "", "description": ""}
            
            for line in titles_content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith('1. ') or line.startswith('2. ') or line.startswith('3. '):
                    if current_title["title"]:
                        titles.append(current_title.copy())
                        current_title = {"type": "", "title": "", "description": ""}
                    current_title["type"] = line
                elif '/' in line and not line.startswith('（'):
                    current_title["title"] = line
                elif line.startswith('（'):
                    current_title["description"] = line
            
            if current_title["title"]:
                titles.append(current_title.copy())
            
            st.markdown("### 請選擇研究題目")
            for i, title in enumerate(titles):
                with st.container():
                    st.markdown(f"**{title['type']}**")
                    st.markdown(f"**題目：** {title['title']}")
                    st.markdown(f"**說明：** {title['description']}")
                    if st.button(f"選擇此題目", key=f"select_title_{i}"):
                        st.session_state.selected_title = title
                        st.session_state.step = 7
                        st.rerun()
                st.markdown("---")

    # 生成完整內容
    if st.session_state.step == 7 and st.session_state.get('selected_title'):
        st.header("第七步：生成研究目的")
        st.info(f"**已選擇的題目：**\n\n{st.session_state.selected_title['title']}\n\n**類型：**\n{st.session_state.selected_title['type']}\n\n**說明：**\n{st.session_state.selected_title['description']}")
        
        # 檢查輸入資料完整性
        if not st.session_state.literature_summary or len(st.session_state.literature_summary.strip()) < 100:
            st.warning("⚠️ 請確保提供足夠詳細的文獻資料，這將有助於生成更好的研究目的。")
            st.markdown("""
            **文獻資料應包含：**
            1. 完整的 APA 格式引用
            2. 文獻的主要發現
            3. 研究方法說明
            4. 理論框架描述
            5. 研究貢獻說明
            """)
        
        # 生成研究目的按鈕
        if st.button("生成完整研究目的"):
            with st.spinner("正在生成研究目的..."):
                # 直接調用生成函數
                purpose_content, references = generate_full_content(
                    st.session_state.research_topic,
                    st.session_state.research_content,
                    st.session_state.literature_summary,
                    st.session_state.selected_title
                )
                
                if purpose_content and references:
                    st.session_state.generated_purpose = purpose_content
                    st.session_state.references = references
                    
                    # 顯示生成的內容
                    st.markdown("## 📝 研究目的")
                    st.info(f"**{st.session_state.selected_title}**")
                    st.markdown(st.session_state.generated_purpose)
                    st.caption(f"*內容長度：{len(st.session_state.generated_purpose)} 字*")
                    
                    st.markdown("### 📚 參考文獻")
                    st.markdown(st.session_state.references)
                    st.caption(f"*參考文獻數量：{len(st.session_state.references.splitlines())} 筆*")
                    
                    # 如果已經生成內容，顯示「開始文獻分析」按鈕
                    if st.session_state.generated_purpose:
                        st.info("您可以在側邊欄選擇「文獻分析工具」來開始進行文獻分析。")
                    
                    # 儲存研究目的內容
                    save_research_purpose(st.session_state.generated_purpose)
                else:
                    st.error("生成內容失敗，請重試。")

    # 如果已經生成內容，顯示「開始文獻分析」按鈕
    if st.session_state.generated_purpose:
        st.info("您可以在側邊欄選擇「文獻分析工具」來開始進行文獻分析。")
        
        # 儲存研究目的內容
        save_research_purpose(st.session_state.generated_purpose)

    # 文獻探討階段
    if st.session_state.step == 8:
        st.header("文獻探討階段")
        
        # 顯示已選擇的題目和研究目的
        st.markdown("### 已選擇的研究題目")
        st.markdown(st.session_state.selected_title)
        st.markdown("### 研究目的")
        st.markdown(st.session_state.generated_purpose)
        st.markdown("### 目前的參考文獻")
        st.markdown(st.session_state.references)
        
        # 生成文獻探討架構
        if not st.session_state.get('literature_sections'):
            with st.spinner("正在分析研究目的，規劃文獻探討架構..."):
                sections = generate_literature_review_sections(
                    st.session_state.selected_title,
                    st.session_state.generated_purpose,
                    st.session_state.references
                )
                st.session_state.literature_sections = sections
        
        # 顯示文獻探討架構和搜尋建議
        if st.session_state.literature_sections:
            st.subheader("文獻探討架構")
            for section in st.session_state.literature_sections:
                with st.expander(f"第 {section['order']} 節：{section['title']}", expanded=True):
                    st.markdown(f"**說明：** {section['description']}")
                    st.markdown("**建議搜尋關鍵字：**")
                    st.code(section['search_terms'])
                    
                    # 文獻收集區
                    st.markdown("### 文獻收集")
                    literature_key = f"literature_{section['order']}"
                    if literature_key not in st.session_state.collected_literature:
                        st.session_state.collected_literature[literature_key] = []
                    
                    # 新增文獻表單
                    with st.form(f"add_literature_{section['order']}"):
                        apa_citation = st.text_area("APA 引用格式：", key=f"apa_{section['order']}")
                        summary = st.text_area("文獻摘要：", key=f"summary_{section['order']}")
                        if st.form_submit_button("新增文獻"):
                            if apa_citation and summary:
                                st.session_state.collected_literature[literature_key].append({
                                    'citation': apa_citation,
                                    'summary': summary
                                })
                                st.success("文獻已新增！")
                                st.rerun()
                    
                    # 顯示已收集的文獻
                    if st.session_state.collected_literature[literature_key]:
                        st.markdown("**已收集的文獻：**")
                        for i, lit in enumerate(st.session_state.collected_literature[literature_key]):
                            st.markdown(f"文獻 {i+1}:")
                            st.markdown(f"引用: {lit['citation']}")
                            st.markdown(f"摘要: {lit['summary']}")
                            st.markdown("---")
            
            # 生成文獻探討按鈕
            if st.button("生成文獻探討", key="generate_literature_review"):
                with st.spinner("正在生成文獻探討..."):
                    literature_review = generate_full_literature_review(
                        st.session_state.selected_title,
                        st.session_state.generated_purpose,
                        st.session_state.literature_sections,
                        st.session_state.collected_literature
                    )
                    if literature_review:
                        st.markdown("### 文獻探討")
                        st.markdown(literature_review['content'])
                        st.markdown("### 更新後的參考文獻")
                        st.markdown(literature_review['references'])
                        st.session_state.references = literature_review['references']
                        st.success("文獻探討已生成完成！")

def generate_literature_review_sections(title, purpose, references):
    """生成文獻探討的分節架構"""
    prompt = f"""
請根據以下研究資訊，規劃文獻探討的架構：

研究題目：
{title}

研究目的：
{purpose}

目前的參考文獻：
{references}

請規劃 3-5 個文獻探討的主要段落，每個段落需包含：
1. 段落標題
2. 內容說明
3. 建議的搜尋關鍵字（中英對照）

回覆格式：
===段落1===
標題：[段落標題]
說明：[本段落要探討的重點]
搜尋關鍵字：[關鍵字列表]

===段落2===
...以此類推
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位專業的學術研究者，擅長規劃文獻探討架構。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        result = response.choices[0].message.content.strip()
        sections = []
        current_section = {}
        
        for line in result.splitlines():
            if line.startswith('===段落') and line.endswith('==='):
                if current_section:
                    sections.append(current_section)
                current_section = {'order': len(sections) + 1}
            elif line.startswith('標題：'):
                current_section['title'] = line.replace('標題：', '').strip()
            elif line.startswith('說明：'):
                current_section['description'] = line.replace('說明：', '').strip()
            elif line.startswith('搜尋關鍵字：'):
                current_section['search_terms'] = line.replace('搜尋關鍵字：', '').strip()
        
        if current_section:
            sections.append(current_section)
        
        return sections
    except Exception as e:
        st.error(f"生成文獻探討架構時發生錯誤：{str(e)}")
        return None

def generate_full_literature_review(title, purpose, sections, collected_literature):
    """生成完整的文獻探討內容"""
    prompt = f"""
請根據以下資料，撰寫一份完整的文獻探討（至少 3500 字）：

研究題目：
{title}

研究目的：
{purpose}

各節文獻資料：
{json.dumps(collected_literature, ensure_ascii=False, indent=2)}

要求：
1. 總字數至少 3500 字
2. 依照各節規劃的主題分段撰寫
3. 每段文獻都要適當引用並整合相關文獻
4. 段落之間要有適當的轉折
5. 最後要列出完整的參考文獻（APA格式）

請依照以下格式回覆：

===文獻探討===
[3500字以上的文獻探討內容]

===參考文獻===
[APA格式的參考文獻列表]
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一位專業的學術研究者，擅長撰寫文獻探討。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        result = response.choices[0].message.content.strip()
        parts = result.split('===參考文獻===')
        
        return {
            'content': parts[0].replace('===文獻探討===', '').strip(),
            'references': parts[1].strip() if len(parts) > 1 else ''
        }
    except Exception as e:
        st.error(f"生成文獻探討時發生錯誤：{str(e)}")
        return None

if __name__ == "__main__":
    main() 