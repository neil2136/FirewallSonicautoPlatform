import sys
import os
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
from utm import Firewall
from modules.API.highavailability import StatusApi
from modules.API.highavailability import SettingsApi
from modules.API.highavailability import AdvancedApi
from modules.API.highavailability import MonitoringApi
ip = '192.168.168.168'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
ha_status = StatusApi(fw)
ha_settings = SettingsApi(fw)
ha_advanced = AdvancedApi(fw)
ha_monitoring = MonitoringApi(fw)

############################################################################
# Status page #
############################################################################
# output0_0 = ha_status.show_ha_status()
# output0_1 = ha_status.show_ha_settings()
# print('-------------------output:start-------------------')
# print(output0_0)
# print(output0_1)
# print('--------------------output:end--------------------')

############################################################################
# Settings page #
############################################################################
# mode options can be : active_standby, active_active_dpi, active_active_clustering, active_active_clustering_dpi
settings_opt = {
        'mode'              : 'active_standby',
        'control_interface' : 'X6',
        'data_interface'    : 'X4',
        'secondary_serial'  : '18C24100358A',
        'preempt'           : False,
        'virtual_mac'       : False,
        'encryption'        : False,
        'stateful_synchronization': False,
}
# not update
# settings_dict1 = {
#     'mode': 'active_active_clustering',
#     'stateful_synchronization': False,
#     'control_interface': 'X10',
#     'active_active_cluster_link': [{'interface': 'X11', 'link': 1}, {'interface': 'X12', 'link': 2}],
#     'data_interface': 'X13',
#     'dpi_interface': [{'id': 1, 'interface': 'X14'}],
#     'generate_backup_firmware': True,
#     'node_num': 2,
# #    'switched_link': True, # when True, option 'active_active_cluster_link' no need link 2
#     'rank': [{'node': 1, 'rank': 'owner', 'virtual_group': 1},
#              {'node': 1, 'rank': 'standby', 'virtual_group': 2},
#              {'node': 2, 'rank': 'standby', 'virtual_group': 1},
#              {'node': 2, 'rank': 'owner', 'virtual_group': 2}],
#     'serial': [{'node': 1, 'secondary': '000000000007'},
# #               {'node': 2, 'primary': '000000000008'},
#                {'node': 2, 'secondary': '00:00:00:00:00:06'}],
# }

# output1_0 = ha_settings.config_mode_active(**settings_opt)
# #output1_1 = ha_settings.config_mode_active_clustering(**settings_dict1)
# print('-------------------output:start-------------------')
# print(output1_0)
# #print(output1_1)
# print('--------------------output:end--------------------')

############################################################################
# Advanced page #
############################################################################
adv_dict0 = {
    'heartbeat_interval'    : 1000,     # default 1000, min 1000, max 300000.
    'failover_trigger_level': 5,        # default 5, min 4, max 99.
    'probe_interval'        : 20,       # default 20, min 5, max 255
    'probe_count'           : 3,        # default 3, min 3, max 10.
    'election_delay_time'   : 3,        # default 3, min 3, max 255.
    'sdwan_hold_down_time'  : 10,
    'failover_when_aggregate_down': False,
    'include_certificates_keys': True,
    # 'mgmt_heartbeat'      : True,
    # 'route_hold_down_time': 45,

}

# output2_1 = ha_advanced.config_ha_advanced(**adv_dict0)
# output2_2 = ha_advanced.synchronize_settings()
# output2_3 = ha_advanced.synchronize_firmware()
# output2_4 = ha_advanced.force_failover()
# print('-------------------output:start-------------------')
# print(output2_1)
# print(output2_2)
# print(output2_3)
# print(output2_4)
# print('--------------------output:end--------------------')

############################################################################
# Monitoring page #
############################################################################
monitor_opt_v4 = {
    'interface'             : 'X0',
    'version'               : 'ipv4',
    'link_monitoring'       : True,
    'primary'               : '192.168.168.169',
    'secondary'             : '192.168.168.170',
    'allow_management'      : True,
    'logical_probe_enable'  : False,
    'logical_probe_ip'      : '11.11.11.254',
    'override_virtual_mac_enable': False,
    'override_virtual_mac'  : '1A:C2:41:00:2D:99',
}
# monitor_opt_v6 = {
#     'interface'             : 'X0',
#     'version'               : 'ipv4',
#     'link_monitoring'       : True,
#     'primary'               : '192.168.168.169',
#     'secondary'             : '192.168.168.170',
#     'allow_management'      : True,
#     'logical_probe_enable'  : False,
#     'logical_probe_ip'      : '11.11.11.254',
#     'override_virtual_mac_enable': False,
#     'override_virtual_mac'  : '1A:C2:41:00:2D:99',
# }
# output3_0 = ha_monitoring.show_monitoring(**monitor_opt_v4)
# output3_1 = ha_monitoring.config_ha_monitoring(**monitor_opt_v4)
# # output3_2 = ha_monitoring.show_monitoring(**monitor_opt_v6)
# # output3_3 = ha_monitoring.config_ha_monitoring(**monitor_opt_v6)
# print('-------------------output:start-------------------')
# print(output3_0)
# print(output3_1)
# # print(output3_2)
# # print(output3_3)
# print('--------------------output:end--------------------')



