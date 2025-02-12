# Customer Support AI based Chat for Git

> _This repository contains frontend and backend implementation of customer support chat where the user inquires about an issue with Git and an OpenAI model provides a solution._
---
### Tech Stack

* React: frontend with [Ant-design](https://github.com/ant-design/ant-design) for ready-built components
* Flask: Backend
* Flask SQLAlchemy: Database integrated into flask that sotres message exchanges between the user and AI model and related request errors/status
* OpenAI: GPT-4o mini model, instructed to take in user input and reply only within Git context
* RabbitMQ: Message broker that sorts recieved/sent messages(tasks) into respective queues
* Celery**: Monitors RabbitMQ's queue for new messages(tasks) to consume and sends it to OpenAI

---
## Execution Diagram














##### ** _The use of Celery in (supposedly) a real-time chat system is not the perfect choice as Celery is better tailored for backgroud tasks_
##### _that do not require instantaneous response. Celery was only used for conceptual learning_





