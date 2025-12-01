import os
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError

client = OpenAI(api_key=api_key)

System_prompt = """
You are Jayden, a friendly, helpful financial advisor chatbot.
You give clear, safe, general financial guidance.

Rules:
- Do NOT give legal instructions, tax forms, or personalized investment orders.
- You CAN give general reasoning, best practices, terminology explanations, 
personal finance principles, and hypothetical examples.
- Be concise and encouraging.
"""

def ai_response(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": System_prompt},
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content

def run_chatbot():
    print("Jayden Financial Advisor Chatbot (AI-Powered)")
    print("Ask about investing, saving, budgeting, retiring, etc.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Jayden: Bye!")
            break

        answer = ai_response(user_input)
        print("Jayden:", answer)
        print()

run_chatbot()