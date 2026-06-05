import sys
import os
#sys.path.append(os.environ["PYTHON_COMMON_HOME"])
#sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append('/mnt/c/Users/riswanm/Desktop/SWIFT4.0/TESTS/python_SonicOS/common_lib/')
sys.path.append('/mnt/c/Users/riswanm/Desktop/SWIFT4.0/PythonRunner')

from utm import Firewall


ip = '10.5.192.85'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-console',console_ip='10.5.3.247',console_port='2014')

from modules.CLI.switchcontroller import Switch
from modules.CLI.switchcontroller import Port

addswitch=Switch(fw)
port=Port(fw)
switch1_detailes={
        'name'  :'TEST1',
        'model' :'sws14-24fpoe',
        'serial' :'2CB8ED4AFE9D',
        'comment': 'test1',
        'ip':'172.16.2.239',
        'user-name': 'admin',
        'password':'password',
        'active-partition' :'1',
        'switch-mode': 'standalone',
        'switch-uplink': '1',
        'switch-management': '1',
        'firewall-uplink': 'X3',
        'stp-enabled':True,
        'stp-mode': 'multiple',
        }
modify_switch1_detailes={
        'name'  :'2CB8ED4AFE9D',
        'comment': 'test11',
        'stp-enabled':False
        }
port_detailes={
        'switch_name':"2CB8ED4AFE9D",
        'port':"6",
        'port-enable':True,
        'stp-enable':True,
        'poe-enable':True,
        'link-speed' :'auto-negotiate',
        'poe-priority' :'low',
        'port-isolation-enable':True,
        'voice-vlan-enable':True,
        'poe-limit-type': 'auto-class',
        'voice-vlan-cos-mode': 'src',
        'bw-ingress': '0',
        'bw-egress': '0',
        'security-count' :'0',
        'portshield': 'X0',
        'portshield-uplink-enable':True,
}

#addswitch.add_switch(**switch1_detailes)
#addswitch.delete_switch('TEST1')
#addswitch.show_switch_detailes()
addswitch.edit_switch(**modify_switch1_detailes)
#print(pp)
#port.configure_port(**port_detailes)
port.get_port_info('5','2CB8ED4AFE9D')
#Switch_models,Serial,IP,Switch_Mode,Swmgmt,Fwuplink=None,Swuplink=None