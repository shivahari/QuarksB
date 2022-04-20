"""
pytest configuration file
"""
import concurrent.futures
import os
import sys
import pytest
from ..helpers.cloudwatch_helper import CloudWatchHelper
from ..helpers.sqs_helper import SqsHelper
from ..helpers.skype_helper import SkypeHelper

@pytest.fixture
def sqs_instance(request):
    "pytest fixture for SQS module"

    return SqsHelper()

@pytest.fixture
def skype_instance(request):
    "pytest fixture for Skype module"
    return SkypeHelper()

@pytest.fixture
def concurrent_obj(request):
    "pytest fixture for Skype module"

    return concurrent.futures

@pytest.fixture
def cloudwatch_instance(request):
    "pytest fixture for Cloudwatch module"

    return CloudWatchHelper()
