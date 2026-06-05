import re
import sys
import os
from pprint import pprint
#sys.path.append(os.environ['PYTHON_SONICOS_HOME']+'/common_lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
import modules.CLI.policy
from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')

setting_obj = modules.CLI.policy.Settings(fw)
#out = setting_obj.enable_dpissl_server('disable')  ### 'enable', 'disable'
out = setting_obj.change_dpissl_mode('global')    ### 'policy', 'global'

#policy_obj = modules.CLI.policy.SecurityPolicyCli(fw)
#out = policy_obj.del_all_policies(msg=True)
pprint(out)

