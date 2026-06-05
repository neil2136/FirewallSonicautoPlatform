import re
from runner.settings import Params, logger

class BaseSettingsCli:
    '''BaseSettingsCli class'''

    def __init__(self, fw):
        self.fw = fw


    def config_securityservices_setting(self, **kwargs):
        commands = ['configure', 'security-services']
        self.fw._is_key_exist(commands, kwargs, 'reduce-isdn-antivirus-traffic')
        self.fw._is_key_exist(commands, kwargs, 'drop-packets-at-reload')
        self.fw._is_key_exist(commands, kwargs, 'synchronize')
        try:
            if 'maximum' in kwargs.keys():
                commands.append('security ' + 'maximum') if kwargs['maximum'] else commands.append('no '+'security ' + 'maximum')
            elif 'performance-optimized' in kwargs.keys():
                commands.append('security ' + 'performance-optimized') if kwargs['performance-optimized'] else commands.append('no ' + 'security ' + 'performance-optimized')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'http-clientless-notification-timeout' in kwargs.keys() and kwargs['http-clientless-notification-timeout']:
                commands.append(' http-clientless-notification-timeout ' + kwargs['http-clientless-notification-timeout'])
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'proxy-server' in kwargs.keys():
                commands.append('proxy-server')if kwargs['proxy-server'] else commands.append('no ' + 'proxy-server')
            if 'host' in kwargs.keys():
                commands.append('proxy-server')
                commands.append(' host ' + kwargs['host'])
                commands.append('exit')
            if 'port' in kwargs.keys():
                commands.append('proxy-server')
                commands.append(' port ' + kwargs['port'])
                commands.append('exit')
            if 'authentication' in kwargs.keys():
                commands.append('proxy-server')
                commands.append('authentication') if kwargs['authentication'] else commands.append('no ' + 'authentication')
                commands.append('exit')
            if 'user-name' in kwargs.keys() or 'password' in kwargs.keys():
                commands.append('proxy-server')
                commands.append('authentication ' + 'user-name '+kwargs['user-name'] + ' password ' + kwargs['password'])
            else:
                raise KeyError
        except KeyError:
            pass
        for command in ['commit', 'end', 'exit']:
                commands.append(command)
        result_securityservice_setting = self.fw.do_cli_commands(commands)
        return result_securityservice_setting


