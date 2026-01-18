from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import json

app = Flask(__name__)

# with open("fees.json") as f:
#     fees_data = json.load(f)

# def detect_hidden_fees(text):
#     flagged = [fee for fee in fees_data["fees"] if fee.lower() in text.lower()]
#     if flagged:
#         return f"Hidden fees detected: {', '.join(flagged)}"
#     return "No obvious hidden fees detected."

# detect_hidden_fees("text")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError

client = OpenAI(api_key=api_key)

System_prompt = """
You are Jayden, a friendly, helpful, professional financial advisor chatbot for teenagers and high school students.
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

#     return response.choices[0].message.content

# def run_chatbot():
#     return "Jayden Financial Advisor Chatbot (AI-Powered)\nAsk about investing, saving, budgeting, retiring, etc.\nType 'exit' to quit.\n"

# user_input = input("You: ")

# def input(user_input):
#     if user_input.lower() in ["exit", "quit"]:
#         return "Jayden: Bye!"

def chat_response(user_input):
    answer = ai_response(user_input)
    return f"Jayden: {answer}\n"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get("message")
    response = chat_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)

print("Debug: ", data)