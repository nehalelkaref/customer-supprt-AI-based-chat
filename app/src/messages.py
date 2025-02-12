from openai import OpenAI
from dotenv import load_dotenv
from celery import Celery
from .model import ChatMessage
from . import db
import pika
import json
import os
from .run import app


load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery_app.task(name='api.messages.process_message')
def process_message(message, correlation_id):
    try:
        response = call_llm(message)
        response_dict = {'content':response, 'correlation_id':correlation_id}
        
    except:
        with app.app_context():
            prev_entry = ChatMessage.query.filter_by(correlation_id=correlation_id).first()
            prev_entry.error=True
            if not prev_entry.notes:
                
                prev_entry.notes = ' | LLM Error'
            else:
                prev_entry.notes = prev_entry.notes + ' | LLM Error'
                
            db.session.commit()
    
        response_dict = {'content':'ERROR', 'correlation_id':correlation_id}
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()
    
    channel.queue_declare(queue='responses')
    channel.basic_publish(exchange='', routing_key='responses',body=json.dumps(response_dict))
    connection.close()
    

def call_llm(msg):
    prompt = f'You will be given a question or an issue or a complaint relating to Github, \
        you are required to provide an answer. \
        If you do not know the answer reply with "Your issue has been relayed to our \
        representatives, we will get back to you shortly." Reply with just the answer.'

    
    completion =client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "assistant", "content": prompt},
            {"role": "user", "content": msg}
        ])
    return completion.choices[0].message.content
        
    