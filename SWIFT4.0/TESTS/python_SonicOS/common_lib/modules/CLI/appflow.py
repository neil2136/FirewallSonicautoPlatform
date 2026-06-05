import re
from PythonRunner.runner.settings import logger

class AppFlowSettingCli:
    '''AppflowsettingCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_appflow_setting(self, *kwargs):
    commands = ['show appflow base']
    output = self.fw.do_cli_commands(commands, tag=1)[1]
    return output



    def config_appflow_setting(self, **kwargs):
        commands = ['configure', 'appflow']
        try:
            if 'connections' in kwargs.keys() and kwargs['connections']:
                commands.append(' report ' + 'connections ' + kwargs['connections'])
            if 'dropped' in kwargs.keys():
                commands.append(' report ' + 'dropped') if kwargs['dropped'] else commands.append('no ' + 'report ' + 'dropped')
            if 'stack' in kwargs.keys():
                commands.append(' report ' + 'stack') if kwargs['stack'] else commands.append('no ' + 'report ' + 'stack')
            if 'ipv6-flows' in kwargs.keys():
                commands.append(' report ' + 'ipv6-flows') if kwargs['ipv6-flows'] else commands.append('no ' + 'report ' + 'ipv6-flows')
            if 'upload-timeout' in kwargs.keys() and kwargs['upload-timeout']:
                commands.append(' report ' + 'upload-timeout ' + kwargs['upload-timeout'])
            else:
             raise KeyError
        except KeyError:
            logger.error("Error in report keys")
        try:
            if 'data-collection-realtime' in kwargs.keys():
                commands.append(' real-time ' + 'data-collection') if kwargs['data-collection-realtime'] else commands.append('no ' + ' real-time ' + 'data-collection')
            if 'top-applications' or 'bits-per-second' or 'packets-per-second' or 'average-packet-size' or 'connections-per-second' or 'core-utilization' or 'memory-utilization' in kwargs.keys():
                commands.append(' real-time ' + 'collect-for ' + 'top-applications') if kwargs['top-applications'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'top-applications')
                commands.append(' real-time ' + 'collect-for ' + 'bits-per-second') if kwargs['bits-per-second'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'bits-per-second')
                commands.append(' real-time ' + 'collect-for ' + 'packets-per-second') if kwargs['packets-per-second'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'packets-per-second')
                commands.append(' real-time ' + 'collect-for ' + 'average-packet-size') if kwargs['average-packet-size'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'average-packet-size')
                commands.append(' real-time ' + 'collect-for ' + 'connections-per-second') if kwargs['connections-per-second'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'connections-per-second')
                commands.append(' real-time ' + 'collect-for ' + 'core-utilization') if kwargs['core-utilization'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'core-utilization')
                commands.append(' real-time ' + 'collect-for ' + 'memory-utilization') if kwargs['memory-utilization'] else commands.append('no ' + ' real-time ' + 'collect-for ' + 'memory-utilization')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'data-collection-aggregate' in kwargs.keys():
                commands.append(' aggregate ' + 'data-collection') if kwargs['data-collection-aggregate'] else commands.append('no ' + ' real-time ' + 'data-collection')
            if 'applications' or 'user' or 'ip' or 'threat' or 'geo-ip' or 'url' in kwargs.keys():
                commands.append('aggregate ' + 'collect-for ' + 'applications') if kwargs['applications'] else commands.append('no ' + 'aggregate ' + 'collect-for' + 'applications')
                commands.append('aggregate ' + 'collect-for ' + 'user') if kwargs['user'] else commands.append('no ' + 'aggregate ' + 'collect-for ' + 'user')
                commands.append('aggregate ' + 'collect-for ' + 'ip') if kwargs['ip'] else commands.append('no ' + 'aggregate ' + 'collect-for ' + 'ip')
                commands.append('aggregate ' + 'collect-for ' + 'threat') if kwargs['threat'] else commands.append('no ' + 'aggregate ' + 'collect-for ' + 'threat')
                commands.append('aggregate ' + 'collect-for ' + 'geo-ip') if kwargs['geo-ip'] else commands.append('no ' + 'aggregate ' + 'collect-for ' + 'geo-ip')
                commands.append('aggregate ' + 'collect-for ' + 'url') if kwargs['url'] else commands.append('no ' + 'aggregate ' + 'collect-for ' + 'url')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'local-collector' in kwargs.keys():
                commands.append(' flows-to ' + 'local-collector') if kwargs['local-collector'] else commands.append('no ' + ' flows-to ' + 'local-collector')
            else:
                raise KeyError
        except KeyError:
            logger.error("Key missing for flows-to local collector")
        try:
            if 'gifs' or 'jpegs' or 'pngs' or 'js' or 'xmls' or 'jsons' or 'css' or 'htmls' or 'aspx' or 'cms' in kwargs.keys():
                commands.append('include-url-types ' + 'gifs') if kwargs['gifs'] else commands.append('no ' + 'include-url-types ' + 'gifs')
                commands.append('include-url-types ' + 'jpegs') if kwargs['jpegs'] else commands.append('no ' + 'include-url-types ' + 'jpegs')
                commands.append('include-url-types ' + 'pngs') if kwargs['pngs'] else commands.append('no ' + 'include-url-types ' + 'pngs')
                commands.append('include-url-types ' + 'js') if kwargs['js'] else commands.append('no ' + 'include-url-types ' + 'js')
                commands.append('include-url-types ' + 'xmls') if kwargs['xmls'] else commands.append('no ' + 'include-url-types ' + 'xmls')
                commands.append('include-url-types ' + 'jsons') if kwargs['jsons'] else commands.append('no ' + 'include-url-types ' + 'jsons')
                commands.append('include-url-types ' + 'css') if kwargs['css'] else commands.append('no ' + 'include-url-types ' + 'css')
                commands.append('include-url-types ' + 'htmls') if kwargs['htmls'] else commands.append('no ' + 'include-url-types ' + 'htmls')
                commands.append('include-url-types ' + 'aspx') if kwargs['aspx'] else commands.append('no ' + 'include-url-types ' + 'aspx')
                commands.append('include-url-types ' + 'cms') if kwargs['cms'] else commands.append('no ' + 'include-url-types ' + 'cms')
            else:
                raise KeyError
        except KeyError:
            logger.info("missing key in server_ip ")
        self.fw._is_key_exist(commands, kwargs, 'geo-ip-resolution')

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result_appflow_setting = self.fw.do_cli_commands(commands)
        return result_appflow_setting

class GmsFlowServerCli:
    '''GmsFlowServerCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_gmsflow_server(self, *kwargs):
    commands = ['show appflow gmsflow-server']
    output = self.fw.do_cli_commands(commands, tag=1)[1]
    return output 
 

    def config_gmsflow_server(self, **kwargs):
        commands = ['configure', 'appflow', 'gmsflow-server']
        self.fw._is_key_exist(commands, kwargs, 'flows')
        self.fw._is_key_exist(commands, kwargs, 'real-time')
        try:
            if 'open' or 'close' in kwargs.keys():
                commands.append(' report ' + 'open') if kwargs['open'] else commands.append('no ' + 'report ' + 'open')
                commands.append(' report ' + 'close') if kwargs['close'] else commands.append('no ' + 'report ' + 'close')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'threat' or 'application' or 'user' or 'vpn-tunnel' or 'url' in kwargs.keys():
                commands.append(' report ' + 'update ' + 'threat') if kwargs['threat'] else commands.append('no ' + 'report ' + 'update ' + 'threat')
                commands.append(' report ' + 'update ' + 'application') if kwargs['application'] else commands.append('no ' + 'report ' + 'update ' + 'application')
                commands.append(' report ' + 'update ' + 'user') if kwargs['user'] else commands.append('no ' + 'report ' + 'update ' + 'user')
                commands.append(' report ' + 'update ' + 'vpn-tunnel') if kwargs['vpn-tunnel'] else commands.append('no ' + 'report ' + 'update ' + 'vpn-tunnel')
                commands.append(' report ' + 'update ' + 'url') if kwargs['url'] else commands.append('no ' + 'report ' + 'update ' + 'url')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'connections' or 'users' or 'urls' or 'url_ratings' or 'vpns' or 'devices' or 'spams' or 'locations' or 'voips' in kwargs.keys():
                commands.append('dynamic-flows ' + 'connections') if kwargs['connections'] else commands.append('no ' + 'dynamic-flows ' + 'connections')
                commands.append('dynamic-flows ' + 'users') if kwargs['users'] else commands.append('no ' + 'dynamic-flows ' + 'users')
                commands.append('dynamic-flows ' + 'urls') if kwargs['urls'] else commands.append('no ' + 'dynamic-flows ' + 'urls')
                commands.append('dynamic-flows ' + 'url-ratings') if kwargs['url-ratings'] else commands.append('no ' + 'dynamic-flows ' + 'url-ratings')
                commands.append('dynamic-flows ' + 'vpns') if kwargs['vpns'] else commands.append('no ' + 'dynamic-flows ' + 'vpns')
                commands.append('dynamic-flows ' + 'devices') if kwargs['devices'] else commands.append('no ' + 'dynamic-flows ' + 'devices')
                commands.append('dynamic-flows ' + 'spams') if kwargs['spams'] else commands.append('no ' + 'dynamic-flows ' + 'spams')
                commands.append('dynamic-flows ' + 'locations') if kwargs['locations'] else commands.append('no ' + 'dynamic-flows ' + 'locations')
                commands.append('dynamic-flows ' + 'voips') if kwargs['voips'] else commands.append('no ' + 'dynamic-flows ' + 'voips')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            commands.append('server-ip')
            if 'ip' in kwargs.keys() and kwargs['ip']:
                commands.append('ip ' + kwargs['ip'] )
            if 'vpn-source-ip' in kwargs.keys() and kwargs['vpn-source-ip']:
                commands.append('vpn-source-ip ' + kwargs['vpn-source-ip'])
            if 'communication-timeout' in kwargs.keys() and kwargs['communication-timeout']:
                #commands.append('server-ip')
                commands.append('communication-timeout ' + kwargs['communication-timeout'])
            if 'auto-synchronize' in kwargs.keys():
                #commands.append('server-ip')
                self.fw._is_key_exist(commands, kwargs, 'auto-synchronize')
            else:
                raise KeyError

        except KeyError:
            logger.info("missing key in server_ip ")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result_gmsflow = self.fw.do_cli_commands(commands)
        return result_gmsflow

