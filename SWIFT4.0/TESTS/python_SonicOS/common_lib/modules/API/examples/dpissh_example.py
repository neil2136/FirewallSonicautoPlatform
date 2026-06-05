
from utm import Firewall
from modules.API.dpissh import DpiSSHApi

firewall = Firewall('192.168.168.168',
    user='admin',
    password='password',
    supported_config_mode='api')

dpissh_object = DpiSSHApi(firewall)

dpissh_data = {
    'enable': True,
    'application_firewall': True,
    'intrusion_prevention': True,
    'gateway_anti_virus': True,
    'gateway_anti_spyware': True,
    'include_address': 'Default\ Gateway',
    'include_address_type': 'name'
}

retval = dpissh_object.config_general_settings(**dpissh_data)
print(retval)

