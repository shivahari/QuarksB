"""
Skype conf
"""
import random

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
MESSAGE = 'This is a test message - ' + ''.join(random.choices(['s', 'h', 'i', 'v', 'a']))
