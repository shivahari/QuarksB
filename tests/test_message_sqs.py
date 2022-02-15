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
            future = executor.submit(sqs_instance.get_message_from_queue, sqs_conf.SQS_NAME, sqs_conf.config)
            # wait 3 secs before triggering Skype message
            sent_message = skype_conf.MESSAGE
            skype_url = skype_conf.SKYPE_SENDER_ENDPOINT
            time.sleep(3)
            trigger_skype_message = skype_instance.post_message_on_skype(sent_message, skype_url)
            sqs_messages = future.result()

        # validate if message found
        message_found = False
        for received_message in sqs_messages:
            if sent_message == received_message:
                message_found = True
                break
        assert message_found, "Did not receive the test message"

    except Exception as err:
        raise(err)
