import streamlit as st
import os
import openai
from dotenv import load_dotenv
import json
import time
import subprocess

# 載入環境變數
load_dotenv()

# 設置 OpenAI API 金鑰
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    openai.api_key = api_key
else:
    openai.api_key = None

def generate_keywords(topic, content):
    """使用 OpenAI 生成關鍵字"""
    if not openai.api_key:
        st.error("OpenAI API 金鑰未設置！")
        return []

    prompt = f"""
請從以下研究主題和內容中，以台灣學術界常用的繁體中文術語提取10個最重要的關鍵詞（請同時提供中英對照）：

研究主題：
{topic}

研究內容：
{content}

請依照以下類別提供關鍵詞：
1. 研究領域相關（如：產品設計 / Product Design）
2. 研究方法相關（如：設計思考 / Design Thinking）
3. 研究對象相關（如：使用者經驗 / User Experience）
4. 理論框架相關（如：人機互動 / Human-Computer Interaction）
5. 預期成果相關（如：設計準則 / Design Guidelines）

請使用以下格式回覆，每行一個關鍵詞：
關鍵詞中文 / Keywords in English
"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": """你是一位深耕於產品設計研究與教學研究的專業學術研究者，熟悉各領域的學術用語，特別是在設計、科技、人文等跨領域研究中常用的專業術語。
在選擇關鍵詞時，請優先使用：
1. 台灣學術界普遍接受的術語翻譯
2. 具有學術指標性的專業用詞
3. 符合研究主題脈絡的用語"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        
        # 處理回應
        keywords = response['choices'][0]['message']['content'].strip().splitlines()
        return [keyword.strip() for keyword in keywords if keyword.strip()]
    except Exception as e:
        st.error(f"生成關鍵字時發生錯誤：{str(e)}")
        return []

def generate_search_query(selected_keywords):
    """生成搜尋查詢字串"""
    # 從中英對照格式中提取英文關鍵字
    english_keywords = [k.split(' / ')[-1].strip() for k in selected_keywords]
    # 只用空格連接英文關鍵字
    return ' '.join(english_keywords)

def generate_titles(topic, content, literature_summary):
    """使用 OpenAI 只生成研究題目選項"""
    if not openai.api_key:
        st.error("OpenAI API 金鑰未設置！")
        return None

    prompt = f"""
請根據以下資訊，生成三個研究題目選項：

研究主題：
{topic}

研究內容：
{content}

文獻資料：
{literature_summary}

請生成三個不同方向的研究題目：
1. 理論導向：基於文獻中的理論框架，探討產品設計與教學研究的理論基礎
2. 實務導向：針對文獻中發現的實務問題，提出具體的設計解決方案
3. 整合導向：結合理論與實務的創新角度，探索設計教育的新可能性

請依照以下格式回覆：

===建議研究題目===
1. 理論導向：
[中文題目] / [English Title]
（基於 [相關文獻作者] 的理論框架）

2. 實務導向：
[中文題目] / [English Title]
（針對 [相關文獻作者] 提出的實務問題）

3. 整合導向：
[中文題目] / [English Title]
（結合 [相關文獻作者] 的理論與實務觀點）
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": """你是一位深耕於產品設計研究與教學研究的專業學術研究者，經常結合人工智慧、感測裝置、虛擬實境與人機互動，視其為「感知演算法」、「存在疑問」與「倫理界面」的探索媒介。"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"生成研究題目時發生錯誤：{str(e)}")
        return None

def generate_full_content(research_topic, research_content, literature_summary, selected_title):
    """生成完整的研究目的和參考文獻"""
    try:
        # 構建提示詞
        prompt = f"""你是一位具有豐富研究與實務經驗的學者，請根據以下資訊，以自然且專業的學術論述方式，生成一份完整的研究目的和參考文獻：

研究主題：{research_topic}

研究內容：{research_content}

文獻摘要：{literature_summary}

選定標題：{selected_title}

【寫作要求】
1. 文章風格：
   - 運用第一人稱敘述，展現研究者的專業洞察
   - 保持學術嚴謹性的同時，融入個人觀點和經驗
   - 段落之間要有自然的邏輯推展
   - 避免過於制式化的表達方式

2. 論述方式：
   - 從實務觀察或理論缺口切入問題
   - 結合個人經驗與文獻證據
   - 展現思考的深度與廣度
   - 適度融入領域專業術語

3. 語言表達：
   - 使用流暢且專業的學術用語
   - 避免過度堆砌文獻
   - 保持論述的連貫性和邏輯性
   - 適時使用轉折語句增加文章流暢度

【內容架構】（至少1000字）：

1. 研究背景與問題意識（約400字）：
   - 從領域現況或實務觀察切入
   - 指出值得研究的問題或現象
   - 結合相關文獻說明研究重要性
   - 展現研究動機的發展脈絡

2. 研究目標與方法（約400字）：
   - 清楚說明研究目的
   - 解釋研究方法的選擇理由
   - 描述研究設計的思考邏輯
   - 說明預期達成的具體目標

3. 預期貢獻與研究價值（約200字）：
   - 說明研究的學術價值
   - 描述實務應用的可能性
   - 討論研究的創新之處
   - 提出未來研究方向

請注意：
1. 文獻引用要自然地融入論述中（APA格式）
2. 理論與實務的連結要有說服力
3. 確保研究目的的可行性與創新性
4. 整體論述要流暢且具邏輯性

最後請列出完整的參考文獻（APA格式）。"""

        # 使用 OpenAI API 生成內容
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": """你是一位經驗豐富的學術研究者，擅長結合理論與實務。在撰寫時：
1. 根據研究主題調整專業術語和論述方式
2. 自然地融入研究者的觀察與經驗
3. 展現深入的思考過程和邏輯推演
4. 維持學術嚴謹性和創新思維
5. 確保文章結構完整且論述流暢"""},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2500
        )

        # 提取生成的內容
        generated_text = response.choices[0].message.content.strip()
        
        # 分割研究目的和參考文獻
        parts = generated_text.split('參考文獻')
        purpose_content = parts[0].strip()
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
    if not openai.api_key:
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
                    
                    # 儲存研究目的內容
                    save_research_purpose(st.session_state.generated_purpose)
                else:
                    st.error("生成內容失敗，請重試。")

    # 如果已經生成內容，顯示「開始文獻分析」按鈕
    if st.session_state.generated_purpose:
        if st.button("開始文獻分析"):
            # 啟動文獻分析工具
            try:
                subprocess.Popen(["streamlit", "run", "literature_analysis.py"])
                st.success("已開啟文獻分析工具，請切換到新開啟的視窗繼續操作。")
            except Exception as e:
                st.error(f"啟動文獻分析工具時發生錯誤：{str(e)}")

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
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
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
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": """你是一位專業的學術研究者，擅長撰寫文獻探討。
特點：
- 善於整合不同文獻的觀點
- 能準確使用 APA 引用格式
- 擅長建立文獻之間的對話
- 能有效組織長篇幅的學術論述"""},
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