class AppFlowServerCli:
    '''AppFlowServerCli class'''

    def __init__(self, fw):
        self.fw = fw


    def config_appflow_server(self, **kwargs):
        commands = ['configure', 'appflow', 'appflow-server']
        self.fw._is_key_exist(commands, kwargs, 'flows')
        self.fw._is_key_exist(commands, kwargs, 'real-time')
        try:
            if 'open' in kwargs.keys():
                commands.append(' report ' + 'open') if kwargs['open'] else commands.append('no ' + 'report ' + 'open')
            if 'close' in kwargs.keys():
                commands.append(' report ' + 'close') if kwargs['close'] else commands.append('no ' + 'report ' + 'close')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'threat' or 'application' or 'user' or 'vpn-tunnel' or 'url' in kwargs.keys():
                commands.append(' report ' + 'update ' + 'threat') if kwargs['threat'] else commands.append('no ' + 'report ' + 'update ' + 'threat')
                commands.append(' report ' + 'update ' + 'application') if kwargs['application'] else commands.append('no ' + 'report ' + 'update ' + 'application')
                commands.append(' report ' + 'update ' + 'user') if kwargs['user'] else commands.append('no ' + 'report ' + 'update ' + 'user')
                commands.append(' report ' + 'update ' + 'vpn-tunnel') if kwargs['vpn-tunnel'] else commands.append('no ' + 'report ' + 'update ' + 'vpn-tunnel')
                commands.append(' report ' + 'update ' + 'url') if kwargs['url'] else commands.append('no ' + 'report ' + 'update ' + 'url')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            if 'connections' or 'users' or 'urls' or 'url_ratings' or 'vpns' or 'devices' or 'spams' or 'locations' or 'voips' in kwargs.keys():
                commands.append('dynamic-flows ' + 'connections') if kwargs['connections'] else commands.append('no ' + 'dynamic-flows ' + 'connections')
                commands.append('dynamic-flows ' + 'users') if kwargs['users'] else commands.append('no ' + 'dynamic-flows ' + 'users')
                commands.append('dynamic-flows ' + 'urls') if kwargs['urls'] else commands.append('no ' + 'dynamic-flows ' + 'urls')
                commands.append('dynamic-flows ' + 'url-ratings') if kwargs['url-ratings'] else commands.append('no ' + 'dynamic-flows ' + 'url-ratings')
                commands.append('dynamic-flows ' + 'vpns') if kwargs['vpns'] else commands.append('no ' + 'dynamic-flows ' + 'vpns')
                commands.append('dynamic-flows ' + 'devices') if kwargs['devices'] else commands.append('no ' + 'dynamic-flows ' + 'devices')
                commands.append('dynamic-flows ' + 'spams') if kwargs['spams'] else commands.append('no ' + 'dynamic-flows ' + 'spams')
                commands.append('dynamic-flows ' + 'locations') if kwargs['locations'] else commands.append('no ' + 'dynamic-flows ' + 'locations')
                commands.append('dynamic-flows ' + 'voips') if kwargs['voips'] else commands.append('no ' + 'dynamic-flows ' + 'voips')
            else:
                raise KeyError
        except KeyError:
            pass
        try:
            commands.append('server-ip')
            if 'keep-alive' in kwargs.keys():
                self.fw._is_key_exist(commands, kwargs, 'keep-alive')
            if 'ip' in kwargs.keys() and kwargs['ip']:
                commands.append('ip ' + kwargs['ip'] )
            if 'vpn-source-ip' in kwargs.keys() and kwargs['vpn-source-ip']:
                commands.append('vpn-source-ip ' + kwargs['vpn-source-ip'])
            if 'max-flows' in kwargs.keys() and kwargs['max-flows']:
                commands.append('communication-timeout ' + kwargs['communication-timeout'])
            if 'max-flows' in kwargs.keys() and kwargs['max-flows']:
                commands.append('max-flows ' + kwargs['max-flows'])
            if 'firewall-name' in kwargs.keys() and kwargs['firewall-name']:
                commands.append('firewall-name ' + kwargs['firewall-name'])
            if 'passphrase' in kwargs.keys():
                commands.append('passphrase ' + kwargs['passphrase'])
            if 'auto-synchronize' in kwargs.keys():
                self.fw._is_key_exist(commands, kwargs, 'auto-synchronize')
            else:
                raise KeyError

        except KeyError:
            logger.info("missing key in server_ip ")
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result_appflow_server = self.fw.do_cli_commands(commands)
        return result_appflow_server

