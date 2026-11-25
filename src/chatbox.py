from openai import APIError
from src.check_API import MODEL_NAME, get_client
from src.dataset_loader import load_dataset_context

STYLE_INSTRUCTIONS = {
    "Balanced": "Give a clear, well-structured, balanced explanation.",
    "Quick Summary": "Keep the answer concise and direct using short bullet points.",
    "Step-by-Step": "Break the explanation down into numbered, easy-to-follow steps.",
    "With Examples": "Include clear, practical academic examples to illustrate your explanation.",
}


def ask_chatbox(question: str, style: str = "Balanced") -> str:
    client = get_client()
    if client is None:
        return "ERROR: XAI_API_KEY not found in .env file."

    dataset_context = load_dataset_context()
    style_guide = STYLE_INSTRUCTIONS.get(style, STYLE_INSTRUCTIONS["Balanced"])

    system_instruction = (
        "You are Assignment Buddy, an academic assistant for university students (CSC649). "
        "Help with essay structure, referencing (APA, Harvard, IEEE), paraphrasing, research, and study tips. "
        "Promote academic integrity—guide students rather than writing graded assignments for them. "
        f"{style_guide}"
    )

    if dataset_context:
        system_instruction += (
            "\n\nUse the following verified Q&A knowledge base when relevant:\n"
            f"{dataset_context}"
        )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content or "No response returned from Grok."
    except APIError as err:
        return f"⚠️ Grok API error: {err.message}"