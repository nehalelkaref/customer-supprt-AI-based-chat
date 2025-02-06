from flask import Blueprint, request
import pika

bp = Blueprint('bp', __name__, )

# run docker instance for RabbitMQ: docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
def send_chat(msg):
    
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='assistance')
    channel.basic_publish(exchange='',routing_key='assistance',body=msg)
    connection.close()
    
@bp.route('/chat', methods=['POST'])
def get_message():
    msg = request.json['msg']
    send_chat(msg)
    return msg

    