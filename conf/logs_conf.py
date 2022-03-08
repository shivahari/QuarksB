"""
Logs conf
"""
import os
import time

log_group = "/aws/lambda/staging-newsletter-url-filter"
timestr = time.strftime("%Y%m%d-%H%M%S")
message = 'This is a test message - ' + timestr
skype_channel = os.environ.get('CHANNEL_ID')
query="fields @timestamp, @message | sort @timestamp desc | limit 10 |filter strcontains(@message, '%s')"
