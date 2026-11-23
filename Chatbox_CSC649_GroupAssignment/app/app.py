
import streamlit as st
import csv
from dotenv import load_dotenv
from google import genai
import os
from pathlib import Path
from difflib import SequenceMatcher

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="Assignment Buddy",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# LOAD CSV DATASET
# --------------------------------

DATASET_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "assignment_buddy_dataset.csv"
)

# Load API key from the main project folder
load_dotenv(
    Path(__file__).resolve().parent.parent / ".env"
)

gemini_api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=gemini_api_key) if gemini_api_key else None

@st.cache_data
def load_dataset():
    with open(DATASET_PATH, "r", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        return list(reader)

try:
    dataset = load_dataset()
    dataset_error = None
except FileNotFoundError:
    dataset = []
    dataset_error = "Dataset not found. Please check your data folder."

# --------------------------------
# CHATBOT SEARCH FUNCTION
# --------------------------------




def get_answer(user_question):

    # STEP 1: Handle greetings
    greeting = user_question.lower().strip()

    greetings = [
        "hello",
        "hi",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    if greeting in greetings:
        return (
            "Hello! 👋 Welcome to Assignment Buddy. "
            "I'm here to help you with assignments, "
            "academic writing, research and referencing. "
            "What would you like to learn today?"
        )

    # STEP 2: Check dataset
    if not dataset:
        return "Sorry, the academic dataset is unavailable."

    # STEP 3: Check API key
    if client is None:
        return "API key not found. Please check your .env file."

    # STEP 4: Search for relevant dataset entries
    matches = []

    for item in dataset:
        question = item["Question"]

        score = SequenceMatcher(
            None,
            user_question.lower().strip(),
            question.lower().strip()
        ).ratio()

        matches.append({
            "question": question,
            "answer": item["Answer"],
            "score": score
        })

    # STEP 5: Sort by similarity
    matches.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    # STEP 6: Select the three best matches
    relevant_matches = [
        item for item in matches[:3]
        if item["score"] >= 0.30
    ]

    if not relevant_matches:
        return (
            "Sorry, I couldn't find relevant information "
            "in my academic dataset. Please try another "
            "question about assignments, research or referencing."
        )

    # STEP 7: Prepare dataset context
    context = ""

    for item in relevant_matches:
        context += (
            f"\nQuestion: {item['question']}"
            f"\nAnswer: {item['answer']}\n"
        )

    # STEP 8: Include conversation history
    conversation = []

    for message in st.session_state.messages[-6:]:
        conversation.append({
            "role": message["role"],
            "content": message["content"]
        })

    conversation.append({
        "role": "user",
        "content": f"""
        Student question: {user_question}

        Relevant information from our custom academic dataset:
        {context}

        Answer using the supplied academic information as your
        primary source. Explain it clearly and naturally.

        If the information is insufficient, say so.
        """
    })

    
    # STEP 9: Generate answer using Gemini
    try:
        prompt = f"""
        You are Assignment Buddy, an academic learning assistant.

        Help university students with assignments, research,
        referencing and academic writing.

        Use the supplied custom academic dataset as your
        primary source. Explain concepts simply and naturally.
        Do not invent unsupported facts.

        Student question: {user_question}

        Relevant information from our academic dataset:
        {context}

        Answer the student's question clearly.
        If the information is insufficient, say so.
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print("Gemini API Error:", type(e).__name__, str(e))
        st.error(f"Gemini service error: {type(e).__name__}: {str(e)}")
        return "Sorry, I couldn't get an answer. Please check the error above."





# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #f4f7fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1100px;
}

/* Main header */

.hero {
    background: linear-gradient(120deg, #183b70, #3478c9);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(30, 70, 130, 0.15);
}

.hero h1 {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero p {
    color: #e3edff;
    font-size: 15px;
    margin-bottom: 0;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8edf5;
}

.sidebar-title {
    color: #183b70;
    font-size: 23px;
    font-weight: 800;
}

/* Chat messages */

.stChatMessage {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 16px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(20, 50, 90, 0.03);
}

/* Chat input */

.stChatInput textarea {
    border-radius: 15px !important;
}

/* Buttons */

.stButton button {
    border-radius: 12px;
    font-weight: 600;
    min-height: 42px;
}

/* Section headings */

.section-heading {
    color: #183b70;
    font-size: 19px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 12px;
}

.small-text {
    color: #718096;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------

with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">🤖 Assignment Buddy</div>',
        unsafe_allow_html=True
    )

    st.caption("Your Academic AI Assistant")

    st.divider()

    st.markdown("### 📚 About")

    st.write(
        "Assignment Buddy helps students understand "
        "academic assignments, research, referencing "
        "and writing."
    )

    st.divider()

    st.markdown("### 📊 Dataset Information")

    st.metric("Available Q&A Pairs", len(dataset))

    st.caption("Knowledge source: Custom academic CSV dataset")

    st.divider()

    st.markdown("### ⚙️ Chat Settings")

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### ℹ️ Project Information")

    st.write("**Course:** CSC649")
    st.write("**Project:** Domain-Specific Chatbot")
    st.write("**Version:** 1.0")

    st.divider()

    st.caption("Developed by CSC649 Group Project Team")

# --------------------------------
# MAIN HEADER
# --------------------------------

st.markdown("""
<div class="hero">
    <h1>🤖 Assignment Buddy</h1>
    <p>
        Your personal academic assistant.
        Ask questions about assignments, research,
        referencing and academic writing.
    </p>
</div>
""", unsafe_allow_html=True)

if dataset_error:
    st.error(dataset_error)

# --------------------------------
# CHAT SESSION
# --------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# --------------------------------
# WELCOME SCREEN
# --------------------------------

if not st.session_state.messages:

    st.markdown(
        '<div class="section-heading">👋 Welcome! How can I help you today?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="small-text">Choose a suggested question or type your own below.</p>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "📝 How do I start an assignment?",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "How should I start an assignment?"
            )
            st.rerun()

        if st.button(
            "📚 What is APA referencing?",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "What is APA referencing?"
            )
            st.rerun()

    with col2:
        if st.button(
            "🔍 What is plagiarism?",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "What is plagiarism?"
            )
            st.rerun()

        if st.button(
            "💡 What is critical thinking?",
            use_container_width=True
        ):
            st.session_state.pending_question = (
                "What is critical thinking?"
            )
            st.rerun()

    st.divider()

# --------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# --------------------------------
# CHAT INPUT
# --------------------------------

user_question = st.chat_input(
    "💬 Type your academic question here..."
)

# Handle suggested questions

if "pending_question" in st.session_state:

    user_question = st.session_state.pop("pending_question")

# --------------------------------
# GENERATE CHATBOT RESPONSE
# --------------------------------

if user_question:

    # Save user message

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    # Get response from CSV

    bot_response = get_answer(user_question)

    # Save assistant response

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })

    # Refresh to display both messages

    st.rerun()

# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.markdown(
    """
    <p style="text-align:center; color:#8492a6; font-size:12px;">
        Assignment Buddy | CSC649 Group Project<br>
        Powered by Python, Streamlit and a Custom Q&A Dataset
    </p>
    """,
    unsafe_allow_html=True
)