class ExternalCollectorCli:
    '''ExternalCollectorCli class'''

    def __init__(self, fw):
        self.fw = fw

    def show_external_collector(self, *kwargs):
    commands = ['show appflow external-collector']
    output = self.fw.do_cli_commands(commands, tag=1)[1]
    return output  
 

    def config_external_collector(self, **kwargs):
        commands = ['configure', 'appflow', 'external-collector']
        self.fw._is_key_exist(commands, kwargs, 'flows')
        if 'ip' in kwargs.keys() and kwargs['ip']:
            commands.append('ip ' + kwargs['ip'])
        if 'vpn-source-ip' in kwargs.keys() and kwargs['vpn-source-ip']:
            commands.append('vpn-source-ip ' + kwargs['vpn-source-ip'])
        if 'port' in kwargs.keys() and kwargs['port']:
            commands.append('port ' + kwargs['port'])
        if 'reporting-format' in kwargs.keys() and kwargs['reporting-format']:
            commands.append('reporting-format ' + kwargs['reporting-format'])
            #commands.append('reporting-format')
            try:
                if kwargs['reporting-format'] == 'netflow-5' or 'netflow-9' or 'ipfix' or 'ipfix-with-extensions':
                    try:
                        if 'open' in kwargs.keys():
                            commands.append(' report ' + 'open') if kwargs['open'] else commands.append('no ' + 'report ' + 'open')
                        if 'close' in kwargs.keys():
                            commands.append(' report ' + 'close') if kwargs['close'] else commands.append('no ' + 'report ' + 'close')
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                    try:
                        if 'threat' or 'application' or 'user' or 'vpn-tunnel' or 'url' in kwargs.keys():
                            commands.append(' report ' + 'update '+ 'threat') if kwargs['threat'] else commands.append('no ' + 'report ' + 'update ' + 'threat')
                            commands.append(' report ' + 'update ' + 'application') if kwargs['application'] else commands.append('no ' + 'report ' + 'update ' + 'application')
                            commands.append(' report ' + 'update ' + 'user') if kwargs['user'] else commands.append('no ' + 'report ' + 'update ' + 'user')
                            commands.append(' report ' + 'update ' + 'vpn-tunnel') if kwargs['vpn-tunnel'] else commands.append('no ' + 'report ' + 'update ' + 'vpn-tunnel')
                            commands.append(' report ' + 'update ' + 'url') if kwargs['url'] else commands.append('no ' + 'report ' + 'update ' + 'url')
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                    try:
                        if 'active-timeout' in kwargs.keys() and kwargs['active-timeout']:
                            commands.append('no ' + 'report ' + 'kilobytes-exchanged')
                            commands.append(' report ' + 'active-timeout ' + kwargs['active-timeout'])
                        if 'kilobytes' in kwargs.keys():
                            commands.append('no ' + 'report ' + 'active-timeout')
                            commands.append(' report ' + 'kilobytes-exchanged ' + 'kilobytes ' + kwargs['kilobytes'])
                            if 'once' in kwargs.keys():
                                commands.append(' report ' + 'kilobytes-exchanged ' + 'once ') if kwargs['once'] else commands.append('no ' + ' report ' + 'kilobytes-exchanged ' + 'once ')
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                        #logger("Missing active-timeout and kilboytes keys in report")
                if kwargs['reporting-format'] == 'netflow-9' or 'ipfix' or 'ipfix-with-extensions':
                    try:
                        if 'templates' in kwargs.keys():
                            commands.append('send ' + 'templates') if kwargs['templates'] else commands.append('no ' + 'send ' + 'templates')
                        else:
                            raise KeyError
                    except KeyError:
                        pass
                        #logger ("Missing templates key in send")
                if kwargs['reporting-format'] == 'ipfix-with-extensions':
                    if 'static-flows' in kwargs.keys():
                        commands.append('send ' + 'static-flows') if kwargs['static-flows'] else commands.append('no ' + 'send ' + 'static-flows')

                    try:
                      if 'connections' or 'users' or 'urls' or 'url_ratings' or 'vpns' or 'devices' or 'spams' or 'locations' or 'voips' in kwargs.keys():
                        commands.append('dynamic-flows ' + 'connections') if kwargs['connections'] else commands.append('no ' + 'dynamic-flows ' + 'connections')
                        commands.append('dynamic-flows ' + 'users') if kwargs['users'] else commands.append('no ' + 'dynamic-flows ' + 'users')
                        commands.append('dynamic-flows ' + 'urls') if kwargs['urls'] else commands.append('no ' + 'dynamic-flows ' + 'urls')
                        commands.append('dynamic-flows ' + 'url-ratings') if kwargs['url-ratings'] else commands.append('no ' + 'dynamic-flows ' + 'url-ratings')
                        commands.append('dynamic-flows ' + 'vpns') if kwargs['vpns'] else commands.append('no ' + 'dynamic-flows ' + 'vpns')
                        commands.append('dynamic-flows ' + 'devices') if kwargs['devices'] else commands.append('no ' + 'dynamic-flows ' + 'devices')
                        commands.append('dynamic-flows ' + 'spams') if kwargs['spams'] else commands.append('no ' + 'dynamic-flows ' + 'spams')
                        commands.append('dynamic-flows ' + 'locations') if kwargs['locations'] else commands.append('no ' + 'dynamic-flows ' + 'locations')
                        commands.append('dynamic-flows ' + 'voips') if kwargs['voips'] else commands.append('no ' + 'dynamic-flows ' + 'voips')
                      else:
                          raise KeyError
                    except KeyError:
                        pass
                        #logger("Missing dynamic flows key")
                    try:
                      if 'applications' or 'viruses' or 'spyware' or 'intrusions' or 'location_map' or 'services' or 'rating_map' or 'table_map' or 'column_map' in kwargs.keys():

                        commands.append('static-flows ' + 'applications') if kwargs['applications'] else commands.append('no ' + 'static-flows ' + 'applications')
                        commands.append('static-flows ' + 'viruses') if kwargs['viruses'] else commands.append('no ' + 'static-flows ' + 'viruses')
                        commands.append('static-flows ' + 'spyware') if kwargs['spyware'] else commands.append('no ' + 'static-flows ' + 'spyware')
                        commands.append('static-flows ' + 'intrusions') if kwargs['intrusions'] else commands.append('no ' + 'static-flows ' + 'intrusions')
                        commands.append('static-flows ' + 'location_map') if kwargs['location_map'] else commands.append('no ' + 'static-flows ' + 'location_map')
                        commands.append('static-flows ' + 'services') if kwargs['services'] else commands.append('no ' + 'static-flows ' + 'services')
                        commands.append('static-flows ' + 'rating_map') if kwargs['rating_map'] else commands.append('no ' + 'static-flows ' + 'rating_map')
                        commands.append('static-flows ' + 'table_map') if kwargs['table_map'] else commands.append('no ' + 'static-flows ' + 'table_map')
                        commands.append('static-flows ' + 'column_map') if kwargs['column_map'] else commands.append('no ' + 'static-flows ' + 'column_map')
                      else:
                          raise KeyError
                    except KeyError:
                        pass
                    try:
                       if 'top-10-apps' or 'interface-statistics' or 'core-utilization' or 'memory-utilization' in kwargs.keys():
                         commands.append('ipfix-reports ' + 'top-10-apps') if kwargs['top-10-apps'] else commands.append('no ' + 'ipfix-reports ' + 'top-10-apps')
                         commands.append('ipfix-reports ' + 'interface-statistics') if kwargs['interface-statistics'] else commands.append('no ' + 'ipfix-reports ' + 'interface-statistics')
                         commands.append('ipfix-reports ' + 'core-utilization') if kwargs['core-utilization'] else commands.append('no ' + 'ipfix-reports ' + 'core-utilization')
                         commands.append('ipfix-reports ' + 'memory-utilization') if kwargs['memory-utilization'] else commands.append('no ' + 'ipfix-reports ' + 'memory-utilization')
                       else:
                           raise KeyError
                    except KeyError:
                           pass
            except ValueError:
                logger.error("Error in reporting format value")

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result_external_collector = self.fw.do_cli_commands(commands)
        return result_external_collector




































