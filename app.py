import streamlit as st
from workflow import run_workflow

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }
    
    /* Main container */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 1rem 2rem 8rem 2rem;
    }
    
    /* Logo */
    .logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        padding: 15px 20px;
        background: rgba(10, 25, 40, 0.7);
        border-radius: 15px;
        border: 1px solid rgba(74, 158, 255, 0.2);
        margin-bottom: 25px;
    }
    .logo-container .title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .logo-container .subtitle {
        color: #7a9ab5;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Section headers */
    .section-title {
        color: #4a9eff;
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    
    /* Info boxes */
    .info-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 15px 20px;
        border-radius: 10px;
        border-left: 3px solid #4a9eff;
        margin: 8px 0;
    }
    .info-box p {
        color: #e8f0fe;
        margin: 0;
        font-size: 1rem;
    }
    
    .highlight-box {
        background: rgba(20, 50, 80, 0.25);
        padding: 15px 20px;
        border-radius: 10px;
        border: 1px solid rgba(74, 158, 255, 0.15);
        margin: 8px 0;
    }
    .highlight-box p {
        color: #c8d6e5;
        line-height: 1.8;
        margin: 6px 0;
    }
    
    .creator-box {
        background: rgba(20, 50, 80, 0.35);
        border-radius: 10px;
        padding: 15px;
        margin: 12px 0;
        border: 1px solid rgba(74, 158, 255, 0.15);
        text-align: center;
    }
    .creator-box .name {
        color: #4a9eff;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 5px 0;
    }
    .creator-box .title {
        color: #00d4ff;
        font-size: 0.85rem;
        margin: 5px 0;
    }
    
    .divider {
        border: none;
        border-top: 1px solid rgba(74, 158, 255, 0.15);
        margin: 25px 0;
    }
    
    .footer-text {
        text-align: center;
        color: #4a6a7a;
        font-size: 0.75rem;
        margin: 10px 0;
    }
    
    /* Feature grid */
    .feature-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px 20px;
        padding: 5px 0;
    }
    .feature-item {
        color: #c8d6e5;
        padding: 4px 0;
        font-size: 0.95rem;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 0.5rem 0 !important;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] {
        padding: 12px 18px;
        border-radius: 18px;
        color: #e8f0fe;
        max-width: 75%;
    }
    
    /* User messages - right aligned */
    .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
        background: rgba(30, 70, 110, 0.7);
        border: 1px solid rgba(74, 158, 255, 0.25);
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        margin-right: 0;
    }
    
    /* Assistant messages - left aligned */
    .stChatMessage:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stMarkdownContainer"] {
        background: rgba(20, 50, 80, 0.45);
        border: 1px solid rgba(0, 212, 255, 0.15);
        border-radius: 18px 18px 18px 4px;
        margin-left: 0;
        margin-right: auto;
    }
    
    /* Chat input */
    .stChatInput {
        background: rgba(10, 25, 40, 0.95) !important;
        border: 2px solid rgba(74, 158, 255, 0.35) !important;
        border-radius: 30px !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    .stChatInput textarea {
        color: #ffffff !important;
        background: transparent !important;
    }
    .stChatInput textarea::placeholder {
        color: #8899aa !important;
    }
    .stChatInput button {
        background: linear-gradient(135deg, #4a9eff, #00d4ff) !important;
        border: none !important;
        border-radius: 20px !important;
        color: white !important;
    }
    
    /* Welcome box */
    .welcome-box {
        text-align: center;
        padding: 2.5rem 2rem;
        background: rgba(20, 50, 80, 0.25);
        border-radius: 20px;
        border: 1px solid rgba(74, 158, 255, 0.12);
        margin: 20px auto;
        max-width: 550px;
    }
    .welcome-box h2 {
        color: #4a9eff;
        font-size: 1.6rem;
        margin-bottom: 0.5rem;
    }
    .welcome-box p {
        color: #9ab5cc;
        font-size: 1rem;
    }
    .welcome-box .examples {
        color: #b0c4de;
        font-size: 0.9rem;
        margin-top: 10px;
        line-height: 1.8;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# MAIN CONTENT
# ============================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ============================================================
# HEADER WITH LOGO
# ============================================================
st.markdown("""
<div class="logo-container">
    <div>
        <p class="title">🤖 Dani</p>
        <p class="subtitle">Your Intelligent Weather AI Agent</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# ABOUT DANI
# ============================================================
st.markdown('<p class="section-title">🌤️ About Dani</p>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
    <p>Dani converts natural-language weather requests into accurate forecasts using advanced AI and real-time weather data.</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KEY FEATURES
# ============================================================
st.markdown('<p class="section-title">✨ Key Features</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("📍 **Location-based forecasts**")
    st.markdown("🌡️ **Temperature & precipitation**")
    st.markdown("📅 **1-7 day predictions**")

with col2:
    st.markdown("🤖 **Natural language understanding**")
    st.markdown("🔒 **Secure & reliable**")
    st.markdown("⚡ **Real-time weather data**")

# ============================================================
# TRY ASKING
# ============================================================
st.markdown("""
<div class="info-box" style="border-left-color:#00d4ff; margin-top:15px;">
    <p>💡 <strong>Try asking:</strong><br>
    <span style="color:#b0c4de;">"What's the weather in Karachi today?"</span><br>
    <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# ABOUT ME
# ============================================================
st.markdown('<p class="section-title">👨‍💻 About Me</p>', unsafe_allow_html=True)

st.markdown("""
<div class="highlight-box">
    <p>Hi, I'm <strong style="color:#4a9eff;">Daniyal Riaz</strong>, an <strong style="color:#00d4ff;">AI Offensive Security Enthusiast</strong>, <strong style="color:#00d4ff;">Ethical Hacker</strong>, and <strong style="color:#00d4ff;">Bug Bounty Hunter</strong>.</p>
    <p>I'm passionate about finding vulnerabilities and helping organizations secure their digital assets.</p>
    <p>🎯 <strong style="color:#4a9eff;">My Vision:</strong> Creating AI applications with security at the forefront.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="creator-box">
    <p class="name">👨‍💻 Created with ❤️ by Daniyal Riaz</p>
    <p class="title">AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<p class="footer-text">© 2026 Dani Weather Agent • Built with security in mind 🔒</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ============================================================
# CHAT INTERFACE
# ============================================================
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome message
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
        <h2>👋 Hello! I'm Dani</h2>
        <p>Ask me about the weather anywhere in the world.</p>
        <div class="examples">
            💡 Try: "What's the weather in Karachi today?"<br>
            💡 Try: "Will it rain in Lahore tomorrow?"
        </div>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_query = st.chat_input("Ask Dani about the weather...")

if user_query:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
    
    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("🌤️ Dani is checking the forecast..."):
            result = run_workflow(user_query)
            if isinstance(result, dict):
                answer = result.get("answer", "Sorry, I couldn't generate a response.")
            else:
                answer = str(result)
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
