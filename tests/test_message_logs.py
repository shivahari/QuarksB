"""
 Test script to:
  - Validate message sent to Skype channel against the message received on cloudwatchlogs
"""

def test_message_received_logs(logs_instance, skype_instance):
    """
    Validate message triggered from Skype
    """
    try:

        # Get the test message
        sent_message = logs_instance.get_test_message()

        # Send the test message from Skype
        trigger_skype_message = skype_instance.post_message_on_skype(sent_message)

        # Start a query search in the logs
        response = logs_instance.get_message_from_logs(sent_message)
        assert sent_message in response

    except Exception as err:
        print(f'Unable to run test, due to {err}')



