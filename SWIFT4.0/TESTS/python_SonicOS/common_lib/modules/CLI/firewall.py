import re
from utm import FirewallCLI
#from runner.settings import LOGGING

from runner.settings import logger


class AccessRuleCli:
    '''AccessRuleCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_access_rule(self, **kwargs):
        if not self.validate_access_rule_parameters(**kwargs):
            logger.error('parameter error!')
            return False
        commands = ['configure']
        command = self.get_access_rule_parameters_identify(**kwargs)
        commands.append(command)
        commands.extend(self.get_access_rule_parameters_others(**kwargs))
        if 'extracmds' in kwargs.keys() and kwargs['extracmds']:
            for command in kwargs['extracmds']:
                commands.append(command)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_access_rule(self, **kwargs):
        if not self.validate_access_rule_parameters(**kwargs):
            logger.error('parameter error!')
            return False
        commands = ['configure']
        command = 'no ' + self.get_access_rule_parameters_identify(**kwargs)
        commands.append(command)
        for command in ['commit', 'end']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_access_rule(self, **kwargs):
        if not self.validate_access_rule_parameters(**kwargs):
            logger.error('parameter error!')
            return False
        commands = ['configure']
        command = self.get_access_rule_parameters_identify(**kwargs)
        commands.append(command)
        commands.extend(self.get_access_rule_parameters_edit(**kwargs))
        commands.extend(self.get_access_rule_parameters_others(**kwargs))
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    # edit cmd: access-rule ipv4 uuid xxx
    def edit_access_rule_by_uuid(self, **kwargs):
        if 'version' in kwargs.keys() and 'uuid' in kwargs.keys():
            if kwargs['version'] == 'v6':
                command = 'access-rule ipv6 uuid {}'.format(kwargs['uuid'])
            else:
                command = 'access-rule ipv4 uuid {}'.format(kwargs['uuid'])
            commands = ['configure']
            commands.append(command)
            commands.extend(self.get_access_rule_parameters_edit(**kwargs))
            commands.extend(self.get_access_rule_parameters_others(**kwargs))
            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            result = self.fw.do_cli_commands(commands)
            return result
        else:
            logger.error('key version or uuid is not exist in kwargs.')
            return False

    def restore_access_rule(self):
        commands = ['configure']
        command = 'access-rule restore-defaults'
        commands.append(command)
        for command in ['commit', 'end']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    # show access-rules ipv4 from WAN to LAN custom
    def show_access_rules(self, **kwargs):
        commands = []
        command = 'show access-rules'
        if 'version' in kwargs.keys() and kwargs['version']:
            command = command + ' ' + kwargs['version']
        if 'from' in kwargs.keys() and kwargs['from']:
            if 'to' not in kwargs.keys() or not kwargs['to']:
                logger.error('to should specified with from')
                return False
            else:
                command = command + ' ' + 'from ' + kwargs['from'] + ' to ' + kwargs['to']
        if 'action' in kwargs.keys() and kwargs['action']:
            command = command + ' action ' + kwargs['action']
        if 'src_name' in kwargs.keys() and kwargs['src_name']:
            command = command + ' source address name ' + kwargs['src_name']
        if 'dst_name' in kwargs.keys() and kwargs['dst_name']:
            command = command + ' destination address name ' + kwargs['dst_name']
        if 'service_name' in kwargs.keys() and kwargs['service_name']:
            command = command + ' service name ' + kwargs['service_name']         
        if 'type' in kwargs.keys() and kwargs['type']:
            command = command + ' ' + kwargs['type']
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output
        
    def show_access_rule_by_name(self, version='ipv4', name='Default\ Access\ Rule'):
        cmd = [f'show access-rule {version} name {name}']
        return self.fw.do_cli_commands(cmd, tag=1)[1]

    # list_access_rule_cli, cmd: access-rule ?
    def list_access_rule_cli(self):
        commands = ['configure', 'access-rule ?']
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result

    @staticmethod
    def validate_access_rule_parameters(**kwargs):
        # validate parameters
        required_parameters = ['from', 'to', 'action']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False

        if kwargs['action'] not in ['allow', 'deny', 'discard']:
            logger.error('action should be one of allow, deny and discard')
            return False

        if 'src_name' in kwargs.keys() and 'src_group' in kwargs.keys():
            logger.error('only one of src_name and src_group can be specified')
            return False

        if 'service_name' in kwargs.keys() and 'service_group' in kwargs.keys():
            logger.error('only one of service_name and service_group can be specified')
            return False

        if 'dst_name' in kwargs.keys() and 'dst_group' in kwargs.keys():
            logger.error('only one of dst_name and dst_group can be specified')
            return False

        if 'src_name_new' in kwargs.keys() and 'src_group_new' in kwargs.keys():
            logger.error('only one of src_name_new and src_group_new can  be specified')
            return False

        if 'dst_name_new' in kwargs.keys() and 'dst_group_new' in kwargs.keys():
            logger.error('only one of dst_name_new and dst_group_new can be specified')
            return False

        if 'service_name_new' in kwargs.keys() and 'service_group_new' in kwargs.keys():
            logger.error('only one of service_name_new and service_group_new can be specified')
            return False

        return True

    @staticmethod
    def get_access_rule_parameters_identify(**kwargs):
        # combine commands
        if 'version' in kwargs.keys() and kwargs['version'] == 'v6':
            command = 'access-rule ipv6 from "' + \
                kwargs['from'].upper() + '" to "' + kwargs['to'].upper() + \
                '" action ' + kwargs['action']
        else:
            command = 'access-rule ipv4 from "' + \
                kwargs['from'].upper() + '" to "' + kwargs['to'].upper() + \
                '" action ' + kwargs['action']

        # config source if source is specified
        if 'src_name' in kwargs.keys() and kwargs['src_name']:
            command += ' source address name "' + kwargs['src_name'] + '"'
        elif 'src_group' in kwargs.keys() and kwargs['src_group']:
            command += ' source address group "' + kwargs['src_group'] + '"'
        elif 'src_addr' in kwargs.keys() and kwargs['src_addr']:
            command += ' source address "' + kwargs['src_addr'] + '"'
        # config source port if source port is specified
        if 'port_name' in kwargs.keys() and kwargs['port_name']:
            command += ' source port name "' + kwargs['port_name'] + '"'
        elif 'port_group' in kwargs.keys() and kwargs['port_group']:
            command += ' source port group "' + kwargs['port_group'] + '"'
        # config service if service is specified
        if 'service_name' in kwargs.keys() and kwargs['service_name']:
            command += ' service name "' + kwargs['service_name'] + '"'
        elif 'service_group' in kwargs.keys() and kwargs['service_group']:
            command += ' service group "' + kwargs['service_group'] + '"'
        # config destination if destination is specified
        if 'dst_name' in kwargs.keys() and kwargs['dst_name']:
            command += ' destination address name "' + kwargs['dst_name'] + '"'
        elif 'dst_group' in kwargs.keys() and kwargs['dst_group']:
            command += ' destination address group "' + kwargs['dst_group'] + '"'
        elif 'dst_addr' in kwargs.keys() and kwargs['dst_addr']:
            command += ' destination address "' + kwargs['dst_addr'] + '"'
        # config schedule if schedule is specified
        if 'schedule_name' in kwargs.keys() and kwargs['schedule_name']:
            command += ' schedule  name "' + kwargs['schedule_name'] + '"'
        elif 'schedule_days_SU-SA' in kwargs.keys() and kwargs['schedule_days_SU-SA']:
            command += ' schedule  days SU-SA time 00:00 24:00'
        elif 'schedule_days_M-T' in kwargs.keys() and kwargs['schedule_days_M-T']:
            if kwargs['schedule_days_M-T'] == '00:00':
                command += ' schedule days M-T-W-TH-F time 00:00 08:00'
            elif kwargs['schedule_days_M-T'] == '08:00':
                command += ' schedule days M-T-W-TH-F time 08:00 17:00'
            elif kwargs['schedule_days_M-T'] == '17:00':
                command += ' schedule days M-T-W-TH-F time 17:00 24:00'
        elif 'schedule_days_SU-M' in kwargs.keys() and kwargs['schedule_days_SU-M']:
            if kwargs['schedule_days_SU-M']['time1'] == '02:00':
                command += ' schedule days SU-M-T-W-TH-F-SA time 02:00 03:00'
            elif kwargs['schedule_days_SU-M']['time1'] == '00:00':
                command += ' schedule days SU-M-T-W-TH-F-SA time 00:00 ' + kwargs['schedule_days_SU-M']['time2']
        return command

    @staticmethod
    def get_access_rule_parameters_others(**kwargs):
        commands = []
        # config users_included if users_included is specified
        if 'users_included' in kwargs.keys() and kwargs['users_included']:
            commands.append('users included ' + kwargs['users_included'])
        elif 'users_included_group' in kwargs.keys() and kwargs['users_included_group']:
            commands.append('users included group "' + kwargs['users_included_group'] + '"')
        # config users_excluded if users_excluded is specified
        if 'users_excluded' in kwargs.keys() and kwargs['users_excluded']:
            commands.append('users excluded ' + kwargs['users_excluded'])
        elif 'users_excluded_group' in kwargs.keys() and kwargs['users_excluded_group']:
            commands.append('users excluded group "' + kwargs['users_excluded_group'] + '"')
        # enable/disable logging
        FirewallCLI._is_key_exist(commands, kwargs, 'logging')
        # enable/disable fragments
        FirewallCLI._is_key_exist(commands, kwargs, 'fragments')
        # enable/disable flow-reporting
        FirewallCLI._is_key_exist(commands, kwargs, 'flow-reporting')
        # enable/disable packet-monitoring
        FirewallCLI._is_key_exist(commands, kwargs, 'packet-monitoring')
        # enable/disable management
        FirewallCLI._is_key_exist(commands, kwargs, 'management')
        # enable/disable botnet-filter
        FirewallCLI._is_key_exist(commands, kwargs, 'botnet-filter')
        # enable/disable geo-ip-filter
        FirewallCLI._is_key_exist(commands, kwargs, 'geo-ip-filter')
        # enable/disable sip
        FirewallCLI._is_key_exist(commands, kwargs, 'sip')
        # enable/disable h323
        FirewallCLI._is_key_exist(commands, kwargs, 'h323')
        # enable/disable management
        FirewallCLI._is_key_exist(commands, kwargs, 'management')
        # config tcp_timeout if tcp_timeout is specified
        FirewallCLI._is_key_exist(commands, kwargs, 'tcp_timeout', 'tcp timeout')
        # config udp_timeout if tcp_timeout is specified
        FirewallCLI._is_key_exist(commands, kwargs, 'udp_timeout', 'udp timeout')
        # config max-connections if max-connections is specified
        FirewallCLI._is_key_exist(commands, kwargs, 'max-connections')
        # config connection_limit_src if connection_limit_src is specified
        FirewallCLI._is_key_exist(commands, kwargs, 'connection_limit_src', 'connection source threshold')
        # config connection_limit_dst if connection_limit_dst is specified
        FirewallCLI._is_key_exist(commands, kwargs, 'connection_limit_dst', 'connection destination threshold')
        # enable/disable dpi
        FirewallCLI._is_key_exist(commands, kwargs, 'dpi')
        # enable/disable dpi_ssl_client
        FirewallCLI._is_key_exist(commands, kwargs, 'dpi_ssl_client', 'dpi-ssl client')
        # enable/disable dpi_ssl_server
        FirewallCLI._is_key_exist(commands, kwargs, 'dpi_ssl_server', 'dpi-ssl server')
        # comment
        if 'comment' in kwargs.keys() and kwargs['comment']:
            commands.append('comment "' + kwargs['comment'] + '"')
        if 'name' in kwargs.keys() and kwargs['name']:
            commands.append('name "' + kwargs['name'] + '"')
        FirewallCLI._is_key_exist(commands, kwargs, 'priority', 'priority manual')
        FirewallCLI._is_key_exist(commands, kwargs, 'priority_end', 'priority')
        FirewallCLI._is_key_exist(commands, kwargs, 'priority_auto', 'priority')
        # config quality-of-service dscp if qos_dscp is specified
        if 'qos_dscp' in kwargs.keys():
            if kwargs['qos_dscp'] == 'preserve' or kwargs['qos_dscp'] == 'map':
                commands.append('quality-of-service dscp ' + kwargs['qos_dscp'])
            elif 'explicit' in kwargs['qos_dscp'].keys():
                commands.append('quality-of-service dscp explicit ' + str(kwargs['qos_dscp']['explicit']))
        # config quality-of-service class-of-service if qos_cos is specified
        if 'qos_cos' in kwargs.keys():
            if kwargs['qos_cos'] == 'preserve' or kwargs['qos_cos'] == 'map':
                commands.append('quality-of-service class-of-service ' + kwargs['qos_cos'])
            elif 'explicit' in kwargs['qos_cos'].keys():
                commands.append('quality-of-service class-of-service explicit ' + kwargs['qos_cos']['explicit'])
        # enable/disable geo-ip-filter
        FirewallCLI._is_key_exist(commands, kwargs, 'geo-ip-filter')
        return commands

    @staticmethod
    def get_access_rule_parameters_edit(**kwargs):
        commands = []
        if 'from_new' in kwargs.keys() and 'from_new' in kwargs.keys():
            commands.append('from ' + kwargs['from_new'])
        if 'to_new' in kwargs.keys() and 'to_new' in kwargs.keys():
            commands.append('to ' + kwargs['to_new'])
        if 'action_new' in kwargs.keys() and 'action_new' in kwargs.keys():
            commands.append('action ' + kwargs['action_new'])

        if 'src_name_new' in kwargs.keys() and kwargs['src_name_new']:
            commands.append('source address name "' + kwargs['src_name_new'] + '"')
        elif 'src_group_new' in kwargs.keys() and kwargs['src_group_new']:
            commands.append('source address group "' + kwargs['src_group_new'] + '"')
        elif 'src_addr' in kwargs.keys() and kwargs['src_addr']:
            commands.append('source address "' + kwargs['src_addr'] + '"')

        # config destination if destination is specified
        if 'dst_name_new' in kwargs.keys() and kwargs['dst_name_new']:
            commands.append('destination address name "' + kwargs['dst_name_new'] + '"')
        elif 'dst_group_new' in kwargs.keys() and kwargs['dst_group_new']:
            commands.append('destination address group "' + kwargs['dst_group_new'] + '"')
        elif 'dst_addr' in kwargs.keys() and kwargs['dst_addr']:
            commands.append('destination address "' + kwargs['dst_addr'] + '"')

        # config service if service is specified
        if 'service_name_new' in kwargs.keys() and kwargs['service_name_new']:
            commands.append('service name "' + kwargs['service_name_new'] + '"')
        elif 'service_group_new' in kwargs.keys() and kwargs['service_group_new']:
            commands.append('service group "' + kwargs['service_group_new' + '"'])
        # edit schedule if schedule is specified
        if 'schedule_name_new' in kwargs.keys() and kwargs['schedule_name_new']:
            commands.append('schedule  name "' + kwargs['schedule_name'] + '"')
        elif 'schedule_days_SU-SA_new' in kwargs.keys() and kwargs['schedule_days_SU-SA_new']:
            commands.append('schedule  days SU-SA time 00:00 24:00')
        elif 'schedule_days_M-T_new' in kwargs.keys() and kwargs['schedule_days_M-T_new']:
            if kwargs['schedule_days_M-T_new'] == '00:00':
                commands.append('schedule days M-T-W-TH-F time 00:00 08:00')
            elif kwargs['schedule_days_M-T_new'] == '08:00':
                commands.append('schedule days M-T-W-TH-F time 08:00 17:00')
            elif kwargs['schedule_days_M-T_new'] == '17:00':
                commands.append('schedule days M-T-W-TH-F time 17:00 24:00')
        elif 'schedule_days_SU-M_new' in kwargs.keys() and kwargs['schedule_days_SU-M_new']:
            if kwargs['schedule_days_SU-M_new']['time1'] == '02:00':
                commands.append('schedule days SU-M-T-W-TH-F-SA time 02:00 03:00')
            elif kwargs['schedule_days_SU-M_new']['time1'] == '00:00':
                commands.append('schedule days SU-M-T-W-TH-F-SA time 00:00 ' + kwargs['schedule_days_SU-M_new']['time2'])

        if  'client_dpi_ssl' in kwargs.keys() and kwargs['client_dpi_ssl']:
            commands.append('dpi-ssl client')
        elif  'client_dpi_ssl' in kwargs.keys() and not kwargs['client_dpi_ssl']:
            commands.append('no dpi-ssl client')

        if  'server_dpi_ssl' in kwargs.keys() and kwargs['server_dpi_ssl']:
            commands.append('dpi-ssl server')
        elif  'server_dpi_ssl' in kwargs.keys() and not kwargs['server_dpi_ssl']:
            commands.append('no dpi-ssl server')

        # enable or disable access rule
        FirewallCLI._is_key_exist(commands, kwargs, 'enable')
        if 'new_enable' in kwargs.keys() and kwargs['new_enable']:
            commands.append(kwargs['new_enable'])
        return commands


class ContentFilterObjectCli:
    '''ContentFilterObjectCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_uri_list_object(self, **kwargs):
        commands = ['configure', 'content-filter']
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        if ('keyword' not in kwargs.keys() or not kwargs['keyword']) and ('uri' not in kwargs.keys() or not kwargs['uri']):
            logger.error('one of keyword and uri should be specified')
            return False
        commands.append('uri-list-object "' + kwargs['name'] + '"')
        if 'type' in kwargs.keys() and kwargs['type']:
            commands.append('type ' + kwargs['type'])
        if 'keyword' in kwargs.keys() and kwargs['keyword']:
            for keyword in kwargs['keyword']:
                commands.append('keyword "' + keyword + '"')
        if 'uri' in kwargs.keys() and kwargs['uri']:
            for uri in kwargs['uri']:
                commands.append('uri "' + uri + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_uri_list_object(self, *name):
        commands = ['configure', 'content-filter']
        if not name:
            commands.append('no uri-list-objects')
        else:
            for uri_list in name:
                commands.append('no uri-list-object "' + uri_list + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_uri_list_object(self, name=None):
        commands = []
        if name:
            command = 'show content-filter uri-list-object "' + name + '"'
        else:
            command = 'show content-filter uri-list-objects'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def add_uri_list_group(self, **kwargs):
        commands = ['configure', 'content-filter']
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        commands.append('uri-list-group "' + kwargs['name'] + '"')
        if 'object_list' in kwargs.keys() and kwargs['object_list']:
            for object in kwargs['object_list']:
                commands.append('uri-list-object "' + object + '"')
        if 'group_list' in kwargs.keys() and kwargs['group_list']:
            for group in kwargs['group_list']:
                commands.append('uri-list-group "' + group + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_uri_list_group(self, *name):
        commands = ['configure', 'content-filter']
        if not name:
            commands.append('no uri-list-groups')
        else:
            for uri_group in name:
                commands.append('no uri-list-group "' + uri_group + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_uri_list_group(self, name=None):
        commands = []
        if name:
            command = 'show content-filter uri-list-group "' + name + '"'
        else:
            command = 'show content-filter uri-list-groups'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def add_cfs_action_object(self, **kwargs):
        commands = ['configure', 'content-filter']
        if not self.get_cfs_action_object_parameter(**kwargs):
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_action_object_parameter(**kwargs))
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_cfs_action_object(self, **kwargs):
        commands = ['configure', 'content-filter']
        if not self.get_cfs_action_object_parameter(**kwargs):
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_action_object_parameter(**kwargs))
        if 'name_new' in kwargs.keys() and kwargs['name_new']:
            commands.append('name ' + kwargs['name_new'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    @staticmethod
    def get_cfs_action_object_parameter(**kwargs):
        commands = []
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        commands.append('action "' + kwargs['name'] + '"')
        if 'action' in kwargs.keys() and kwargs['action']:
            if kwargs['action'].lower() not in ['block', 'confirm', 'passphrase'] :
                logger.error('action should be in "block" "confirm" "passphrase"! ')
                return False
            else:
                command = kwargs['action']
        if 'page' in kwargs.keys() and kwargs['page']:
            command = command + ' page custom "' + kwargs['page'] + '"'
        else:
            command += ' page default'
        commands.append(command)
        if 'password' in kwargs.keys() and kwargs['password'] and kwargs['action'].lower() == 'passphrase':
            commands.append('passphrase password ' + kwargs['password'])
        if 'active_time' in kwargs.keys() and kwargs['active_time']:
            if kwargs['action'].lower() == 'block':
                logger.error('active_time cannot be set for block action')
                return False
            elif kwargs['active_time'] < 1 or kwargs['active_time'] > 9999:
                logger.error('active_time should be in 1-9999')
                return False
            else:
                command = kwargs['action'] + ' active-time ' + str(kwargs['active_time'])
        if 'wipe-cookies' in kwargs.keys():
            commands.append('wipe-cookies ')
        commands.append(command)
        return commands

    def del_cfs_action_object(self, *name):
        commands = ['configure', 'content-filter']
        if not name:
            commands.append('no actions')
        else:
            for action in name:
                commands.append('no action "' + action + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_cfs_action_object(self, name=None):
        commands = ['configure', 'content-filter']
        if name:
            command = 'show content-filter action name "' + name + '"'
        else:
            command = 'show content-filter actions'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def add_cfs_profile_object(self, **kwargs):
        commands = ['configure', 'content-filter']
        if self.get_cfs_profile_object_parameter(**kwargs) is False:
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_profile_object_parameter(**kwargs))
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_cfs_profile_object(self, **kwargs):
        commands = ['configure', 'content-filter']
        if self.get_cfs_profile_object_parameter(**kwargs) is False:
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_profile_object_parameter(**kwargs))
        if 'name_new' in kwargs.keys() and kwargs['name_new']:
            commands.append('name ' + kwargs['name_new'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    @staticmethod
    def get_cfs_profile_object_parameter(**kwargs):
        commands = []
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        commands.append('profile "' + kwargs['name'] + '"')
        if 'allowed_uri_list' in kwargs.keys() and kwargs['allowed_uri_list']:
            commands.append('uri-list allowed "' + kwargs['allowed_uri_list'] + '"')
        if 'forbidden_uri_list' in kwargs.keys() and kwargs['forbidden_uri_list']:
            commands.append('uri-list forbidden "' + kwargs['forbidden_uri_list'] + '"')
        if 'search_order' in kwargs.keys() and kwargs['search_order']:
            commands.append('uri-list search-order "' + kwargs['search_order'] + '"')
        if 'forbidden_operation' in kwargs.keys() and kwargs['forbidden_operation']:
            commands.append('uri-list forbidden-operation ' + kwargs['forbidden_operation'])

        if 'categories' in kwargs.keys() and kwargs['categories']:
            commands.append('categories ' + kwargs['categories'])

        if 'allowed_category_list' in kwargs.keys() and kwargs['allowed_category_list']:
            for category in kwargs['allowed_category_list']:
                commands.append('category "' + category + '" allow')
        if 'blocked_category_list' in kwargs.keys() and kwargs['blocked_category_list']:
            for category in kwargs['blocked_category_list']:
                commands.append('category "' + category + '" block')
        if 'bwm_category_list' in kwargs.keys() and kwargs['bwm_category_list']:
            for category in kwargs['bwm_category_list']:
                commands.append('category "' + category + '" bwm')
        if 'confirm_category_list' in kwargs.keys() and kwargs['confirm_category_list']:
            for category in kwargs['confirm_category_list']:
                commands.append('category "' + category + '" confirm')
        if 'passphrase_category_list' in kwargs.keys() and kwargs['passphrase_category_list']:
            for category in kwargs['passphrase_category_list']:
                commands.append('category "' + category + '" passphrase')

        FirewallCLI._is_key_exist(commands, kwargs, 'https-filtering')
        FirewallCLI._is_key_exist(commands, kwargs, 'smart-filter')
        FirewallCLI._is_key_exist(commands, kwargs, 'safe-search')
        FirewallCLI._is_key_exist(commands, kwargs, 'google-force-safe-search')
        FirewallCLI._is_key_exist(commands, kwargs, 'youtube-restrict-mode')
        FirewallCLI._is_key_exist(commands, kwargs, 'bing-force-safe-search')
        if 'consent' in kwargs.keys() and kwargs['consent']:
            if kwargs['consent']['enable']:
                commands.append('consent required')
                if 'user-idle-timeout' in kwargs['consent'].keys() and kwargs['consent']['user-idle-timeout']:
                    commands.append('consent user-idle-timeout ' + str(kwargs['consent']['user-idle-timeout']))
                if 'optional_page_url' in kwargs['consent'].keys() and kwargs['consent']['optional_page_url']:
                    commands.append('consent optional page-url ' + kwargs['consent']['optional_page_url'])
                if 'mandatory_page_url' in kwargs['consent'].keys() and kwargs['consent']['mandatory_page_url']:
                    commands.append('consent mandatory page-url ' + kwargs['consent']['mandatory_page_url'])
                if 'mandatory_address_name' in kwargs['consent'].keys() and kwargs['consent']['mandatory_address_name']:
                    commands.append('consent mandatory address name "' + kwargs['consent']['mandatory_address_name'] + '"')
                if 'mandatory_address_group' in kwargs['consent'].keys() and kwargs['consent']['mandatory_address_group']:
                    commands.append('consent mandatory address group "' + kwargs['consent']['mandatory_address_group'] + '"')
            else:
                commands.append('no consent required')
        FirewallCLI._is_key_exist(commands, kwargs, 'custom_header_insertion', 'custom-header insertion')
        if 'custom_header_entry' in kwargs.keys() and kwargs['custom_header_entry']:
            tmp_command = 'custom-header entry "' + kwargs['custom_header_entry']['domain'] + '" '+ \
                          kwargs['custom_header_entry']['key'] + '" ' + kwargs['custom_header_entry']['value']
            commands.append(tmp_command)
        return commands

    def del_cfs_profile_object(self, *name):
        commands = ['configure', 'content-filter']
        if not name:
            commands.append('no profiles')
        else:
            for profile in name:
                commands.append('no profile "' + profile + '"')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_cfs_profile_object(self, name=None):
        commands = []
        if name:
            command = 'show content-filter profile name "' + name + '"'
        else:
            command = 'show content-filter profiles'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class ContentFilterPoliciesCli:
    '''ContentFilterPoliciesCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_cfs_policy_object(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type cfs',]
        if self.get_cfs_policy_object_parameter(**kwargs) is False:
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_policy_object_parameter(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_cfs_policy_object(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type cfs']
        if self.get_cfs_policy_object_parameter_edit(**kwargs) is False:
            logger.error('parameter error!')
            return False
        commands.extend(self.get_cfs_policy_object_parameter_edit(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_cfs_policy_object(self, *name):
        commands = ['configure', 'content-filter', 'filter-type cfs']
        if not name:
            commands.append('no policies')
        else:
            for policy in name:
                commands.append('no policy "' + policy + '"')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_cfs_policy_object(self, name=None):
        commands = []
        if name:
            command = 'show content-filter cfs policy name "' + name + '"'
        else:
            command = 'show content-filter cfs policies'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    @staticmethod
    def get_cfs_policy_object_parameter(**kwargs):
        commands = []
        required_parameters = ['name', 'profile', 'action']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        if 'cfs' in kwargs.keys() and kwargs['cfs']:
            commands.append('cfs')
            commands.append('policy "' + kwargs['name'] + '"')
        else:
            logger.error('if you want to add or edit cfs policy,cfs should be specified')
            return False 
        commands.append('profile "' + kwargs['profile'] + '"')
        commands.append('action "' + kwargs['action'] + '"')
        if 'src_zone' in kwargs.keys() and kwargs['src_zone']:
            commands.append('source zone ' + kwargs['src_zone'].upper())
        if 'dst_zone' in kwargs.keys() and kwargs['dst_zone']:
            commands.append('destination zone ' + kwargs['dst_zone'].upper())

        # config schedule if schedule is specified
        command = ''
        if 'schedule_name' in kwargs.keys() and kwargs['schedule_name']:
            command = 'schedule  name "' + kwargs['schedule_name'] + '"'
        elif 'schedule_days_SU-SA' in kwargs.keys() and kwargs['schedule_days_SU-SA']:
            command = 'schedule  days SU-SA time 00:00 24:00'
        elif 'schedule_days_M-T' in kwargs.keys() and kwargs['schedule_days_M-T']:
            if kwargs['schedule_days_M-T'] == '00:00':
                command = 'schedule days M-T-W-TH-F time 00:00 08:00'
            elif kwargs['schedule_days_M-T'] == '08:00':
                command = 'schedule days M-T-W-TH-F time 08:00 17:00'
            elif kwargs['schedule_days_M-T'] == '17:00':
                command = 'schedule days M-T-W-TH-F time 17:00 24:00'
        elif 'schedule_days_SU-M' in kwargs.keys() and kwargs['schedule_days_SU-M']:
            if kwargs['schedule_days_SU-M']['time1'] == '02:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 02:00 03:00'
            elif kwargs['schedule_days_SU-M']['time1'] == '00:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 00:00 ' + kwargs['schedule_days_SU-M']['time2']
        if command:
            commands.append(command)
        # config users_included if users_included is specified
        if 'users_included' in kwargs.keys() and kwargs['users_included']:
            commands.append('user included ' + kwargs['users_included'])
        elif 'users_included_group' in kwargs.keys() and kwargs['users_included_group']:
            commands.append('user included group "' + kwargs['users_included_group'] + '"')
        # config users_excluded if users_excluded is specified
        if 'users_excluded' in kwargs.keys() and kwargs['users_excluded']:
            commands.append('user excluded ' + kwargs['users_excluded'])
        elif 'users_excluded_group' in kwargs.keys() and kwargs['users_excluded_group']:
            commands.append('user excluded group "' + kwargs['users_excluded_group'] + '"')

        if 'src_addr_excluded_name' in kwargs.keys() and kwargs['src_addr_excluded_name']:
            commands.append('source address excluded name "' + kwargs['src_addr_excluded_name'] + '"')
        elif 'src_addr_excluded_group' in kwargs.keys() and kwargs['src_addr_excluded_group']:
            commands.append('source address excluded group "' + kwargs['src_addr_excluded_group'] + '"')
        if 'src_addr_included_name' in kwargs.keys() and kwargs['src_addr_included_name']:
            commands.append('source address included name "' + kwargs['src_addr_included_name'] + '"')
        elif 'src_addr_included_group' in kwargs.keys() and kwargs['src_addr_included_group']:
            commands.append('source address included group "' + kwargs['src_addr_included_group'] + '"')
        return commands

    @staticmethod
    def get_cfs_policy_object_parameter_edit(**kwargs):
        commands = []
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        commands.append('policy "' + kwargs['name'] + '"')
        if 'name_new' in kwargs.keys() and kwargs['name_new']:
            commands.append('name "' + kwargs['name_new'] + '"')
        if 'profile' in kwargs.keys() and kwargs['profile']:
            commands.append('profile "' + kwargs['profile'] + '"')
        if 'action' in kwargs.keys() and kwargs['action']:
            commands.append('action "' + kwargs['action'] + '"')
        if 'src_zone' in kwargs.keys() and kwargs['src_zone']:
            commands.append('source zone ' + kwargs['src_zone'].upper())
        if 'dst_zone' in kwargs.keys() and kwargs['dst_zone']:
            commands.append('destination zone ' + kwargs['dst_zone'].upper())
        if 'enable' in kwargs.keys() and kwargs['enable'] is False:
            commands.append('no enable')
        return commands

    def websense_config(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type websense', 'websense']
        if self.websense_config_parameter(**kwargs) is False:
            logger.error('parameter error!')
            return False
        commands.extend(self.websense_config_parameter(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    @staticmethod
    def websense_config_parameter(**kwargs):
        commands = []
        if 'block-flash' in kwargs.keys():
            if kwargs['block-flash']:
                commands.append('block flash')
            else:
                commands.append('no block flash')
        if 'block-cookies' in kwargs.keys():
            if kwargs['block-cookies']:
                commands.append('block cookies')
            else:
                commands.append('no block cookies')
        if 'block-cookies' in kwargs.keys():
            if kwargs['block-cookies']:
                commands.append('block cookies')
            else:
                commands.append('no block cookies')
        if 'exclude-administrator' in kwargs.keys():
            if kwargs['exclude-administrator']:
                commands.append('exclude administrator')
            else:
                commands.append('no exclude administrator')
        
        if 'https-content-filtering' in kwargs.keys() and kwargs['https-content-filtering']:
            commands.append('https-content-filtering')
        return commands

    def show_websense(self, websense = True):
        commands = []
        if websense:
            command = 'show content-filter websense '
        else:
            command = 'show content-filter '
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output
class ActionObjectCli:
    '''ContentFilterPoliciesCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_action_object(self, **kwargs):
        commands = ['configure']
        if not self.get_action_object_parameters(**kwargs):
            logger.error('parameter error!')
            return False
        commands.extend(self.get_action_object_parameters(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_action_object(self, **kwargs):
        commands = ['configure']
        if not self.get_action_object_parameters(**kwargs):
            logger.error('parameter error!')
            return False
        commands.extend(self.get_action_object_parameters_edit(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_action_object(self, *name):
        commands = ['configure']
        if not name:
            commands.append('no action-objects')
        else:
            for action_name in name:
                commands.append('no action-object "' + action_name + '"')
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_action_object(self, name=None):
        commands = []
        if name:
            command = 'show action-object "' + name + '"'
        else:
            command = 'show action-objects'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    @staticmethod
    def get_action_object_parameters(**kwargs):
        commands = []
        required_parameters = ['name', 'action', 'content']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        commands.append('action-object "' + kwargs['name'] + '"')
        commands.append('action "' + kwargs['action'] + '"')
        commands.append('content "' + kwargs['content'] + '"')
        return commands

    @staticmethod
    def get_action_object_parameters_edit(**kwargs):
        commands = []
        if 'name' not in kwargs.keys() or not kwargs['name']:
            logger.error('name should be specified')
            return False
        commands.append('action-object "' + kwargs['name'] + '"')
        if 'name_new' in kwargs.keys() and kwargs['name_new']:
            commands.append('name "' + kwargs['name_new'] + '"')
        if 'action' in kwargs.keys() and kwargs['action']:
            commands.append('action "' + kwargs['action'] + '"')
        if 'content' in kwargs.keys() and kwargs['content']:
            commands.append('content "' + kwargs['content'] + '"')
        return commands


class MatchObjectCli:
    '''MatchObjectCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_match_object(self, **kwargs):
        commands = ['configure']
        required_parameters = ['name', 'type', 'content-entry']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        commands.append('match-object "' + kwargs['name'] + '"')
        commands.append('type ' + kwargs['type'])
        for content in kwargs['content-entry']:
            commands.append('content-entry "' + content + '"')

        FirewallCLI._is_key_exist(commands, kwargs, 'match-type')  # partial regex
        FirewallCLI._is_key_exist(commands, kwargs, 'input-representation')  # alphanumeric hexadecimal
        if kwargs['type'] == 'file-content' and 'negative-matching' in kwargs.keys():
            logger.error('file-content type do not have parameter negative-matching')
        FirewallCLI._is_key_exist(commands, kwargs, 'negative-matching')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_match_object(self, *name):
        commands = ['configure']
        if not name:
            commands.append('no match-objects')
        else:
            for match_name in name:
                commands.append('no match-object "' + match_name + '"')
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_match_object(self, name=None):
        commands = []
        if name:
            command = 'show match-object "' + name + '"'
        else:
            command = 'show match-objects'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class EmailObjectCli:
    '''EmailObjectCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_email_object(self, **kwargs):
        commands = ['configure']
        required_parameters = ['name', 'match-type', 'content-entry']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        commands.append('email-object "' + kwargs['name'] + '"')
        commands.append('match-type ' + kwargs['match-type'])
        for content in kwargs['content-entry']:
            commands.append('content-entry "' + content + '"')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_email_object(self, *name):
        commands = ['configure']
        if not name:
            commands.append('no email-objects')
        else:
            for match_name in name:
                commands.append('no email-object "' + match_name + '"')
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_email_object(self, name=None):
        commands = []
        if name:
            command = 'show email-object "' + name + '"'
        else:
            command = 'show email-objects'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class BandwidthObjectCli:
    '''BandwidthObjectCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_bandwidth_object(self, **kwargs):
        commands = ['configure']
        required_parameters = ['name', ]
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False

        if ('maximum_kbps' not in kwargs.keys() or not kwargs['maximum_kbps']) and ('maximum_mbps' not in kwargs.keys() or not kwargs['maximum_mbps']):
            logger.error('one of maximum_kbps and maximum_mbps should be specified')
            return False
        if ('maximum_kbps' in kwargs.keys() and kwargs['maximum_kbps']) and ('maximum_mbps' in kwargs.keys() and kwargs['maximum_mbps']):
            logger.error('only one of maximum_kbps and maximum_mbps can be specified')
            return False

        commands.append('bandwidth-object "' + kwargs['name'] + '"')
        if 'maximum_kbps' in kwargs.keys() and kwargs['maximum_kbps']:
            commands.append('maximum kbps ' + str(kwargs['maximum_kbps']))
        if 'maximum_mbps' in kwargs.keys() and kwargs['maximum_mbps']:
            commands.append('maximum mbps ' + str(kwargs['maximum_mbps']))
        if 'guaranteed_kbps' in kwargs.keys() and kwargs['guaranteed_kbps']:
            commands.append('guaranteed kbps ' + str(kwargs['guaranteed_kbps']))
        if 'guaranteed_mbps' in kwargs.keys() and kwargs['guaranteed_mbps']:
            commands.append('guaranteed mbps ' + str(kwargs['guaranteed_mbps']))
        if 'per_ip_kbps' in kwargs.keys() and kwargs['per_ip_kbps']:
            commands.append('per-ip-management kbps ' + str(kwargs['per_ip_kbps']))
        if 'per_ip_mbps' in kwargs.keys() and kwargs['per_ip_mbps']:
            commands.append('per-ip-management mbps ' + str(kwargs['per_ip_mbps']))
        FirewallCLI._is_key_exist(commands, kwargs, 'action')
        FirewallCLI._is_key_exist(commands, kwargs, 'priority')
        if 'comment' in kwargs.keys() and kwargs['comment']:
            commands.append('comment "' + str(kwargs['comment']) + '"')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_bandwidth_object(self, *name):
        commands = ['configure']
        if not name:
            commands.append('no bandwidth-objects')
        else:
            for band_name in name:
                commands.append('no bandwidth-object "' + band_name + '"')
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_bandwidth_object(self, name=None):
        commands = []
        if name:
            command = 'show bandwidth-object "' + name + '"'
        else:
            command = 'show bandwidth-objects'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class AppControlCli:
    '''AppControlCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_ac_global(self, **kwargs):
        commands = ['configure', 'app-control']
        FirewallCLI._is_key_exist(commands, kwargs, 'enable')
        FirewallCLI._is_key_exist(commands, kwargs, 'log-all')
        FirewallCLI._is_key_exist(commands, kwargs, 'log-filename')
        FirewallCLI._is_key_exist(commands, kwargs, 'log-redundancy', 'log-redundancy filter')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def reset_ac(self):
        commands = ['configure', 'app-control', "reset"]
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def config_ac(self, **kwargs):
        commands = ['configure', 'app-control']
        required_parameters = ['category', ]
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        if kwargs['category'].isdigit():
            command = 'category id  ' + str(kwargs['category']) + ' '
        else:
            command = 'category name  ' + kwargs['category'] + ' '
        if 'application' in kwargs.keys() and kwargs['application']:
            if kwargs['application'].isdigit():
                command += 'application id ' + str(kwargs['application']) + ' '
            else:
                command += 'application name ' + kwargs['application'] + ' '
        if 'signature' in kwargs.keys() and kwargs['signature']:
            if kwargs['signature'].isdigit():
                command += 'signature id ' + str(kwargs['signature']) + ' '
            else:
                command += 'signature name ' + kwargs['signature'] + ' '
        commands.append(command)

        FirewallCLI._is_key_exist(commands, kwargs, 'log')
        FirewallCLI._is_key_exist(commands, kwargs, 'block')

        if 'InIP_group' in kwargs.keys() and kwargs['InIP_group']:
            commands.append('included ip group "' + kwargs['InIP_group'] + '"')
        elif 'InIP_name' in kwargs.keys() and kwargs['InIP_name']:
            commands.append('included ip name "' + kwargs['InIP_name'] + '"')
        else:
            commands.append('included ip app')

        if 'ExIP_group' in kwargs.keys() and kwargs['ExIP_group']:
            commands.append('excluded ip group "' + kwargs['ExIP_group'] + '"')
        elif 'ExIP_name' in kwargs.keys() and kwargs['ExIP_name']:
            commands.append('excluded ip name "' + kwargs['ExIP_name'] + '"')
        else:
            commands.append('excluded ip app')
        # config users_included if users_included is specified
        if 'users_included' in kwargs.keys() and kwargs['users_included']:
            commands.append('included users ' + kwargs['users_included'])
        elif 'users_included_group' in kwargs.keys() and kwargs['users_included_group']:
            commands.append('included users group "' + kwargs['users_included_group'] + '"')
        else:
            commands.append('included users app')
        # config users_excluded if users_excluded is specified
        if 'users_excluded' in kwargs.keys() and kwargs['users_excluded']:
            commands.append('user excluded ' + kwargs['users_excluded'])
        elif 'users_excluded_group' in kwargs.keys() and kwargs['users_excluded_group']:
            commands.append('user excluded group "' + kwargs['users_excluded_group'] + '"')
        else:
            commands.append('included excluded app')
        # config schedule if schedule is specified
        command = ''
        if 'schedule_name' in kwargs.keys() and kwargs['schedule_name']:
            command = 'schedule  name "' + kwargs['schedule_name'] + '"'
        elif 'schedule_days_SU-SA' in kwargs.keys() and kwargs['schedule_days_SU-SA']:
            command = 'schedule  days SU-SA time 00:00 24:00'
        elif 'schedule_days_M-T' in kwargs.keys() and kwargs['schedule_days_M-T']:
            if kwargs['schedule_days_M-T'] == '00:00':
                command = 'schedule days M-T-W-TH-F time 00:00 08:00'
            elif kwargs['schedule_days_M-T'] == '08:00':
                command = 'schedule days M-T-W-TH-F time 08:00 17:00'
            elif kwargs['schedule_days_M-T'] == '17:00':
                command = 'schedule days M-T-W-TH-F time 17:00 24:00'
        elif 'schedule_days_SU-M' in kwargs.keys() and kwargs['schedule_days_SU-M']:
            if kwargs['schedule_days_SU-M']['time1'] == '02:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 02:00 03:00'
            elif kwargs['schedule_days_SU-M']['time1'] == '00:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 00:00 ' + kwargs['schedule_days_SU-M']['time2']
        if command:
            commands.append(command)
        # config log_redundancy
        if 'log_redundancy' in kwargs.keys() and kwargs['log_redundancy'] == 'app':
            commands.append('log-redundancy app')
        elif 'log_redundancy' in kwargs.keys() and kwargs['log_redundancy'].isdigit():
            commands.append('log-redundancy filter ' + str(kwargs['log_redundancy']))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def enable_exclude_list(self, **kwargs):
        commands = ['configure', 'app-control']
        required_parameters = ['type', ]
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        if kwargs['type'].lower() == 'ips':
            command = 'exclusion list ips'
        elif kwargs['type'].lower() == 'ao':
            command = 'exclusion list object '
            if ('ao_group' not in kwargs.keys() or not kwargs['ao_group']) and ('ao_name' not in kwargs.keys() or not kwargs['ao_name']):
                logger.error('one of ao_group ao_name should be specified')
                return False
            if 'ao_group' in kwargs.keys() and kwargs['ao_group']:
                command += 'group "' + kwargs['ao_group'] + '"'
            if 'ao_name' in kwargs.keys() and kwargs['ao_name']:
                command += 'name "' + kwargs['ao_name'] + '"'
        commands.append(command)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

# show app-control category name APP-UPDATE application name 360Safe
    def show_app_control(self, **kwargs):
        commands = []
        command = 'show app-control'
        if 'category' in kwargs.keys() and kwargs['category']:
            command = command + ' category name ' + kwargs['category']
        if 'application' in kwargs.keys() and kwargs['application']:
            command = command + ' application name ' + kwargs['application']
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class AppRuleCli:
    '''AppControlCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_app_setting(self, **kwargs):
        commands = ['configure', 'app-rules']
        FirewallCLI._is_key_exist(commands, kwargs, 'enable')
        FirewallCLI._is_key_exist(commands, kwargs, 'log-redundancy')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_app_rule(self, **kwargs):
        commands = ['configure', 'app-rules']
        required_parameters = ['name', 'type']
        for parameter in required_parameters:
            if parameter not in kwargs.keys() or not kwargs[parameter]:
                logger.error('{} should be specified'.format(parameter))
                return False
        commands.append('policy "' + kwargs['name'] + '"')

        if kwargs['type'] in ['app-control', 'cfs', 'ips', 'smtp-client']:
            commands.append('type ' + kwargs['type'])
        elif kwargs['type'] == 'ftp_client_download':
            commands.append('type ftp client download')
        elif kwargs['type'] == 'ftp_client_upload':
            commands.append('type ftp client upload')
        elif kwargs['type'] == 'ftp_data_transfer':
            commands.append('type ftp data_transfer')
        elif kwargs['type'] == 'http_client':
            commands.append('type http client')
        elif kwargs['type'] == 'http_server':
            commands.append('type http server')
        elif kwargs['type'] == 'pop3_client':
            commands.append('type pop3 client')
        elif kwargs['type'] == 'pop3_server':
            commands.append('type pop3 server')

        if 'src_addr_group' in kwargs.keys() and kwargs['src_addr_group']:
            commands.append('source address group "' + kwargs['src_addr_group'] + '"')
        if 'src_addr_name' in kwargs.keys() and kwargs['src_addr_name']:
            commands.append('source address name "' + kwargs['src_addr_name'] + '"')
        if 'dst_addr_group' in kwargs.keys() and kwargs['dst_addr_group']:
            commands.append('destination address group "' + kwargs['dst_addr_group'] + '"')
        if 'dst_addr_name' in kwargs.keys() and kwargs['dst_addr_name']:
            commands.append('destination address name "' + kwargs['dst_addr_name'] + '"')
        if 'excl_addr_group' in kwargs.keys() and kwargs['excl_addr_group']:
            commands.append('exclusion address group "' + kwargs['excl_addr_group'] + '"')
        if 'excl_addr_name' in kwargs.keys() and kwargs['excl_addr_name']:
            commands.append('exclusion address name "' + kwargs['excl_addr_name'] + '"')
        if 'src_service' in kwargs.keys() and kwargs['src_service']:
            commands.append('source service name "' + kwargs['src_service'] + '"')
        if 'dst_service' in kwargs.keys() and kwargs['dst_service']:
            commands.append('destination service name "' + kwargs['dst_service'] + '"')
        if 'match_object' in kwargs.keys() and kwargs['match_object']:
            commands.append('match-object object "' + kwargs['match_object'] + '"')
        if 'match_object_exclude' in kwargs.keys() and kwargs['match_object_exclude']:
            commands.append('match-object object exclude "' + kwargs['match_object'] + '"')
        if 'match_object_include' in kwargs.keys() and kwargs['match_object_include']:
            commands.append('match-object object include "' + kwargs['match_object_include'] + '"')
        if 'action_object' in kwargs.keys() and kwargs['action_object']:
            commands.append('action-object "' + kwargs['action_object'] + '"')

        # for type ips
        if 'addr_group' in kwargs.keys() and kwargs['addr_group']:
            commands.append('address group "' + kwargs['addr_group'] + '"')
        if 'addr_name' in kwargs.keys() and kwargs['src_addr_name']:
            commands.append('address name "' + kwargs['src_addr_name'] + '"')
        FirewallCLI._is_key_exist(commands, kwargs, 'zone_name', 'zone name')
        FirewallCLI._is_key_exist(commands, kwargs, 'ips-message-format')
        # for type ips

        FirewallCLI._is_key_exist(commands, kwargs, 'logging')
        FirewallCLI._is_key_exist(commands, kwargs, 'app-control-message-format')
        FirewallCLI._is_key_exist(commands, kwargs, 'log_individual', 'log individual')
        if 'log_redundancy' in kwargs.keys() and kwargs['log_redundancy'] == 'global':
            commands.append('log redundancy global')
        elif 'log_redundancy' in kwargs.keys() and kwargs['log_redundancy'].isdigit():
            commands.append('log redundancy interval ' + str(kwargs['log_redundancy']))

        if 'direction_advanced_from' in kwargs.keys() and kwargs['direction_advanced_from']:
            if kwargs['direction_advanced_from'] == 'any':
                commands.append('direction advanced from any')
            else:
                commands.append('direction advanced from zone ' + kwargs['direction_advanced_from'].upper())
        if 'direction_advanced_to' in kwargs.keys() and kwargs['direction_advanced_to']:
            if kwargs['direction_advanced_to'] == 'any':
                commands.append('direction advanced to any')
            else:
                commands.append('direction advanced to zone ' + kwargs['direction_advanced_to'].upper())
        if 'direction_basic' in kwargs.keys() and kwargs['direction_basic']:
            commands.append('direction basic ' + kwargs['direction_basic'])

        # config users_included if users_included is specified
        if 'users_included' in kwargs.keys() and kwargs['users_included']:
            commands.append('user included ' + kwargs['users_included'])
        elif 'users_included_group' in kwargs.keys() and kwargs['users_included_group']:
            commands.append('user included group "' + kwargs['users_included_group'] + '"')
        # config users_excluded if users_excluded is specified
        if 'users_excluded' in kwargs.keys() and kwargs['users_excluded']:
            commands.append('user excluded ' + kwargs['users_excluded'])
        elif 'users_excluded_group' in kwargs.keys() and kwargs['users_excluded_group']:
            commands.append('user excluded group "' + kwargs['users_excluded_group'] + '"')
        # config schedule if schedule is specified

        command = ''
        if 'schedule_name' in kwargs.keys() and kwargs['schedule_name']:
            command = 'schedule  name "' + kwargs['schedule_name'] + '"'
        elif 'schedule_days_SU-SA' in kwargs.keys() and kwargs['schedule_days_SU-SA']:
            command = 'schedule  days SU-SA time 00:00 24:00'
        elif 'schedule_days_M-T' in kwargs.keys() and kwargs['schedule_days_M-T']:
            if kwargs['schedule_days_M-T'] == '00:00':
                command = 'schedule days M-T-W-TH-F time 00:00 08:00'
            elif kwargs['schedule_days_M-T'] == '08:00':
                command = 'schedule days M-T-W-TH-F time 08:00 17:00'
            elif kwargs['schedule_days_M-T'] == '17:00':
                command = 'schedule days M-T-W-TH-F time 17:00 24:00'
        elif 'schedule_days_SU-M' in kwargs.keys() and kwargs['schedule_days_SU-M']:
            if kwargs['schedule_days_SU-M']['time1'] == '02:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 02:00 03:00'
            elif kwargs['schedule_days_SU-M']['time1'] == '00:00':
                command = 'schedule days SU-M-T-W-TH-F-SA time 00:00 ' + kwargs['schedule_days_SU-M']['time2']
        if command:
            commands.append(command)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_app_rule(self, *name):
        commands = ['configure', 'app-rules']
        if not name:
            commands.append('no policies')
        else:
            for policy_name in name:
                commands.append('no policy "' + policy_name + '"')
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_app_rule(self, name=None):
        commands = []
        if name:
            command = 'show app-rules policy "' + name + '"'
        else:
            command = 'show app-rules policies'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output
