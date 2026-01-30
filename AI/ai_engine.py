def generate_ai_answer(question: str, memory: list) -> str:
    """
    Later replace this with OpenAI / Gemini / Llama
    """
    if memory:
        last_q, last_a = memory[-1]
        return f"You asked: {question}. Previously you said: {last_q}"

    return f"AI Answer: {question}"
