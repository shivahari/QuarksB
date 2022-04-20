"""
Helper module for Skype
"""
import os
import sys
import requests
from .base_helper import BaseHelper

class SkypeHelper(BaseHelper):
    """
    Skype Helper object
    """
    def post_message_on_skype(self, skype_message, skype_url):
        "Posts a predefined message on the set Skype channel"
        try:
            headers = {'Content-Type': 'application/json'}
            payload = {"msg" : skype_message,
                      "channel": os.environ['CHANNEL_ID'],
                      "API_KEY": os.environ['API_KEY']}

            response = requests.post(url=skype_url,
                                     json=payload, headers=headers)
            if response.status_code == 200:
                self.write(f'Successfully sent the Skype message - {skype_message}')
            else:
                self.write(f'Failed to send Skype message', level='error')
        except Exception as err:
            raise Exception(f'Unable to post message to Skype channel, due to {err}')
        return response, skype_message
