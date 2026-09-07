import streamlit as st
from workflow import run_workflow

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS & ANIMATIONS
# ============================================================
st.markdown("""
<style>
    /* Hide Streamlit default UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Dark Background */
    .stApp {
        background-color: #060c12;
        position: relative;
        overflow: hidden;
    }

    /* CSS Animated Rain Background Overlay */
    .stApp::before {
        content: "";
        position: fixed;
        top: -100px;
        left: 0;
        width: 100%;
        height: 120%;
        z-index: 0;
        pointer-events: none;
        background-image: 
            radial-gradient(2px 80px at 20px 30px, rgba(74, 158, 255, 0.4), transparent),
            radial-gradient(1.5px 60px at 100px 80px, rgba(0, 212, 255, 0.3), transparent),
            radial-gradient(2px 90px at 200px 10px, rgba(74, 158, 255, 0.35), transparent),
            radial-gradient(1.5px 70px at 300px 120px, rgba(0, 212, 255, 0.4), transparent),
            radial-gradient(2px 80px at 450px 40px, rgba(74, 158, 255, 0.3), transparent),
            radial-gradient(1.5px 65px at 600px 90px, rgba(0, 212, 255, 0.35), transparent),
            radial-gradient(2px 85px at 750px 15px, rgba(74, 158, 255, 0.4), transparent),
            radial-gradient(1.5px 75px at 900px 100px, rgba(0, 212, 255, 0.3), transparent);
        background-size: 900px 600px;
        animation: rain 1.2s linear infinite;
    }

    @keyframes rain {
        0% { transform: translateY(-100px); }
        100% { transform: translateY(500px); }
    }

    /* Ensure content stays above rain */
    .main .block-container, section[data-testid="stSidebar"] {
        position: relative;
        z-index: 1;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(8, 16, 26, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(74, 158, 255, 0.15) !important;
    }
    
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #4a9eff !important;
    }

    /* Sidebar Logo Header */
    .sidebar-logo {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.15);
        margin-bottom: 20px;
    }
    .sidebar-logo .logo-text {
        font-size: 2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    .sidebar-logo .logo-sub {
        color: #7a9ab5;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 4px 0 0 0;
    }

    /* Sidebar Info Boxes */
    .sidebar-section-title {
        color: #4a9eff;
        font-size: 0.9rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .sidebar-info-box {
        background: rgba(18, 38, 62, 0.4);
        border: 1px solid rgba(74, 158, 255, 0.15);
        padding: 12px 14px;
        border-radius: 10px;
        margin: 8px 0;
    }
    .sidebar-info-box p {
        color: #c8d6e5 !important;
        margin: 0;
        font-size: 0.85rem;
        line-height: 1.5;
    }

    .sidebar-feature {
        color: #c8d6e5 !important;
        padding: 4px 0;
        font-size: 0.85rem;
        margin: 0;
    }

    .sidebar-divider {
        border: none;
        border-top: 1px solid rgba(74, 158, 255, 0.1);
        margin: 20px 0;
    }

    .sidebar-footer {
        text-align: center;
        color: #53708a !important;
        font-size: 0.7rem;
        margin: 4px 0;
    }

    /* Modern AI Agent Header */
    .chat-header {
        text-align: center;
        padding: 20px 0 10px 0;
        margin-bottom: 25px;
    }
    .chat-header .badge {
        display: inline-block;
        background: rgba(74, 158, 255, 0.1);
        color: #00d4ff;
        border: 1px solid rgba(0, 212, 255, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .chat-header .chat-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .chat-header .chat-subtitle {
        color: #8da4b8;
        font-size: 0.95rem;
        margin-top: 6px;
    }

    /* Welcome Card Glassmorphism */
    .welcome-box {
        text-align: center;
        padding: 2.5rem 2rem;
        background: rgba(14, 28, 44, 0.5);
        backdrop-filter: blur(8px);
        border-radius: 16px;
        border: 1px solid rgba(74, 158, 255, 0.15);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        margin: 20px auto 40px auto;
        max-width: 580px;
    }
    .welcome-box h2 {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .welcome-box p {
        color: #9ab5cc;
        font-size: 0.9rem;
    }
    .welcome-box .examples {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 18px;
    }
    .example-tag {
        background: rgba(74, 158, 255, 0.08);
        border: 1px solid rgba(74, 158, 255, 0.2);
        color: #b0c4de;
        padding: 8px 14px;
        border-radius: 8px;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <p class="logo-text">DANI AI</p>
        <p class="logo-sub">Weather Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-section-title">⚡ Agent Overview</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info-box">
        <p>Dani converts natural-language requests into accurate forecasts using autonomous weather workflows.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-section-title">✨ Capabilities</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">📍 Global location intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">🌧️ Real-time precipitation tracking</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">📅 1-7 day probabilistic forecasts</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-feature">🧠 Context-aware parsing</p>', unsafe_allow_html=True)
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-section-title">👨‍💻 Security Lead</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info-box">
        <p>Architected by <strong style="color:#4a9eff;">Daniyal Riaz</strong><br>
        <span style="color:#7a9ab5; font-size:0.75rem;">AI Security & Vulnerability Researcher</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-footer">© 2026 Dani Weather Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-footer">End-to-End Encrypted & Secure 🔒</p>', unsafe_allow_html=True)

# ============================================================
# MAIN CHAT INTERFACE
# ============================================================
st.markdown("""
<div class="chat-header">
    <div class="badge">● AI Agent Active</div>
    <div class="chat-title">Weather Intelligence Console</div>
    <div class="chat-subtitle">Ask anything about atmospheric conditions globally</div>
</div>
""", unsafe_allow_html=True)

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome card display
if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
        <h2>System Ready</h2>
        <p>Ask a question to query current weather status or future forecasts.</p>
        <div class="examples">
            <div class="example-tag">💡 "What is the precipitation outlook for Karachi today?"</div>
            <div class="example-tag">💡 "Will it rain in Lahore tomorrow afternoon?"</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Render active conversation
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input Box
user_query = st.chat_input("Enter weather query or location...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing atmospheric data..."):
            try:
                result = run_workflow(user_query)
                answer = result.get("answer", "No data returned.") if isinstance(result, dict) else str(result)
            except Exception as e:
                answer = "⚠️ System encountered an issue retrieving forecast data."
                st.error(f"Execution Error: {e}")
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
