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
    
    /* Left column - About section */
    .left-column {
        background: rgba(10, 25, 40, 0.92);
        border-right: 1px solid rgba(74, 158, 255, 0.15);
        padding: 2rem 1.5rem;
        min-height: 100vh;
        height: 100%;
        border-radius: 0;
    }
    
    .left-column .logo-text {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0 0 5px 0;
    }
    
    .left-column .subtitle-text {
        color: #7a9ab5;
        font-size: 0.9rem;
        margin: 0 0 20px 0;
    }
    
    .left-column .section-title {
        color: #4a9eff;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 8px;
    }
    
    .left-column .info-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 12px 15px;
        border-radius: 10px;
        border-left: 3px solid #4a9eff;
        margin: 5px 0 10px 0;
    }
    .left-column .info-box p {
        color: #e8f0fe;
        margin: 0;
        font-size: 0.9rem;
    }
    
    .left-column .about-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 12px 15px;
        border-radius: 10px;
        border: 1px solid rgba(74, 158, 255, 0.12);
        margin: 5px 0 10px 0;
    }
    .left-column .about-box p {
        color: #c8d6e5;
        line-height: 1.7;
        margin: 5px 0;
        font-size: 0.9rem;
    }
    
    .left-column .creator-box {
        background: rgba(20, 50, 80, 0.35);
        border-radius: 10px;
        padding: 12px;
        margin: 10px 0;
        border: 1px solid rgba(74, 158, 255, 0.12);
        text-align: center;
    }
    .left-column .creator-box .name {
        color: #4a9eff;
        font-weight: 700;
        font-size: 0.95rem;
        margin: 3px 0;
    }
    .left-column .creator-box .title {
        color: #00d4ff;
        font-size: 0.75rem;
        margin: 3px 0;
    }
    
    .left-column .divider {
        border: none;
        border-top: 1px solid rgba(74, 158, 255, 0.1);
        margin: 18px 0;
    }
    
    .left-column .footer-text {
        text-align: center;
        color: #4a6a7a;
        font-size: 0.65rem;
        margin: 8px 0;
    }
    
    .left-column .feature-item {
        color: #c8d6e5;
        padding: 3px 0;
        font-size: 0.9rem;
    }
    
    /* Right column - Chat area */
    .right-column {
        padding: 1.5rem 2rem 7rem 2rem;
        min-height: 100vh;
    }
    
    .right-column .chat-header {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.1);
        margin-bottom: 20px;
    }
    .right-column .chat-header .chat-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .right-column .chat-header .chat-subtitle {
        color: #7a9ab5;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 0.4rem 0 !important;
    }
    
    .stChatMessage [data-testid="stMarkdownContainer"] {
        padding: 10px 16px;
        border-radius: 18px;
        color: #e8f0fe;
        max-width: 80%;
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
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
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
    
    /* Welcome box in chat */
    .welcome-box {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: rgba(20, 50, 80, 0.2);
        border-radius: 20px;
        border: 1px solid rgba(74, 158, 255, 0.1);
        margin: 30px auto;
        max-width: 500px;
    }
    .welcome-box h2 {
        color: #4a9eff;
        font-size: 1.5rem;
        margin-bottom: 0.3rem;
    }
    .welcome-box p {
        color: #9ab5cc;
        font-size: 0.95rem;
    }
    .welcome-box .examples {
        color: #b0c4de;
        font-size: 0.85rem;
        margin-top: 8px;
        line-height: 1.8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .left-column {
            min-height: auto;
            padding: 1rem;
        }
        .right-column {
            padding: 1rem 1rem 6rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TWO COLUMN LAYOUT
# ============================================================
col_left, col_right = st.columns([3, 7])

# ============================================================
# LEFT COLUMN - About Section
# ============================================================
with col_left:
    st.markdown('<div class="left-column">', unsafe_allow_html=True)
    
    # Logo
    st.markdown('<p class="logo-text">🤖 Dani</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Weather AI Agent</p>', unsafe_allow_html=True)
    
    # About Dani
    st.markdown('<p class="section-title">🌤️ About Dani</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        <p>Dani converts natural-language weather requests into accurate forecasts using advanced AI and real-time weather data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown('<p class="section-title">✨ Key Features</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">📍 Location-based forecasts</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">🌡️ Temperature & precipitation</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">📅 1-7 day predictions</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">🤖 Natural language understanding</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">🔒 Secure & reliable</p>', unsafe_allow_html=True)
    st.markdown('<p class="feature-item">⚡ Real-time weather data</p>', unsafe_allow_html=True)
    
    # Try Asking
    st.markdown("""
    <div class="info-box" style="border-left-color:#00d4ff; margin-top:12px;">
        <p>💡 <strong>Try asking:</strong><br>
        <span style="color:#b0c4de;">"What's the weather in Karachi?"</span><br>
        <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
    # About Me
    st.markdown('<p class="section-title">👨‍💻 About Me</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="about-box">
        <p>Hi, I'm <strong style="color:#4a9eff;">Daniyal Riaz</strong>.</p>
        <p>I'm an <strong style="color:#00d4ff;">AI Offensive Security Enthusiast</strong>, <strong style="color:#00d4ff;">Ethical Hacker</strong>, and <strong style="color:#00d4ff;">Bug Bounty Hunter</strong>.</p>
        <p>Passionate about finding vulnerabilities and helping organizations secure their digital assets.</p>
        <p>🎯 <strong style="color:#4a9eff;">My Vision:</strong> Creating AI applications with security at the forefront.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Creator
    st.markdown("""
    <div class="creator-box">
        <p class="name">👨‍💻 Created with ❤️ by Daniyal Riaz</p>
        <p class="title">AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<p class="footer-text">© 2026 Dani Weather Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="footer-text">Built with security in mind 🔒</p>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RIGHT COLUMN - Chat Area
# ============================================================
with col_right:
    st.markdown('<div class="right-column">', unsafe_allow_html=True)
    
    # Chat Header
    st.markdown("""
    <div class="chat-header">
        <p class="chat-title">💬 Chat with Dani</p>
        <p class="chat-subtitle">Ask me about the weather anywhere in the world</p>
    </div>
    """, unsafe_allow_html=True)
    
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
                try:
                    result = run_workflow(user_query)
                    if isinstance(result, dict):
                        answer = result.get("answer", "Sorry, I couldn't generate a response.")
                    else:
                        answer = str(result)
                except Exception as e:
                    answer = "⚠️ I couldn't retrieve the weather forecast. Please try again."
                    st.error(f"Error: {e}")
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
