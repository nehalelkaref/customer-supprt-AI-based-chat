from celery import Celery
from openai import OpenAI

from dotenv import load_dotenv
import os


load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery_app.task(name='api.messages.process_message')
def process_message(message):
    return call_llm(message)


def call_llm(msg):
    prompt = f'You will be given a question or an issue or a complaint relating to Github, \
        you are required to provide an answer. \
        If you do not know the answer reply with "Your issue has been relayed to our \
        representatives, we will get back to you shortly." Reply with just the answer.'

    
    completion = client.chat.completions.create(
    model="gpt-4o-mini-2024-07-18",
    messages=[
        {"role": "assistant", "content": prompt},
        {"role": "user", "content": msg}
    ]
    )
    return completion.choices[0].message.content
    
    