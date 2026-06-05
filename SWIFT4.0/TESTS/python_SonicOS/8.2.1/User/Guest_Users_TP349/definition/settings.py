from inspect import Parameter
import sys
import os
import copy

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + 'User/Guest_Users_TP349')

import re
import paramunittest
from nose_parameterized import parameterized

from runner.settings import logger, Params
from runner.unittest.setup import Test
from runner.utils.assertion import Assertion
from utm import Firewall
from util.enhancedinfo import show_testcase_info
from modules.API import system
from modules.API.users import UserGuestApi

fw = Firewall('192.168.168.168', user='admin', password='sonicauto', supported_config_mode='api')
guest_user = UserGuestApi(fw)
diag_obj = system.DiagnosticApi(fw)
# define path
TESTPLAN = os.environ["PYTHON_SONICOS_HOME"]+'/User/Guest_Users_TP349/testplan/Guest_Users_TP349.json'

add_guestuser_account = {
          'action': 'add',
          'accountname': 'guest123',
          'password': "password",
          'activate_on_login': True,
          'enable_guest_service_privilege': True,
          'login_uniqueness': False,
          'account_lifetime': False,
          'acco_lifetime': 3,
          'acco_lifetype': 'days',
          'prune_on_expiry': True
          
          }
