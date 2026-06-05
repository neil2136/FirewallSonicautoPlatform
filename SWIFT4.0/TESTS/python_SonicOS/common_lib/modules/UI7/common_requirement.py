from modules.UI7.common_require import *
from runner.settings import logger

class CommonRequire:
    def __init__(self):

        self.SANDBOX_USER = "gmsauto@sonicwall.com"
        self.SANDBOX_PASSWORD = "B5MufvGsDLLKIauuXs+WJJXhOWTqaR6hvqn1436lgkhanl6HDW0QhXtU7Ds0OyjEL/4oDvNRP8jxO7h7ilhxE80" \
                           "Ls8QQZoX6Ru7dwi1/hUCAoViOCwKUa0mxkh/6p/QDoTODUIzkx3+gKJK1hlxCdISEdy/gSHvvOh1Iaze/hMw="
        self.MSW_API_SERVER = '10.5.50.120'
        self.MSW_USER = "testaccount"
        self.MSW_USER_ENCRYPT_PASSWORD = "B5MufvGsDLLKIauuXs+WJJXhOWTqaR6hvqn1436lgkhanl6HDW0QhXtU7Ds0OyjEL/4oDvNRP8jxO7h7ilhxE80" \
                                    "Ls8QQZoX6Ru7dwi1/hUCAoViOCwKUa0mxkh/6p/QDoTODUIzkx3+gKJK1hlxCdISEdy/gSHvvOh1Iaze/hMw="
        self.initialize_variables()

    def initialize_variables(self):

        global testbed_id, MODEL_LEVEL
#        if openstack == '1':
#            data = use_openstack_testbed()
#            testbed_id = data['TESTBED_ID']
#        else:
#            data = use_static_testbed(testbed_id)
#        self.FW_USERNAME   = data['FW_USERNAME']
#        self.URL           = data['FW_IP']
#        self.URL           = "https://" + self.URL
#        self.FW_SERIAL_NO  = data['FW_SERIAL_NO']
#        self.FW_AUTH_CODE  = data['FW_AUTH_CODE']
#        self.FW_REG_CODE   = data['FW_REG_CODE']
#        self.MODEL         = data['FW_MODEL']
#        self.FW_IP         = data['FW_IP']
#        self.FW_PASSWORD   = data['FW_PASSWORD']

        self.FW_USERNAME   = "admin"
        self.FW_IP         = "192.168.168.168"
        self.FW_PASSWORD   = "password"
        self.URL           = "https://" + self.FW_IP
        #self.URL           = "10.6.0.90"
        #self.FW_SERIAL_NO  = "C0EAE4599FAC"
        #self.FW_AUTH_CODE  = "GVBV-93HB"
        #self.FW_REG_CODE   = "B4JPPQ3Q"
        #self.MODEL         = "NSA6600"