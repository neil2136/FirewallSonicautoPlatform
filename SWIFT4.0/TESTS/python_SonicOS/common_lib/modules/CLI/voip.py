from utm import FirewallCLI
from runner.settings import logger

class VoIPCli:
    ''' VoIP CLI based commands '''
    def __init__(self, fw):
        self.fw = fw

    '''List all the available commands'''
    def show_voip(self):
        commands = ['show voip']
        try:
            output = self.fw.do_cli_commands(commands, tag=1)[1]
            return output
        except:
            logger.error('Unable to configure CLI')
            return False


     ''' Enables basic default check box settings'''
    def general_settings(self, **kwargs):
        commands = ['configure', 'voip']
        teardown = ['commit', 'end', 'exit']
        self.fw._is_key_exist(commands, kwargs, 'consistent nat')
        self.fw._is_key_exist(commands, kwargs, 'sip')
        self.fw._is_key_exist(commands, kwargs, 'h323')
        self.fw._is_key_exist(commands, kwargs, 'flush-all')
        for command in teardown:
            commands.append(command)
            logger.info(commands)
        try:
            result = self.fw.do_cli_commands(commands)
            return result
        except:
            logger.error('Unable to configure CLI')
            return False
			

    '''Configures SIP settings with user values'''
    def sip(self, **kwargs):
        commands = ['configure', 'voip', 'sip']
        teardown = ['commit', 'end', 'exit']
        if 'signaling-port' in kwargs.keys():
            if 0 < kwargs['signaling-port'] < 65336:
                commands.append('signaling-port ' + kwargs['signaling-port'])
            else:
                raise ValueError("Not the valid port number for the sip port")
        
        if 'signaling-timeout' in kwargs.keys():
            if 29 < kwargs['signaling-timeout'] < 100001:
                commands.append('signaling-timeout ' + kwargs['signaling-timeout'])
            else:
                raise ValueError("Not the valid signaling timeout number for the sip port")
				
        if 'media-timeout' in kwargs.keys():
            if 29 < kwargs['media-timeout'] < 3601:
                commands.append('media-timeout ' + kwargs['media-timeout'])
            else:
                raise ValueError("Not the valid media timeout number for the sip port")
				
        if 'endpoint-block-interval' in kwargs.keys() :
            if 9 < kwargs['endpoint-block-interval'] < 864001:
                commands.append('endpoint-block-interval ' + kwargs['endpoint-block-interval'])
            else:
                raise ValueError("Not the valid endpoint-block-interval number for the sip port")
				
        if 'failed-registration-threshold' in kwargs.keys():
            if 0 < kwargs['failed-registration-threshold'] < 101:
                commands.append('failed-registration-threshold ' + kwargs['failed-registration-threshold'])
            else:
                raise ValueError("Not the valid failed-registration-threshold number for the sip port")

        if 'registration-anomaly-tracking' in kwargs.keys():
            if 9 < kwargs['registration-anomaly-tracking'] < 864001:
                commands.append('registration-anomaly-tracking ' + kwargs['registration-anomaly-tracking'])
            else:
                raise ValueError("Not the valid registration-anomaly-tracking number for the sip port")

        self.fw._is_key_exist(commands, kwargs, 'endpoint-registration-anomaly-tracking')
        self.fw._is_key_exist(commands, kwargs, 'non-sip-packets')
        self.fw._is_key_exist(commands, kwargs, 'b2bua-support')
        for command in teardown:
            commands.append(command)
        logger.info(commands)
        try:
            result = self.fw.do_cli_commands(commands)
            return result
        except:
            logger.error('Unable to configure CLI')
            return False
    
   
    '''Configures H323 settings with user values'''
    def h323(self, **kwargs):
        commands = ['configure', 'voip', 'h323']
        teardown = ['commit', 'end', 'exit']
		
        if 'inactivity-timeout' in kwargs.keys():
            if 59 < kwargs['inactivity-timeout'] < 122401:
                commands.append('inactivity-timeout ' + kwargs['inactivity-timeout'])
            else:
                raise ValueError("Not the valid inactivity-timeout number for the H323")
					
        self.fw._is_key_exist(commands, kwargs, 'only-gatekeeper-calls')
        self.fw._is_key_exist(commands, kwargs, 'gatekeeper-ip')
        for command in teardown:
            commands.append(command)
        logger.info(commands)
        try:
            result = self.fw.do_cli_commands(commands)
            return result
        except:
            logger.error('Unable to configure CLI')
            return False