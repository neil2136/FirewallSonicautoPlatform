import os
import sys
import re
import requests

print("For Simulate HTTP access...")
response = requests.get('http://www.baidu.com')
print(response)
print(f'response code is {response.status_code}')
