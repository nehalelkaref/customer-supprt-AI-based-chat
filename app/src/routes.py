from flask import Blueprint, request, jsonify
from flask_cors import CORS
from . import db
from .model import ChatMessage
import pika
import json
import time


bp = Blueprint('bp', __name__, )
CORS(bp)
# run docker instance for RabbitMQ: docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
def send_chat(msg, correlation_id):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
        channel = connection.channel()
        properties = pika.BasicProperties(
            reply_to='responses',
            correlation_id =correlation_id
        )
        
        channel.queue_declare(queue='assistance')
        channel.basic_publish(exchange='',routing_key='assistance',body=msg, properties=properties)
        connection.close()

        db_entry = ChatMessage(correlation_id=correlation_id, user_message=msg)
        db.session.add(db_entry)
        db.session.commit()
    except:
        db_entry=ChatMessage(correlation_id=correlation_id,
                            user_message=msg,
                            error=True,
                            notes= "Rabbit | Assistance queue")
        db.session.add(db_entry)
        db.session.commit()
    
def await_repsonse(correlation_id, timeout=10):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='responses')
    
    response = None
    start_time=time.time()
    
    def callback(channel, method, properties, body):
        nonlocal response

        response_data = json.loads(body)
        if response_data.get('correlation_id') == correlation_id:
            response = response_data.get('content')
            channel.basic_ack(delivery_tag=method.delivery_tag)
            
            prev_entry = ChatMessage.query.filter_by(correlation_id=correlation_id).first()
            
            prev_entry.bot_message = response
            prev_entry.error = False
            db.session.commit()
            
            
    channel.basic_consume(queue='responses', on_message_callback=callback, auto_ack=False)
    
    while (not response and (time.time()-start_time<timeout)):
        connection.process_data_events(time_limit=1)  
    channel.close()
    connection.close()
    return response
    
    
@bp.route('/chat', methods=['POST'])
def get_message():
    msg = request.json['content']
    correlation_id = str(int(time.time()*1000))
    send_chat(msg, correlation_id)
    response = await_repsonse(correlation_id)

    if ((not response) or response=='ERROR'):
        prev_entry = ChatMessage.query.filter_by(correlation_id=correlation_id).first()
            
        prev_entry.error = True
        if (not prev_entry.notes):
            prev_entry.notes = ' | Task has not been consumed'
        else:
            prev_entry.notes = prev_entry.notes + ' | Task has not been consumed'
        return jsonify({'sender':'Bot',
                        'content':'Your inquiry has been sent. There is an error \
                            at our end and we will get back to you shortly.'})
        
    return jsonify({'sender':'Bot','content':response})
    

    