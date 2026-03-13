"""
Groq Interactive Chat
"""

from groq import Groq
from dotenv import load_dotenv
load_dotenv() 

MODEL = "llama-3.1-8b-instant"
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def interactive_chat():

    print("="*60)
    print("🤖 GROQ INTERACTIVE CHAT")
    print("Type 'quit' to exit")
    print("="*60)

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Keep responses concise."}
    ]

    while True:

        user_input = input("\n👤 You: ").strip()

        if user_input.lower() in ["quit", "exit", "q"]:
            print("👋 Chat ended")
            break

        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})

        try:

            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                max_tokens=200
            )

            ai_reply = response.choices[0].message.content

            print(f"\n🤖 AI: {ai_reply}")

            messages.append({"role": "assistant", "content": ai_reply})

        except Exception as e:
            print("\n❌ Error:", e)
            break


if __name__ == "__main__":
    interactive_chat()