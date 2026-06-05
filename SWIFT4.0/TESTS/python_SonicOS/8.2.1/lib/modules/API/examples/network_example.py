import sys
import os
#sys.path.append(os.environ["SONICOS_HOME"]+'/6.5.4/python_lib')
sys.path.append('/home/python_lib')
from utm import Firewall
from modules.API.network import WebproxyApi

ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

webproxy = WebproxyApi(fw)
webproxy_dict = {
    'server':'1.1.1.1',
    'port':'3128',
    'bypass_upon_failure': True,
    'forward_public_requests':True,
}
rc = webproxy.config_webproxy(**webproxy_dict)
if rc:
    print('Config webproxy success')
else:
    print('Config weproxy fail')

webproxy_dict_fail = {
    'server':'1.1.1.1',
    'port':'-1',
    'bypass_upon_failure':True,
    'forward_public_requests':True,
}
rc = webproxy.config_webproxy(**webproxy_dict_fail, msg=True)
if rc[0]:
    print('Config webproxy success')
else:
    print('Config webproxy fail, fail code:')
    print(rc[1]['status']['info'][0]['message'])

# rc = webproxy.edit_bypass_upon_failure(True)
# rc = webproxy.edit_bypass_upon_failure(False)
# rc = webproxy.edit_forward_public_requests(True)
# rc = webproxy.edit_forward_public_requests(False)
rc = webproxy.add_user_proxy_server('1.1.1.1','2.2.2.2')
rc = webproxy.del_user_proxy_server('1.1.1.1','2.2.2.2')
output = webproxy.show_webproxy()
print('44444444')
print(output)



'''
from modules.API.network import InterfaceIPv4Api
x2 = InterfaceIPv4Api(fw)
x2_static_opt = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'static',
    'ip': '2.34.5.6',
    'netmask': '255.255.255.0',
    'gateway': '2.34.5.1',
    'mgmt_http': False,
    # 'mac_ovesrride': '345678901222'
}
x2_dhcp_opt = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'dhcp',
}
# rc = x2.config_interface(**x2_static_opt)
# rc = x2.config_interface(**x2_dhcp_opt)
x2_pppoe_opt_dynamic = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': True,
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}
x2_pppoe_opt_unnumber = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': False,
    'pppoe_unnumbered': 'X4',
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}
x2_pppoe_opt_ip = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pppoe',
    'pppoe_user': '',
    'pppoe_passwd': '',
    'pppoe_service': '',
    'pppoe_schedule': 'always_on',
    'pppoe_dynamic': False,
    'pppoe_ip': '1.2.3.4',
    'pppoe_inactivity': 0,
    'pppoe_lcp_echo_packets': False,
    'pppoe_reconnect': 0,    
}

# rc = x2.config_interface(**x2_pppoe_opt_dynamic)
# rc = x2.config_interface(**x2_pppoe_opt_unnumber)
# rc = x2.config_interface(**x2_pppoe_opt_ip)

x2_pptp_opt_static = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_user': 'pptp_test',
    'pptp_passwd': 'password',
    'pptp_server': '10.10.10.10',
    'pptp_schedule': 'always_on',
    'pptp_dynamic': False,
    'pptp_ip': '1.2.3.4',
    'pptp_netmask': '255.255.255.0',
    'pptp_gateway': '1.2.3.40',
    'pptp_inactivity': 0,
}
x2_pptp_opt_dyn = {
    'if': 'x2',
    'zone': 'WAN',
    'mode': 'pptp',
    'pptp_user': 'pptp_test',
    'pptp_passwd': 'password',
    'pptp_server': '10.10.10.10',
    'pptp_schedule': 'always_on',
    'pptp_dynamic': True,
    'pptp_inactivity': 0,
}
# rc = x2.config_interface(**x2_pptp_opt_static)
# rc = x2.config_interface(**x2_pptp_opt_dyn)

x2_l2bridge = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'l2bridge',
    'bridge_to': 'x4',
    'vlan_filtering_mode': 'allow',
    'filtered_vlan' : '6 7',
}
# rc = x2.config_interface(**x2_l2bridge)

x2_lan_static = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'static',
    'ip': '11.11.11.11',
    'netmask': '255.255.255.0',
    'gateway' : '11.11.11.12',
}
#rc = x2.config_interface(**x2_lan_static)
x2_lan_unnumber = {
    'if': 'x2',
    'zone': 'DMZ',
    'mode': 'unnumbered',
    'ip': '11.11.11.11',
    'netmask': '255.255.255.0',
    'gateway' : '11.11.11.12',
}
rc = x2.config_interface(**x2_lan_unnumber)
rc = x2.unassign_interface(**x2_lan_unnumber)
'''

