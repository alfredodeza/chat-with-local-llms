import os
import openai

openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")
model_name = os.getenv("MODEL_NAME")


def ai_chat(user_message):
    message_text = [
       {"role":"system","content":"You are a friendly AI assistant that helps people find information and answer questions."},
       {"role": "user", "content": user_message}
    ]

    completion = openai.ChatCompletion.create(
      model=model_name,
      messages=message_text,
      temperature=0.7,
      max_tokens=800,
      top_p=0.95,
      frequency_penalty=0,
      presence_penalty=0,
      stop=None
    )
    return completion


print("Welcome! how can I help you today?")

while True:
    user_message = input(">> ")
    completion = ai_chat(user_message)
    # Completion will return a response that we need to use to get the acctual string
    print(completion)
    print(completion['choices'][0]['message']['content'])
