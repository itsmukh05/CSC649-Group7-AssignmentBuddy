import csv
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# --- 1. PATHS & BACKEND STATUS ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env", override=True)

from src.chatbox import ask_chatbox

DATASET_CANDIDATES = [
    PROJECT_ROOT / "data" / "assignment_buddy_dataset.csv",
    PROJECT_ROOT / "Chatbox_CSC649_GroupAssignment" / "data" / "assignment_buddy_dataset.csv",
]
BACKEND_CONNECTED = bool(os.getenv("XAI_API_KEY"))
EXIT_COMMANDS = {"exit", "quit", "bye", "goodbye"}


# --- 2. PAGE CONFIG & ANIMATED CSS ---
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
        padding-top: 2.6rem;
        padding-bottom: 5.5rem;
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

    @keyframes pulseDot {
        0% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(34, 197, 94, 0); }
        100% { box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }
    }

    @keyframes pulseAmber {
        0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
        70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
        100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
    }

    @keyframes slideUpFade {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
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

    .status-pill {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding: 0.55rem 0.85rem;
        border-radius: 10px;
        font-size: 0.84rem;
        font-weight: 600;
        margin-top: 0.35rem;
    }

    .status-live {
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
    }

    .status-preview {
        background-color: #FFFBEB;
        color: #92400E;
        border: 1px solid #FDE68A;
    }

    .dot-green {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #22C55E;
        animation: pulseDot 2s infinite;
        flex-shrink: 0;
    }

    .dot-amber {
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #F59E0B;
        animation: pulseAmber 2s infinite;
        flex-shrink: 0;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #CBD5E1;
        background-color: #FFFFFF;
        padding: 0.7rem 1rem;
        text-align: left;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background-color 0.18s ease;
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        border-color: #2563EB;
        color: #1D4ED8;
        background-color: #EFF6FF;
        box-shadow: 0 8px 18px rgba(37, 99, 235, 0.14);
    }

    [data-testid="stChatMessage"] {
        animation: slideUpFade 0.32s ease-out;
        border-radius: 14px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.65rem;
    }

    [data-testid="stChatMessage"]:has(.user-bubble-tag) {
        background-color: #EFF6FF;
        border: 1px solid #BFDBFE;
    }

    [data-testid="stChatMessage"]:has(.bot-bubble-tag) {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stChatMessage"] .stButton > button {
        width: auto;
        min-height: 1.85rem;
        padding: 0.18rem 0.65rem;
        font-size: 0.8rem;
        border-radius: 8px;
        text-align: center;
        white-space: nowrap;
        background-color: #FFFFFF;
        border: 1px solid #CBD5E1;
        color: #334155;
    }

    [data-testid="stChatMessage"] .stButton > button:hover {
        transform: translateY(-1px);
        border-color: #2563EB;
        color: #1D4ED8;
        background-color: #DBEAFE;
        box-shadow: 0 3px 8px rgba(37, 99, 235, 0.12);
    }

    .msg-role-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.25rem;
    }

    .user-bubble-tag {
        color: #1D4ED8;
    }

    .bot-bubble-tag {
        color: #475569;
    }

    .integrity-box {
        padding: 0.85rem;
        border-radius: 10px;
        background-color: #EFF6FF;
        border-left: 4px solid #2563EB;
        font-size: 0.83rem;
        color: #1E293B;
        line-height: 1.45;
    }

    .app-footer {
        text-align: center;
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid #E2E8F0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --- 3. DATA & HELPER FUNCTIONS ---
STARTER_TOPICS = {
    "✍️ Writing": [
        ("📝", "What should I include in an introduction?"),
        ("🎯", "How do I write a good paragraph?"),
    ],
    "📚 Referencing": [
        ("📖", "What is APA referencing?"),
        ("🔍", "How can I avoid plagiarism?"),
    ],
    "🤝 Study & AI": [
        ("👥", "How can I prepare for a group assignment?"),
        ("🤖", "Can AI help me with assignments?"),
    ],
}


@st.cache_data
def count_dataset_pairs() -> int:
    """Count rows in the custom Q&A CSV dataset if present."""
    for path in DATASET_CANDIDATES:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8-sig") as file:
                    return sum(1 for _ in csv.DictReader(file))
            except Exception:
                return 0
    return 0


def format_chat_for_download(messages: list[dict]) -> str:
    """Format conversation history as a downloadable text file."""
    lines = [
        "Assignment Buddy - Chat Transcript",
        f"Exported: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "=" * 46,
        "",
    ]
    for msg in messages:
        speaker = "Student" if msg["role"] == "user" else "Assignment Buddy"
        lines.append(f"{speaker}:\n{msg['content']}\n")
    return "\n".join(lines)


def stream_response_text(text: str):
    """Yield response tokens smoothly while preserving markdown line breaks."""
    for token in re.findall(r"\S+\s*", text):
        yield token
        time.sleep(0.018)


# --- 4. SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = None
if "editing_idx" not in st.session_state:
    st.session_state.editing_idx = None

dataset_count = count_dataset_pairs()


# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🎓 Assignment Buddy")
    st.caption("Your Interactive Academic AI Assistant")

    if BACKEND_CONNECTED:
        st.markdown(
            '<div class="status-pill status-live"><span class="dot-green"></span>Backend Live (Grok + CSV)</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-pill status-preview"><span class="dot-amber"></span>Preview Mode (Awaiting Backend)</div>',
            unsafe_allow_html=True,
        )

    st.divider()

    st.markdown("#### 📊 Knowledge Base")
    st.metric(
        label="Available Q&A Pairs",
        value=dataset_count if dataset_count > 0 else "Pending",
    )
    st.caption("Source: Custom academic CSV dataset (`assignment_buddy_dataset.csv`)")

    st.divider()

    st.markdown("#### 🎛️ Session Controls")
    user_msg_count = sum(1 for m in st.session_state.messages if m["role"] == "user")
    st.caption(f"Questions asked this session: **{user_msg_count}**")

    enable_typing_effect = st.toggle(
        "✨ Typing animation",
        value=True,
        help="Animate Assignment Buddy's replies word by word.",
    )

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_prompt = None
        st.session_state.editing_idx = None
        st.toast("Conversation cleared!", icon="🧹")
        st.rerun()

    st.download_button(
        label="💾 Download Chat (.txt)",
        data=format_chat_for_download(st.session_state.messages),
        file_name="assignment_buddy_chat.txt",
        mime="text/plain",
        disabled=(user_msg_count == 0),
        use_container_width=True,
    )

    st.divider()

    st.markdown(
        '<div class="integrity-box"><strong>Academic Integrity Note</strong><br>'
        "Assignment Buddy provides academic guidance and examples. Always write "
        "your final work in your own words and verify citations.</div>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.caption("**Course:** CSC649  \n**Domain:** Education – Academic Assistance")


# --- 6. ANIMATED HERO BANNER ---
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


# --- 7. INTERACTIVE ANSWER STYLE SELECTOR ---
style_options = ["Balanced", "Quick Summary", "Step-by-Step", "With Examples"]
if hasattr(st, "segmented_control"):
    chosen_style = st.segmented_control(
        "Answer style:",
        options=style_options,
        default="Balanced",
    )
    response_style = chosen_style or "Balanced"
else:
    response_style = st.radio(
        "Answer style:",
        options=style_options,
        horizontal=True,
    )


# --- 8. TABBED STARTER CARDS (SHOWN BEFORE FIRST MESSAGE) ---
if len(st.session_state.messages) == 0:
    st.markdown("#### 👋 Welcome! Pick a topic or ask your own question below")
    tabs = st.tabs(list(STARTER_TOPICS.keys()))

    for tab_idx, (topic_name, prompts) in enumerate(STARTER_TOPICS.items()):
        with tabs[tab_idx]:
            col1, col2 = st.columns(2)
            for q_idx, (icon, question) in enumerate(prompts):
                target_col = col1 if q_idx % 2 == 0 else col2
                with target_col:
                    if st.button(f"{icon}  {question}", key=f"starter_{tab_idx}_{q_idx}"):
                        st.session_state.messages.append(
                            {"role": "user", "content": question, "source": None}
                        )
                        st.session_state.pending_prompt = question
                        st.toast("Question sent!", icon="✨")
                        st.rerun()


# --- 9. CHAT HISTORY (WITH INLINE EDIT FOR USER MESSAGES) ---
for idx, message in enumerate(st.session_state.messages):
    is_user = message["role"] == "user"
    avatar = "🧑‍🎓" if is_user else "🤖"

    with st.chat_message(message["role"], avatar=avatar):
        if is_user:
            header_col, btn_col = st.columns([11, 1])
            with header_col:
                st.markdown(
                    '<div class="msg-role-label user-bubble-tag">You</div>',
                    unsafe_allow_html=True,
                )
            with btn_col:
                if st.session_state.editing_idx != idx:
                    if st.button("✏️", key=f"edit_btn_{idx}", help="Edit message"):
                        st.session_state.editing_idx = idx
                        st.rerun()

            if st.session_state.editing_idx == idx:
                edited_text = st.text_area(
                    "Edit message",
                    value=message["content"],
                    key=f"edit_input_{idx}",
                    label_visibility="collapsed",
                    height=90,
                )
                save_col, cancel_col, _ = st.columns([2.4, 1.6, 6])
                with save_col:
                    if st.button("✅ Save & Send", key=f"save_edit_{idx}"):
                        cleaned_edit = edited_text.strip()
                        if cleaned_edit:
                            st.session_state.messages = st.session_state.messages[:idx]
                            st.session_state.messages.append(
                                {"role": "user", "content": cleaned_edit, "source": None}
                            )
                            st.session_state.pending_prompt = cleaned_edit
                            st.session_state.editing_idx = None
                            st.toast("Message updated! Regenerating reply...", icon="✏️")
                            st.rerun()
                        else:
                            st.warning("Message cannot be empty.")
                with cancel_col:
                    if st.button("Cancel", key=f"cancel_edit_{idx}"):
                        st.session_state.editing_idx = None
                        st.rerun()
            else:
                st.markdown(message["content"])
        else:
            st.markdown(
                '<div class="msg-role-label bot-bubble-tag">Assignment Buddy</div>',
                unsafe_allow_html=True,
            )
            st.markdown(message["content"])


# --- 10. PROCESS PENDING REPLY ---
if st.session_state.pending_prompt:
    prompt_to_answer = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            '<div class="msg-role-label bot-bubble-tag">Assignment Buddy</div>',
            unsafe_allow_html=True,
        )

        if prompt_to_answer.lower().strip("!?. ") in EXIT_COMMANDS:
            reply = (
                "Goodbye! Good luck with your assignment. 🎓\n\n"
                "You can save this session anytime using **💾 Download Chat (.txt)** "
                "or start fresh with **🗑️ Clear Conversation** in the sidebar."
            )
        else:
            with st.spinner("Thinking..."):
                try:
                    reply = ask_chatbox(prompt_to_answer, style=response_style)
                except Exception as exc:
                    reply = (
                        "⚠️ **Unable to reach the AI backend right now.**\n\n"
                        "Please check that your `XAI_API_KEY` is set in `.env` and try again.\n\n"
                        f"*Details: `{exc}`*"
                    )

        if enable_typing_effect and hasattr(st, "write_stream"):
            st.write_stream(stream_response_text(reply))
        else:
            st.markdown(reply)

    st.session_state.messages.append(
        {"role": "assistant", "content": reply, "source": None}
    )


# --- 11. CHAT INPUT BAR ---
if typed_input := st.chat_input("Type your academic question here..."):
    cleaned = typed_input.strip()
    if cleaned:
        st.session_state.editing_idx = None
        st.session_state.messages.append({"role": "user", "content": cleaned, "source": None})
        st.session_state.pending_prompt = cleaned
        st.rerun()


# --- 12. FOOTER ---
st.markdown(
    '<div class="app-footer">Assignment Buddy | CSC649 Group Project • Built with Python, Streamlit, Custom CSV Dataset & xAI Grok</div>',
    unsafe_allow_html=True,
)