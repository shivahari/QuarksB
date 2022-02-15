"""
Skype conf
"""
import time

SKYPE_SENDER_ENDPOINT = "https://skype-sender.qxf2.com/send-message"
timestr = time.strftime("%Y%m%d-%H%M%S")
MESSAGE = 'This is a test message - ' + timestr