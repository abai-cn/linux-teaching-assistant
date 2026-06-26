"""
Linux 课助教 · DeepSeek V4
"""
import streamlit as st
import os
from modules import grade, ocr_image, analyze_completion, diagnose_student, generate_questions, ask

st.set_page_config(page_title="Linux 课助教", page_icon="🐧", layout="wide")

# ── API Key 持久化 ──────────────────────────
KEY_FILE = os.path.join(os.path.dirname(__file__), ".apikey")

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE) as f:
            return f.read().strip()
    return ""

def save_key(key):
    with open(KEY_FILE, "w") as f:
        f.write(key)

# ── 轻量 CSS ────────────────────────────────
st.markdown("""
<style>
    .stApp { background: #111; }
    header[data-testid="stHeader"] { display: none; }
    section[data-testid="stSidebar"] { background: #1a1a1a; }
    section[data-testid="stSidebar"] * { color: #ddd !important; }
    .stChatMessage { background: #1e1e1e; border-radius: 14px; padding: 14px 18px; margin: 6px 0; }
    [data-testid="stChatMessageAvatar"] { font-size: 1.4rem !important; }
    .stChatMessage [data-testid="chat-avatar"] { font-size: 1.4rem !important; }
    .stButton > button { border-radius: 10px; }
    h1, h2, h3, p, .stMarkdown { color: #eee !important; }
    .stChatInput textarea { background: #222 !important; color: #eee !important; border-color: #333 !important; }
    .stAlert { background: #2a2a2a !important; color: #ddd !important; }
</style>
""", unsafe_allow_html=True)

# ── 初始化 ────────────────────────────────
WELCOME = """你好！我是 **Linux 课助教** 🐧

直接跟我说你想做什么：
• 粘贴学生脚本 → 我批改
• 发成绩数据 → 我分析
• 描述学生情况 → 我诊断
• 说出题要求 → 我出题"""

if "msgs" not in st.session_state:
    st.session_state.msgs = [{"role": "assistant", "content": WELCOME}]
if "model" not in st.session_state:
    st.session_state.model = "deepseek-v4-flash"

# ── 侧边栏 ────────────────────────────────
with st.sidebar:
    st.title("🐧 Linux 课助教")

    if st.button("＋ 新对话", use_container_width=True):
        st.session_state.msgs = [{"role": "assistant", "content": WELCOME}]
        st.rerun()

    st.divider()
    st.subheader("🔑 API Key")

    # 云端：仅 session；本地：自动记住
    is_cloud = "STREAMLIT_RUNTIME" in os.environ or os.environ.get("STREAMLIT_SHARING_MODE") == "streamlit"
    saved = "" if is_cloud else load_key()

    # 已保存 Key 时只显示状态，不显示输入框
    if "key_ready" not in st.session_state:
        st.session_state.key_ready = bool(saved)

    if st.session_state.key_ready:
        model = st.selectbox("模型",
            ["deepseek-v4-flash", "deepseek-v4-pro"],
            label_visibility="collapsed"
        )
        st.session_state.model = model
        st.success(f"✅ {model}")
        api_key = saved or st.session_state.get("api_key_val", "")
        if st.button("更换 Key", use_container_width=True):
            st.session_state.key_ready = False
            st.session_state.api_key_val = ""
            if not is_cloud and os.path.exists(KEY_FILE):
                os.remove(KEY_FILE)
            st.rerun()
    else:
        api_key = st.text_input("API Key", type="password", placeholder="sk-...", value=saved, label_visibility="collapsed")
        if api_key:
            st.session_state.key_ready = True
            st.session_state.api_key_val = api_key
            if not is_cloud:
                save_key(api_key)
            st.rerun()
        else:
            st.info("在 [platform.deepseek.com](https://platform.deepseek.com) 免费获取")

    has_key = st.session_state.key_ready

    st.divider()
    st.caption("📁 上传截图")
    uploaded = st.file_uploader("上传", type=["png", "jpg", "jpeg", "txt", "csv"], label_visibility="collapsed")

# ── 无 Key ───────────────────────────────
if not has_key:
    st.markdown("""
    <div style="text-align:center;padding:80px 0;">
        <div style="font-size:4rem;">🐧</div>
        <h1>Linux 课助教</h1>
        <p>为 Linux 课程老师打造的 AI 教学助手</p>
        <p>👈 请在左侧填入API Key</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── 智能路由 ──────────────────────────────
def smart_route(text: str) -> str:
    m = st.session_state.get("model", "deepseek-v4-flash")
    t = text.lower()
    has_code = "```" in text or "#!/bin" in text or any(c in t for c in ["echo ", "grep ", "chmod ", "tar ", "find ", "#!/usr"])
    has_data = text.count("-") >= 3 and any(k in t for k in ["分", "成绩", "作业"])
    is_grade = any(k in t for k in ["批改", "评分", "改一下", "批一下"])
    is_analysis = any(k in t for k in ["分析", "统计", "完成情况", "分布"])
    is_diag = any(k in t for k in ["诊断", "学情", "薄弱", "掌握"])
    is_gen = any(k in t for k in ["出题", "题目", "练习题", "生成"])

    if has_code and (is_grade or len(text) > 300):
        return grade(api_key, text, model=m)
    elif has_data or is_analysis:
        return analyze_completion(api_key, text, model=m)
    elif is_diag:
        return diagnose_student(api_key, text, model=m)
    elif is_gen:
        return generate_questions(api_key, text, model=m)
    else:
        return ask(api_key, text, system="你是 Linux 课助教。用中文回复，简洁专业。", model=m)

# ── 消息区 ───────────────────────────────
for msg in st.session_state.msgs:
    avatar = "🐧" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# ── 输入 ─────────────────────────────────
if prompt := st.chat_input("给 Linux 课助教发消息..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    with st.chat_message("assistant", avatar="🐧"):
        with st.spinner(""):
            response = smart_route(prompt)
            st.markdown(response)
            st.session_state.msgs.append({"role": "assistant", "content": response})

# ── 文件上传处理 ─────────────────────────
if uploaded:
    m = st.session_state.get("model", "deepseek-v4-flash")
    fname = uploaded.name
    ftype = fname.split(".")[-1].lower()

    if ftype in ("png", "jpg", "jpeg"):
        st.session_state.msgs.append({"role": "user", "content": f"📸 {fname}"})
        with st.spinner("识别截图..."):
            code = ocr_image(api_key, uploaded.getvalue(), f"image/{ftype}", model=m)
        with st.spinner("批改中..."):
            response = grade(api_key, code, model=m)
        st.session_state.msgs.append({"role": "assistant", "content": response})
    else:
        text = uploaded.getvalue().decode("utf-8")
        st.session_state.msgs.append({"role": "user", "content": f"📎 {fname}\n{text}"})
        with st.spinner(""):
            st.session_state.msgs.append({"role": "assistant", "content": smart_route(text)})
    st.rerun()
