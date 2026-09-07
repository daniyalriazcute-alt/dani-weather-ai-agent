import streamlit as st
from agent.workflow import run_workflow

st.set_page_config(
    page_title="Dani — Secure Weather AI Agent",
    page_icon="🤖",
    layout="wide",
)

with open("logo.svg", "r", encoding="utf-8") as f:
    logo_svg = f.read()

st.markdown(
    f"""
    <div style="display:flex;align-items:center;gap:16px;margin-bottom:12px">
      <img src="data:image/svg+xml;utf8,{logo_svg.replace("#","%23").replace("<","%3C").replace(">","%3E").replace('"','%22')}" width="78">
      <div>
        <h1 style="margin:0">Dani</h1>
        <p style="margin:0;color:#777">Secure Weather AI Agent</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Multi-stage workflow • RAG • Weather tool • Groq • OWASP Top 10 for LLM Applications 2025")

with st.sidebar:
    st.subheader("About Dani")
    st.write(
        "Dani converts natural-language weather requests into a validated location "
        "and forecast query, retrieves trusted weather/security context, calls a weather "
        "tool, and generates a concise answer."
    )
    st.markdown("**Security controls**")
    st.write("• Prompt-injection resistance")
    st.write("• Tool allowlisting")
    st.write("• Input/output validation")
    st.write("• RAG source boundaries")
    st.write("• No secrets in prompts")
    st.write("• Error-safe tool handling")
    st.write("• Minimal tool privileges")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_query = st.chat_input("Ask Dani: e.g. 'What will the weather be in Karachi tomorrow?'")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Dani is checking the forecast securely..."):
            result = run_workflow(user_query)
        st.markdown(result["answer"])

        with st.expander("Workflow trace"):
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
