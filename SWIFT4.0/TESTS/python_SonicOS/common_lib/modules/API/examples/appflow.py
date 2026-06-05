import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + "../../"
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.appflowsettings import GmsflowreportingApi
from modules.API.appflowsettings import ExternalcollectorApi  
from modules.API.appflowsettings import AppflowserverApi 
from modules.API.appflowsettings import AppflowsettingsApi

ip = '10.5.92.56'   # Device IP address

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
##########Object CTA Report ################
generate_cta_report = CTAApi(fw)
#########value for appflow########################
edit_appflow_settings= AppflowsettingsApi(fw)
############ Enabling the Flow Server ###################
def urilistobject():
    app = {
            'connections': 'interface-based',
            'dropped': False,
            'stack': True,
            'ipv6_flows': False,
            'upload_timeout': 60,
            'real_time':{
                'data_collection': True
            },
            'aggregate': {
                'data_collection': True
            },
            'top_applications': True,
            'bits_per_second': True,
            'packets_per_second': False,
            'average_packet_size': False,
            'connections_per_second': True,
            'core_utilization': False,
            'memory_utilization': True,
            'aggregate_data_collection': True,
            'applications': True,
            'user': True,
            'ip': False,
            'threat': True,
            'geo_ip': True,
            'url': False,
            'local_collector': True,
            'gifs': True,
            'jpegs': True,
            'pngs': True,
            'js': False,
            'xmls': False,
            'jsons': False,
            'css': True,
            'htmls': True,
            'aspx': False,
            'cms': False,
            'geo_ip_resolution': False

    }
    response = edit_appflow_settings.config_appflow_setting(**app)
    print(response)
    if response:
        print('Modifying appflow settings success')
    else:
        print('Error in Modifying appflow settings')

urilistobject()######## enabling/disabling of appflow reporting ###################

enable_gmsflow_server= GmsflowreportingApi(fw)
disable_gmsflow_server=GmsflowreportingApi(fw)

############ Enabling the Flow Server ###################

def enable_flow_server():
    gmsflow = {
        'flows': True,
        'real_time': True,
         'open': True,
         'close': True,
         'threat': True,
         'application': True,
         'update_user': True,
         'vpn_tunnel': True,
         'update_url': True,
         "connections": True,
         "dynamic_users": True,
         "dynamic_urls": True,
         "url_ratings": True,
         "vpns": True,
         "devices": True,
         "spams": True,
         "locations": True,
         "voips": True,
         "ip": "1.1.1.0",
         "vpn_source_ip": "2.2.2.2",
         "communication_timeout": 90,
         "auto_synchronize": True

    }

    rc = enable_gmsflow_server.config_gmsflow_reporting(**gmsflow)
    if rc:
            print('GMS FLOW SERVER Enabled ')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')
enable_flow_server()

############### Disabling the Flow Server ####################

def disable_flow_server():
    gmsflow = {
        'flows': False,
        'real_time': False,
         'open': False,
         'close': False,
         'threat': False,
         'application': False,
         'update_user': False,
         'vpn_tunnel': False,
         'update_url': False,
         "connections": False,
         "dynamic_users": False,
         "dynamic_urls": False,
         "url_ratings": False,
         "vpns": False,
         "devices": False,
         "spams": False,
         "locations": False,
         "voips": False,
         "ip": "1.1.1.0",
         "vpn_source_ip": "2.2.2.2",
         "communication_timeout": 100,
         "auto_synchronize": False

    }

    rc = disable_gmsflow_server.config_gmsflow_reporting(**gmsflow)
    if rc:
            print('GMS FLOW SERVER Disabled')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')
disable_flow_server()

####################################################################################################3

####### enabling/disabling of appflow reporting ###################

enable_appflow_server1 = AppflowserverApi(fw)
disable_appflow_server1 = AppflowserverApi(fw)
#enable_appflow_server.config_appflow_server()
############ Enabling the Flow Server ###################

def enable_appflow_server():
    appflow = {
        'flows': True,
        'real_time': True,
         'open': True,
         'close': True,
         'threat': True,
         'application': True,
         'update_user': True,
         'vpn_tunnel': True,
         'update_url': True,
         "connections": True,
         "dynamic_users": True,
         "dynamic_urls": True,
         "url_ratings": True,
         "vpns": True,
         "devices": True,
         "spams": True,
         "locations": True,
         "voips": True,
         "keep_alive": True,
         "ip": "1.1.1.0",
         "vpn_source_ip": "2.2.2.2",
         "max_flows": 100000,
         "communication_timeout": 90,
         "firewall_name": "Sonicwall_Appflow",
         "passphrase": "sonicwall",
         "auto_synchronize": True

    }


    rc = enable_appflow_server1.config_appflow_server(**appflow)

    if rc:
            print('APP FLOW SERVER Enabled ')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')


