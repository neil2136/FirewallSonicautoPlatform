import modules.CLI.highavailability
from utm import Firewall
ip = '192.168.168.168'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')

ha_status = modules.CLI.highavailability.StatusCli(fw)
ha_settings = modules.CLI.highavailability.SettingsCli(fw)
ha_adv = modules.CLI.highavailability.AdvancedCli(fw)
ha_monitoring = modules.CLI.highavailability.MonitoringCli(fw)

############################################################################
# Status page #
############################################################################
status_dict0 = {
    'version': 'ipv4',
    'interface': 'X0',
}

#output1_0 = ha_status.show_high_availability()
#output1_1 = ha_status.show_high_availability_status()
#output1_2 = ha_status.show_high_availability_monitoring(**status_dict0)
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print(output1_2)
#print('--------------------output:end--------------------')

############################################################################
# Settings page #
############################################################################
# mode options can be : active-standby, active-active-dpi, active-active-clustering, active-active-clustering-dpi
settings_dict0 = {
    'mode': 'active-standby',
    'control-interface': 'X6',
    'secondary-serial': '000000000099',
}

settings_dict1 = {
    'mode': 'active-standby',
#    'primary-serial': '000000000102',
    'generate-backup-firmware': True,
    'preempt': True,
    'virtual-mac': True,
}

settings_dict2 = {
    'mode': 'active-standby',
    'stateful-synchronization': True,
    'data-interface': 'X10',
}

settings_dict3 = {
    'mode': 'active-active-dpi',
    'enable-encryption': True,
    'control-interface': 'X8',
    'data-interface': 'X8',
    'dpi-interface': '1 X10',
}

settings_dict4 = {
    'mode': 'active-active-clustering',
#    'node': [1,2,2],
#    'dut': ['secondary','primary','secondary'],
#    'serial-number': ['000000000001','000000000002','000000000001'],
#    'rank node': [1,1,2,2],
#    'virtual-group': [1,2,1,2],
#    'group-rank': ['owner','standby','standby','owner'],
    'serial node 1 secondary': '000000000001',
    'rank node 1 virtual-group 1': 'owner',
    'rank node 1 virtual-group 2': 'standby',
    'serial node 2 primary': '000000000002',
    'serial node 2 secondary': '000000000003',
    'rank node 2 virtual-group 1': 'standby',
    'rank node 2 virtual-group 2': 'owner',
    'control-interface': 'X3',
    'active-active-cluster-link 1': 'X2',
    'active-active-cluster-link 2': 'X4',
}
#output1_1 = ha_settings.config_settings_mode_active(**settings_dict0)
#output1_2 = ha_settings.config_settings(**settings_dict1)
#output1_3 = ha_settings.enable_stateful_synchronization(**settings_dict2)
#output1_4 = ha_settings.enable_encrypt_contorl_info(**settings_dict3)
#output1_5 = ha_settings.config_settings_mode_active_clustering(**settings_dict4)
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print(output1_2)
#print(output1_3)
#print(output1_4)
#print(output1_5)
#print('--------------------output:end--------------------')

############################################################################
# Advanced page #
############################################################################
adv_dict0 = {
    'heartbeat-interval': '1002',
    'failover-trigger-level': '6',
    'probe interval': '21',
    'probe count': '4',
    'election-delay-time': '5',
    'failover-when-aggregate-down': True,
    'include-certificates-keys': True,
}

#output1_0 = ha_adv.config_advance(**adv_dict0)
#output1_1 = ha_adv.synchronize_settings()
#output1_2 = ha_adv.synchronize_firmware()
#output1_3 = ha_adv.force_failover()
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print(output1_2)
#print(output1_3)
#print('--------------------output:end--------------------')

############################################################################
# Monitoring page #
############################################################################
monitoring_dict0 = {
    'version': 'ipv4',
    'interface': 'X0',
    'allow-management': True,
    'link-monitoring': True,
    'logical-probe': '192.168.168.19',
    'override-virtual-mac': '000000000111',
    'primary': '192.168.168.10',
    'secondary': '192.168.168.11',
}

#output1_0 = ha_monitoring.config_monitoring_interface(**monitoring_dict0)
#output1_1 = ha_adv.force_failover()
#print('-------------------output:start-------------------')
#print(output1_0)
#print(output1_1)
#print('--------------------output:end--------------------')