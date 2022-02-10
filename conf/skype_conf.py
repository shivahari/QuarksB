"""
Skype conf
"""
import time

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
MESSAGE = 'This is a test message - ' + ''.join(time.time().__str__().split('.'))
