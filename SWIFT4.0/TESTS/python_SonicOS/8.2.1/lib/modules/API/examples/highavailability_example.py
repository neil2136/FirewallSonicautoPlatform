import sys
import os
sys.path.append('/DEV_TESTS/SonicOS/6.5.4/python_lib')
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
#output0_0 = ha_status.show_ha_status()
#output0_1 = ha_status.show_ha_settings()
#print('-------------------output:start-------------------')
#print(output0_0)
#print(output0_1)
#print('--------------------output:end--------------------')

############################################################################
# Settings page #
############################################################################
# mode options can be : active_standby, active_active_dpi, active_active_clustering, active_active_clustering_dpi
settings_dict0 = {
    'mode': 'active_standby',
    'control_interface': 'X6',
    'secondary_serial': '000000000097',
    'data_interface': 'X8',
    'dpi_interface': [{'id': 1, 'interface': 'X5'}],
    'generate_backup_firmware': True,
    'preempt': True,
    'virtual_mac': True,
    'stateful_synchronization': True,
}

settings_dict1 = {
    'mode': 'active_active_clustering',
    'stateful_synchronization': False,
    'control_interface': 'X10',
    'active_active_cluster_link': [{'interface': 'X11', 'link': 1}, {'interface': 'X12', 'link': 2}],
    'data_interface': 'X13',
    'dpi_interface': [{'id': 1, 'interface': 'X14'}],
    'generate_backup_firmware': True,
    'node_num': 2,
#    'switched_link': True, # when True, option 'active_active_cluster_link' no need link 2
    'rank': [{'node': 1, 'rank': 'owner', 'virtual_group': 1},
             {'node': 1, 'rank': 'standby', 'virtual_group': 2},
             {'node': 2, 'rank': 'standby', 'virtual_group': 1},
             {'node': 2, 'rank': 'owner', 'virtual_group': 2}],
    'serial': [{'node': 1, 'secondary': '000000000007'},
#               {'node': 2, 'primary': '000000000008'},
               {'node': 2, 'secondary': '00:00:00:00:00:06'}],
}

#output1_0 = ha_settings.config_mode_active(**settings_dict0)
#output1_1 = ha_settings.config_mode_active_clustering(**settings_dict1)
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print('--------------------output:end--------------------')

############################################################################
# Advanced page #
############################################################################
adv_dict0 = {
    'heartbeat_interval': 1002,
    'failover_trigger_level': 6,
    'probe interval': 21,
    'probe count': 4,
    'election_delay_time': 5,
    'failover_when_aggregate_down': True,
    'include_certificates_keys': True,
}

#output2_1 = ha_advanced.config_ha_advanced(**adv_dict0)
#print('-------------------output:start-------------------')
#print(output2_1)
#print('--------------------output:end--------------------')

############################################################################
# Monitoring page #
############################################################################
monitoring_dict0 = {
    'interface': 'X0',
}

monitoring_dict1 = {
    'version': 'ipv4',
    'interface': 'X1',
    'interface_info': {
        'ipv4': {
            'allow_management': True,
            'link_monitoring': True,
            'logical_probe': '172.17.1.99',
            'override_virtual_mac': '00:00:00:00:01:15',
            'primary': '172.17.1.98',
            'secondary': '172.17.1.97',
        }
#        'ipv6': {
#            'allow_management': True,
#            'logical_probe': '2001:1200::155',
#            'primary': '2001:1200::156',
#            'secondary': '2001:1200::157',
#        }
    }
}

#output3_0 = ha_monitoring.show_monitoring(**monitoring_dict0)
#output3_1 = ha_monitoring.config_ha_monitoring(**monitoring_dict1)
#print('-------------------output:start-------------------')
#print(output3_0)
#print(output3_1)
#print('--------------------output:end--------------------')