enable_appflow_server()

############### Disabling the Flow Server ####################

def disable_appflow_server():
    appflow = {
        'flows': False,
        'real_time': False,
         'open': False,
         'close': False,
         'threat': False,
         'application': False,
         'update_user': False,
         'vpn_tunnel': False,
         'update_url': False,
         "connections": False,
         "dynamic_users": False,
         "dynamic_urls": False,
         "url_ratings": False,
         "vpns": False,
         "devices": False,
         "spams": False,
         "locations": False,
         "voips": False,
         "keep_alive": True,
         "ip": "1.1.1.0",
         "vpn_source_ip": "2.2.2.2",
         "max_flows": 100000,
         "communication_timeout": 90,
         "firewall_name": "Sonicwall_Appflow",
         "passphrase": "sonicwall",
         "auto_synchronize": False

    }

    rc = disable_appflow_server1.config_appflow_server(**appflow)
    if rc:
            print('APP FLOW SERVER Disabled')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')


disable_appflow_server()

#################################################################################################################


######## enabling/disabling of appflow reporting ###################

enable_external_collector1 = ExternalcollectorApi(fw)
disable_external_collector1 = ExternalcollectorApi(fw)
#enable_appflow_server.config_appflow_server()
############ Enabling the Flow Server ###################

def enable_external_collector():
    external_collector = {
        'flows': True,
        'reporting_format': 'ipfix',
        'ip': '1.1.1.0',
        'vpn_source_ip': '2.2.2.2',
        'port': 200,
 ##report option #####
        'open': True,
         'close': True,
        'active_timeout': 100,
      #   'kilobytes': 100,
       #  'once':True,
 ### update option ########
         'threat': True,
         'application': True,
         'user': True,
         'vpn_tunnel': True,
         'url': True,
####dynamic flow ###############
         "connections": True,
         "users": True,
         "urls": True,
         "url_ratings": True,
         "vpns": True,
         "devices": True,
         "spams": True,
         "locations": True,
         "voips": True,
#########Send templates##################

        "templates": True,
        "static_flows": True,

###########static flows ##########
        "applications": True,
        "viruses": True,
        "spyware": True,
        "intrusions": True,
        "location_map": True,
        "services": True,
        "rating_map": True,
        "table_map": True,
        "column_map": True,
#########ipfix reports#########
        "top_10_apps": True,
        "interface_statistics": True,
        "core_utilization": True,
        "memory_utilization": True


    }


    rc = enable_external_collector1.config_external_collector(**external_collector)

    if rc:
            print('APP FLOW SERVER Enabled ')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')


enable_external_collector()

############### Disabling the Flow Server ####################

def disable_external_collector():
    external_collector = {
        'flows': False,
        'reporting_format': 'ipfix',
        'ip': '1.1.1.1',
        'vpn_source_ip': '2.1.1.2',
        'port': 300,
        ##report option #####
        'open': False,
        'close': False,
        #'active_timeout': 0,
        'kilobytes': 10,
        'once': False,
        ### update option ########
        'threat': False,
        'application': False,
        'user': False,
        'vpn_tunnel': False,
        'url': False,
        ####dynamic flow ###############
        "connections": False,
        "users": False,
        "urls": False,
        "url_ratings": False,
        "vpns": False,
        "devices": False,
        "spams": False,
        "locations": False,
        "voips": False,
        #########Send templates##################

        "templates": False,
        "static_flows": False,

        ###########static flows ##########
        "applications": False,
        "viruses": False,
        "spyware": False,
        "intrusions": False,
        "location_map": False,
        "services": False,
        "rating_map": False,
        "table_map": False,
        "column_map": False,
        #########ipfix reports#########
        "top_10_apps": False,
        "interface_statistics": False,
        "core_utilization": False,
        "memory_utilization": False

    }

    rc = disable_external_collector1.config_external_collector(**external_collector)
    if rc:
            print('APP FLOW SERVER Disabled')
    else:
            print('#####Error while configuring GMS FLOW SERVER##################')


disable_external_collector()


