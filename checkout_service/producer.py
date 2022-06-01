import pika  
import json  
import config as cfg 

connection = pika.BlockingConnection(pika.ConnectionParameters(host=cfg.RABBIT_HOST))  
channel = connection.channel() 
channel.queue_declare(queue=cfg.QUEUE_TOPIC) 

def publish(message):
    channel.basic_publish(exchange='', routing_key=cfg.QUEUE_TOPIC, body=message) 


print(" [x] Sent data to RabbitMQ") 

connection.close()  