import streamlit as st
from workflow import run_workflow

# Page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" # This ensures sidebar is open on desktop
)

# --- Custom CSS (Minimal & Safe) ---
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }
    
    /* Style the sidebar container */
    section[data-testid="stSidebar"] {
        background-color: rgba(10, 25, 40, 0.98) !important;
        border-right: 2px solid rgba(74, 158, 255, 0.2) !important;
        padding: 2rem 1.5rem !important;
    }
    
    /* Sidebar text colors */
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #4a9eff !important;
    }
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] li {
        color: #c8d6e5 !important;
    }

    /* Custom boxes for sidebar */
    .sidebar-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 12px 15px;
        border-radius: 10px;
        margin: 8px 0;
        border-left: 3px solid #4a9eff;
    }
    .sidebar-box p {
        color: #e8f0fe !important;
        margin: 0;
    }
    
    .about-me-box {
        background: rgba(20, 50, 80, 0.3);
        padding: 12px 15px;
        border-radius: 10px;
        border: 1px solid rgba(42, 90, 138, 0.3);
        margin: 8px 0;
    }
    .about-me-box p {
        color: #c8d6e5 !important;
        line-height: 1.6 !important;
    }
    .highlight {
        color: #4a9eff !important;
        font-weight: 600;
    }
    .highlight-cyan {
        color: #00d4ff !important;
        font-weight: 500;
    }
    
    .creator-badge {
        background: rgba(20, 50, 80, 0.4);
        border-radius: 10px;
        padding: 12px;
        margin-top: 12px;
        border: 1px solid rgba(42, 90, 138, 0.3);
        text-align: center;
    }
    .creator-badge .name {
        color: #4a9eff !important;
        font-weight: 700;
    }
    .creator-badge .title {
        color: #00d4ff !important;
        font-size: 0.75rem;
    }
    .creator-badge .heart {
        color: #ff6b6b !important;
    }
    
    .copyright {
        text-align: center;
        margin-top: 15px;
        padding-top: 10px;
        border-top: 1px solid rgba(26, 58, 90, 0.3);
    }
    .copyright p {
        color: #4a6a7a !important;
        font-size: 0.65rem !important;
    }

    /* Chat message styling */
    .stChatMessage [data-testid="stMarkdownContainer"] {
        background: rgba(30, 60, 90, 0.4);
        border-radius: 18px;
        padding: 12px 18px;
        color: #e8f0fe;
        border: 1px solid rgba(74, 158, 255, 0.15);
    }
    /* User messages - align right */
    .stChatMessage [data-testid="stMarkdownContainer"] {
        margin-left: auto;
        margin-right: 0;
        max-width: 75%;
    }
    /* Assistant messages - align left */
    .stChatMessage:nth-child(even) [data-testid="stMarkdownContainer"] {
        margin-left: 0;
        margin-right: auto;
        background: rgba(20, 50, 80, 0.3);
        border-color: rgba(0, 212, 255, 0.15);
    }
    
    /* Welcome box */
    .welcome-box {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(20, 50, 80, 0.2);
        border-radius: 20px;
        border: 1px solid rgba(74, 158, 255, 0.1);
        max-width: 600px;
        margin: 2rem auto;
    }
    .welcome-box h2 {
        color: #4a9eff;
    }
    .welcome-box p {
        color: #7a9ab5;
    }
    .welcome-box .examples {
        color: #b0c4de;
    }

    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 15px 20px;
        background: rgba(10, 25, 40, 0.6);
        border-radius: 15px;
        border: 1px solid rgba(26, 58, 90, 0.3);
        margin-bottom: 20px;
    }
    .logo-container svg {
        width: 55px;
        height: 55px;
        filter: drop-shadow(0 0 10px rgba(74, 158, 255, 0.3));
    }
    .logo-container .title {
        font-size: 2rem;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin: 0;
    }
    .logo-container .subtitle {
        color: #7a9ab5;
        font-size: 0.9rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTENT ---
with st.sidebar:
    st.markdown("## 🌤️ About Dani")
    st.markdown("""
    <div class="sidebar-box">
        <p>Dani converts natural-language weather requests into accurate forecasts using advanced AI and real-time weather data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features")
    st.markdown("""
    - 📍 Location-based forecasts
    - 🌡️ Temperature & precipitation
    - 📅 1-7 day predictions
    - 🤖 Natural language understanding
    - 🔒 Secure & reliable
    """)
    
    st.markdown("""
    <div class="sidebar-box" style="border-left-color:#00d4ff;margin-top:12px;">
        <p>💡 <strong>Try asking:</strong><br>
        <span style="color:#b0c4de;">"What's the weather in Karachi?"</span><br>
        <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("## 👨‍💻 About Me")
    st.markdown("""
    <div class="about-me-box">
        <p>Hi, I'm <span class="highlight">Daniyal Riaz</span>, an <span class="highlight-cyan">AI Offensive Security Enthusiast</span>, <span class="highlight-cyan">Ethical Hacker</span>, and <span class="highlight-cyan">Bug Bounty Hunter</span>.</p>
        <p>I'm passionate about finding vulnerabilities and helping organizations secure their digital assets.</p>
        <p>🎯 <span class="highlight">My Vision:</span> Creating AI applications with security at the forefront.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="creator-badge">
        <p class="name">👨‍💻 Created with <span class="heart">❤️</span> by Daniyal Riaz</p>
        <p class="title">AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="copyright">
        <p>© 2026 Dani Weather Agent</p>
        <p>Built with security in mind 🔒</p>
    </div>
    """, unsafe_allow_html=True)

# --- MAIN CHAT AREA ---

# Logo and Header
st.markdown("""
<div class="logo-container">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r="48" fill="#0a1922" stroke="#4a9eff" stroke-width="2"/>
        <rect x="25" y="20" width="50" height="45" rx="8" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1.5"/>
        <circle cx="38" cy="38" r="5" fill="#00d4ff"/>
        <circle cx="62" cy="38" r="5" fill="#00d4ff"/>
        <circle cx="38" cy="38" r="2" fill="#ffffff"/>
        <circle cx="62" cy="38" r="2" fill="#ffffff"/>
        <rect x="35" y="48" width="30" height="4" rx="2" fill="#4a9eff"/>
        <line x1="50" y1="20" x2="50" y2="10" stroke="#4a9eff" stroke-width="2"/>
        <circle cx="50" cy="8" r="3" fill="#ff6b6b"/>
        <rect x="20" y="30" width="5" height="15" rx="2" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1"/>
        <rect x="75" y="30" width="5" height="15" rx="2" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1"/>
    </svg>
    <div>
        <p class="title">Dani</p>
        <p class="subtitle">Your Intelligent Weather AI Agent</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display welcome message or chat history
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
else:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input
user_query = st.chat_input("Ask Dani about the weather...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("🌤️ Dani is checking the forecast..."):
            result = run_workflow(user_query)
        st.markdown(result["answer"])
        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
    
    st.rerun()
