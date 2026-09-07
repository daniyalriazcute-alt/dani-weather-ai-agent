import streamlit as st
from workflow import run_workflow

# Page configuration
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🌤️",
    layout="wide",
)

# Custom CSS for Navy Blue Theme
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
    }
    
    /* Main container */
    .main > div {
        background: transparent;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #e8f0fe !important;
        font-family: 'Segoe UI', sans-serif !important;
    }
    
    /* Paragraph text */
    p, li, label, .stMarkdown, .stText {
        color: #c8d6e5 !important;
    }
    
    /* Chat messages - User */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) {
        background: rgba(30, 60, 90, 0.6) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border-left: 3px solid #4a9eff !important;
    }
    
    /* Chat messages - Assistant */
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) {
        background: rgba(20, 50, 80, 0.4) !important;
        border-radius: 15px !important;
        padding: 15px !important;
        margin: 8px 0 !important;
        border-left: 3px solid #00d4ff !important;
    }
    
    /* Chat input */
    .stChatInput > div {
        background: rgba(20, 40, 60, 0.8) !important;
        border: 1px solid #2a4a6a !important;
        border-radius: 25px !important;
        padding: 5px 15px !important;
    }
    
    .stChatInput input {
        color: #e8f0fe !important;
        background: transparent !important;
    }
    
    .stChatInput input::placeholder {
        color: #8899aa !important;
    }
    
    /* Sidebar */
    .css-1d391kg, .css-1d391kg > div {
        background: rgba(10, 25, 40, 0.95) !important;
        border-right: 1px solid #1a3a5a !important;
    }
    
    .sidebar .sidebar-content {
        background: rgba(10, 25, 40, 0.95) !important;
    }
    
    /* Sidebar text */
    .css-1d391kg p, .css-1d391kg li, .css-1d391kg label {
        color: #b0c4de !important;
    }
    
    .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3 {
        color: #e8f0fe !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a4a7a, #2a6aaa) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2a5a8a, #3a7aba) !important;
        box-shadow: 0 4px 15px rgba(74, 158, 255, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background: rgba(20, 50, 80, 0.5) !important;
        color: #b0c4de !important;
        border-radius: 10px !important;
        border: 1px solid #1a3a5a !important;
    }
    
    .streamlit-expanderContent {
        background: rgba(10, 30, 50, 0.6) !important;
        border-radius: 0 0 10px 10px !important;
        border: 1px solid #1a3a5a !important;
        border-top: none !important;
    }
    
    /* Caption */
    .stCaption {
        color: #7a9ab5 !important;
        font-size: 0.9rem !important;
        padding: 8px 0 !important;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-color: #4a9eff transparent #4a9eff transparent !important;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0a1922;
    }
    ::-webkit-scrollbar-thumb {
        background: #2a5a8a;
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #3a7aba;
    }
    
    /* Expander JSON */
    .stJson {
        background: rgba(10, 25, 40, 0.8) !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    
    /* Code blocks */
    code {
        color: #00d4ff !important;
        background: rgba(0, 100, 200, 0.2) !important;
        padding: 2px 6px !important;
        border-radius: 4px !important;
    }
    
    /* Horizontal line */
    hr {
        border-color: #1a3a5a !important;
        margin: 20px 0 !important;
    }
    
    /* Creator badge */
    .creator-badge {
        background: rgba(20, 50, 80, 0.4);
        border-radius: 10px;
        padding: 12px 15px;
        margin-top: 15px;
        border: 1px solid #1a3a5a;
        text-align: center;
    }
    .creator-badge p {
        margin: 5px 0;
        color: #7a9ab5;
        font-size: 0.85rem;
    }
    .creator-badge .name {
        color: #4a9eff;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .creator-badge .heart {
        color: #ff6b6b;
    }
    .creator-badge .title {
        color: #00d4ff;
        font-size: 0.8rem;
        font-weight: 400;
    }
    
    /* Security badge */
    .security-badge {
        background: rgba(255, 50, 50, 0.1);
        border: 1px solid rgba(255, 50, 50, 0.3);
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 10px;
        text-align: center;
    }
    .security-badge p {
        color: #ff6b6b;
        font-size: 0.75rem;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)

# Logo and Title Section
with open("logo.svg", "r", encoding="utf-8") as f:
    logo_svg = f.read()

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:20px;margin-bottom:20px;padding:20px;background:rgba(10,25,40,0.6);border-radius:15px;border:1px solid #1a3a5a;">
      <img src="data:image/svg+xml;utf8,{logo_svg.replace('#','%23').replace('<','%3C').replace('>','%3E').replace('"','%22')}" width="90">
      <div>
        <h1 style="margin:0;font-size:2.8rem;background:linear-gradient(135deg,#4a9eff,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">Dani</h1>
        <p style="margin:0;color:#7a9ab5;font-size:1.1rem;">Intelligent Weather AI Agent</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("⚡ Multi-stage workflow • RAG • Weather tool • Groq • OWASP Top 10 for LLM Applications 2025")

# Sidebar - Updated with Professional About Me Section
with st.sidebar:
    st.markdown("""
    <div style="padding:10px 0;">
        <h3 style="color:#4a9eff;margin-bottom:15px;">🌤️ About Dani</h3>
        <p style="color:#b0c4de;line-height:1.6;">
            Dani is your intelligent weather assistant that converts natural-language weather 
            requests into accurate forecasts. Using advanced AI and real-time weather data, 
            Dani provides you with reliable weather information for any location worldwide.
        </p>
        <br>
        <h4 style="color:#4a9eff;">✨ Key Features</h4>
        <ul style="color:#b0c4de;list-style-type:none;padding-left:0;">
            <li style="padding:5px 0;">📍 <strong>Location-based forecasts</strong></li>
            <li style="padding:5px 0;">🌡️ <strong>Temperature & precipitation data</strong></li>
            <li style="padding:5px 0;">📅 <strong>1-7 day predictions</strong></li>
            <li style="padding:5px 0;">🤖 <strong>Natural language understanding</strong></li>
            <li style="padding:5px 0;">🔒 <strong>Secure & reliable</strong></li>
        </ul>
        <br>
        <div style="background:rgba(20,50,80,0.3);padding:15px;border-radius:10px;border-left:3px solid #4a9eff;">
            <p style="color:#7a9ab5;font-size:0.9rem;margin:0;">
                💡 Try asking:<br>
                <span style="color:#b0c4de;">"What's the weather in Karachi today?"</span><br>
                <span style="color:#b0c4de;">"Will it rain in Lahore tomorrow?"</span>
            </p>
        </div>
        
        <hr style="margin:20px 0;">
        
        <!-- About Me Section - AI Offensive Security -->
        <h3 style="color:#4a9eff;margin-bottom:10px;">👨‍💻 About Me</h3>
        <div style="background:rgba(20,50,80,0.3);padding:15px;border-radius:10px;border:1px solid #1a3a5a;">
            <p style="color:#b0c4de;line-height:1.7;margin:0;">
                Hi, I'm <span style="color:#4a9eff;font-weight:600;">Daniyal Riaz</span>, 
                an <span style="color:#00d4ff;font-weight:500;">AI Offensive Security Enthusiast</span>, 
                <span style="color:#00d4ff;font-weight:500;">Ethical Hacker</span>, and 
                <span style="color:#00d4ff;font-weight:500;">Bug Bounty Hunter</span>.
            </p>
            <br>
            <p style="color:#b0c4de;line-height:1.7;margin:0;">
                I am passionate about finding vulnerabilities in digital assets and helping 
                organizations secure their infrastructure. My mission is to make the digital 
                world safer through responsible disclosure and proactive security measures.
            </p>
            <br>
            <p style="color:#b0c4de;line-height:1.7;margin:0;">
                🎯 <strong style="color:#4a9eff;">My Vision:</strong><br>
                Creating AI applications with security at the forefront. I believe that 
                innovation and security should go hand in hand to build trustworthy and 
                resilient digital solutions.
            </p>
        </div>
        
        <!-- Security Badge -->
        <div class="security-badge">
            <p>🔐 Security-First AI Development • Responsible Disclosure • Ethical Hacking</p>
        </div>
        
        <!-- Creator Badge -->
        <div class="creator-badge">
            <p class="name">👨‍💻 Created with <span class="heart">❤️</span> by Daniyal Riaz</p>
            <p class="title">AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter</p>
            <p style="font-size:0.7rem;color:#5a7a8a;margin-top:5px;">Building Secure AI Solutions</p>
        </div>
        
        <!-- Copyright Footer -->
        <div style="margin-top:15px;text-align:center;">
            <p style="color:#5a7a8a;font-size:0.7rem;">© 2026 Dani Weather Agent • All rights reserved</p>
            <p style="color:#4a5a6a;font-size:0.6rem;margin-top:3px;">Built with security in mind 🔒</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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
        st.markdown(result["answer"])

        # Expandable workflow trace
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
