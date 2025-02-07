from celery import Celery

celery_app = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery_app.task(name='api.messages.process_message')
def process_message(message):
    # to do: Call AI model
    return ('Ok, will be right with you!')

