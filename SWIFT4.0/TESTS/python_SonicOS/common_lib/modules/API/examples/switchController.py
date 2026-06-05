import sys
sys.path.append('/DEV_TESTS/python_SonicOS/7.0.0/lib/modules/API/')
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

from switchcontroller import *
from utm import Firewall


import os

#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')





ip = '10.5.194.103'

fw = Firewall(ip, user='admin', password='password',
              supported_config_mode='api')

testSwtichController = Switch(fw)

switch_data={
                "id": "2CB8ED4AF4BD",
                "name": "2CB8ED4AF4BD",
                "model": "sws14-48fpoe",
                "serial": "2CB8ED4AF4BD",
                "comment": "SonicWALL SWS12-8POE",
                "ip": "193.114.3.199",
                "switch_mode": "standalone",
                "switch_uplink": 1,
                "switch_management": 1,
                "firewall_uplink": "X4"
            }
voice_vlan={
                        "switch": "2CB8ED4AF4BD",
                        "state": "disabled",
                        "vlan": 2,
                        "priority_tag": 7,
                        "dscp": 50
                    }
#-----------------switch------------------------ ------------      
def test_get_switch():
    output=testSwtichController.get_switch()
    print(output)

def test_add_switch():
    output=testSwtichController.add_switch(**switch_data)
    print("add here")
    print(output)

def test_delete_switch():
    output=testSwtichController.delete_switch("2CB8ED4AF4BA")
    print("delete here")
    print(output)
def test_upgrade_switch():
    output=testSwtichController.firmware_upgrade_cloud("2CB8ED4AFE9D",1,"1.0.0.1-4")
    print("upgrade here")
    print(output)
def test_restart_switch():
    output=testSwtichController.restart("2CB8ED4AFE9D")
    print("restart here")
    print(output)
def test_authorize_switch():
    output=testSwtichController.authorize("2CB8ED4AFE9D")
    print("authorize here")
    print(output)
#-----------------------------Port--------------------------
def test_get_port():
    output=testSwtichController.get_port()
    print("get port daata")
    print(output)
def test_get_by_nmae_port():
    output=testSwtichController.get_port()
    print("get port daata")
    print(output)
def test_configure_port():
    output=testSwtichController.get_port()
    print("get port daata")
    print(output)
def test_configure_by_name_port():
    output=testSwtichController.get_port()
    print("get port daata")
    print(output)


#---------------------------voicevlan-------------------------

def test_voice_vlan():
    output=

if __name__ == "__main__":
    #test_get_switch()
    #test_add_switch()
    #test_delete_switch()
    #test_get_switch()
    #test_upgrade_switch()
    test_voice_vlan()