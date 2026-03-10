from groq import Groq

import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": "write an essay about heart broken lover ie dil tuta aashiq in 8 lines in hindi"}
    ]
)

print(response.choices[0].message.content)