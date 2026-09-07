import streamlit as st
import streamlit.components.v1 as components
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
# RAIN ANIMATION (BACKGROUND CANVAS)
# ============================================================
rain_html = """
<style>
    body {
        margin: 0;
        overflow: hidden;
        background: transparent;
    }
    canvas {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -1;
        pointer-events: none;
    }
</style>
<canvas id="rainCanvas"></canvas>
<script>
    const canvas = document.getElementById('rainCanvas');
    const ctx = canvas.getContext('2d');
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);
    
    const drops = [];
    const count = 75;
    
    for (let i = 0; i < count; i++) {
        drops.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            length: Math.random() * 20 + 10,
            speed: Math.random() * 10 + 12,
            opacity: Math.random() * 0.3 + 0.1
        });
    }
    
    function draw() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < drops.length; i++) {
            const d = drops[i];
            ctx.beginPath();
            ctx.strokeStyle = `rgba(74, 158, 255, ${d.opacity})`;
            ctx.lineWidth = 1.2;
            ctx.moveTo(d.x, d.y);
            ctx.lineTo(d.x, d.y + d.length);
            ctx.stroke();
            
            d.y += d.speed;
            if (d.y > canvas.height) {
                d.y = -d.length;
                d.x = Math.random() * canvas.width;
            }
        }
        requestAnimationFrame(draw);
    }
    draw();
</script>
"""
components.html(rain_html, height=0)

# ============================================================
# CUSTOM STYLES
# ============================================================
st.markdown("""
<style>
    /* Hide default header elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Main Dark Theme */
    .stApp {
        background-color: #0b131e !important;
    }

    /* Sidebar Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(13, 23, 36, 0.95) !important;
        border-right: 1px solid rgba(74, 158, 255, 0.15) !important;
    }

    /* Robot Logo Container */
    .robot-icon-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 10px;
    }
    
    .robot-icon {
        width: 64px;
        height: 64px;
        filter: drop-shadow(0px 0px 12px rgba(0, 212, 255, 0.4));
    }

    /* Sidebar Typography */
    .sidebar-logo {
        text-align: center;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid rgba(74, 158, 255, 0.15);
        margin-bottom: 20px;
    }
    .sidebar-logo .logo-text {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4a9eff, #00d4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 4px 0 0 0;
    }
    .sidebar-logo .logo-sub {
        color: #7a9ab5;
        font-size: 0.8rem;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin: 4px 0 0 0;
    }

    .sidebar-section-title {
        color: #4a9eff;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 20px;
        margin-bottom: 8px;
    }

    .sidebar-info-box {
        background: rgba(20, 38, 58, 0.5);
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

    /* Main Console Header */
    .chat-header {
        text-align: center;
        padding: 10px 0 20px 0;
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
        margin-bottom: 12px;
    }
    .chat-header .chat-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
    }
    .chat-header .chat-subtitle {
        color: #8da4b8;
        font-size: 0.9rem;
        margin-top: 6px;
    }

    /* Welcome Card */
    .welcome-box {
        text-align: center;
        padding: 2rem 1.5rem;
        background: rgba(18, 32, 48, 0.6);
        border-radius: 16px;
        border: 1px solid rgba(74, 158, 255, 0.15);
        margin: 20px auto 30px auto;
        max-width: 550px;
    }
    .welcome-box h2 {
        color: #ffffff;
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .welcome-box p {
        color: #9ab5cc;
        font-size: 0.9rem;
    }
    .example-tag {
        background: rgba(74, 158, 255, 0.08);
        border: 1px solid rgba(74, 158, 255, 0.2);
        color: #b0c4de;
        padding: 8px 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        margin-top: 8px;
    }

    /* Chat Input Styling */
    .stChatInputContainer {
        padding-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# SVG Robot Icon Definition
ROBOT_SVG = """
<svg class="robot-icon" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="32" cy="8" r="3" fill="#00D4FF"/>
    <line x1="32" y1="11" x2="32" y2="18" stroke="#4A9EFF" stroke-width="2.5"/>
    <rect x="10" y="27" width="4" height="10" rx="2" fill="#4A9EFF"/>
    <rect x="50" y="27" width="4" height="10" rx="2" fill="#4A9EFF"/>
    <rect x="14" y="18" width="36" height="28" rx="8" fill="#12263E" stroke="#00D4FF" stroke-width="2"/>
    <rect x="18" y="23" width="28" height="14" rx="5" fill="#0A131E" stroke="#4A9EFF" stroke-width="1.5"/>
    <circle cx="26" cy="30" r="3" fill="#00D4FF"/>
    <circle cx="38" cy="30" r="3" fill="#00D4FF"/>
    <line x1="24" y1="40" x2="40" y2="40" stroke="#4A9EFF" stroke-width="2" stroke-linecap="round"/>
    <rect x="27" y="46" width="10" height="4" fill="#4A9EFF"/>
    <path d="M20 50 C20 50, 24 58, 32 58 C40 58, 44 50, 44 50" stroke="#00D4FF" stroke-width="2" fill="none"/>
</svg>
"""

# ============================================================
# SIDEBAR CONTENT
# ============================================================
with st.sidebar:
    st.markdown('<div class="sidebar-logo"><div class="robot-icon-container">' + ROBOT_SVG + '</div><p class="logo-text">DANI AI</p><p class="logo-sub">Weather Intelligence</p></div>', unsafe_allow_html=True)
    
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
    
    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-section-title">👨‍💻 Security Lead</p>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sidebar-info-box">
        <p>Architected by <strong style="color:#4a9eff;">Daniyal Riaz</strong><br>
        <span style="color:#7a9ab5; font-size:0.75rem;">AI Security & Vulnerability Researcher</span></p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="sidebar-footer">© 2026 Dani Weather Agent</p>', unsafe_allow_html=True)

# ============================================================
# CHAT INTERFACE
# ============================================================
st.markdown('<div class="chat-header"><div class="robot-icon-container">' + ROBOT_SVG + '</div><div class="badge">● AI Agent Active</div><div class="chat-title">Weather Intelligence Console</div><div class="chat-subtitle">Ask anything about atmospheric conditions globally</div></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if not st.session_state.messages:
    st.markdown("""
    <div class="welcome-box">
        <h2>System Ready</h2>
        <p>Ask a question to query current weather status or future forecasts.</p>
        <div class="example-tag">💡 "What is the precipitation outlook for Karachi today?"</div>
        <div class="example-tag">💡 "Will it rain in Lahore tomorrow afternoon?"</div>
    </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Enter weather query or location...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing atmospheric data..."):
            try:
                result = run_workflow(user_query)
                answer = result.get("answer", "No response generated.") if isinstance(result, dict) else str(result)
            except Exception as e:
                answer = "⚠️ Could not process forecast request."
                st.error(f"Error: {e}")
        st.markdown(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
