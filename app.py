# 注意：在本地运行时需要执行 pip install streamlit
import streamlit as st
import random
import re
import spacy

# 页面标题
st.title("🧩 句酷重构 - 英语造句练习")

# 1. 侧边栏：上传语料
st.sidebar.header("第一步：导入语料")
raw_text = st.sidebar.text_area("在此粘贴你的英文材料:", "The quick brown fox jumps over the wall.")

# 2. 逻辑处理 (复用你之前的代码)
def get_tokens(text):
    return re.findall(r"[\w']+|[.,!?;]", text)

if raw_text:
    sentences = re.split(r'([.?!])\s*', raw_text)
    # 简单演示：取第一个完整的句子
    target_sentence = sentences[0] + (sentences[1] if len(sentences)>1 else "")
    correct_tokens = get_tokens(target_sentence)
    
    # 3. 界面展示：乱序单词
    st.subheader("第二步：连词成句")
    st.write("请在脑海中对以下单词排序：")
    
    shuffled = correct_tokens[:]
    random.seed(42) # 固定随机种子方便演示
    random.shuffle(shuffled)
    
    # 用按钮展示单词
    cols = st.columns(len(shuffled))
    for i, word in enumerate(shuffled):
        cols[i].button(word, key=f"word_{i}")

    # 4. 提交区
    user_input = st.text_input("请在此输入你组合好的句子:")
    
    if st.button("检查答案"):
        if user_input.strip().lower() == target_sentence.strip().lower():
            st.success("🎉 太棒了！完全正确！")
        else:
            st.error("💡 差一点点，再试试看？")
            st.info(f"正确答案是: {target_sentence}")
