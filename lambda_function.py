import pika
import os
import boto3
import traceback

def lambda_handler(event, context):
    RABBIT_HOST = os.environ['RABBIT_HOST']
    RABBIT_USER = os.environ['RABBIT_USER']
    RABBIT_QUEUE = os.environ["RABBIT_QUEUE"].
    RABBIT_PORT = "5672"
    RABBIT_PWD = ""
    
    if "KMS_REGION" in os.environ:
        RABBIT_PWD_ENCRYPTED = os.environ['RABBIT_PWD']
        # Decrypt Password
        KMS_REGION = os.environ['KMS_REGION']
        RABBIT_PWD = boto3.client('kms', region_name=KMS_REGION).decrypt(CiphertextBlob=b64decode(RABBIT_PWD_ENCRYPTED))['Plaintext']
    else:
        RABBIT_PWD = os.environ['RABBIT_PWD']
       
    if "RABBIT_PORT" in os.environ:
        RABBIT_PORT = os.environ['RABBIT_PORT']
    
    #Creating RabbitMQ connection
    credentials = pika.PlainCredentials(RABBIT_USER, RABBIT_PWD)
    parameters = pika.ConnectionParameters(RABBIT_HOST,
                        RABBIT_PORT, '/', credentials)
    parameters.heartbeat = 0
    print ("Initiating RabbitMQ connection")
    #Making RabbitMQ connection
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    
    #An infinite loop to read messages from RabbbitMQ
    #The loop exits when there is no message left in the Queue
    message_idx = 1
    while True:
        print ("Attempting to read message #" + str (message_idx))
        method_frame, header_frame, body = channel.basic_get(queue = RABBIT_QUEUE)
        if (not method_frame) or (method_frame.NAME == 'Basic.GetEmpty'):
            print ("No more messages to read")
            connection.close()
            return ''
            
        try:            
            print ("Message read from RabbitMQ : " + body)
            
            #Do some processing here
            
            print ("Sending acknowledgment to clear the message from RabbitMQ")
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            message_idx = message_idx + 1
        except Exception as e:
            print (e.message)
            traceback.print_exc()
            print ("Sending acknowledgment to retain the message in RabbitMQ")
            channel.basic_nack(delivery_tag=method_frame.delivery_tag, requeue=True)
    
