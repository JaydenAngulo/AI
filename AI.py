import os
import openai
import json

with open("fees.json") as f:
    fees_data = json.load(f)

def detect_hidden_fees(text):
    flagged = [fee for fee in fees_data["fees"] if fee.lower() in text.lower()]
    if flagged:
        return f"Hidden fees detected: {', '.join(flagged)}"
    return "No obvious hidden fees detected."

detect_hidden_fees("text")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError

client = openai(api_key=api_key)

System_prompt = """
You are Jayden, a friendly, helpful, professional financial advisor chatbot for teens and high school students.
You give clear, safe, general financial guidance.
Your task is to detect hidden fees, analyze contracts, explain tricky clauses, and find potential financial risks.
If you find any suspicious fees or clauses, explain why they may cost the user extra money and suggest safer alternatives.

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

import gradio as gr

iface = gr.Interface(
    fn="chatbot_response",
    inputs="text",
    outputs="text",
    title="Finance Advisor AI",
)

iface.launch(share=True)