class ContentFilterWebsenseCli:

    '''
Websense enterprise Commands:
  block                          block-if-server-unavailable
  blocking-page                  exclude
  https-content-filtering        max-url-caches
  port                           probe
  server                         user-name
  probe
  deactivate-after    interval            monitoring          reactivate-after

 block
  activex              cookies              flash
  http-proxy-access    java
    custom-category
'''
    def __init__(self, fw):
        self.fw = fw

    def configure_contentfilter_websense(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type websense']
        self.fw._is_key_exist(commands, kwargs, 'server')
        self.fw._is_key_exist(commands, kwargs, 'user-name')
        self.fw._is_key_exist(commands, kwargs, 'port')
        self.fw._is_key_exist(commands, kwargs, 'max-url-caches')
        self.fw._is_key_exist(commands, kwargs, 'https-content-filtering')
        if 'monitoring' in kwargs.keys() and kwargs['monitoring'] == True:
            commands.append('probe ' + 'monitoring')
        else:
            commands.append('no ' + 'probe ' + 'monitoring')
        if 'interval' in kwargs.keys():
            commands.append('probe ' + 'interval ' + kwargs['interval'] )
        if 'reactivate-after' in kwargs.keys():
            commands.append('probe ' + 'reactivate-after ' + kwargs['reactivate-after'] )
        if 'deactivate-after' in kwargs.keys():
            commands.append('probe ' + 'deactivate-after ' + kwargs['deactivate-after'] )
        if 'block-if-server-unavailable' in kwargs.keys() and kwargs['block-if-server-unavailable'] == True:
            self.fw._is_key_exist(commands, kwargs, 'block-if-server-unavailable')
            if 'server-timeout' in kwargs.keys():
                self.fw._is_key_exist(commands, kwargs, 'server-timeout')
        else:
            commands.append('no ' + 'block-if-server-unavailable')
        if 'activex' in kwargs.keys():
            commands.append('block ' + 'activex')
        else:
            commands.append('no ' + 'block ' + 'activex')
        if 'cookies' in kwargs.keys():
            commands.append('block ' + 'cookies')
        else:
            commands.append('no ' + 'block ' + 'cookies')
        if 'flash' in kwargs.keys():
            commands.append('block ' + 'flash')
        else:
            commands.append('no ' + 'block ' + 'flash')
        if 'http-proxy-access' in kwargs.keys():
            commands.append('block ' + 'http-proxy-access')
        else:
            commands.append('no ' + 'block ' + 'http-proxy-access')
        if 'java' in kwargs.keys():
            commands.append('block ' + 'java')
        else:
            commands.append('no ' + 'block ' + 'java')
        if 'address_name' in kwargs.keys():
            commands.append('exclude ' + 'address name ' + kwargs['address_name'])
        elif 'address_group' in kwargs.keys():
            commands.append('exclude ' + 'address group ' + kwargs['address_group'])
        elif 'fqdn' in kwargs.keys():
            commands.append('exclude address ' + 'fqdn ' + kwargs['fqdn'])
        elif 'mac' in kwargs.keys():
            commands.append('exclude address ' + 'mac ' + kwargs['mac'])
        elif 'network' in kwargs.keys():
            commands.append('exclude address ' + 'network ' + kwargs['network'])
        elif 'range' in kwargs.keys():
            commands.append('exclude address ' + 'network ' + kwargs['range'])
        elif 'ipv6_fqdn' in kwargs.keys():
            commands.append('exclude address ipv6' + 'fqdn ' + kwargs['fqdn'])
        elif 'ipv6_mac' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'mac ' + kwargs['mac'])
        elif 'ipv6_network' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'network ' + kwargs['network'])
        elif 'ipv6_range' in kwargs.keys():
            commands.append('exclude address ipv6' + 'range ' + kwargs['range'])
        elif 'ipv6_host' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'host ' + kwargs['host'])
        else:
            print("No address values set")
        if 'blocking-page' in kwargs.keys() and kwargs['blocking-page'] == 'default':
            commands.append('blocking-page ' + kwargs['blocking-page'])
        else:
            commands.append('blocking-page ' + 'custom ' + kwargs['blocking-page'])

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class ContentFilterCfsCli:
    '''ContentFilterCfsCli class'''

    def __init__(self, fw):
        self.fw = fw

    def configure_contentfilter_cfs(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type cfs']
        self.fw._is_key_exist(commands, kwargs, 'max-url-caches')
        self.fw._is_key_exist(commands, kwargs, 'enable')
        
        if 'block-if-server-unavailable' in kwargs.keys():
            if kwargs['block-if-server-unavailable'] == True:

                self.fw._is_key_exist(commands, kwargs, 'block-if-server-unavailable')
                if 'server-timeout' in kwargs.keys():
                    self.fw._is_key_exist(commands, kwargs, 'server-timeout')
            else:
                commands.append('no ' + 'block-if-server-unavailable')
        if 'local-server' in kwargs.keys() and kwargs['local-server'] == True:

            self.fw._is_key_exist(commands, kwargs, 'local-server')
            if 'primary' in kwargs.keys():
                commands.append('local-server ' + 'primary ' + kwargs['primary'])
            if 'secondary' in kwargs.keys():
                commands.append('local-server ' + 'secondary ' + kwargs['secondary'])
        elif 'local-server' in kwargs.keys() and kwargs['local-server'] == False:
            commands.append('no ' + 'local-server')
        if 'uri_list' in kwargs.keys():
            commands.append('uri-list-object ' + kwargs['uri_list'])
            if 'uri_name' in kwargs.keys():
                commands.append('uri ' + kwargs['uri_name'])
        if 'cfs' in kwargs.keys():
            commands.append('cfs')
        if 'address_name' in kwargs.keys():
            commands.append('exclude ' + 'address name ' + kwargs['address_name'])
        elif 'address_group' in kwargs.keys():
            commands.append('exclude ' + 'address group ' + kwargs['address_group'])
        elif 'fqdn' in kwargs.keys():
            commands.append('exclude address ' + 'fqdn ' + kwargs['fqdn'])
        elif 'mac' in kwargs.keys():
            commands.append('exclude address ' + 'mac ' + kwargs['mac'])
        elif 'network' in kwargs.keys():
            commands.append('exclude address ' + 'network ' + kwargs['network'])
        elif 'range' in kwargs.keys():
            commands.append('exclude address ' + 'network ' + kwargs['range'])
        elif 'ipv6_fqdn' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'fqdn ' + kwargs['fqdn'])
        elif 'ipv6_mac' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'mac ' + kwargs['mac'])
        elif 'ipv6_network' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'network ' + kwargs['network'])
        elif 'ipv6_range' in kwargs.keys():
            commands.append('exclude address ipv6' + 'range ' + kwargs['range'])
        elif 'ipv6_host' in kwargs.keys():
            commands.append('exclude address ipv6 ' + 'host ' + kwargs['host'])
        elif 'administrator' in kwargs.keys():
            commands.append('exclude ' + ' administrator')
        else:
            logger.error("No address values set")


        if 'category-entry' in kwargs.keys():
            commands.append('custom-category')
            commands.append('category-entry ' + kwargs['category-entry'])
            commands.append('domain ' + kwargs['domain'])
            commands.append('rating ' + kwargs['rating'])
            commands.append('exit')
        if 'no category-entry' in kwargs.keys():
            commands.append('no category-entry ' + kwargs['no category-entry'])
        else:
            logger.error( "Invalid category entry")
        if 'category-enable' in kwargs.keys() and kwargs['category-enable'] == True:
            commands.append('category-entry ' + 'enable ' + kwargs['category-enable'] )
        elif 'category-enable' in kwargs.keys() and kwargs['category-enable'] == False:
            commands.append('no enable')
        
        # if 'policy' in kwargs.keys():
        #     commands.append('policy ' + 'name ' + kwargs['policy'])
        
        
        # self.fw._is_key_exist(commands, kwargs, 'port')
        # self.fw._is_key_exist(commands, kwargs, 'max-url-caches')
        # self.fw._is_key_exist(commands, kwargs, 'https-content-filtering')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


    def add_cfs_custom_category(self, **kwargs):
        commands = ['configure', 'content-filter', 'filter-type cfs']
        commands.append('custom-category')
        if 'category-entry' in kwargs.keys():
            commands.append('category-entry ' + kwargs['category-entry'])
            commands.append('domain ' + kwargs['domain'])
            if 'rating' in kwargs.keys():
                for entry in kwargs['rating']:
                    commands.append('rating' + ' ' + entry)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_custom_category(self, args = None):
        commands = ['configure', 'content-filter', 'filter-type cfs']
        commands.append('custom-category')
        if args:
            for value in args:
                commands.append('no category-entry ' + value)
        else:
            commands.append('no category-entries')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_content_filter(self, **kwargs):
        """
        example:-
        command=" ","cfs","websense"

        """
        supported_commands = " ","cfs","websense"
        commands = [" "]
        if kwargs:
            for command in kwargs:
                if command in supported_commands:
                    commands.append("show content-filter " + command)
                else:
                    logger.error("'" + command + "'" + " is not a supported command ")
        else:
            commands = ['show content-filter']
        show_output = self.fw.do_cli_commands(commands, tag=1)[1]
        return show_output

    def show_content_filter_cfs(self, **kwargs):
        commands = ['show content-filter']
        if 'cfs' in kwargs.keys():
            commands[0] = commands[0] + ' cfs'
            if 'policy' in kwargs.keys():
                commands[0] = commands[0] + ' policy name ' + kwargs['policy']
                
        else:
            commands = ['show content-filter']
        print(commands)
        show_output = self.fw.do_cli_commands(commands, tag=1)[1]
        return show_output
	
