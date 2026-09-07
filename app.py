import streamlit as st
from workflow import run_workflow

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit default chrome we don't want, WITHOUT hiding the
       sidebar collapse/expand arrow (that arrow lives inside <header>,
       so hiding <header> itself would strand users with no sidebar). */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}

    /* Keep the header element itself present (so its children, like the
       sidebar toggle, still render) but make it visually transparent and
       hide just the toolbar/menu bits inside it. */
    header[data-testid="stHeader"] {
        background: transparent !important;
        box-shadow: none !important;
    }
    [data-testid="stToolbar"] {
        visibility: hidden !important;
    }

    /* Force the sidebar open/close control to ALWAYS stay visible and
       clickable, regardless of any other rule above or any collapsed
       state Streamlit puts the sidebar into. This is the actual fix for
       the "sidebar disappears and never comes back" issue. */
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {
        visibility: visible !important;
        display: flex !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }
    [data-testid="collapsedControl"] svg,
    [data-testid="stSidebarCollapseButton"] svg {
        fill: #4a9eff !important;
    }

    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: rgba(10, 25, 40, 0.98) !important;
        border-right: 1px solid rgba(74, 158, 255, 0.15) !important;
        padding: 2rem 1.5rem !important;
        width: 320px !important;
        min-width: 320px !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #4a9eff !important;
    }
    
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li {
        color: #c8d6e5 !important;
    }
    
    /* Sidebar logo */
    .sidebar-logo {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.1);
        margin-bottom: 20px;
    }
    .sidebar-logo .logo-text {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .sidebar-logo .logo-sub {
        color: #7a9ab5;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* Sidebar sections */
    .sidebar-section-title {
        color: #4a9eff;
        font-size: 1rem;
        font-weight: 600;
        margin-top: 18px;
        margin-bottom: 6px;
    }
    
    .sidebar-info-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 10px 14px;
        border-radius: 8px;
        border-left: 3px solid #4a9eff;
        margin: 4px 0 8px 0;
    }
    .sidebar-info-box p {
        color: #e8f0fe;
        margin: 0;
        font-size: 0.85rem;
    }
    
    .sidebar-about-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 10px 14px;
        border-radius: 8px;
        border: 1px solid rgba(74, 158, 255, 0.1);
        margin: 4px 0 8px 0;
    }
    .sidebar-about-box p {
        color: #c8d6e5;
        line-height: 1.6;
        margin: 4px 0;
        font-size: 0.85rem;
    }
    
    .sidebar-creator {
        background: rgba(20, 50, 80, 0.35);
        border-radius: 8px;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid rgba(74, 158, 255, 0.1);
        text-align: center;
    }
    .sidebar-creator .name {
        color: #4a9eff;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 2px 0;
    }
    .sidebar-creator .title {
        color: #00d4ff;
        font-size: 0.7rem;
        margin: 2px 0;
    }
    
    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(74, 158, 255, 0.08);
        margin: 15px 0;
    }
    
    .sidebar-footer {
        text-align: center;
        color: #4a6a7a;
        font-size: 0.6rem;
        margin: 8px 0;
    }
    
    .sidebar-feature {
        color: #c8d6e5;
        padding: 2px 0;
        font-size: 0.85rem;
        margin: 0;
    }
    
    /* Chat area */
    .chat-container {
        padding: 1rem 2rem 7rem 2rem;
        max-width: 900px;
        margin: 0 auto;
    }
    
    .chat-header {
        text-align: center;
        padding: 15px 0 20px 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.08);
        margin-bottom: 20px;
    }
    .chat-header .chat-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .chat-header .chat-subtitle {
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
    
    .stChatMessage:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stMarkdownContainer"] {
        background: rgba(30, 70, 110, 0.7);
        border: 1px solid rgba(74, 158, 255, 0.25);
        border-radius: 18px 18px 4px 18px;
        margin-left: auto;
        margin-right: 0;
    }
    
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
    
    /* Welcome box */
    .welcome-box {
        text-align: center;
        padding: 2.5rem 1.5rem;
        background: rgba(20, 50, 80, 0.2);
        border-radius: 20px;
        border: 1px solid rgba(74, 158, 255, 0.08);
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
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            padding: 1rem !important;
        }
        .chat-container {
            padding: 0.5rem 1rem 6rem 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR - All About Information
# ============================================================
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="sidebar-logo">
        <p class="logo-text">🤖 Dani</p>
        <p class="logo-sub">Weather AI Agent</p>
    </div>
    """, unsafe_allow_html=True)
    
    # About Dani
    st.markdown('<p class="sidebar-section-title">🌤️ About Dani</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info-box">
        <p>Dani converts natural-language weather requests into accurate forecasts using advanced AI and real-time weather data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.markdown('<p class="sidebar-section-title">✨ Key Features</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">📍 Location-based forecasts</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">🌡️ Temperature & precipitation</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">📅 1-7 day predictions</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">🤖 Natural language understanding</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">🔒 Secure & reliable</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">⚡ Real-time weather data</p>', unsafe_allow_html=True)
    
    # Try Asking
    st.markdown("""
    <div class="sidebar-info-box" style="border-left-color:#00d4ff; margin-top:10px;">
        <p>💡 <strong>Try asking:</strong><br>
        <span style="color:#b0c4de;">"What's the weather in Karachi?"</span><br>
        <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    # About Me
    st.markdown('<p class="sidebar-section-title">👨‍💻 About Me</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-about-box">
        <p>Hi, I'm <strong style="color:#4a9eff;">Daniyal Riaz</strong>.</p>
        <p>I'm an <strong style="color:#00d4ff;">AI Offensive Security Enthusiast</strong>, <strong style="color:#00d4ff;">Ethical Hacker</strong>, and <strong style="color:#00d4ff;">Bug Bounty Hunter</strong>.</p>
        <p>Passionate about finding vulnerabilities and helping organizations secure their digital assets.</p>
        <p>🎯 <strong style="color:#4a9eff;">My Vision:</strong> Creating AI applications with security at the forefront.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Creator
    st.markdown("""
    <div class="sidebar-creator">
        <p class="name">👨‍💻 Created with ❤️ by Daniyal Riaz</p>
        <p class="title">AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Footer
    st.markdown('<p class="sidebar-footer">© 2026 Dani Weather Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-footer">Built with security in mind 🔒</p>', unsafe_allow_html=True)

# ============================================================
# MAIN CHAT AREA
# ============================================================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

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
