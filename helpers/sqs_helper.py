"""
Helper module for sqs messages
"""
import json
import os
import sys
import boto3
from botocore.exceptions import ClientError

# add project root to sys path
#sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers.base_helper import BaseHelper

class SqsHelper(BaseHelper):
    """
    SQS Helper object
    """

    def get_sqs_client(self,config):
        """
        Return sqs_client object
        :param self:
        :return sqs_client: SQS client object
        """
        try:
            sqs_client = boto3.client('sqs', config=config)
            self.write(f'Created SQS client')
        except ClientError as err:
            self.write(f'Exception - {err}, Unable to create SQS client', level='error')
        except Exception as err:
            self.write(f'Unable to create SQS client, due to {err}', level='error') 

        return sqs_client

    def get_message_from_queue(self, queue_name, config, attempts=3):
        """
        Get message from queue
        :param self:
        :param queue_name: queue name
        :param attempts: number of attempts to get the message
        :return messages: messages list object
        """
        try:
            sqs_client = self.get_sqs_client(config)
            queue = boto3.resource('sqs').get_queue_by_name(QueueName=queue_name)
            messages = []

            # run retrieve request with multiple attempts
            for attempt in range(attempts):
                self.write(f'Finding message in queue')
                message_obj = sqs_client.receive_message(QueueUrl=queue.url,
                                                    AttributeNames=['All'],
                                                    MaxNumberOfMessages=5,
                                                    WaitTimeSeconds=20)
                self.write(f'Message object - {message_obj} from attempt - {attempt}')
                message = self.extract_messages(message_obj)
                messages.append(message)
            self.write(f'Messages object - {messages}')
        except ClientError as err:
            self.write(f'Exception - {err}, Unable to get message from queue', level='error')
        except Exception as err:
            self.write(f'Unable to get messages from queue, due to {err}', level='error') 

        return messages

    def extract_messages(self, message_object):
        """
        Extracts the body of the message from the API response object
        :param self:
        :param message_object: message object attained through receive_message sqs method
        :param message: message stripped from the message object
        :receive message syntax: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Client.receive_message
        """
        try:
            msg_body = []
            messages = message_object.get('Messages',[])
            for msg in messages:
                str_body = msg.get('Body')
                if str_body:
                    dict_body = json.loads(str_body)
                    msg_body.append(json.loads(dict_body.get('Message')).get('msg'))
            if msg_body:
                self.write(f'Message found - {msg_body}')
            else:
                self.write(f'No messages found in the message object')    
        except Exception as err:
            self.write(f'Unable to strip message from message body, due to {err}', level='error')

        return msg_body
