"""
Helper module for sqs messages
"""
import json
import os
import sys
import time
import boto3
from botocore.exceptions import ClientError

from .base_helper import BaseHelper
from ..conf import sqs_conf

class SqsHelper(BaseHelper):
    """
    SQS Helper object
    """

    def get_sqs_client(self):
        """
        Return sqs_client object
        :param self:
        :return sqs_client: SQS client object
        """
        try:
            sqs_client = boto3.client('sqs', config=sqs_conf.config)
            self.write(f'Created SQS client')
        except ClientError as err:
            self.write(f'Exception - {err}, Unable to create SQS client', level='error')
        except Exception as err:
            self.write(f'Unable to create SQS client, due to {err}', level='error') 

        return sqs_client

    def get_sqs_queue(self, queue_name):
        """
        Get queue
        :param self:
        :param queue_name: queue name
        :return queue: queue object
        """
        try:
            queue = boto3.resource('sqs').get_queue_by_name(QueueName=queue_name)
            self.write(f'Attained SQS queue by name')
        except ClientError as err:
            self.write(f'Exception - {err}, Unable to get SQS queue', level='error')
        except Exception as err:
            self.write(f'Unable to get SQS queue, due to {err}', level='error') 

        return queue

    def get_message_from_queue(self, queue_name, attempts=3):
        """
        Get message from queue
        :param self:
        :param queue_name: queue name
        :param attempts: number of attempts to get the message
        :return messages: messages list object
        """
        try:
            sqs_client = self.get_sqs_client()
            queue = self.get_sqs_queue(queue_name)
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
        """
        try:
            msg_body = []
            messages = message_object.get('Messages',[])
            if messages:
                for msg in messages:
                    str_body = msg.get('Body')
                    if str_body:
                        dict_body = json.loads(str_body)
                        get_msg = json.loads(dict_body.get('Message'))
                        if get_msg:
                            msg_body.append(get_msg.get('msg'))
            if msg_body:
                self.write(f'Message found - {msg_body}')
        except Exception as err:
            self.write(f'Unable to strip message from message body, due to {err}', level='error')

        return msg_body
