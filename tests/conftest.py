"""
pytest configuration file
"""
import concurrent.futures
import os
import sys
import pytest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.sqs_helper import SqsHelper
from helpers.skype_helper import SkypeHelper

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
