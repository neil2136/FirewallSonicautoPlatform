import sys
import os
from pprint import pprint
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

from utm import Firewall

ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')


from modules.API.captureatp import CaptureAtpApi
catp = CaptureAtpApi(fw)

#out = catp.show_capatp()
#pprint(out)
#out = catp.show_atp_setting()
#pprint(out)

out = catp.show_md5_ex()
pprint(out)

