import modules.CLI.dpissh
from utm import Firewall



fw = Firewall(ip = '192.168.168.168',
    user = 'admin',
    password = 'password',
    supported_config_mode = 'cli-ssh')

dpissh_object = modules.CLI.dpissh.DpiSSHCli(fw)

dpissh_cli = {
    'enable':		    None,
    'intrusion-prevention': True,
    'exclude address':      'DMZ\ Subnets',
    'exclude address type': 'group',
    'include address':      'Default\ Gateway',
    'include address type': 'name',
    'include service':      'BGP',
    'include service type': 'name',
    'exclude service':      'AD\ Server',
    'exclude service type': 'group',
    'include user':         'Guest\ Administrators',
    'include user type':    'group',
    'exclude user':         None,
    'excluse user type':    'guests'    
}

retval = dpissh_object.general_settings(**dpissh_cli)
print (retval)

