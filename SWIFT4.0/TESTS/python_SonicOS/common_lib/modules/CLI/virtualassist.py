import re


class VirtualAssistCli:
    '''VirtualAssistCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_virtual_assist(self, *kwargs):
        supported_commands = " ", "virtual-assist" 
        commands = [" "]
        for command in kwargs:
            if command in supported_commands:
	            commands.append('show ' + command)
	        else:
	            logger("'" + command + "'" + " is not a supported command ")
	    output = self.fw.do_cli_commands(commands, tag=1)[1]
	    return output 


    def config_virtualassist(self, **kwargs):
        commands = ['configure', 'virtual-assist']
        self.fw._is_key_exist(commands, kwargs, 'support-without-invitation')
        self.fw._is_key_exist(commands, kwargs, 'link-on-portal-login')

        try:
            if 'assistance-code' in kwargs.keys() and kwargs['assistance-code']:
                commands.append(' assistance-code ' + kwargs['assistance-code'])
            if 'customer-access-link' in kwargs.keys() and kwargs['customer-access-link']:
                commands.append(' customer-access-link ' + kwargs['customer-access-link'])
            if 'disclaimer' in kwargs.keys() and kwargs['disclaimer']:
                commands.append(' disclaimer ' + kwargs['disclaimer'])
            if 'technician-email-list' in kwargs.keys() and kwargs['technician-email-list']:
                commands.append(' technician-email-list ' + kwargs['technician-email-list'])
            if 'invitation-subject' in kwargs.keys() and kwargs['invitation-subject']:
                commands.append(' invitation-subject ' + kwargs['invitation-subject'])
            if 'invitation-message' in kwargs.keys() and kwargs['invitation-message']:
                commands.append(' invitation-message ' + kwargs['invitation-message'])
            if 'max-requests' in kwargs.keys() and kwargs['max-requests']:
                commands.append(' max-requests ' + kwargs['max-requests'])
            if 'limit-message' in kwargs.keys() and kwargs['limit-message']:
                commands.append(' limit-message ' + kwargs['limit-message'])
            if 'max-requests-one-ip' in kwargs.keys() and kwargs['max-requests-one-ip']:
                commands.append(' max-requests-one-ip ' + kwargs['max-requests-one-ip'])
            if 'pending-request-expiration' in kwargs.keys() and kwargs['pending-request-expiration']:
                commands.append(' pending-request-expiration ' + kwargs['pending-request-expiration'])
            else:
                raise KeyError
        except KeyError:
            logger("Missing key in vrtual assist")

        try:
            temp = 0
            if 'host' in kwargs.keys():
                while temp < len(kwargs['host']):
                    commands.append('deny-requests ' + 'host ' + kwargs['host'][temp])
                    temp +=1
            if 'network' in kwargs.keys():
                while temp < len(kwargs['network']):
                    commands.append('deny-requests ' + 'network ' + kwargs['network'][temp])
                    temp +=1
            else:
                raise KeyError
        except KeyError:
            logger("Error while creating the host or network key")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def delete_host_network(self, **kwargs):
        commands = ['configure', 'virtual-assist']
        try:
            temp = 0
            if 'del_host_ip' in kwargs.keys():
                while temp < len(kwargs['del_host_ip']):
                    commands.append('no ' + 'deny-requests ' + 'host ' + kwargs['del_host_ip'][temp])
                    temp += 1
            if 'del_network_ip' in kwargs.keys():
                while temp < len(kwargs['del_network_ip']):
                    commands.append('no ' + 'deny-requests ' + 'network ' + kwargs['del_network_ip'][temp])
                    temp += 1
            else:
                raise KeyError
        except KeyError:
            logger("Error while creating the del host or network key")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        del_result = self.fw.do_cli_commands(commands)
        return del_result


































