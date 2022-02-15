"""
Queue conf
"""
from botocore.config import Config

SQS_NAME = "staging-newsletter-generator"
config = Config(
   retries = {
      'max_attempts': 10,
      'mode': 'standard'
   }
)
