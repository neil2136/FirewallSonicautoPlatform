import re
from utm import FirewallCLI
from runner.settings import logger

class ExportlogCli:
    '''export log '''
    '''example: export log ftp ftp://ftp.myserver.local/log.wri'''

    def __init__(self, fw):
        self.fw = fw

    def export_log(self, **kwargs):
        commands = ['export log ']
        if ('format' in kwargs.keys):
            commands.append(kwargs['format'])
        else:
            pass
        commands.append(' ftp ')
        if('ftp_url' in kwargs.keys):
            commands.append(kwargs['ftp_url'])
        else:
            return False
        result = self.fw.do_cli_commands(commands)
        return result


class ClearlogCli:
    '''clear log '''
    '''example: clear log'''

    def __init__(self, fw):
        self.fw = fw

    def clear_log(self, **kwargs):
        commands = ['config','clear log']
        result = self.fw.do_cli_commands(commands)
        return result


class EmaillogCli:
    '''email log '''
    '''example: email log'''

    def __init__(self, fw):
        self.fw = fw

    def clear_log(self, **kwargs):
        commands = ['email log']
        result = self.fw.do_cli_commands(commands)
        return result


class LogdisplayCli:
    '''Configure time range and max unm for showing log view in CLI'''
    '''example: log display max-number 100 '''
    '''         log display time-range last 5 minutes'''

    def __init__(self, fw):
        self.fw = fw

    def log_display(self, **kwargs):
        return True


class SyslogSettingsCli:
    ''' syslog settings '''
    default_options = {
        # Setting portion
        'id'                : 'firewall',       # user defined string
        'name'              : '',               # server name or ip
        'port'              : 514,              # server port
        'facility'          : 'local-use0',     # facility
        'format'            : 'default',        # default, webtrends, enhanced-syslog, arcSight
        'type'              : 'syslog-server',  # syslog-server, analyzer
        'profile'           : 0,
        'enabled'           : True,
        # 'addr_obj'  : '',                   # syslog address object name

        # Switch
        # 'override_s': 'off',                # on or off
        'en_erl'            : 'off',            # on or off
        'en_drl'            : 'off',            # on or off
        'en_ndpp'           : 'off',            # on or off

        'evt_lmt'           : 1000,             # rating limit, events / sec
        'data_lmt'          : 10000000,         # rating limit, bytes / sec

        # Add server portion
        'local_interface'   : '',             # local interface
        'outbound_interface': '',               # outboundnterface
    }

    def __init__(self, fw):
        self.fw = fw

    def add_syslog_server(self,**kwargs):
        self.options = dict(SyslogSettingsCli.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        commands = ['configure','log syslog',]

        if kwargs['name']:
            line = 'syslog-server server name '
            line += f'{kwargs["name"]} port {kwargs["port"]} profile {kwargs["profile"]}'
            commands.append(line)
        else:
            logger.error('Error! Name needed.')
        if kwargs['enabled']:
            commands.append('enabled')
        else:
            commands.append('no enabled')
        commands.append(f'id {kwargs["id"]}')
        commands.append(f'facility {kwargs["facility"]}')
        commands.append(f'format {kwargs["format"]}')
        commands.append(f'type {kwargs["type"]}')
        commands.append(f'format {kwargs["format"]}')

        if kwargs['en_erl'] == 'on':
            commands.append(f'event-rate-limiting {kwargs["evt_lmt"]}')
        if kwargs['en_drl'] == 'on':
            commands.append(f'data-rate-limiting {kwargs["data_lmt"]}')

        if kwargs['outbound_interface'] and kwargs['local_interface']:
            commands.append(f'outbound-interface {kwargs["outbound_interface"]}')
            commands.append(f'local-interface {kwargs["local_interface"]}')

        if kwargs['en_ndpp'] == 'on':
            commands.append('exit')
            commands.append('ndpp')
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        (rc,output) = self.fw.do_cli_commands(commands,tag=True)
        return rc

    def disable_ndpp(self):
        commands = ['configure', 'log syslog', ]
        commands.append('no ndpp')
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        (rc, output) = self.fw.do_cli_commands(commands, tag=True)
        return rc

    def del_all_syslog_servers(self):
        commands = ['configure', 'log syslog', ]
        commands.append('no servers')
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        (rc, output) = self.fw.do_cli_commands(commands, tag=True)
        return rc


class AuditLogsCli:
    '''Auditing Logs '''

    def __init__(self, fw):
        self.fw = fw
        self.settings_options = ['display-on-console', 'enable', 'supplemental-changes']

    def _do_settings_on_audit_log(self, cmd):
        commands = ['config', 'log audit',]
        commands.append(cmd)
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def enable_display_on_console(self):
        return self._do_settings_on_audit_log(self.settings_options[0])

    def disable_display_on_console(self):
        return self._do_settings_on_audit_log('no ' + self.settings_options[0])

    def enable_audit_log(self):
        return self._do_settings_on_audit_log(self.settings_options[1])

    def disable_audit_log(self):
        return self._do_settings_on_audit_log('no ' + self.settings_options[1])

    def enable_supplemental_changes(self):
        return self._do_settings_on_audit_log(self.settings_options[2])

    def disable_supplemental_changes(self):
        return self._do_settings_on_audit_log('no ' + self.settings_options[2])

    def show_audit_logs(self, args=None):
        commands = []
        command = 'show log audit'
        if args == 'view':
            command += args
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class LogAutomationCli:
    '''Log Automation'''

    def __init__(self, fw):
        self.fw = fw

    def _do_settings_on_log_automation(self, cmd):
        commands = ['config', 'log automation']
        commands.append(cmd)
        command = ['commit', 'end', 'exit']
        commands.extend(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def cfg_email_address(self, **kwargs):
        cmd = ''
        if 'type' in kwargs.keys() and 'email' in kwargs.keys():
            cmd = 'email-address ' + kwargs['type'] + ' ' + kwargs['email']
        else:
            logger.error('Make sure the parameter is specified right')
        return self._do_settings_on_log_automation(cmd), cmd

    def cfg_email_format_audit(self, format=None):
        e_au_format = ['csv', 'html', 'plain-text']
        cmd = ''
        if format in e_au_format:
            cmd = 'email-format-audit ' + format
        else:
            logger.error('Make sure the parameter is specified right')
        return self._do_settings_on_log_automation(cmd), cmd

    def cfg_email_period(self, **kwargs):
        cmd = ''
        if 'period' in kwargs.keys() and kwargs['period']:
            cmd = 'send-audit ' + kwargs['period'] + ' '
            if kwargs['period'] == 'daily':
                if 'hour' in kwargs.keys() and 'minute' in kwargs.keys():
                    cmd += 'hour {} minute {}'.format(str(kwargs['hour']), str(kwargs['minute']))
            elif kwargs['period'] == 'weekly':
                if 'week' in kwargs.keys() and 'hour' in kwargs.keys() and 'minute' in kwargs.keys():
                    cmd += '{} hour {} minute {}'.format(kwargs['week'], str(kwargs['hour']), str(kwargs['minute']))
        else:
            logger.error('Make sure the parameter is specified right')
        return self._do_settings_on_log_automation(cmd), cmd

    def show_log_automation(self):
        commands = ['show log automation']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output