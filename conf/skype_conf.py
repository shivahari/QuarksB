"""
Skype conf
"""
from datetime import datetime

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
MESSAGE = 'Test message sent on ' + datetime.now().strftime('%d-%m-%Y %H:%M:%S')
