import streamlit as st
from workflow import run_workflow

# Page configuration
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }
    
    /* Left column styling */
    .left-column {
        background: rgba(10, 25, 40, 0.95);
        border-right: 2px solid rgba(74, 158, 255, 0.2);
        padding: 2rem 1.5rem;
        min-height: 100vh;
        height: 100%;
        border-radius: 0;
    }
    
    .left-column h2 {
        color: #4a9eff !important;
        font-size: 1.3rem !important;
        margin-top: 0 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .left-column h3 {
        color: #4a9eff !important;
        font-size: 1.1rem !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .left-column p {
        color: #c8d6e5 !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
    }
    
    .left-column li {
        color: #c8d6e5 !important;
        padding: 4px 0 !important;
        list-style-type: none !important;
    }
    
    /* Sidebar boxes */
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
        font-size: 0.9rem !important;
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
        font-size: 0.85rem !important;
        line-height: 1.6 !important;
        margin: 0 0 6px 0 !important;
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
        font-size: 0.95rem !important;
    }
    
    .creator-badge .title {
        color: #00d4ff !important;
        font-size: 0.75rem !important;
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
        margin: 2px 0 !important;
    }
    
    .divider {
        border: none;
        border-top: 1px solid rgba(26, 58, 90, 0.3);
        margin: 1.5rem 0;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 0.5rem 0 !important;
    }
    
    /* User messages */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) .stMarkdown {
        background: rgba(30, 60, 90, 0.6);
        border-radius: 18px 18px 18px 4px;
        padding: 12px 18px;
        max-width: 75%;
        margin-left: auto;
        border: 1px solid rgba(74, 158, 255, 0.2);
        color: #e8f0fe;
    }
    
    /* Assistant messages */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) .stMarkdown {
        background: rgba(20, 50, 80, 0.3);
        border-radius: 18px 18px 4px 18px;
        padding: 12px 18px;
        max-width: 75%;
        margin-right: auto;
        border: 1px solid rgba(0, 212, 255, 0.15);
        color: #e8f0fe;
    }
    
    /* Chat input */
    .stChatInput {
        position: fixed;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 50%;
        max-width: 600px;
        z-index: 999;
        padding: 0.5rem 1rem;
        background: rgba(10, 25, 40, 0.95);
        border-radius: 30px;
        border: 2px solid rgba(74, 158, 255, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
    }
    .stChatInput > div {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }
    .stChatInput input {
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 12px 16px !important;
        background: transparent !important;
        border: none !important;
        outline: none !important;
        caret-color: #4a9eff !important;
    }
    .stChatInput input::placeholder {
        color: #aabbcc !important;
        font-size: 0.95rem !important;
        opacity: 1 !important;
    }
    .stChatInput input:focus {
        color: #ffffff !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    .stChatInput button {
        background: linear-gradient(135deg, #4a9eff, #00d4ff) !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 8px 20px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    .stChatInput button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 4px 20px rgba(74, 158, 255, 0.4) !important;
    }
    
    /* Welcome message */
    .welcome-box {
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(20, 50, 80, 0.2);
        border-radius: 20px;
        border: 1px solid rgba(74, 158, 255, 0.1);
        margin: 2rem auto;
        max-width: 600px;
    }
    .welcome-box h2 {
        color: #4a9eff;
        font-size: 1.8rem;
        margin-bottom: 0.5rem;
    }
    .welcome-box p {
        color: #7a9ab5;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    .welcome-box .examples {
        color: #b0c4de;
        font-size: 0.95rem;
        margin-top: 1rem;
    }
    
    /* Logo container */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
        margin-bottom: 20px;
        padding: 15px 20px;
        background: rgba(10, 25, 40, 0.6);
        border-radius: 15px;
        border: 1px solid rgba(26, 58, 90, 0.3);
    }
    .logo-container svg {
        width: 55px;
        height: 55px;
        filter: drop-shadow(0 0 10px rgba(74, 158, 255, 0.3));
        animation: pulse 3s ease-in-out infinite;
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
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Right column - main content */
    .main-content {
        padding: 1rem 2rem 6rem 2rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TWO COLUMN LAYOUT - LEFT = SIDEBAR, RIGHT = CHAT
# ============================================================
col1, col2 = st.columns([3, 9])

# ============================================================
# LEFT COLUMN - All About Me Content (VISIBLE ALWAYS)
# ============================================================
with col1:
    st.markdown('<div class="left-column">', unsafe_allow_html=True)
    
    st.markdown("## 🌤️ About Dani")
    st.markdown("""
    <div class="sidebar-box">
        <p>Dani converts natural-language weather requests into accurate forecasts using advanced AI and real-time weather data.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Key Features")
    st.markdown("""
    <ul>
        <li>📍 Location-based forecasts</li>
        <li>🌡️ Temperature & precipitation</li>
        <li>📅 1-7 day predictions</li>
        <li>🤖 Natural language understanding</li>
        <li>🔒 Secure & reliable</li>
    </ul>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-box" style="border-left-color:#00d4ff;margin-top:12px;">
        <p>💡 <strong>Try asking:</strong><br>
        <span style="color:#b0c4de;">"What's the weather in Karachi?"</span><br>
        <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# RIGHT COLUMN - Chat Area
# ============================================================
with col2:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
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

    # Display welcome message if no messages
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
    user_query = st.chat_input("Ask Dani about the weather...", key="chat_input")

    if user_query:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("🌤️ Dani is checking the forecast..."):
                result = run_workflow(user_query)
            st.markdown(result["answer"])
            st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
        
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
