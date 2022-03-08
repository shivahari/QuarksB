"""
AWS CloudWatchLogs conf
"""
cloudwatch_log_group = '/aws/lambda/staging-newsletter-url-filter'
cloudwatch_query = "fields @timestamp, @message | filter @message like 'Test message sent on '"