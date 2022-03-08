"""
 Helper module for AWS CloudWatchLogs messages
"""
from datetime import datetime, timedelta
import os
import sys
import time
import boto3
from botocore.exceptions import ClientError

# add project root to sys path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.base_helper import BaseHelper
from conf import logs_conf as conf

class CloudWatchHelper(BaseHelper):
    """
    CloudWatch Helper object
    """

    def get_client(self):
        """
        Create logs clientlogs
        :param self:
        :return client: cloudwtch logs client
        """
        try:
            client = boto3.client('logs')
            self.write(f'Created logs client')
            return client
        except ClientError as err:
            self.write(f'Unable to create logs client due to {err}', level='error')
        except Exception as err:
            self.write(f'Unable to create logs due to {err}', level='error')

    def get_query_id(self, message):
        """
        Frame a query and schedule it
        :param self:
        :param message: Message triggered from Skype
        :return query_id: Query ID
        """
        query_id = None
        try:
            query = conf.query % (message)
            self.write(f'The query is {query}')
            client = self.get_client()
            start_query_response = client.start_query(logGroupName=conf.log_group,
                                                    startTime=int((datetime.now() - timedelta(minutes=10)).timestamp()),
                                                    endTime=int(datetime.now().timestamp()),
                                                    queryString=query)
            self.write(f'The Query rsponse is {start_query_response}')
            query_id = start_query_response.get('queryId')
            self.write(f'The Query ID is {query_id}')
        except Exception as err:
            self.write(f'Unable to frame query and schedule logs due to {err}', level='error')

        return query_id

    def get_message_from_logs(self, message):
        """
        Retrieves messages from CloudWatch logs
        :param self:
        :return messages_from_log: Messages from cloudwatch log
        """
        self.write('Initiating a 180 sec wait')
        time.sleep(180)
        query_response = None
        message_from_log = None
        query_status_flag = True
        try:
            query_id = self.get_query_id(message)
            client = self.get_client()
            while query_status_flag:
                query_response = client.get_query_results(queryId=query_id)
                if query_response.get('status', None)  == 'Complete':
                    query_status_flag = False
                else:
                    self.write(f'Running cloudwatchlog query')
                    time.sleep(2)
            if query_response:
                self.write(f'Response object from cloudwatch {query_response}')
                message_from_log = self.extract_message(query_response)
                if message_from_log:
                    self.write(f'Fetched {message_from_log} from log')

            return message_from_log
        except Exception as err:
            self.write(f'Unable to get message from logs due to {err}!', level='error')

    def extract_message(self, query_response):
        """
        Extract message from Cloudwatch logs
        :param self:
        :param query_response: query search response from logs
        :return message: Message from the log
        """
        message = None
        try:
            messages = query_response.get('results', [])
            if messages:
                for message in messages:
                    print(message)
                    for fields in message:
                        for key, value in fields.items():
                            if key == '@message':
                                message = value
                                self.write('Extracted {message} from the logs')
            else:
                self.write(f'Unable to fetch message from logs', level='error')

            return message
        except Exception as err:
            self.write(f'Unable to extract  message from logs due to {err}!', level='error')

    def get_test_message(self):
        """
        Get the test Message to be triggred
        :param self:
        :return test_message: Message to be triggered
        """
        test_message = conf.message

        return test_message
