import sys
import os
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall
from modules.API.switching import VlanTrunkApi
ip = '192.168.168.168'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

vlan_obj=VlanTrunkApi(fw)
vlan_ports={
    'port': 'X10',
    'vlan_id': [103, 101],
}
# vlan_obj.add_trunk_ports(**vlan_ports)
# vlan_obj.edit_trunk_ports(**vlan_ports)
vlan_obj.delete_vlan_trunk(**vlan_ports)
rc=vlan_obj.show_vlan_trunk()

print(rc)