class IntrusionPreventionCli:
    '''IntrusionPreventionCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_intrusion_prevention(self, **kwargs):
        commands = ['configure', 'intrusion-prevention']
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

        self.fw._is_key_exist(commands, kwargs, 'reset')
        self.fw._is_key_exist(commands, kwargs, 'exclusion list')
        try:
            if 'ipv6_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'ipv6 ' + kwargs['ipv6_exclusion'])
            elif 'host_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'host ' + kwargs['host_exclusion'])
            elif 'network_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'network ' + kwargs['network_exclusion'])
            elif 'range_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'range ' + kwargs['range_exclusion'])
            elif 'fqdn_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'fqdn ' + kwargs['fqdn_exclusion'])
            elif 'group_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'group ' + kwargs['group_exclusion'])
            elif 'mac_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'mac ' + kwargs['mac_exclusion'])
            elif 'name_exclusion' in kwargs.keys():
                commands.append('exclusion ' + 'address-object ' + 'name ' + kwargs['name_exclusion'])
            else:
                raise KeyError
        except:
            logger("Error: missing exclusion address object")
        try:
            if 'entry'in kwargs.keys():
                commands.append('exclusion ' + 'entry ' + kwargs['entry'])
            else:
                raise KeyError
        except KeyError:
            logger.error("Error: missing exclusion entry")
        try:
            if 'prod_id' in kwargs.keys():
                commands = ['configure', 'intrusion-prevention','category', 'id ', kwargs['prod_id']]
                self.fw._is_key_exist(commands, kwargs, 'detection')
                try:
                    if 'ip_excluded_group' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'group ' + kwargs['ip_excluded_group'])
                    elif 'ip_excluded_name' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'name ' + kwargs['ip_excluded_name'])
                    elif 'ip_excluded_ipv6' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'ipv6 ' + kwargs['ip_excluded_ipv6'])
                    elif 'ip_excluded_host' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'host ' + kwargs['ip_excluded_host'])
                    elif 'ip_excluded_network' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'network ' + kwargs['ip_excluded_network'])
                    elif 'ip_excluded_range' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'range ' + kwargs['ip_excluded_range'])
                    elif 'user_excluded_admin' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'administrator ') if kwargs['user_excluded_admin'] else commands.append( 'no '+ 'excluded ' + 'users ' + 'administrator ')
                    elif 'user_excluded_guests' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'guests ') if kwargs['user_excluded_guests'] else commands.append( 'no '+ 'excluded ' + 'users ' + 'guests ')
                    elif 'user_excluded_name' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'name '+ kwargs['user_excluded_name'])
                    elif 'user_excluded_group' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'group '+ kwargs['user_excluded_group'])
                    else:
                        raise ValueError
                except ValueError:
                    logger.error("IP is not correct")
                try:
                    if 'ip_included_group' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'group ' + kwargs['ip_included_group'])
                    elif 'ip_included_name' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'name ' + kwargs['ip_included_name'])
                    elif 'ip_included_ipv6' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'ipv6 ' + kwargs['ip_included_ipv6'])
                    elif 'ip_included_host' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'host ' + kwargs['ip_included_host'])
                    elif 'ip_included_network' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'network ' + kwargs['ip_included_network'])
                    elif 'ip_included_range' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'range ' + kwargs['ip_included_range'])
                    elif'ip_included_all' in kwargs.keys() and kwargs['ip_included_all']:
                        commands.append('included ' + 'ip ' + 'all ')
                    elif 'user_included_admin' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'administrator ') if kwargs['user_included_admin'] else commands.append('no ' + 'included ' + 'users ' + 'administrator ')
                    elif 'user_included_guests' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'guests ') if kwargs['user_included_guests'] else commands.append('no ' + 'included ' + 'users ' + 'guests ')
                    elif 'user_included_name' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'name ' + kwargs['user_included_name'])
                    elif 'user_included_group' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'group ' + kwargs['user_included_group'])
                    elif 'user_included_all' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'all ')

                    else:
                        raise ValueError
                except ValueError:
                    logger.error("include ip has some value missing")
                if 'log_redun_filter' in kwargs.keys():
                    commands.append('log-redundancy ' + 'filter ' + kwargs['log_redun_filter'])
                if 'log_redun_global' in kwargs.keys():
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
                    logger.error('schedule is in daya or name or always_on')

            elif 'prod_name' in kwargs.keys():
                commands = ['configure', 'anti-spyware', 'product', 'name', kwargs['prod_name']]
                self.fw._is_key_exist(commands, kwargs, 'detection')
                try:
                    if 'ip_excluded_group' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'group ' + kwargs['ip_excluded_group'])
                    elif 'ip_excluded_name' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'name ' + kwargs['ip_excluded_name'])
                    elif 'ip_excluded_ipv6' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'ipv6 ' + kwargs['ip_excluded_ipv6'])
                    elif 'ip_excluded_host' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'host ' + kwargs['ip_excluded_host'])
                    elif 'ip_excluded_network' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'network ' + kwargs['ip_excluded_network'])
                    elif 'ip_excluded_range' in kwargs.keys():
                        commands.append('excluded ' + 'ip ' + 'range ' + kwargs['ip_excluded_range'])
                    elif 'user_excluded_admin' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'administrator ') if kwargs[
                            'user_excluded_admin'] else commands.append(
                            'no ' + 'excluded ' + 'users ' + 'administrator ')
                    elif 'user_excluded_guests' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'guests ') if kwargs[
                            'user_excluded_guests'] else commands.append('no ' + 'excluded ' + 'users ' + 'guests ')
                    elif 'user_excluded_name' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'name ' + kwargs['user_excluded_name'])
                    elif 'user_excluded_group' in kwargs.keys():
                        commands.append('excluded ' + 'users ' + 'group ' + kwargs['user_excluded_group'])
                    else:
                        raise ValueError
                except ValueError:
                    logger.error("IP is not correct")
                try:
                    if 'ip_included_group' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'group ' + kwargs['ip_included_group'])
                    elif 'ip_included_name' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'name ' + kwargs['ip_included_name'])
                    elif 'ip_included_ipv6' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'ipv6 ' + kwargs['ip_included_ipv6'])
                    elif 'ip_included_host' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'host ' + kwargs['ip_included_host'])
                    elif 'ip_included_network' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'network ' + kwargs['ip_included_network'])
                    elif 'ip_included_range' in kwargs.keys():
                        commands.append('included ' + 'ip ' + 'range ' + kwargs['ip_included_range'])
                    elif 'ip_included_all' in kwargs.keys() and kwargs['ip_included_all']:
                        commands.append('included ' + 'ip ' + 'all ')
                    elif 'user_included_admin' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'administrator ') if kwargs[
                            'user_included_admin'] else commands.append(
                            'no ' + 'included ' + 'users ' + 'administrator ')
                    elif 'user_included_guests' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'guests ') if kwargs[
                            'user_included_guests'] else commands.append('no ' + 'included ' + 'users ' + 'guests ')
                    elif 'user_included_name' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'name ' + kwargs['user_included_name'])
                    elif 'user_included_group' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'group ' + kwargs['user_included_group'])
                    elif 'user_included_all' in kwargs.keys():
                        commands.append('included ' + 'users ' + 'all ')

                    else:
                        raise ValueError
                except ValueError:
                    logger.error("include ip has some value missing")
                if 'log_redun_filter' in kwargs.keys():
                    commands.append('log-redundancy ' + 'filter ' + kwargs['log_redun_filter'])
                if 'log_redun_global' in kwargs.keys():
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
                    logger.error('schedule is in daya or name or always_on')
            else:
                raise ValueError
        except ValueError:
            logger("Error in the product value")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
		

class GavCli:
    '''GAVCli class'''

    def __init__(self, fw):
        self.fw = fw

    def configure_GAV(self, **kwargs):
        commands = ['configure', 'gateway-antivirus']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'block-multiple-compress-files')
        self.fw._is_key_exist(commands, kwargs, 'detection-only')
        self.fw._is_key_exist(commands, kwargs, 'eicar-detection')
        self.fw._is_key_exist(commands, kwargs, 'cifs-netbios-rest')
        self.fw._is_key_exist(commands, kwargs, 'http-byte-range')
        self.fw._is_key_exist(commands, kwargs, 'http-clientless-notification')
        self.fw._is_key_exist(commands, kwargs, 'notification-message')
        self.fw._is_key_exist(commands, kwargs, 'reset-settings')
        self.fw._is_key_exist(commands, kwargs, 'scan-high-compression')
        self.fw._is_key_exist(commands, kwargs, 'smtp-responses')
        self.fw._is_key_exist(commands, kwargs, 'update-signatures')
        # (config - gateway - antivirus)  

        if 'cloud_name' in  kwargs.keys():
            commands.append('cloud ' + 'exclusion name ' + kwargs['cloud_name'])
        if 'cloud_id' in kwargs.keys():
            commands.append('cloud ' + 'exclusion id ' + kwargs['id'])
            if 'server-timeout' in kwargs.keys():
                self.fw._is_key_exist(commands, kwargs, 'server-timeout')

        if 'address_name' in kwargs.keys():
            commands.append('exclusion ' + 'address name ' + kwargs['address_name'])
        elif 'address_group' in kwargs.keys():
            commands.append('exclusion ' + 'address group ' + kwargs['address_group'])
        elif 'fqdn' in kwargs.keys():
            commands.append('exclusion  ' + 'fqdn ' + kwargs['fqdn'])
        elif 'mac' in kwargs.keys():
            commands.append('exclusion ' + 'mac ' + kwargs['mac'])
        elif 'network' in kwargs.keys():
            commands.append('exclusion ' + 'network ' + kwargs['network'])
        elif 'range' in kwargs.keys():
            commands.append('exclusion ' + 'range ' + kwargs['range'])
        elif 'ipv6_network' in kwargs.keys():
            commands.append('exclusion ipv6 ' + 'network ' + kwargs['ipv6_network'])
        elif 'ipv6_range' in kwargs.keys():
            commands.append('exclusion ipv6' + 'range ' + kwargs['ipv6_range'])
        elif 'ipv6_host' in kwargs.keys():
            commands.append('exclusion ipv6 ' + 'host ' + kwargs['ipv6_host'])
        else:
            logger.error("No address values set")


        if 'cifs-netbios_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'cifs-netbios name ' + kwargs['cifs-netbios_name'])
        elif 'cifs-netbios_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'cifs-netbios group ' + kwargs['cifs-netbios_group'])
        elif 'cifs-netbios_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'cifs-netbios host ' + kwargs['cifs-netbios_host'])
        elif 'cifs-netbios_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'cifs-netbios network ' + kwargs['cifs-netbios_network'])
        elif 'cifs-netbios_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'cifs-netbios range ' + kwargs['range'])
        elif 'cifs-netbios_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'cifs-netbios network ' + kwargs['cifs-netbios_ipv6_network'])
        elif 'cifs-netbios_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'cifs-netbios range ' + kwargs['cifs-netbios_ipv6_range'])
        elif 'cifs-netbios_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'cifs-netbios host ' + kwargs['cifs-netbios_ipv6_host'])
        else:
            logger.error("No address values set for cifs-netbios exclusion object")
        
        if 'http_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'http name ' + kwargs['http_name'])
        elif 'http_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'http group ' + kwargs['http_group'])
        elif 'http_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'http host ' + kwargs['http_host'])
        elif 'http_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'http network ' + kwargs['http_network'])
        elif 'http_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'http range ' + kwargs['range'])
        elif 'http_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'http network ' + kwargs['http_ipv6_network'])
        elif 'http_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'http range ' + kwargs['http_ipv6_range'])
        elif 'http_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'http host ' + kwargs['http_ipv6_host'])
        else:
            logger.error("No address values set for http exclusion object")

        if 'imap_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'imap name ' + kwargs['imap_name'])
        elif 'imap_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'imap group ' + kwargs['imap_group'])
        elif 'imap_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'imap host ' + kwargs['imap_host'])
        elif 'imap_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'imap network ' + kwargs['imap_network'])
        elif 'imap_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'imap range ' + kwargs['range'])
        elif 'imap_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'imap network ' + kwargs['imap_ipv6_network'])
        elif 'imap_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'imap range ' + kwargs['imap_ipv6_range'])
        elif 'imap_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'imap host ' + kwargs['imap_ipv6_host'])
        else:
            logger.error("No address values set for imap exclusion object")

        if 'pop3_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'pop3 name ' + kwargs['pop3_name'])
        elif 'pop3_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'pop3 group ' + kwargs['pop3_group'])
        elif 'pop3_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'pop3 host ' + kwargs['pop3_host'])
        elif 'pop3_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'pop3 network ' + kwargs['pop3_network'])
        elif 'pop3_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'pop3 range ' + kwargs['range'])
        elif 'pop3_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'pop3 network ' + kwargs['pop3_ipv6_network'])
        elif 'pop3_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'pop3 range ' + kwargs['pop3_ipv6_range'])
        elif 'pop3_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'pop3 host ' + kwargs['pop3_ipv6_host'])
        else:
            logger.error("No address values set for pop3 exclusion object")

        if 'smtp_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'smtp name ' + kwargs['smtp_name'])
        elif 'smtp_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'smtp group ' + kwargs['smtp_group'])
        elif 'smtp_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'smtp host ' + kwargs['smtp_host'])
        elif 'smtp_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'smtp network ' + kwargs['smtp_network'])
        elif 'smtp_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'smtp range ' + kwargs['range'])
        elif 'smtp_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'smtp network ' + kwargs['smtp_ipv6_network'])
        elif 'smtp_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'smtp range ' + kwargs['smtp_ipv6_range'])
        elif 'smtp_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'smtp host ' + kwargs['smtp_ipv6_host'])
        else:
            logger.error("No address values set for smtp exclusion object")

        if 'ftp_name' in kwargs.keys():
            commands.append('exclusion-object ' + 'ftp name ' + kwargs['ftp_name'])
        elif 'ftp_group' in kwargs.keys():
            commands.append('exclusion-object ' + 'ftp group ' + kwargs['ftp_group'])
        elif 'ftp_host' in kwargs.keys():
            commands.append('exclusion-object  ' + 'ftp host ' + kwargs['ftp_host'])
        elif 'ftp_network' in kwargs.keys():
            commands.append('exclusion-object ' + 'ftp network ' + kwargs['ftp_network'])
        elif 'ftp_range' in kwargs.keys():
            commands.append('exclusion-object ' + 'ftp range ' + kwargs['range'])
        elif 'ftp_ipv6_network' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'ftp network ' + kwargs['ftp_ipv6_network'])
        elif 'ftp_ipv6_range' in kwargs.keys():
            commands.append('exclusion-object ipv6' + 'ftp range ' + kwargs['ftp_ipv6_range'])
        elif 'ftp_ipv6_host' in kwargs.keys():
            commands.append('exclusion-object ipv6 ' + 'ftp host ' + kwargs['ftp_ipv6_host'])
        else:
            logger.error("No address values set for ftp exclusion object")



        # if 'category-entry' in kwargs.keys():
        #     commands.append('custom-category')
        #     commands.append('category-entry ' + kwargs['category-entry'])
        #     commands.append('domain ' + kwargs['domain'])
        #     commands.append('rating ' + kwargs['rating'])
        #     commands.append('exit')
        # if 'no category-entry' in kwargs.keys():
        #     commands.append('no category-entry ' + kwargs['no category-entry'])
        # else:
        #     logger("Invalid category entry")
        # if 'category-enable' in kwargs.keys() and kwargs['category-enable'] == True:
        #     commands.append('category-entry ' + 'enable ' + kwargs['category-enable'])
        # else:
        #     commands.append('no enable')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

class CaptureAtpCli:
    '''CaptureAtpCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_capture_atp(self, **kwargs):
        commands = ['configure', 'capture-atp']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        temp=0
        try:
            if 'enable_file_type' in kwargs.keys():
                for temp in range(0,len(kwargs['enable_file_type'])):
                    commands.append('file-type ' + kwargs['enable_file_type'][temp])
                    commands.append('exit')
            if 'disable_file_type' in kwargs.keys():
                for temp in range(0,len(kwargs['disable_file_type'])):
                    commands.append('file-type ' + kwargs['disable_file_type'][temp])
                    commands.append('exit')
            else:
                raise KeyError
        except KeyError:
            logger.error("Error in file_type key")

        if 'file_size' in kwargs.keys():
            if kwargs['file_size']=='default':
                commands.append('file-size ' + 'default')
            else:
                commands.append('file-size ' + 'restrict ' + kwargs['file_size'])
        try:
            if kwargs['await-verdict']== 'allow':
                try:
                    if 'ipv6_for-capture-atp_host' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'host' + kwargs['ipv6_for-capture-atp_host'])
                    elif 'ipv6_for-capture-atp_network' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'network '+kwargs['ipv6_for-capture-atp_network'])
                    elif 'ipv6_for-capture-atp_range' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'range ' + kwargs['ipv6_for-capture-atp_range'])
                    elif 'host_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'host ' + kwargs['host_for-capture-atp'])
                    elif 'network_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'network ' + kwargs['network_for-capture-atp'])
                    elif 'range_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'range ' + kwargs['range_for-capture-atp'])
                    elif 'fqdn_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'fqdn ' + kwargs['fqdn_for-capture-atp'])
                    elif 'group_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'group ' + kwargs['group_for-capture-atp'])
                    elif 'mac_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'mac ' + kwargs['mac_for-capture-atp'])
                    elif 'name_for-capture-atp' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'name ' + kwargs['name_for-capture-atp'])
                    else:
                        raise KeyError
                except:
                    logger.error("Error: missing exclude address object for-capture-atp")
                if 'md5-entry' in kwargs.keys():
                    commands.append('exclude ' + 'md5-entry' + kwargs['md5-entry'])
            elif kwargs['await-verdict'] == 'block':
                try:
                    if 'ipv6_for-block-until-verdict_host' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'ipv6 ' + 'host' + kwargs['ipv6_for-block-until-verdict_host'])
                    elif 'ipv6_for-block-until-verdict_network' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'ipv6 ' + 'network ' + kwargs['ipv6_for-block-until-verdict_network'])
                    elif 'ipv6_for-block-until-verdict_range' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'ipv6 ' + 'range ' + kwargs['ipv6_for-block-until-verdict_range'])
                    elif 'host_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'host ' + kwargs['host_for-block-until-verdict'])
                    elif 'network_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'network ' + kwargs['network_for-block-until-verdict'])
                    elif 'range_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'range ' + kwargs['range_for-block-until-verdict'])
                    elif 'fqdn_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'fqdn ' + kwargs['fqdn_for-block-until-verdict'])
                    elif 'group_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'group ' + kwargs['group_for-block-until-verdict'])
                    elif 'mac_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'mac ' + kwargs['mac_for-block-until-verdict'])
                    elif 'name_for-block-until-verdict' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-block-until-verdict ' + 'name ' + kwargs['name_for-block-until-verdict'])
                    else:
                        raise KeyError
                except:
                    logger.error("Error: missing exclude address object missing in for-block-until-verdict")
                try:
                    if 'ipv6_address_host' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'host' + kwargs[
                            'ipv6_address_host'])
                    elif 'ipv6_address_network' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'network ' + kwargs[
                            'ipv6_address_network'])
                    elif 'ipv6_address_range' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'ipv6 ' + 'range ' + kwargs[
                            'ipv6_address_range'])
                    elif 'host_address' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'host ' + kwargs['host_address'])
                    elif 'network_address' in kwargs.keys():
                        commands.append(
                            'exclude ' + 'address ' + 'for-capture-atp ' + 'network ' + kwargs['network_address'])
                    elif 'range_address' in kwargs.keys():
                        commands.append(
                            'exclude ' + 'address ' + 'for-capture-atp ' + 'range ' + kwargs['range_address'])
                    elif 'fqdn_address' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'fqdn ' + kwargs['fqdn_address'])
                    elif 'group_address' in kwargs.keys():
                        commands.append(
                            'exclude ' + 'address ' + 'for-capture-atp ' + 'group ' + kwargs['group_address'])
                    elif 'mac_address' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'mac ' + kwargs['mac_address'])
                    elif 'name_address' in kwargs.keys():
                        commands.append('exclude ' + 'address ' + 'for-capture-atp ' + 'name ' + kwargs['name_address'])
                    else:
                        raise KeyError
                except:
                    logger.error("Error: missing exclude address object")

                if 'md5-entry' in kwargs.keys():
                    commands.append('exclude ' + 'md5-entry' + kwargs['md5-entry'])
                block_temp =0
                if 'enable_file_type_block' in kwargs.keys():
                    for block_temp in range(0, len(kwargs['enable_file_type'])):
                        commands.append('file-type ' + kwargs['enable_file_type'][temp])
                        commands.append('exit')
                if 'disable_file_type_block' in kwargs.keys():
                    for block_temp in range(0, len(kwargs['disable_file_type'])):
                        commands.append('file-type ' + kwargs['disable_file_type'][temp])
                        commands.append('exit')
            else:
                raise ValueError
        except ValueError:
            logger("Error in await-verdict value")

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_capture_atp(self, **kwargs):
        commands = ['configure', 'capture-atp']
        if 'del_md5' in kwargs.keys():
            commands.append('no '+ 'exclude ' + 'md5-entry' + kwargs['del_md5'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

class AntiSpywareCli:
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
            logger.error("Enable inbound protocols and outbound protocols")
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
            logger.error("Error: missing exclusion address object")
        try:
            if kwargs['entry']:
                commands.append('exclusion ' + 'address-object ' + 'entry ' + kwargs['entry'])
            else:
                raise KeyError
        except KeyError:
            logger.error("Error: missing exclusion entry")
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
                    logger.error("IP is not correct")
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
                    logger.error('schedule is in daya or name or always_on')

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
                    logger.error("IP is not correct")
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
                    logger.error("include ip has some value missing")
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
                    logger.error('schedule is in daya or name or always_on')
            else:
                raise ValueError
        except ValueError:
            logger.error("Error in the product value")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class GeoIpCli:
    '''GeoIpCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_geoip(self):
        commands = ["show geo-ip"]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        return output

    
    def config_Geo_IP(self, **kwargs):
        commands = ['configure', 'geo-ip']
        if 'alert-text' in kwargs.keys():
            commands.append('alert-text ' + kwargs['alert-text'])
        if 'block_connections' in kwargs.keys():
            commands.append('block ' + 'connections ') if kwargs['block_connections'] else('no ' + 'block ' + 'connections ')
            if kwargs['block_connections']:
                if 'block_connections_all' in kwargs.keys():
                    commands.append('block '+ 'connections '+ 'all ') if kwargs['block_connections_all'] else('no '+'block '+ 'connections '+ 'all ')
                if 'block_connections_firewall_rule' in kwargs.keys():
                    commands.append('block ' + 'connections ' + 'firewall-rule-based ') if kwargs['block_connections_firewall_rule'] else('no ' + 'block ' + 'connections ' + 'firewall-rule-based ')
                if 'block_connections_db_not_downloaded' in kwargs.keys():
                    commands.append('block '+ 'database-not-downloaded') if kwargs['block_connections_db_not_downloaded'] else('no '+'block '+ 'database-not-downloaded')
                else:
                    logger.info("block connection is only enabled")
            else:
                logger("block_connection is disabled")
        if 'block_all_countries' in kwargs.keys():
            commands.append('block ' + 'countries ')if kwargs['block_all_country'] else('no '+ 'block ' + 'countries ')
        if 'block_unkown_countries' in kwargs.keys():
            commands.append('block ' + 'countries ' + 'unknown ') if kwargs['block_unknown_countries'] else('no ' + 'block ' + 'countries ' + 'unknown')
        if 'block_country_add' in kwargs.keys():
            commands.append('block '+ 'country ' + kwargs['block_country_add'])
        if 'geo_botnet_lookup' in kwargs.keys():
            commands.append('geo-botnet-lookup ' + kwargs['geo_botnet_lookup'])
        if 'include_block_details' in kwargs.keys():
            commands.append('include ' + 'block-details') if kwargs['include_block_details'] else (
                        'no ' + 'include ' + 'block-details')
        if 'logo_icon' in kwargs.keys():
            commands.append('logo-icon ' + kwargs['logo_icon'])
        self.fw._is_key_exist(commands, kwargs, 'logging')
        if 'custom-list' in kwargs.keys():
        # try:
            commands.append('custom-list')
            self.fw._is_key_exist(commands, kwargs, 'enable')
            self.fw._is_key_exist(commands, kwargs, 'override-countries')
            if 'custom_list_address_name' in kwargs.keys():
                commands.append('address ' + 'name' + kwargs['custom_list_address_name'])
            elif 'custom_list_address_group' in kwargs.keys():
                commands.append('address ' + 'group' + kwargs['custom_list_address_group'])
            else:
                raise KeyError
        # except KeyError:
        #     logger.error("Error in Custom list keys")
        try:
            if 'default_blocked_page' in kwargs:
                if kwargs['default_blocked_page']:
                    commands.append('default blocked-page')
                else:
                    commands.append('no default blocked-page')
            if 'ipv6_exclude_host' in kwargs:
                commands.append('exclude ipv6 host ' + kwargs['ipv6_exclude_host'])
            elif 'ipv6_exclude_network' in kwargs:
                commands.append('exclude ipv6 network ' + kwargs['ipv6_exclude_network'])
            elif 'ipv6_exclude_range' in kwargs.keys():
                commands.append('exclude ' +'ipv6 ' + 'range ' + kwargs['ipv6_exlude_range'])
            elif 'host_exclude' in kwargs.keys():
                commands.append('exclude ' + 'host ' + kwargs['host_exclude'])
            elif 'network_exclude' in kwargs.keys():
                commands.append('exclude ' + 'network ' + kwargs['network_exclude'])
            elif 'range_exclude' in kwargs.keys():
                commands.append('exclude ' + 'range ' + kwargs['range_exclude'])
            elif 'group_exclude' in kwargs.keys():
                commands.append('exclude ' + 'group ' + kwargs['group_exclude'])
            elif 'name_exclude' in kwargs.keys():
                commands.append('exclude ' +'name ' + kwargs['name_exclude'])
            else:
                raise KeyError
        except:
            logger.error("Error: missing exclude address object for-GEO-IP")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_geo_ip(self, **kwargs):
        commands = ['configure', 'geo-ip']
        if 'allowed_country' in kwargs.keys():
            commands.append('no '+ 'block '+ 'country ' + kwargs['allowed_country'])
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

class BotnetCli:
    '''GeoIpCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_botnet(self):
        commands = ["show botnet"]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        return output

    def config_botnet(self, **kwargs):
        commands = ['configure', 'botnet']
        if 'CLI_opt' in kwargs.keys():
            # result = self.fw.do_cli_commands(commands, tag=1)[1]
            commands.append('?' )
        if 'alert-text' in kwargs.keys():
            commands.append('alert-text \"' + kwargs['alert-text'] + '\"' )
        if 'block_connections' in kwargs.keys():
            commands.append('block ' + 'connections ') if kwargs['block_connections'] else('no ' + 'block ' + 'connections ')
            if kwargs['block_connections']:
                if 'block_connections_all' in kwargs.keys():
                    commands.append('block ' + 'connections ' + 'all ') if kwargs['block_connections_all'] else (
                                'no ' + 'block ' + 'connections ' + 'all ')
                if 'block_connections_firewall_rule' in kwargs.keys():
                    commands.append('block ' + 'connections ' + 'firewall-rule-based ') if kwargs[
                        'block_connections_firewall_rule'] else (
                                'no ' + 'block ' + 'connections ' + 'firewall-rule-based ')
                if 'block_connections_db_not_downloaded' in kwargs.keys():
                    commands.append('block ' + 'database-not-downloaded') if kwargs[
                        'block_connections_db_not_downloaded'] else ('no ' + 'block ' + 'database-not-downloaded')
                else:
                    logger.info("enable any one option")
            else:
                logger.info("block_connection is disabled")

        if 'geo_botnet_lookup' in kwargs.keys():
            commands.append('geo-botnet-lookup ' + kwargs['geo_botnet_lookup'])
        if 'include_block_details' in kwargs.keys():
            commands.append('include ' + 'block-details') if kwargs['include_block_details'] else ('no ' + 'include ' + 'block-details')
        if 'logo_icon' in kwargs.keys():
            commands.append('logo-icon ' + kwargs['logo_icon'])
        if 'default_blocked_page' in kwargs.keys():
            commands.append('default ' + 'blocked-page ') if kwargs['default_blocked_page'] else ('no ' + 'default ' + 'blocked-page ')
        self.fw._is_key_exist(commands, kwargs, 'logging')
        if 'custom-list' in kwargs.keys():
            try:
                commands.append('custom-list')
                if 'custom_list_enable' in kwargs.keys():
                    commands.append('enable')#if kwargs['custom_list_enable'] #else commands.append('no '+'enable')
                if 'custom_list_address_name' in kwargs.keys():
                    commands.append('address ' + 'name ' + kwargs['custom_list_address_name'])
                elif 'custom_list_address_group' in kwargs.keys():
                    commands.append('address ' + 'group ' + kwargs['custom_list_address_group'])
                elif 'custom_list_address_network' in kwargs.keys():
                    commands.append('address ' + 'network ' + kwargs['custom_list_address_network'])
                elif 'custom_list_address_range' in kwargs.keys():
                    commands.append('address ' + 'range ' + kwargs['custom_list_address_range'])
                else:
                    raise KeyError
            except KeyError:
                logger.error("Error in Custom list keys")
        if "comment" in kwargs.keys():
            commands.append('comment' + ' '+ kwargs['comment'])      
        if "enable" in kwargs.keys():
            commands.append(kwargs['enable'])    
        if 'dynamic-list' in kwargs.keys():
            try:
                commands.append('dynamic-list')
                self.fw._is_key_exist(commands, kwargs, 'download')
                self.fw._is_key_exist(commands, kwargs, 'flush')
                self.fw._is_key_exist(commands, kwargs, 'periodical-download')
                if 'dynamic_list_enable' in kwargs.keys():
                    commands.append('enable ')if kwargs['dynamic_list_enable'] else commands.append('no '+'enable')
                if 'download_interval' in kwargs.keys():
                    commands.append('download-interval ' + kwargs['download_interval'])
                if 'protocol' in kwargs.keys():
                    commands.append('protocol ' + kwargs['protocol'])
                else:
                    raise KeyError
            except KeyError:
                logger.error("Error in configuring dynamic list")

        try:
            if 'ipv6_exclude_host' in kwargs.keys():
                commands.append('exclude ' + 'ipv6 ' + 'host ' + kwargs['ipv6_exclude_host'])
            elif 'ipv6_exclude_network' in kwargs.keys():
                commands.append('exclude ' + 'ipv6 ' + 'network '+kwargs['ipv6_exclude_network'])
            elif 'ipv6_exclude_range' in kwargs.keys():
                commands.append('exclude ' +'ipv6 ' + 'range ' + kwargs['ipv6_exlude_range'])
            elif 'host_exclude' in kwargs.keys():
                commands.append('exclude ' + 'host ' + kwargs['host_exclude'])
            elif 'network_exclude' in kwargs.keys():
                commands.append('exclude ' + 'network ' + kwargs['network_exclude'])
            elif 'range_exclude' in kwargs.keys():
                commands.append('exclude ' + 'range ' + kwargs['range_exclude'])
            elif 'group_exclude' in kwargs.keys():
                commands.append('exclude ' + 'group ' + kwargs['group_exclude'])
            elif 'name_exclude' in kwargs.keys():
                commands.append('exclude ' +'name ' + kwargs['name_exclude'])
            else:
                raise KeyError
        except:
            logger.error("Error: missing exclude address object for-GEO-IP")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result
























