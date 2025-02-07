import pika
import messages

def callback(pika_channel, method, properties, body):
        message=body.decode()
        return messages.process_message.delay(message)

def consume():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='assistance')
    
    channel.basic_consume(queue='assistance', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()
    
if __name__ == '__main__':
    consume()
    