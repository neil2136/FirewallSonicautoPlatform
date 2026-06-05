import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print('***************',suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../../'
        print('+++++',root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.clientenforcement import *

ip = '10.5.192.97'
clientenforcement_url = '/api/sonicos/client-enforcement/anti-virus/policy'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)

clientenforcement_settings = ClientEnforcementAPI(fw)

def put_clientenforcement_settings():
    clientenforcement_values = {
        'policing': True,
        'interval': 3,
        'low': True,
        'medium': True,
        'high': True
    }

    put_response=clientenforcement_settings.edit_clientenforcement_setting(**clientenforcement_values)
    print('The put update is ',put_response)

def get_clientenforcement_settings():
    get_clientenforcement_response = clientenforcement_settings.get_clientenforcement_settings(clientenforcement_url)
    print(get_clientenforcement_response)


put_clientenforcement_settings()

#************************************
GAV_settings = GAV(fw)


def put_gav_settings():
    gav_put = {
        'enable_GAV': True

    }
    print('debug1')
    put_response = GAV_settings.config_gav(**gav_put)

    print('debug2')
    print('The put update is ', put_response)


# def get_cfs_enforcement_settings():
#    get_cfs_enforcement_resp = cfs_enforcement_settings.get_cfs_enforcement_settings(cfs_enforcement_url)
#    print(get_cfs_enforcement_resp)


put_gav_settings()

#*********************************
def post_cfs_enforcement_settings():
    enforcement_settings = {
        'grace_period': 1,
        #'enforcement_default': 'none',
        #'enforcement_list_inclusion': 'WAN Interface IPv6 Addresses'
    }
    post_response = cfs_enforcement_settings.configure_cfs_enforcement(**enforcement_settings)
    print('The put update is ', post_response)

def get_cfs_enforcement_settings():
    get_cfs_enforcement_resp = cfs_enforcement_settings.get_cfs_enforcement_settings(cfs_enforcement_url)
    print(get_cfs_enforcement_resp)


post_cfs_enforcement_settings()

from modules.API import securityservices
ipsobj = securityservices.IPSApi(fw)
#rc = ipsobj.get_IPS_global()

# ips_global = {
# #     'intrusion_prevention': {
# #         'enable': True,
# #         'signature_group': {
# #             'high_priority': {
# #                 'prevent_all': True,
# #                 'detect_all': True,
# #                 'log_redundancy': {}
# #             },
# #             'medium_priority': {
# #                 'prevent_all': True,
# #                 'detect_all': True,
# #                 'log_redundancy': {}
# #             },
# #             'low_priority': {
# #                 'prevent_all': True,
# #                 'detect_all': True,
# #                 'log_redundancy': {}
# #             }
# #         }
# #     }
# # }
# # rc = ipsobj.config_IPS_global(**ips_global)

edit_json = {
    "intrusion_prevention": {
        "policy": [{
            "id": 6906,
            "included": {
                "ip": {
                    "category": True
                },
                "users": {
                    "category": True
                }
            },
            "excluded": {
                "ip": {
                    "category": True
                },
                "users": {
                    "category": True
                }
            },
            "schedule": {
                "category": True
            },
            "log_redundancy": {
                "category": True
            },
            "category": "SUSPICIOUS-TRAFFIC",
            "name": "Client Application Attack 15",
            "prevention": {},
            "detection": {
                "category": True
            }
        }]
    }
}
# ipsobj.get_ips_signatures(id = 1116)
ipsobj.config_ips_signatures(id = 6906, **edit_json)
