"""
 Test script to:
  - Validate message sent to Skype channel against the message received on SQS
"""
import time
from conf import sqs_conf, skype_conf

def test_message_received_sqs(sqs_instance, skype_instance, concurrent_obj):
    """
    Validate the message triggered from Skype
    """
    try:
        with concurrent_obj.ThreadPoolExecutor() as executor:
            get_client = executor.submit(sqs_instance.get_sqs_client, sqs_conf.config)
            future = executor.submit(sqs_instance.get_message_from_queue, get_client.result(), sqs_conf.SQS_NAME)
            # wait 3 secs before triggering Skype message
            message = skype_conf.MESSAGE
            time.sleep(3)
            trigger_skype_message = skype_instance.post_message_on_skype(message)
            sqs_messages = future.result()

        # validate if message found
        message_flag = False
        for msg in sqs_messages:
            if message in msg:
                message_flag = True
                break
        assert message_flag,f"Could not retrieve the message from the SQS"

    except Exception as err:
        raise(err)
