#from runner.settings import LOGGING
#logger = LOGGING.getLogger(__name__)

from runner.settings import logger


class DpiSSHCli:
    def __init__(self, fw):
        self.fw = fw

    def general_settings(self, flag=0, **cli):
        commands = ['configure', 'dpi-ssh']
        teardown = ['commit', 'end', 'end']

        self.fw._is_key_exist(commands, cli, 'enable')
        self.fw._is_key_exist(commands, cli, 'application-firewall')
        self.fw._is_key_exist(commands, cli, 'intrusion-prevention')
        self.fw._is_key_exist(commands, cli, 'gateway anti-virus')
        self.fw._is_key_exist(commands, cli, 'gateway anti-spyware')
        self.fw._is_key_exist(commands, cli, 'block-port-forwarding')
        self.fw._is_key_exist(commands, cli, 'block-port-forwarding local')
        self.fw._is_key_exist(commands, cli, 'block-port-forwarding remote')
        self.fw._is_key_exist(commands, cli, 'block-port-forwarding x11')

        if 'exclude address' in cli and cli['exclude address'] is None:
            commands.append('no exclude address')
        elif 'exclude address' in cli and 'exclude address type' in cli:
            commands.append('exclude address ' + cli['exclude address type'] + ' ' + cli['exclude address'])
        elif not 'exclude address' in cli and 'exclude address type' in cli:
            logger.error('ERROR: exclude address must be specified')
            return False

        if 'exclude service' in cli and cli['exclude service'] is None:
            commands.append('no exclude service')
        elif 'exclude service' in cli and 'exclude service type' in cli:
            commands.append('exclude service ' + cli['exclude service type'] + ' ' + cli['exclude service'])
        elif not 'exclude service' in cli and 'exclude service type' in cli:
            logger.error('ERROR: exclude service must be specified')
            return False

        if 'exclude user' in cli and cli['exclude user'] is None:
            commands.append('no exclude user')
        elif 'exclude user' in cli and 'exclude user type' in cli:
            commands.append('exclude user ' + cli['exclude address type'] + ' ' + cli['exclude address'])
        elif not 'exclude user' in cli and 'exclude user type' in cli:
            logger.error('ERROR: exclude user must be specified')
            return False

        if 'include address' in cli and cli['include address'].lower() == 'all':
            commands.append('include address all')
        elif 'include address' in cli and 'include address type' in cli:
            commands.append('include address ' + cli['include address type'] + ' ' + cli['include address'])
        elif not 'include address' in cli and 'include address type' in cli:
            logger.error('ERROR: include address must be specified')
            return False

        if 'include service' in cli and cli['include service'].lower() == 'all':
            commands.append('include service all')
        elif 'include service' in cli and 'include service type' in cli:
            commands.append('include service ' + cli['include service type'] + ' ' + cli['include service'])
        elif not 'include service' in cli and 'include service type' in cli:
            logger.error('ERROR: include service must be specified')
            return False

        if 'include user' in cli and cli['include user'].lower() == 'all':
            commands.append('include user all')
        elif 'include user' in cli and 'include user type' in cli:
            commands.append('include user ' + cli['include user type'] + ' ' + cli['include user'])
        elif not 'include user' in cli and 'include user type' in cli:
            logger.error('ERROR: include user must be specified')
            return False

        for command in teardown:
            commands.append(command)
        logger.info(commands)

        try:
            retval = self.fw.do_cli_commands(commands, tag=flag)
            return retval
        except:
            logger.error('Unable to configure CLI')
            return False

    def show_dpi_ssh(self):
        commands = ["show dpi-ssh"]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

