import re
from util.snwl_logging import logger

class antispywareCli:
    '''antispywareCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_antispyware(self, **kwargs):
        commands = ['configure', 'anti-spyware']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        if 'prevent-all_hd' in kwargs.keys():
            commands.append('signature-group ' + 'high-danger ' + 'prevent-all ') if kwargs['prevent-all_hd'] else commands.append('no ' +'signature-group ' + 'high-danger ' + 'prevent-all ')
        if 'detect-all_hd' in kwargs.keys():
            commands.append('signature-group ' + 'high-danger ' + 'detect-all ') if kwargs['detect-all_hd'] else commands.append('no ' + 'signature-group ' + 'high-danger ' + 'detect-all ')
        if 'log-redundancy_hd' in kwargs.keys():
            commands.append('signature-group ' + 'high-danger ' + 'log-redundancy ' + kwargs['log-redundancy_hd']) if kwargs['log-redundancy_hd'] else commands.append('no ' + 'signature-group ' + 'high-danger ' + 'log-redundancy ')
        if 'prevent-all_md' in kwargs.keys():
            commands.append('signature-group ' + 'medium-danger ' + 'prevent-all ') if kwargs['prevent-all_md'] else commands.append('no ' + 'signature-group ' + 'medium-danger ' + 'prevernt-all ')
        if 'detect-all_md' in kwargs.keys():
            commands.append('signature-group ' + 'medium-danger ' + 'detect-all ') if kwargs['detect-all_md'] else commands.append('no ' + 'signature-group ' + 'medium-danger ' + 'detect-all ')
        if 'log-redundancy_md' in kwargs.keys():
            commands.append('signature-group ' + 'medium-danger ' + 'log-redundancy ' + kwargs['log-redundancy_md']) if kwargs['log-redundancy_md'] else commands.append('no ' + 'signature-group ' + 'medium-danger ' + 'log-redundancy ')
        if 'prevent-all_ld' in kwargs.keys():
            commands.append('signature-group ' + 'low-danger ' + 'prevent-all ') if kwargs['prevent-all_ld'] else commands.append('no ' + 'signature-group ' + 'low-danger ' + 'prevernt-all ')
        if 'detect-all_ld' in kwargs.keys():
            commands.append('signature-group ' + 'low-danger ' + 'detect-all ') if kwargs['detect-all_ld'] else commands.append('no ' + 'signature-group ' + 'low-danger ' + 'detect-all ')
        if 'log-redundancy_ld' in kwargs.keys():
            commands.append('signature-group ' + 'low-danger ' + 'log-redundancy ' + kwargs['log-redundancy_ld']) if kwargs['log-redundancy_ld'] else commands.append('no ' + 'signature-group ' + 'low-danger ' + 'log-redundancy ')
        try:
            if 'inbound_inspection_protocols' in kwargs.keys():
                commands.append('inspection ' + 'inbound ' + kwargs['inbound_protocols'])
            if 'outbound_inspection' in kwargs.keys():
                commands.append('inspection ' +  'outbound ') if kwargs['outbound_inspection'] else commands.append('no ' + 'inspection ' +  'outbound ')
            else:
                raise KeyError
        except KeyError:
            logger("Enable inbound protocols and outbound protocols")
        self.fw._is_key_exist(commands, kwargs, 'reset')
        self.fw._is_key_exist(commands, kwargs, 'smtp-response')
        self.fw._is_key_exist(commands, kwargs, 'http-clientless-notification')
        if 'message' in kwargs.keys():
            commands.append('message ' + kwargs['message']) if kwargs['message'] else commands.append('no ' + 'message')
        self.fw._is_key_exist(commands, kwargs, 'exclusion list')
        try:
            if kwargs['ipv6']:
                commands.append('exclusion ' + 'address-object ' + 'ipv6 ' + kwargs['ipv6'])
            elif kwargs['host']:
                commands.append('exclusion ' + 'address-object ' + 'host ' + kwargs['host'])
            elif kwargs['network']:
                commands.append('exclusion ' + 'address-object ' + 'network ' + kwargs['network'])
            elif kwargs['range']:
                commands.append('exclusion ' + 'address-object ' + 'network ' + kwargs['network'])
            elif kwargs['fqdn']:
                commands.append('exclusion ' + 'address-object ' + 'fqdn ' + kwargs['fqdn'])
            elif kwargs['group']:
                commands.append('exclusion ' + 'address-object ' + 'group ' + kwargs['group'])
            elif kwargs['mac']:
                commands.append('exclusion ' + 'address-object ' + 'mac ' + kwargs['mac'])
            elif kwargs['name']:
                commands.append('exclusion ' + 'address-object ' + 'name ' + kwargs['name'])
            else:
                raise KeyError
        except:
            logger("Error: missing exclusion address object")
        try:
            if kwargs['entry']:
                commands.append('exclusion ' + 'address-object ' + 'entry ' + kwargs['entry'])
            else:
                raise KeyError
        except KeyError:
            logger("Error: missing exclusion entry")
        try:
            if 'prod_id' in kwargs.keys():
                commands = ['configure', 'anti-spyware','product', 'id', kwargs['prod_id']]
                self.fw._is_key_exist(commands, kwargs, 'detection')
                try:

                    if kwargs['ip_excluded_group']:
                        commands.append('group ' + kwargs['ip_excluded_group'])
                    elif kwargs['ip_excluded_name']:
                        commands.append('name ' + kwargs['ip_excluded_name'])
                    else:
                        raise ValueError
                except ValueError:
                    logger("IP is not correct")
                if kwargs['sig_id']:
                    commands.append('id ' + kwargs['sig_id'])
                try:
                    if kwargs['included_ip_all']:
                        commands.append('included ' + 'ip ' + kwargs['included_ip_all'])
                    elif kwargs['included_ip_grp']:
                        commands.append('included ' + 'ip ' + 'group ' + kwargs['included_ip_grp'])
                    elif kwargs['included_ip_name']:
                        commands.append('included ' + 'ip ' + 'name ' + kwargs['included_ip_name'])
                    else:
                        raise ValueError
                except ValueError:
                    logger("include ip has some value missing")
                if kwargs['log_redun_filter']:
                    commands.append('log-redundancy ' + 'filter ' + kwargs['log_redun_filter'])
                commands.append('log-redundancy ' + 'global ') if  kwargs['log_redun_global'] else commands.append('no '+ 'log-redundancy ' + 'global ')
                self.fw._is_key_exist(commands, kwargs, 'prevention')
                commands.append('prevention ' + 'global') if kwargs['global_prevenion'] else commands.append('prevention ' + 'global')
                try:
                    if kwargs['schedule_days']:
                        commands.append('schedule ' + 'days' + kwargs['schedule_days'])
                    elif kwargs['schedule_name']:
                        commands.append('schedule ' + 'name' + kwargs['schedule_days'])
                    else:
                         commands.append('schedule ' + 'always-on ') if kwargs['schedule_always_on'] else ("Please put a coorect value", ValueError)

                except ValueError:
                    logger('schedule is in daya or name or always_on')

            elif 'prod_name' in kwargs.keys():
                commands = ['configure', 'anti-spyware', 'product', 'name', kwargs['prod_name']]
                self.fw._is_key_exist(commands, kwargs, 'detection')
                try:

                    if kwargs['ip_excluded_group']:
                        commands.append('group ' + kwargs['ip_excluded_group'])
                    elif kwargs['ip_excluded_name']:
                        commands.append('name ' + kwargs['ip_excluded_name'])
                    else:
                        raise ValueError
                except ValueError:
                    logger("IP is not correct")
                if kwargs['sig_id']:
                    commands.append('id ' + kwargs['sig_id'])
                try:
                    if kwargs['included_ip_all']:
                        commands.append('included ' + 'ip ' + kwargs['included_ip_all'])
                    elif kwargs['included_ip_grp']:
                        commands.append('included ' + 'ip ' + 'group ' + kwargs['included_ip_grp'])
                    elif kwargs['included_ip_name']:
                        commands.append('included ' + 'ip ' + 'name ' + kwargs['included_ip_name'])
                    else:
                        raise ValueError
                except ValueError:
                    logger("include ip has some value missing")
                if kwargs['log_redun_filter']:
                    commands.append('log-redundancy ' + 'filter ' + kwargs['log_redun_filter'])
                commands.append('log-redundancy ' + 'global ') if kwargs['log_redun_global'] else commands.append(
                    'no ' + 'log-redundancy ' + 'global ')
                self.fw._is_key_exist(commands, kwargs, 'prevention')
                commands.append('prevention ' + 'global') if kwargs['global_prevenion'] else commands.append(
                    'prevention ' + 'global')
                try:
                    if kwargs['schedule_days']:
                        commands.append('schedule ' + 'days' + kwargs['schedule_days'])
                    elif kwargs['schedule_name']:
                        commands.append('schedule ' + 'name' + kwargs['schedule_days'])
                    else:
                        commands.append('schedule ' + 'always-on ') if kwargs['schedule_always_on'] else ("Please put a coorect value", ValueError)
                except ValueError:
                    logger('schedule is in daya or name or always_on')
            else:
                raise ValueError
        except ValueError:
            logger("Error in the product value")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result



































