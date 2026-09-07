import streamlit as st
from workflow import run_workflow

# Page configuration
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
)

# Custom CSS for AI Chatbot Style
st.markdown("""
<style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Main background with gradient */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }
    
    /* Make sidebar visible and styled */
    section[data-testid="stSidebar"] {
        background: rgba(10, 25, 40, 0.98) !important;
        border-right: 1px solid rgba(26, 58, 90, 0.5) !important;
        min-width: 300px !important;
        width: 300px !important;
    }
    
    section[data-testid="stSidebar"] .css-1d391kg {
        padding: 2rem 1rem !important;
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
    
    /* Sidebar boxes */
    .sidebar-box {
        background: rgba(20, 50, 80, 0.4) !important;
        padding: 12px 15px !important;
        border-radius: 10px !important;
        margin: 8px 0 !important;
        border-left: 3px solid #4a9eff !important;
    }
    .sidebar-box p {
        color: #e8f0fe !important;
        margin: 0 !important;
        font-size: 0.9rem !important;
    }
    
    .sidebar-title {
        color: #4a9eff !important;
        font-weight: 600 !important;
        margin-top: 15px !important;
        margin-bottom: 8px !important;
        font-size: 1.1rem !important;
    }
    
    .about-me-sidebar {
        background: rgba(20, 50, 80, 0.4) !important;
        padding: 12px 15px !important;
        border-radius: 10px !important;
        border: 1px solid rgba(42, 90, 138, 0.3) !important;
        margin: 8px 0 !important;
    }
    .about-me-sidebar p {
        color: #c8d6e5 !important;
        font-size: 0.85rem !important;
        line-height: 1.6 !important;
        margin: 0 0 6px 0 !important;
    }
    .about-me-sidebar .highlight {
        color: #4a9eff !important;
        font-weight: 600 !important;
    }
    .about-me-sidebar .highlight-cyan {
        color: #00d4ff !important;
        font-weight: 500 !important;
    }
    
    .creator-badge {
        background: rgba(20, 50, 80, 0.5) !important;
        border-radius: 10px !important;
        padding: 12px !important;
        margin-top: 12px !important;
        border: 1px solid rgba(42, 90, 138, 0.3) !important;
        text-align: center !important;
    }
    .creator-badge .name {
        color: #4a9eff !important;
        font-weight: 700 !important;
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
        text-align: center !important;
        margin-top: 15px !important;
        padding-top: 10px !important;
        border-top: 1px solid rgba(26, 58, 90, 0.3) !important;
    }
    .copyright p {
        color: #4a6a7a !important;
        font-size: 0.65rem !important;
        margin: 2px 0 !important;
    }
    
    /* Chat messages */
    .stChatMessage {
        padding: 0.5rem 0 !important;
    }
    
    /* User messages */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background: transparent !important;
        border-left: none !important;
    }
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
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background: transparent !important;
        border-left: none !important;
    }
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
        width: 60%;
        max-width: 700px;
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
        justify-content: center;
        gap: 15px;
        margin-bottom: 10px;
    }
    .logo-container svg {
        width: 60px;
        height: 60px;
        filter: drop-shadow(0 0 10px rgba(74, 158, 255, 0.3));
        animation: pulse 3s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Chat header */
    .chat-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.2);
        margin-bottom: 1rem;
    }
    .chat-header h1 {
        font-size: 2.5rem;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        font-weight: 700;
    }
    .chat-header p {
        color: #7a9ab5;
        font-size: 1rem;
        margin: 5px 0 0 0;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar - Using st.markdown with proper formatting
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
    <div class="sidebar-box" style="border-left-color:#00d4ff !important;">
        <p>💡 <strong>Try asking:</strong><br>
        <span style="color:#b0c4de;">"What's the weather in Karachi?"</span><br>
        <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("## 👨‍💻 About Me")
    st.markdown("""
    <div class="about-me-sidebar">
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

# Main chat area with Classic Robot Logo
st.markdown("""
<div class="chat-header">
    <div class="logo-container">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
            <!-- Background circle -->
            <circle cx="50" cy="50" r="48" fill="#0a1922" stroke="#4a9eff" stroke-width="2"/>
            <!-- Robot head -->
            <rect x="25" y="20" width="50" height="45" rx="8" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1.5"/>
            <!-- Eyes -->
            <circle cx="38" cy="38" r="5" fill="#00d4ff"/>
            <circle cx="62" cy="38" r="5" fill="#00d4ff"/>
            <circle cx="38" cy="38" r="2" fill="#ffffff"/>
            <circle cx="62" cy="38" r="2" fill="#ffffff"/>
            <!-- Mouth -->
            <rect x="35" y="48" width="30" height="4" rx="2" fill="#4a9eff"/>
            <!-- Antenna -->
            <line x1="50" y1="20" x2="50" y2="10" stroke="#4a9eff" stroke-width="2"/>
            <circle cx="50" cy="8" r="3" fill="#ff6b6b"/>
            <!-- Ears -->
            <rect x="20" y="30" width="5" height="15" rx="2" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1"/>
            <rect x="75" y="30" width="5" height="15" rx="2" fill="#1a3a5a" stroke="#4a9eff" stroke-width="1"/>
        </svg>
        <div>
            <h1>Dani</h1>
            <p>Your Intelligent Weather AI Agent</p>
        </div>
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
        
        with st.expander("🔍 View workflow details"):
            st.json({
                "stage": result["stage"],
                "intent": result.get("intent"),
                "retrieved_context": result.get("retrieved_context"),
                "weather_tool": result.get("weather_tool"),
                "security": result.get("security"),
            })

        st.session_state.messages.append(
            {"role": "assistant", "content": result["answer"]}
        )
    
    st.rerun()
