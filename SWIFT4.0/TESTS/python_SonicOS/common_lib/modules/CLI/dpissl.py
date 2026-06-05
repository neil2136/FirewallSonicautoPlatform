#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)
from runner.settings import logger

class ServerSslCli:
    """ServerSslCli class"""
    def __init__(self, fw):
        self.fw = fw

    def config_general_settings(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl server']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'application-firewall')
        self.fw._is_key_exist(commands, kwargs, 'intrusion-prevention')
        self.fw._is_key_exist(commands, kwargs, 'gateway anti-virus')
        self.fw._is_key_exist(commands, kwargs, 'gateway anti-spyware')
        if 'exclude address' in kwargs.keys() and kwargs['exclude address'] is None:
            commands.append('no exclude address')
        elif 'exclude address' in kwargs.keys() and 'exclude address type' in kwargs.keys():
            commands.append('exclude address ' + kwargs['exclude address type'] + ' ' + kwargs['exclude address'])
        elif 'exclude address' not in kwargs.keys() and 'exclude address type' in kwargs.keys():
            logger.error('Exclude address must be specified.')
            return False
        else:
            pass
        if 'exclude user' in kwargs.keys() and kwargs['exclude user'] is None:
            commands.append('no exclude user')
        elif 'exclude user' in kwargs.keys() and 'exclude user type' in kwargs.keys():
            # commands.append('exclude user ' + kwargs['exclude address type'] + ' ' + kwargs['exclude address'])
            # wrong CLI command in user type and user info
            commands.append('exclude user ' + kwargs['exclude user type'] + ' ' + kwargs['exclude user'])
        elif 'exclude user' not in kwargs.keys() and 'exclude user type' in kwargs.keys():
            logger.error('Exclude user must be specified.')
            return False
        else:
            pass
        if 'include address' in kwargs.keys() and kwargs['include address'].lower() == 'all':
            commands.append('include address all')
        elif 'include address' in kwargs.keys() and 'include address type' in kwargs.keys():
            commands.append('include address ' + kwargs['include address type'] + ' ' + kwargs['include address'])
        elif 'include address' not in kwargs.keys() and 'include address type' in kwargs.keys():
            logger.error('Include address must be specified.')
            return False
        else:
            pass
        if 'include user' in kwargs.keys() and kwargs['include user'].lower() == 'all':
            commands.append('include user all')
        elif 'include user' in kwargs.keys() and 'include user type' in kwargs.keys():
            commands.append('include user ' + kwargs['include user type'] + ' ' + kwargs['include user'])
        elif 'include user' not in kwargs.keys() and 'include user type' in kwargs.keys():      
            logger.error('Include user must be specified.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'end']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def add_sslserver(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl server']
        if 'ssl-server' in kwargs.keys() and \
                'certificate' in kwargs.keys() and \
                'server-type' in kwargs.keys():
            if 'cleartext' in kwargs.keys():
                commands.append('ssl-server ' + kwargs['server-type'] + ' ' + kwargs['ssl-server'] + ' certificate ' + kwargs['certificate'] + ' cleartext')
            else:
                commands.append('ssl-server ' + kwargs['server-type'] + ' ' + kwargs['ssl-server'] + ' certificate ' + kwargs['certificate'])
        elif 'ssl-server' not in kwargs.keys() or 'certificate' not in kwargs.keys() or 'server-type' not in kwargs.keys():
            logger.error('Please select a server certificate,address object or group,and specify server type.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def del_sslserver(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl server']
        if 'ssl-server' in kwargs.keys() and \
                'certificate' in kwargs.keys() and \
                'server-type' in kwargs.keys():
            if 'cleartext' in kwargs.keys():
                commands.append('no ssl-server ' + kwargs['server-type'] + ' ' + kwargs['ssl-server'] + ' certificate ' + kwargs['certificate'] + ' cleartext')
            else:
                commands.append(
                    'no ssl-server ' + kwargs['server-type'] + ' ' + kwargs['ssl-server'] + ' certificate ' + kwargs['certificate'])
        elif 'ssl-server' not in kwargs.keys() or 'certificate' not in kwargs.keys() or 'server-type' not in kwargs.keys():
            logger.error('Please select a server certificate,address object or group,and specify server type.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def del_all_sslserver(self):
        # commands = ['configure', 'dpi-ssl server', 'no ssl servers']
        # wrong CLI command, it should be 'no ssl-servers'
        commands = ['configure', 'dpi-ssl server', 'no ssl-servers']
        result = self.fw.do_cli_commands(commands)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        return result

    def show_serverssl(self):
        commands = ["show dpi-ssl server"]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class ClientSslCli:
    """ClientSslCli class"""

    def __init__(self, fw):
        self.fw = fw

    def config_general_settings(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl client']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'application-firewall')
        self.fw._is_key_exist(commands, kwargs, 'intrusion-prevention')
        self.fw._is_key_exist(commands, kwargs, 'gateway anti-virus')
        self.fw._is_key_exist(commands, kwargs, 'gateway anti-spyware')
        self.fw._is_key_exist(commands, kwargs, 'content-filter')
        self.fw._is_key_exist(commands, kwargs, 'authenticate-server-for-decrypted-connections')
        self.fw._is_key_exist(commands, kwargs, 'expired-ca')
        self.fw._is_key_exist(commands, kwargs, 'deployment-server-domains')
        self.fw._is_key_exist(commands, kwargs, 'bypass-decryption')
        self.fw._is_key_exist(commands, kwargs, 'audit-built-in-exclusion')
        self.fw._is_key_exist(commands, kwargs, 'authenticate-server')
        for command in ['commit', 'end', 'end']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def config_cert(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl client']
        if 'resigning-authority' in kwargs.keys():
            commands.append('resigning-authority ' + kwargs['resigning-authority'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def config_objects(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl client']
        if 'exclude address' in kwargs.keys() and kwargs['exclude address'] is None:
            commands.append('no exclude address')
        elif 'exclude address' in kwargs.keys() and \
                'exclude address type' in kwargs.keys():
            commands.append('exclude address ' + kwargs['exclude address type'] + ' ' + kwargs['exclude address'])
        elif 'exclude address' not in kwargs.keys() and \
                'exclude address type' in kwargs.keys():
            logger.error('Exclude address must be specified.')
            return False
        else:
            pass
        if 'exclude service' in kwargs.keys() and kwargs['exclude service'] is None:
            commands.append('no exclude service')
        elif 'exclude service' in kwargs.keys() and 'exclude service type' in kwargs.keys():
            commands.append('exclude service ' + kwargs['exclude service type'] + ' ' + kwargs['exclude service'])
        elif 'exclude service' not in kwargs.keys() and 'exclude service type' in kwargs.keys():
            logger.error('Exclude service must be specified.')
            return False
        else:
            pass
        if 'exclude user' in kwargs.keys() and kwargs['exclude user'] is None:
            commands.append('no exclude user')
        elif 'exclude user' in kwargs.keys() and 'exclude user type' in kwargs.keys():
            # commands.append('exclude user ' + kwargs['exclude address type'] + ' ' + kwargs['exclude address'])
            # wrong CLI command in user type and user info
            commands.append('exclude user ' + kwargs['exclude user type'] + ' ' + kwargs['exclude user'])
        elif 'exclude user' not in kwargs.keys() and 'exclude user type' in kwargs.keys():
            logger.error('Exclude user must be specified.')
            return False
        else:
            pass
        if 'include address' in kwargs.keys() and kwargs['include address'].lower() == 'all':
            commands.append('include address all')
        elif 'include address' in kwargs.keys() and 'include address type' in kwargs.keys():
            commands.append('include address ' + kwargs['include address type'] + ' ' + kwargs['include address'])
        elif 'include address' not in kwargs.keys() and 'include address type' in kwargs.keys():
            logger.error('Include address must be specified.')
            return False
        else:
            pass
        if 'include service' in kwargs.keys() and kwargs['include service'].lower() == 'all':
            commands.append('include service all')
        elif 'include service' in kwargs.keys() and 'include service type' in kwargs.keys():
            commands.append('include service ' + kwargs['include service type'] + ' ' + kwargs['include service'])
        elif 'include service' not in kwargs.keys() and 'include service type' in kwargs.keys():
            logger.error('Include service must be specified.')
            return False
        else:
            pass
        if 'include user' in kwargs.keys() and kwargs['include user'].lower() == 'all':
            commands.append('include user all')
        elif 'include user' in kwargs.keys() and 'include user type' in kwargs.keys():
            # commands.append('include user ' + kwargs['include address type'] + ' ' + kwargs['include address'])
            # wrong CLI command in user type and user info
            commands.append('include user ' + kwargs['include user type'] + ' ' + kwargs['include user'])
        elif 'include user' not in kwargs.keys() and 'include user type' in kwargs.keys():
            logger.error('Include user must be specified.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def add_commonname(self, tag=0, **kwargs):
        commands = ['configure', 'dpi-ssl client']
        if 'common-name' in kwargs.keys() and 'action' in kwargs.keys():
            commands.append('common-name ' + kwargs['common-name'] + ' action ' + kwargs['action'])
        elif 'common-name' in kwargs.keys() and 'action' not in kwargs.keys():
            logger.error('Common-name action must be specified.')
            return False
        elif 'common-name' not in kwargs.keys() and 'action' in kwargs.keys():
            logger.error('Common-name name must be specified.')
            return False
        else:
            pass
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def del_commonname(self, *args):
        commands = ['configure', 'dpi-ssl client']
        if args:
            for value in args:
                commands.append('no common-name ' + value)
        else:
            logger.error("Entry name should be specified")
            return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_all_commonname(self):
        commands = ['configure', 'dpi-ssl client', 'no common-names']
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_clientssl(self):
        commands = ["show dpi-ssl client"]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def config_cfs_category(self, **kwargs):
        commands = ['configure', 'dpi-ssl client']
        self.fw._is_key_exist(commands, kwargs, 'exclude cfs-category-unavailable')
        if 'mode' in kwargs.keys():
            commands.append('cfs-categories ' + kwargs['mode'])
            if 'enable category list' in kwargs.keys():
                for category in kwargs['enable category list']:
                    commands.append('cfs-categories category ' + category)
            if 'disable category list' in kwargs.keys():
                for category in kwargs['disable category list']:
                    commands.append('no cfs-categories category ' + category)
        else:
            logger.error("Please specify cfs category mode")
            return False

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        logger.info(commands)
        result = self.fw.do_cli_commands(commands)
        return result

