import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('/'))
print('***************',suite_absolute_path)
script_list= ['mnt','c','modules', 'CLI']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    print(os.chdir(scriptPath))
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../'
        print('+++++',root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

import modules.CLI.Security_services
from utm import Firewall
ip = '10.5.92.23'
port = '22'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')


Security_services1 = modules.CLI.Security_services.SecurityServicesCli(fw)
security_services_dict = {
    'reduce-isdn-antivirus-traffic': False,
    'drop-packets-at-reload': False,
    'synchronize': True,
    'http-clientless-notification-timeout': '110',
    'proxy-server': True,
    'host': '10.10.10.70',
    'port': '18',
    'authentication': True,
    'user-name': 'test1234',
    'password': 'S0nicwall',
    'maximum': True,
    #'performance-optimized': True
    }
security_services_res = Security_services1.config_securityservices_setting(**security_services_dict, tag=1)
print(security_services_res)

anti_spyware = modules.CLI.Security_services.antispywareCli(fw)
antispyware_dict= {
    'enable': True,
    'prevent-all_hd': True,
	'detect-all_hd' : False,
	'log-redundancy_hd':True,
	'prevent-all_md': True,
	'detect-all_md' : False,
	'log-redundancy_md':True,
	'prevent-all_ld': True,
	'detect-all_ld' : False,
	'log-redundancy_ld':True,
	'inbound_inspection_protocols': None,
	'reset': False,
	'exclusion list': True,
	'entry': '1.1.1.1 2.2.2.2',
	'prod_id': 1,
	'ip_excluded_name': None,
	'sig_id': '2',
	'included_ip_all': None ,
	'prevention': True,
	'global_prevenion': True
	
    }
anti_configue = anti_spyware.config_antispyware(**antispyware_dict, tag=1)
logger.info(anti_configue)

cap_atp = modules.CLI.Security_services.CaptureAtpCli(fw)
captureatp_dict= {
    'enable': True,
    'enable_file_type': [None],
	'disable_file_type':[None],
	'file_size': 'default',
	'await-verdict': 'block',
	'range_for-block-until-verdict':'1.1.1.1 2.2.2.2',
	'md5-entry': None,
	'enable_file_type_block':[None],
	'disable_file_type_block':[None]
		
    }
captureatp_config = cap_atp.config_capture_atp(**captureatp_dict, tag=1)
logger(captureatp_config)

ipv = modules.CLI.Security_services.IntrusionPreventionCli(fw)
intrusion_dict= {
    'enable': True,
    'prevent-all_hd': True,
	'detect-all_hd' : False,
	'log-redundancy_hd':True,
	'prevent-all_md': True,
	'detect-all_md' : False,
	'log-redundancy_md':True,
	'prevent-all_ld': True,
	'detect-all_ld' : False,
	'log-redundancy_ld':True,
	'inbound_inspection_protocols': None,
	'reset': False,
	'exclusion list': True,
	'entry': '1.1.1.1 2.2.2.2',
	'prod_id': 1,
	'ip_excluded_name': None,
	'sig_id': '2',
	'included_ip_all': None ,
	'prevention': True,
	'global_prevenion': True
    }
ipv_configue = ipv.IntrusionPreventionCli(**intrusion_dict, tag=1)
logger(ipv_configue)

geo_ip_filter = modules.CLI.Security_services.Geo_Ip(fw)
geo_ip_dict= {
    'alert-text': None,
    'block_connections_all': False
	'block_connections_firewall_rule':True,
	'geo_botnet_lookup': True,
	'include_block_details': True,
	'logging': True,
	'enable': True,
	'custom_list_address_name':None,
	'network_exclude': '172.16.2.0'
		
	

    }
geo_ip_configure = geo_ip_filter.config_Geo_IP(**geo_ip_dict, tag=1)
logger('geo_ip_configure')

botnet_filter = modules.CLI.Security_services.BotnetCli(fw)
botnet_dict= {
    'alert-text': None,
	'block_connections':False
    'block_connections_all': False
	'block_connections_firewall_rule':True,
	'geo_botnet_lookup': True,
	'include_block_details': True,
	'logging': True,
	'custom_list_enable': True,
	'custom_list_address_name':None,
	'flush' :False,
	'periodical-download':True
	'download_interval': '10',
	'protocol': 'FTP'
	'network_exclude': '172.16.2.0'
	
    }
botnet_config = botnet_filter.config_botnet(**botnet_dict, tag=1)
logger(botnet_config)


