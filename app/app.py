import streamlit as st

# --- 1. PAGE CONFIG & ANIMATED CSS ---
st.set_page_config(
    page_title="Assignment Buddy",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        max-width: 920px;
        padding-top: 1.4rem;
        padding-bottom: 2rem;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes floatIcon {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    .hero-banner {
        background: linear-gradient(125deg, #1E3A8A, #2563EB, #0284C7, #1D4ED8);
        background-size: 260% 260%;
        animation: gradientShift 9s ease infinite;
        color: #FFFFFF;
        padding: 1.8rem 2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
        box-shadow: 0 12px 28px rgba(37, 99, 235, 0.22);
    }
    .hero-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        color: #EFF6FF;
        font-size: 0.74rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        margin-bottom: 0.65rem;
        letter-spacing: 0.04em;
    }
    .hero-title-row {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }
    .hero-icon {
        display: inline-block;
        font-size: 2.1rem;
        animation: floatIcon 3s ease-in-out infinite;
    }
    .hero-banner h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .hero-banner p {
        margin: 0.45rem 0 0 0;
        font-size: 0.97rem;
        color: #E0F2FE;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- 2. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. ANIMATED HERO BANNER ---
st.markdown(
    """
    <div class="hero-banner">
        <div class="hero-badge">CSC649 • DOMAIN-SPECIFIC AI CHATBOT</div>
        <div class="hero-title-row">
            <span class="hero-icon">🎓</span>
            <h1>Assignment Buddy</h1>
        </div>
        <p>Your interactive academic assistant for essay structure, referencing (APA/Harvard/IEEE), paraphrasing, research, and study tips.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- 4. CHAT HISTORY ---
for message in st.session_state.messages:
    avatar = "🧑‍🎓" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# --- 5. CHAT INPUT ---
if typed_input := st.chat_input("Type your academic question here..."):
    cleaned = typed_input.strip()
    if cleaned:
        st.session_state.messages.append({"role": "user", "content": cleaned, "source": None})
        with st.chat_message("user", avatar="🧑‍🎓"):
            st.markdown(cleaned)

        reply = f"**[UI Preview Mode]** You asked: *\"{cleaned}\"* — frontend ready for sidebar and backend integration."
        st.session_state.messages.append({"role": "assistant", "content": reply, "source": None})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(reply)