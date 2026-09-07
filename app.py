import streamlit as st
from workflow import run_workflow


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Dani — Weather AI Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>
        /* Hide Streamlit default UI */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        [data-testid="stSidebar"] { display: none; }

        /* App background */
        .stApp {
            background: linear-gradient(135deg, #0a1922 0%, #1a2a3a 50%, #0d1b2a 100%);
        }

        [data-testid="stAppViewContainer"] {
            background: transparent;
        }

        [data-testid="stMain"] {
            background: transparent;
        }

        [data-testid="stMainBlockContainer"] {
            max-width: 1050px;
            margin: 0 auto;
            padding-top: 2rem;
            padding-bottom: 8rem;
        }

        /* Headings */
        h1, h2, h3 {
            color: #dcecff !important;
        }

        p, li, span {
            color: #c8d6e5;
        }

        /* Logo container */
        .logo-container {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
            padding: 18px 24px;
            background: rgba(10, 25, 40, 0.70);
            border-radius: 15px;
            border: 1px solid rgba(74, 158, 255, 0.18);
            margin: 0 auto 28px auto;
            max-width: 700px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
        }

        .logo-container svg {
            width: 58px;
            height: 58px;
            filter: drop-shadow(0 0 10px rgba(74, 158, 255, 0.45));
            animation: pulse 3s ease-in-out infinite;
        }

        .logo-container .title {
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(135deg, #4a9eff, #00d4ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-container .subtitle {
            color: #7a9ab5 !important;
            font-size: 0.9rem;
            margin: 0;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        /* Info boxes */
        .info-box {
            background: rgba(20, 50, 80, 0.35);
            padding: 15px 20px;
            border-radius: 10px;
            border-left: 3px solid #4a9eff;
            margin: 10px 0;
        }

        .info-box p {
            color: #e8f0fe !important;
            margin: 0;
            font-size: 1rem !important;
        }

        .about-box {
            background: rgba(20, 50, 80, 0.35);
            padding: 15px 20px;
            border-radius: 10px;
            border: 1px solid rgba(74, 158, 255, 0.16);
            margin: 10px 0;
        }

        .about-box p {
            color: #c8d6e5 !important;
            line-height: 1.8 !important;
            margin: 8px 0;
            font-size: 0.95rem !important;
        }

        .creator-box {
            background: rgba(20, 50, 80, 0.45);
            border-radius: 10px;
            padding: 15px;
            margin: 12px 0;
            border: 1px solid rgba(74, 158, 255, 0.16);
            text-align: center;
        }

        .creator-box .name {
            color: #4a9eff !important;
            font-weight: 700;
            font-size: 1.1rem;
            margin: 5px 0;
        }

        .creator-box .title {
            color: #00d4ff !important;
            font-size: 0.85rem;
            margin: 5px 0;
        }

        .creator-box .heart {
            color: #ff6b6b !important;
        }

        .divider {
            border: none;
            border-top: 1px solid rgba(74, 158, 255, 0.18);
            margin: 28px 0;
        }

        /* Feature columns */
        [data-testid="stHorizontalBlock"] {
            gap: 1rem;
        }

        [data-testid="column"] {
            background: rgba(20, 50, 80, 0.20);
            border: 1px solid rgba(74, 158, 255, 0.10);
            border-radius: 12px;
            padding: 12px 16px;
        }

        /* Welcome card */
        .welcome-box {
            text-align: center;
            padding: 3rem 2rem;
            background: rgba(20, 50, 80, 0.30);
            border-radius: 20px;
            border: 1px solid rgba(74, 158, 255, 0.18);
            margin: 2rem auto;
            max-width: 600px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.15);
        }

        .welcome-box h2 {
            color: #4a9eff !important;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }

        .welcome-box p {
            color: #9ab5cc !important;
            font-size: 1.1rem;
            line-height: 1.6;
        }

        .welcome-box .examples {
            color: #b0c4de !important;
            font-size: 0.95rem;
            margin-top: 1rem;
            line-height: 1.8;
        }

        /* Chat messages */
        [data-testid="stChatMessage"] {
            padding: 0.6rem 0 !important;
            background: transparent !important;
        }

        [data-testid="stChatMessageContent"] {
            color: #e8f0fe !important;
        }

        /* User message bubble */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) [data-testid="stChatMessageContent"] {
            background: rgba(30, 70, 110, 0.72);
            border: 1px solid rgba(74, 158, 255, 0.28);
            border-radius: 18px 18px 4px 18px;
            padding: 12px 18px;
        }

        /* Assistant message bubble */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) [data-testid="stChatMessageContent"] {
            background: rgba(20, 50, 80, 0.48);
            border: 1px solid rgba(0, 212, 255, 0.20);
            border-radius: 18px 18px 18px 4px;
            padding: 12px 18px;
        }

        /* Chat input */
        [data-testid="stChatInput"] {
            background: rgba(10, 25, 40, 0.96) !important;
            border: 2px solid rgba(74, 158, 255, 0.38) !important;
            border-radius: 30px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
            backdrop-filter: blur(10px);
        }

        [data-testid="stChatInput"] textarea {
            color: #ffffff !important;
            background: transparent !important;
            caret-color: #4a9eff !important;
        }

        [data-testid="stChatInput"] textarea::placeholder {
            color: #aabbcc !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInput"] button {
            background: linear-gradient(135deg, #4a9eff, #00d4ff) !important;
            border: none !important;
            border-radius: 20px !important;
            color: #ffffff !important;
            transition: all 0.25s ease !important;
        }

        [data-testid="stChatInput"] button:hover {
            transform: scale(1.06) !important;
            box-shadow: 0 4px 20px rgba(74, 158, 255, 0.45) !important;
        }

        /* Mobile improvements */
        @media (max-width: 768px) {
            [data-testid="stMainBlockContainer"] {
                padding: 1rem 1rem 7rem 1rem;
            }

            .logo-container {
                padding: 14px;
            }

            .logo-container .title {
                font-size: 1.6rem;
            }

            .welcome-box {
                padding: 2rem 1rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER WITH ROBOT LOGO
# ============================================================
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)


# ============================================================
# ABOUT DANI - LEFT SIDE
# ============================================================
st.markdown("## 🌤️ About Dani")

st.markdown(
    """
    <div class="info-box">
        <p>
            Dani converts natural-language weather requests into accurate
            forecasts using advanced AI and real-time weather data.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### ✨ Key Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("📍 **Location-based forecasts**")
    st.markdown("🌡️ **Temperature and precipitation**")
    st.markdown("📅 **1–7 day predictions**")

with col2:
    st.markdown("🤖 **Natural language understanding**")
    st.markdown("🔒 **Secure and reliable**")
    st.markdown("⚡ **Real-time weather data**")

st.markdown(
    """
    <div class="info-box" style="border-left-color:#00d4ff; margin-top:15px;">
        <p>
            💡 <strong>Try asking:</strong><br>
            <span style="color:#b0c4de;">
                "What's the weather in Karachi today?"
            </span><br>
            <span style="color:#b0c4de;">
                "Will it rain in Lahore tomorrow?"
            </span>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ============================================================
# ABOUT ME - LEFT SIDE (COMPLETE)
# ============================================================
st.markdown("## 👨‍💻 About Me")

st.markdown(
    """
    <div class="about-box">
        <p>
            Hi, I'm
            <strong style="color:#4a9eff;">Daniyal Riaz</strong>,
            an
            <strong style="color:#00d4ff;">
                AI Offensive Security Enthusiast
            </strong>,
            <strong style="color:#00d4ff;">Ethical Hacker</strong>,
            and
            <strong style="color:#00d4ff;">Bug Bounty Hunter</strong>.
        </p>

        <p>
            I'm passionate about finding vulnerabilities and helping
            organizations secure their digital assets.
        </p>

        <p>
            🎯
            <strong style="color:#4a9eff;">My Vision:</strong>
            Creating AI applications with security at the forefront.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="creator-box">
        <p class="name">
            👨‍💻 Created with
            <span class="heart">❤️</span>
            by Daniyal Riaz
        </p>

        <p class="title">
            AI Offensive Security Enthusiast • Ethical Hacker • Bug Bounty Hunter
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        text-align:center;
        margin-top:15px;
        padding-top:10px;
        border-top:1px solid rgba(74,158,255,0.18);
    ">
        <p style="color:#4a6a7a; font-size:0.75rem; margin:0;">
            © 2026 Dani Weather Agent • Built with security in mind 🔒
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)


# ============================================================
# CHAT STATE
# ============================================================
if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# WELCOME MESSAGE
# ============================================================
if not st.session_state.messages:
    st.markdown(
        """
        <div class="welcome-box">
            <h2>👋 Hello! I'm Dani</h2>
            <p>Ask me about the weather anywhere in the world.</p>

            <div class="examples">
                💡 Try: "What's the weather in Karachi today?"<br>
                💡 Try: "Will it rain in Lahore tomorrow?"
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DISPLAY CHAT HISTORY
# ============================================================
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# ============================================================
# CHAT INPUT AND RESPONSE
# ============================================================
user_query = st.chat_input(
    "Ask Dani about the weather...",
    key="chat_input",
)

if user_query:
    # Save and show the user's query.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_query,
        }
    )

    with st.chat_message("user", avatar="🧑‍💻"):
        st.markdown(user_query)

    # Get and show the assistant response.
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🌤️ Dani is checking the forecast..."):
            try:
                result = run_workflow(user_query)

                if isinstance(result, dict):
                    answer = result.get(
                        "answer",
                        "Sorry, I could not generate a weather response.",
                    )
                else:
                    answer = str(result)

            except Exception as error:
                answer = (
                    "⚠️ I couldn't retrieve the weather forecast right now. "
                    "Please check your API key, internet connection, and "
                    "workflow configuration, then try again."
                )

                st.error(f"Workflow error: {error}")

        st.markdown(answer)

    # Save assistant response in the session chat history.
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    # Refresh so all messages display consistently.
    st.rerun()
