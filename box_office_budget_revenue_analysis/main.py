import os
from openai import OpenAI

# Set your API key here
client = OpenAI(api_key="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")

def chat_with_gpt():
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("GPT Chatbot (type 'exit' to quit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        conversation.append({"role": "user", "content": user_input})

        response = client.chat.completions.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=conversation
        )

        reply = response.choices[0].message.content
        print("Bot:", reply)

        conversation.append({"role": "assistant", "content": reply})

if __name__ == "__main__":
    chat_with_gpt()
