import sys
import os
#sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
#sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append('/DEV_TESTS/python_SonicOS/6.5.4/lib')
sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')

import modules.CLI.sdwan
from utm import Firewall
ip = '192.168.168.168'
port = '22'
fw = Firewall(ip,user='admin',password='password',supported_config_mode='cli-ssh')


appflowsetting1 = modules.CLI.appflowsetting.appflowsettingCli(fw)

show_appflow={
			'commands': 'appflow'
	}
	output_show=appflowsetting1.show_appflow_setting(**show_appflow,tag=1)
appflowsetting_dict= {

            'connections': 'interface-based',
            'dropped': False,
            'stack': False,
            'ipv6-flows': False,
            'upload-timeout': '80',
            'data-collection-realtime': False,
            'top-applications': False,
            'bits-per-second': True,
            'packets-per-second': False,
            'average-packet-size': True,
            'connections-per-second': True,
            'core-utilization': False,
            'memory-utilization': True,
            'data-collection-aggregate': True,
            'applications': True,
            'user': False,
            'ip': True,
            'threat': True,
            'geo-ip': False,
            'url': False,
            'local-collector': True,
            'gifs': True,
            'jpegs': True,
            'pngs': False,
            'js': False,
            'xmls': True,
            'jsons': True,
            'css': False,
            'htmls': True,
            'aspx': False,
            'cms': False,
            'geo-ip-resolution': False

    }
appflow_res = appflowsetting1.config_appflow_setting(**appflowsetting_dict, tag=1)
print(appflow_res)



gmsflowserver1 = modules.CLI.appflowsetting.gmsflowserverCli(fw)

show_gmsflow={
			'commands': 'gmsflow-server'
	}
	output_show=gmsflowserver1.show_gmsflow_server(**show_gmsflow,tag=1)
gmsflow_dict= {
    'flows': True,
    'real-time': False,
    'open': True,
    'close': False,
    'threat': True,
     'application': False,
     'user': False,
     'vpn-tunnel': True,
     'url': True,
     "connections": False,
     "users": False,
     "urls": True,
     "url-ratings": False,
     "vpns": True,
     "devices": True,
     "spams": True,
     "locations": True,
     "voips": False,
     "ip": '1.1.1.1',
     "vpn-source-ip": '2.2.2.3',
     "communication-timeout": '100',
     "auto-synchronize":  False
}
gmsflow_res = gmsflowserver1.config_gmsflow_server(**gmsflow_dict, tag=1)
print(gmsflow_res)

appflowserver1 = modules.CLI.appflowsetting.appflowserverCli(fw)

show_appflow={
			'commands': 'appflow-server'
	}
	output_show=appflowserver1.show_appflow_server(**show_appflow_ser,tag=1)

appflowserver_dict= {
    'flows': True,
    'real-time': True,
    'open': True,
    'close': False,
    'threat': True,
     'application': False,
     'user': False,
     'vpn-tunnel': True,
     'url': True,
     "connections": False,
     "users": False,
     "urls": True,
     "url-ratings": False,
     "vpns": True,
     "devices": False,
     "spams": True,
     "locations": True,
     "voips": False,
     "ip": '1.1.6.1',
     "vpn-source-ip": '2.2.1.3',
    'max-flows': '120000',
     "communication-timeout": '90',
     'firewall-name': 'Sonicwall',
    'passphrase':'sonicwall123',
     "auto-synchronize": True
}
appflow_ser_res = appflowserver1.config_appflow_server(**appflowserver_dict, tag=1)
print(appflow_ser_res)

externalcollector1 = modules.CLI.appflowsetting.externalcollectorCli(fw)

show_ext_collec={
			'commands': 'external-collector'
	}
	output_show=externalcollector1.show_external_collector(**show_ext_collec,tag=1)

external_collector_dict= {
        'flows': True,
        'ip': '1.1.1.1',
        'vpn-source-ip': '2.2.2.5',
        'port': '100',
        'reporting-format': 'ipfix-with-extensions',
 ##report option #####
        'open': True,
         'close': False,
        #'active-timeout': '0',
         'kilobytes': '100',
         'once':True,
 ### update option ########
         'threat': False,
         'application': False,
         'user': True,
         'vpn-tunnel': False,
         'url': True,
####dynamic flow ###############
         "connections": True,
         "users": True,
         "urls": True,
         "url-ratings": True,
         "vpns": True,
         "devices": True,
         "spams": True,
         "locations": True,
         "voips": True,
#########Send templates##################

        "templates": True,
        "static-flows": True,

###########static flows ##########
        "applications": True,
        "viruses": True,
        "spyware": True,
        "intrusions": True,
        "location-map": True,
        "services": True,
        "rating-map": True,
        "table-map": True,
        "column-map": True,
#########ipfix reports#########
        "top-10-apps": True,
        "interface-statistics": True,
        "core-utilization": True,
        "memory-utilization": True

}
exter_collec_res = externalcollector1.config_external_collector(**external_collector_dict, tag=1)
print(exter_collec_res)