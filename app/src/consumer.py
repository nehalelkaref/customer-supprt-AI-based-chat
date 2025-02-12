import pika
from . import messages
def callback(pika_channel, method, properties, body):
    
        message=body.decode()
        pika_channel.basic_ack(delivery_tag=method.delivery_tag)
        return messages.process_message.delay(message,properties.correlation_id)

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='assistance')
    
    channel.basic_consume(queue='assistance', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()
    
if __name__ == '__main__':
    consume()
    