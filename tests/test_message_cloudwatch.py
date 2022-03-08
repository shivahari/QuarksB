"""
 Test script to:
  - Validate message sent to Skype channel against the message processed by Lambda, in the Lambda's CloudWatchLogs
"""
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conf import skype_conf, cloudwatch_conf

def test_message_received_lambda(cloudwatch_instance, skype_instance):
    """
    Validate the message sent from Skype is received by Lambda
    """
    try:
        message_found = False
        skype_response, sent_message = skype_instance.post_message_on_skype(\
                                       skype_conf.MESSAGE, skype_conf.SKYPE_SENDER_ENDPOINT)
        assert skype_response.status_code == 200, 'Test message not delivered to Skype'
        time.sleep(120)
        messages_from_log = cloudwatch_instance.get_message_from_logs(\
                            cloudwatch_conf.cloudwatch_log_group, cloudwatch_conf.cloudwatch_query)
        # CloudWatch Logs API response would be dict, in the format [[{'field':'', 'value':''},{}]]
        for message in messages_from_log:
            for fields in message:
                for key, value in fields.items():
                    if key == 'value' and sent_message.strip() == value.split(',')[0].strip():
                        message_found = True
                        break
        assert message_found, 'Test message not found in CloudWatch logs'
    except Exception as error:
        raise(error)
