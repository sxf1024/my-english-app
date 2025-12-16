import streamlit as st
import random
import re
import spacy

# 页面配置
st.set_page_config(page_title="句酷重构", layout="wide")

# 加载 NLP 模型
@st.cache_resource
def load_nlp():
    try:
        return spacy.load("en_core_web_sm")
    except:
        st.error("模型加载失败，请检查 requirements.txt")
        return None

nlp = load_nlp()

st.title("🧩 英语连词成句训练器")
st.markdown("上传一段英文语料，将其拆解为单词卡片，练习你的造句能力！")

# --- 第一步：输入语料 ---
with st.expander("第一步：输入/修改语料", expanded=True):
    corpus = st.text_area("在此粘贴英文文本:", "The quick brown fox jumps over the lazy dog.", height=150)

# --- 第二步：处理语料 ---
def get_sentences(text):
    # 简单的句子分割
    return re.split(r'(?<=[.?!])\s+', text)

def get_tokens(sentence):
    # 拆分单词和标点
    return re.findall(r"[\w']+|[.,!?;]", sentence)

if corpus:
    all_sentences = get_sentences(corpus)
    
    # 让用户选择要练习哪一句
    if len(all_sentences) > 1:
        selected_idx = st.selectbox("选择要练习的句子:", range(len(all_sentences)), format_func=lambda x: f"句子 {x+1}: {all_sentences[x][:50]}...")
    else:
        selected_idx = 0
    
    target_sentence = all_sentences[selected_idx]
    correct_tokens = get_tokens(target_sentence)

    # --- 第三步：展示打乱的单词 ---
    st.subheader("第二步：开始测试")
    
    # 随机打乱（基于句子内容固定随机种子，防止页面一刷新单词就变位）
    shuffled_tokens = correct_tokens[:]
    random.seed(sum(ord(c) for c in target_sentence))
    random.shuffle(shuffled_tokens)

    st.write("打乱的单词块：")
    # 用亮色的小块展示单词
    st.write(" ".join([f"`{word}`" for word in shuffled_tokens]))

    # --- 第四步：用户输入与校验 ---
    user_answer = st.text_input("请按正确顺序输入完整的句子（注意标点和空格）:", placeholder="在这里输入答案...")

    if st.button("提交检查"):
        user_tokens = get_tokens(user_answer)
        
        # 结果显示
        if user_answer.strip().lower() == target_sentence.strip().lower():
            st.success("🎯 完全正确！你太棒了！")
        else:
            st.warning("🧐 顺序或拼写有误，对比一下：")
            st.write(f"**你的答案:** {user_answer}")
            st.write(f"**标准答案:** {target_sentence}")
        
        # 语法解析
        if nlp:
            st.subheader("💡 深度解析")
            doc = nlp(target_sentence)
            cols = st.columns(len(doc))
            for i, token in enumerate(doc):
                with cols[i % 5]: # 每行显示5个
                    st.metric(label=token.text, value=token.pos_)
                    st.caption(f"功能: {token.dep_}")

st.sidebar.markdown("---")
st.sidebar.info("使用说明：\n1. 粘贴语料\n2. 观察打乱的单词\n3. 在输入框重组句子\n4. 点击检查获取解析")
