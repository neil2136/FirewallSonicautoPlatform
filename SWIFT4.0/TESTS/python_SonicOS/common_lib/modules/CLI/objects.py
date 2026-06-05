import re
from utm import FirewallCLI
#from runner.settings import LOGGING

from runner.settings import logger


class DosActionProfileCli:
    '''DosActionProfileCli'''

    def __init__(self, fw):
        self.fw = fw

    def clone_dos_action_profile(self, name):
        commands = ['configure']
        commands.append('clone dos-action-profile "' + name + '"')
        for command in ['commit', 'end']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class SecurityActionProfilesCli:
    '''SecurityActionProfilesCli'''

    def __init__(self, fw):
        self.fw = fw

    def show_action_profiles(self, mode='all'):
        cmd = 'show security-action-profiles'
        if not mode == 'all':
            cmd = cmd + ' ' + str(mode)
        commands = [cmd]
        out = self.fw.do_cli_commands(commands, 1)[1]
        return out

    def del_all_action_profiles(self, msg=False):
        commands = ['configure', 'no security-action-profiles', 'commit', 'end']
        out = self.fw.do_cli_commands(commands, 1)
        return ( out[0] if not msg else out )


class MatchObjectsDynamicGroupCli:
    def __init__(self, fw):
        self.fw = fw

    def add_dynamic_external_object(self, **kwargs):
        # kwargs is {
        #     "name": self.dynamic_object_name,
        #     "type": "address-group",
        #     "zone": "LAN",
        #     "fqdn": True,
        #     "periodic_download": "interval 1-hour",
        #     "protocol": "ftp",
        #     "server": "10.11.11.11",
        #     "login": "autoroot",
        #     "password": "autopassword",
        #     "directory": "/tmp/test",
        #     "filename": "autofiles"
        # }
        commands = ['configure', ]
        if 'name' in kwargs.keys():
            commands.append('dynamic-external-object ' + kwargs['name'])
        else:
            logger.info(f'not key name in kwargs dict.')
            return False
        if 'new_name' in kwargs.keys():
            commands.append('name ' + kwargs['new_name'])
        self.fw._is_key_exist(commands, kwargs, 'type')
        self.fw._is_key_exist(commands, kwargs, 'zone')
        if 'fqdn' in kwargs.keys() and 'fqdn':
            commands.append('fqdn')
        if 'periodic-download' in kwargs.keys() and kwargs['periodic-download'] == 'interval':
            commands.append('periodic-download ' + kwargs['periodic-download'])
        if 'protocol' in kwargs.keys() and kwargs['protocol'] == 'ftp':
            self.fw._is_key_exist(commands, kwargs, 'protocol')
            self.fw._is_key_exist(commands, kwargs, 'server')
            self.fw._is_key_exist(commands, kwargs, 'login')
            self.fw._is_key_exist(commands, kwargs, 'password')
            self.fw._is_key_exist(commands, kwargs, 'directory')
            self.fw._is_key_exist(commands, kwargs, 'filename')
        else:
            self.fw._is_key_exist(commands, kwargs, 'url')
        commands.extend(['commit', 'end'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_dynamic_external_object(self, object_name):
        commands = ['configure', ]
        if object_name:
            commands.append('no dynamic-external-object ' + object_name)
        else:
            logger.info(f'not object name.')
            return False
        commands.extend(['commit', 'end'])
        result = self.fw.do_cli_commands(commands)
        return result

    def download_dynamic_external_object(self, object_name):
        commands = ['configure', ]
        if object_name:
            commands.append('download dynamic-external-object ' + object_name)
        else:
            logger.info(f'not object name.')
            return False
        commands.extend(['end'])
        result = self.fw.do_cli_commands(commands)
        return result
