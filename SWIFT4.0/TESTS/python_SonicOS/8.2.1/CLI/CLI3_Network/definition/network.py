import re

from utm import is_ipv4
from runner.settings import logger

def _get_version(kwargs):
    ver = ''
    if 'version' in kwargs.keys() and 'v6' in kwargs['version'].lower():
        ver = 'ipv6'
    if 'version' in kwargs.keys() and 'v4' in kwargs['version'].lower():
        ver = 'ipv4'
    return ver 


class WebproxyCli:
    '''WebproxyCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_webproxy(self, tag=0, **kwargs):
        commands = ['configure', 'web-proxy' ]
        if ('server' in kwargs.keys() and 
            'port' in kwargs.keys()):
            commands.append('server ' + kwargs['server'] + ' port ' + kwargs['port'])
        elif ('server' in kwargs.keys() and 
            'port' not in kwargs.keys()):
            logger.error('port must be specified with server.')
            return False
        elif ('server' not in kwargs.keys() and 'port'  in kwargs.keys()):
            logger.error('server must be specified with port.')
            return False
        else:
            pass 
        self.fw._is_key_exist(commands, kwargs, 'bypass-upon-failure')
        self.fw._is_key_exist(commands, kwargs, 'forward-public-requests')
    
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result

    def show_webproxy(self):
        commands = ['show web-proxy']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def add_user_proxy_server(self, *ips):
        commands = ['configure', 'web-proxy' ]
        for ip in ips:
            ip = "user-proxy-server " + ip
            commands.append(ip)
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result


class InterfaceCli:
    '''InterfaceCli class''' 
    
    def __init__(self, fw):
        self.fw = fw
        
    def config_interface(self, add_tag=False, **kwargs):
        if 'if' not in kwargs.keys() or 'zone' not in kwargs.keys():
            logger.error('if and zone must specified.')
        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'static'
        kwargs['if'] = kwargs['if'].upper()
        kwargs['zone'] = kwargs['zone'].upper()
        if kwargs['if'] == 'X0':
            kwargs['zone'] = 'LAN'
        elif kwargs['if'] == 'X1':
            kwargs['zone'] = 'WAN'
        elif kwargs['if'] == 'W0':
            kwargs['zone'] = 'WLAN'
        elif kwargs['if'] == 'MGMT':
            kwargs['zone'] = 'MGMT'            
        else:
            pass
        commands = ['configure', 'interface ' + kwargs['if']]

        if kwargs['mode'] != 'portshield' and kwargs['mode'] != 'nativebridge':
            commands.append('ip-assignment ' + kwargs['zone'] + ' ' + kwargs['mode'])
        if kwargs['zone'] == 'WAN':
            commands_if = self._get_interface_wan(**kwargs)
        elif kwargs['zone'] == 'WLAN':
            commands_if = self._get_interface_wlan(**kwargs)
        else:
            commands_if = self._get_interface_lan(**kwargs)
        if not commands_if:
            return False
        commands.extend(commands_if)
        if kwargs['mode'] != 'native':
            commands.extend(self._get_interface_management(**kwargs))
            commands.extend(self._get_interface_user(**kwargs))
        commands.extend(self._get_advance(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        if add_tag:
            return commands
        else:
            result = self.fw.do_cli_commands(commands)
            return result

    def unassign_interface(self, interface=None):
        commands = []
        if interface.upper() == 'X0' or interface.upper() == 'X1':
            logger.info('interface X0 or X1 cannot be unassigned')
        else:
            commands = ['configure', 'interface ' + interface.upper(), 'no ip-assignment']
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_interface(self, **kwargs):
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of vlan, wlan-tunnel, vpn-tunnel when add an interface.')
            return False
        if kwargs['type'] == 'vlan' and 'if' not in kwargs.keys():
            logger.error('Please specify if name.')
            return False
        commands = ['configure']
        if kwargs['type'] == 'vlan':
            commands_if = self._get_interface_vlan(**kwargs)
        elif kwargs['type'] == 'vpn-tunnel':
            commands_if = self._get_interface_vpntunnel(**kwargs)
        elif kwargs['type'] == 'wlan-tunnel':
            commands_if = self._get_interface_wti(**kwargs)
        elif kwargs['type'] == '4to6':
            commands_if = self._get_interface_4to6(**kwargs)
        else:
            logger.error('{} is not one of vlan, vpn-tunnel, wlan-tunnel, 4to6.'.format(kwargs['type']))

        commands.extend(commands_if)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_interface(self, **kwargs):
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of vlan, wlan-tunnel, vpn-tunnel, 4to6 when add an interface.')
            return False
        if kwargs['type'] == 'vlan' and 'if' not in kwargs.keys():
            logger.error('Please specify if name.')
            return False
        commands = ['configure']
        if kwargs['type'] == 'vlan':
            try:
                commands.append('no interface ' + kwargs['if'] + ' vlan ' + str(kwargs['vlan-tag']))
            except:
                print(kwargs['if'])
                logger.error('vlan-tag must be specified.')
        elif kwargs['type'] == 'wlan-tunnel':
            try:
                commands.append('no interface ' + kwargs['tunnel-name'])
            except:
                logger.error('tunnel-name must be specified.')
        elif kwargs['type'] == 'vpn-tunnel':
            try:
                commands.append('no tunnel-interface vpn ' + kwargs['tunnel-name'])
            except:
                logger.error('tunnel-name must be specified.')
        elif kwargs['type'] == '4to6':
            try:
                commands.append('no tunnel-interface 4to6 ' + kwargs['tunnel-name'])
            except:
                logger.error('tunnel-name must be specified.')    
        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    # add by cyuan
    def add_tunnel_interface_4to6(self,add_tag=False, **kwargs):#add by cyuan
        """
        name: test_tunnelif_4to6
        type:dslite # gre4to6
        bound_if:x1
        """
        commands = ['configure']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new = 'tunnel-interface 4to6',tag=True)

        if 'type' not in kwargs.keys():
            logger.error("Please specify type of one of dslite or gre4to6")
            return False

        if kwargs['type'] in ['dslite','gre4to6']:
            commands.append('type '+kwargs['type'])
            commands_if = self._get_tunnel_interface_4to6(**kwargs)
        else:
            logger.error('{} is not one of dslite, gre4to6'.format(kwargs['type']))

        commands.extend(commands_if)
        for command in ['end','commit','exit']:
            commands.append(command)
        if add_tag:
            return commands
        result = self.fw.do_cli_commands(commands)
        return result
  
    def add_tunnel_interface_ipv6(self, **kwargs):
        if 'type' not in kwargs.keys():
            logger.error('Please specify type to one of manual, 6rd, 6to4, gre, isatap.')
            return False
        if 'name' not in kwargs.keys():
            logger.error('Please specify the tunnel name.')
            return False
        commands = ['configure', 'tunnel-interface ipv6 ' + kwargs['name']]
        if kwargs['type'] == 'manual':
            commands_if = self._get_tunnel_interface_manual(**kwargs)
        elif kwargs['type'] == '6rd':
            commands_if = self._get_tunnel_interface_6rd(**kwargs)
        elif kwargs['type'] == 'gre':
            commands_if = self._get_tunnel_interface_gre(**kwargs)
        elif kwargs['type'] == '6to4':
            commands_if = self._get_tunnel_interface_6to4(**kwargs)
        elif kwargs['type'] == 'isatap':
            commands_if = self._get_tunnel_interface_isatap(**kwargs)
        else:
            logger.error('{} is not one of manual, 6to4, 6rd, gre, isatap.'.format(kwargs['type']))
        commands_if.extend(self._get_interface_management(**kwargs))
        commands_if.extend(self._get_interface_user(**kwargs))
        commands.extend(commands_if)
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result
 
    def edit_tunnel_interface_ipv6(self, **kwargs):
        if 'name' not in kwargs.keys():
            print(kwargs)
            logger.error('Please specify the tunnel name.')
            return False
        commands = ['configure', 'tunnel-interface ipv6 ' + kwargs['name']]
        if kwargs['type'] == 'manual':
            commands_if = self._get_tunnel_interface_manual(**kwargs, tag=False)
        elif kwargs['type'] == '6rd':
            commands_if = self._get_tunnel_interface_6rd(**kwargs, tag=False)
        elif kwargs['type'] == 'gre':
            commands_if = self._get_tunnel_interface_gre(**kwargs, tag=False)
        elif kwargs['type'] == '6to4':
            commands_if = self._get_tunnel_interface_6to4(**kwargs, tag=False)
        elif kwargs['type'] == 'isatap':
            commands_if = self._get_tunnel_interface_isatap(**kwargs, tag=False)
        commands_if.extend(self._get_interface_management(**kwargs))
        commands_if.extend(self._get_interface_user(**kwargs))
        commands.extend(commands_if)
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_tunnel_interface_ipv6(self, name=None):
        commands = ['configure', 'no tunnel-interface ipv6 ' + name]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def config_interface_ipv6(self, add_tag=False, **kwargs):
        if 'if' not in kwargs.keys() or 'zone' not in kwargs.keys():
            logger.error('if and zone must specified.')
        if 'mode' not in kwargs.keys():
            kwargs['mode'] = 'static'
        kwargs['if'] = kwargs['if'].upper()
        kwargs['zone'] = kwargs['zone'].upper()
        if kwargs['if'] == 'X0':
            kwargs['zone'] = 'LAN'
        elif kwargs['if'] == 'X1':
            kwargs['zone'] = 'WAN'
        elif kwargs['if'] == 'W0':
            kwargs['zone'] = 'WLAN'
        elif kwargs['if'] == 'MGMT':
            kwargs['zone'] = 'MGMT'            
        else:
            pass
        commands = ['configure', 'interface ipv6 ' + kwargs['if'], 'ip-assignment ' + kwargs['mode']]   
        if kwargs['zone'] == 'WAN':
            commands_if = self._get_interface_wan_ipv6(**kwargs)
        elif kwargs['zone'] == 'WLAN':
            commands_if = self._get_interface_wlan_ipv6(**kwargs)
        else:
            commands_if = self._get_interface_lan_ipv6(**kwargs)
        # if not commands_if:
        #     return False
        commands.extend(commands_if)
        commands.extend(self._get_interface_management(**kwargs))
        commands.extend(self._get_interface_user(**kwargs))
        commands.extend(self._get_advance_ipv6(**kwargs))
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        if add_tag:
            return commands
        else:
            result = self.fw.do_cli_commands(commands)
            return result

    def _get_interface_wan(self, **kwargs):
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_wan_static(**kwargs)
        elif kwargs['mode'] == 'dhcp':
            commands_if = self._get_interface_wan_dhcp(**kwargs)
        elif kwargs['mode'] == 'l2tp':
            commands_if = self._get_interface_wan_l2tp(**kwargs)
        elif kwargs['mode'] == 'pptp':
            commands_if = self._get_interface_wan_pptp(**kwargs) 
        elif kwargs['mode'] == 'pppoe':
            commands_if = self._get_interface_wan_pppoe(**kwargs)
        elif kwargs['mode'] == 'wire-mode':
            commands_if = self._get_interface_wiremode(**kwargs)
        elif kwargs['mode'] == 'tap-mode':
            commands_if = self._get_interface_tapmode(**kwargs)    
        else:
            logger.error('Make sure wan mode is one of: static, l2tp, pptp, pppoe, wire-mode, tap-mode.')
            return False        
        return commands_if

    def _get_interface_lan(self, **kwargs):
        commands_if = []
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_lan_static(**kwargs)
        elif kwargs['mode'] == 'transparent':
            commands_if = self._get_interface_lan_transparent(**kwargs)
        elif kwargs['mode'] == 'l2bridge':
            commands_if = self._get_interface_lan_l2bridge(**kwargs)
        elif kwargs['mode'] == 'wire-mode':
            commands_if = self._get_interface_wiremode(**kwargs)
        elif kwargs['mode'] == 'tap-mode':
            commands_if = self._get_interface_tapmode(**kwargs)    
        elif kwargs['mode'] == 'unnumbered':
            commands_if = self._get_interface_lan_unnumber(**kwargs)    
        elif kwargs['mode'] == 'portshield':
            commands_if = self._get_interface_lan_portshield(**kwargs)    
        elif kwargs['mode'] == 'nativebridge':
            commands_if = self._get_interface_lan_native(**kwargs)
        else:
            logger.error('Make sure lan mode {} is one of: static, transparent, l2bridge, wire-mode, tap-mode, unnumbered, portshield, nativebridge.'.format(kwargs['mode']))
            return False 
        return commands_if

    def _get_interface_wlan(self, **kwargs):
        commands_if = []
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_lan_static(**kwargs)
        elif kwargs['mode'] == 'l2bridge':
            commands_if = self._get_interface_lan_l2bridge(**kwargs)
        elif kwargs['mode'] == 'portshield':
            commands_if = self._get_interface_lan_portshield(**kwargs)    
        elif kwargs['mode'] == 'nativebridge':
            commands_if = self._get_interface_lan_native(**kwargs)
        else:
            logger.error('Make sure lan mode {} is one of: static, l2bridge, portshield, nativebridge.'.format(kwargs['mode']))
            return False
        if kwargs['mode'] == 'static' or kwargs['mode'] == 'l2bridge':
            self.fw._is_key_exist(commands_if, kwargs, 'sp-limit', key_new='sonicpoint limit')
            if 'sp-reserve-address' in kwargs.keys():
                if kwargs['sp-reserve-address'] == 'manual':
                    if 'sp-reserve-ip' not in kwargs.keys():
                        logger.error('sp-reserve-ip must be specified when manual method.')
                    commands_if.append('sonicpoint reserve-address manual ' + kwargs['sp-reserve-ip'])
                else:
                    commands_if.append('sonicpoint reserve-address dynamic')
        return commands_if

    def _get_interface_wan_static(self, **kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')            
            return False
        elif 'netmask' in kwargs.keys():
            commands_static = ['ip ' + kwargs['ip'] + ' netmask ' + kwargs['netmask']]
        else:
            commands_static = ['ip ' + kwargs['ip'] + ' netmask 255.255.255.0']
        self.fw._is_key_exist(commands_static, kwargs, 'gateway')
        self.fw._is_key_exist(commands_static, kwargs, 'dns1', key_new='dns primary')
        self.fw._is_key_exist(commands_static, kwargs, 'dns2', key_new='dns secondary')
        self.fw._is_key_exist(commands_static, kwargs, 'dns3', key_new='dns tertiary')
        commands_static.append('exit')
        return commands_static

    def _get_interface_wan_dhcp(self, **kwargs):
        commands_dhcp = []
        self.fw._is_key_exist(commands_dhcp, kwargs, 'hostname')
        self.fw._is_key_exist(commands_dhcp, kwargs, 'comment')
        self.fw._is_key_exist(commands_dhcp, kwargs, 'renew-on-link-up')
        self.fw._is_key_exist(commands_dhcp, kwargs, 'renew-on-startup')
        commands_dhcp.append('exit')
        return commands_dhcp

    def _get_interface_wan_pppoe(self, **kwargs):
        commands_pppoe = []
        if ('pppoe-ip' in kwargs.keys() and kwargs['pppoe-ip'] == 'dynamic'):
            commands_pppoe = ['dynamic']
        elif ('pppoe-ip' in kwargs.keys() and is_ipv4(kwargs['pppoe-ip'])):
            commands_pppoe = ['no dynamic', 'ip ' + kwargs['pppoe-ip']]
        self.fw._is_key_exist(commands_pppoe, kwargs, 'unnumbered')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-uname', key_new='user-name')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-servicename', key_new='service-name')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-passwd', key_new='password')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-lcp-echo-packets', key_new='lcp-echo-packets')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-inactivity', key_new='inactivity')
        self.fw._is_key_exist(commands_pppoe, kwargs, 'pppoe-reconnect', key_new='reconnect')
        if 'pppoe-schedule' in kwargs.keys():
            rc = re.search(r"(.*) (\d{2}:\d{2})? to (\d{2}:\d{2})?", kwargs['pppoe-schedule'])
            if rc:
                commands_pppoe.append('schedule days ' + rc.group(1) + ' time ' + rc.group(2) + ' ' + rc.group(3))
            else:
                commands_pppoe.append('schedule ' + kwargs['pppoe-schedule'])
        commands_pppoe.append('exit')
        return commands_pppoe

    def _get_interface_wan_l2tp(self, **kwargs):
        commands_l2tp = []
        if ('l2tp-ip' in kwargs.keys() and kwargs['l2tp-ip'] == 'dynamic'):
            commands_l2tp = ['dynamic']
        elif ('l2tp-ip' in kwargs.keys() and is_ipv4(kwargs['l2tp-ip'])):
            if 'netmask' in kwargs.keys():
                commands_l2tp = ['no dynamic', 'ip ' + kwargs['l2tp-ip'] + ' netmask ' + kwargs['l2tp-netmask']]
            else:
                commands_l2tp = ['no dynamic', 'ip ' + kwargs['l2tp-ip'] + ' netmask 255.255.255.0']
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-name', key_new='user-name')
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-server', key_new='server', tag=True)
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-passwd', key_new='password')
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-shared-secret', key_new='shared-secret')
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-hostname', key_new='hostname')
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-gateway', key_new='gateway')
        self.fw._is_key_exist(commands_l2tp, kwargs, 'l2tp-inactivity', key_new='inactivity')
        commands_l2tp.append('exit')      
        return commands_l2tp     

    def _get_interface_wan_pptp(self, **kwargs):
        commands_pptp = []
        if ('pptp-ip' in kwargs.keys() and kwargs['pptp-ip'] == 'dynamic'):
            commands_pptp = ['dynamic']
        elif ('pptp-ip' in kwargs.keys() and is_ipv4(kwargs['pptp-ip'])):
            if 'netmask' in kwargs.keys():
                commands_pptp = ['no dynamic', 'ip ' + kwargs['pptp-ip'] + ' netmask ' + kwargs['pptp-netmask']]
            else:
                commands_pptp = ['no dynamic', 'ip ' + kwargs['pptp-ip'] + ' netmask 255.255.255.0']
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-name', key_new='user-name')
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-server', key_new='server', tag=True)
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-passwd', key_new='user-name')
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-hostname', key_new='password')
        # if 'pptp-subnet' not in kwargs.keys():
            # kwargs['pptp-subnet'] = '255.255.255.0'
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-subnet', key_new='subnet')
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-gateway', key_new='gateway')
        self.fw._is_key_exist(commands_pptp, kwargs, 'pptp-inactivity', key_new='inactivity')
        commands_pptp.append('exit')
        return commands_pptp

    def _get_interface_wiremode(self, **kwargs):
        commands_wm = []
        self.fw._is_key_exist(commands_wm, kwargs, 'type')
        self.fw._is_key_exist(commands_wm, kwargs, 'linkstate-propagation')
        if 'type' in kwargs.keys():
            if kwargs['type'] == 'inspect' or kwargs['type'] == 'secure':
                self.fw._is_key_exist(commands_wm, kwargs, 'stateful-inspection')
            elif kwargs['type'] == 'inspect':
                self.fw._is_key_exist(commands_wm, kwargs, 'restrict-analysis')
        self.fw._is_key_exist(commands_wm, kwargs, 'paired-interface', tag=True)
        self.fw._is_key_exist(commands_wm, kwargs, 'paired-interface-zone')
        commands_wm.append('exit')
        return commands_wm 

    def _get_interface_tapmode(self, **kwargs):
        commands_tm = []
        self.fw._is_key_exist(commands_tm, kwargs, 'stateful-inspection')
        commands_tm.append('exit')
        return commands_tm     

    def _get_interface_lan_static(self, **kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')            
            return False
        elif 'netmask' in kwargs.keys():
            commands_static = ['ip ' + kwargs['ip'] + ' netmask ' + kwargs['netmask']]
        else:
            commands_static = ['ip ' + kwargs['ip'] + ' netmask 255.255.255.0']
        self.fw._is_key_exist(commands_static, kwargs, 'gateway')
        commands_static.append('exit')
        self.fw._is_key_exist(commands_static, kwargs, 'comment')
        self.fw._is_key_exist(commands_static,kwargs, 'management https')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'management ping')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'management snmp')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'management ssh')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'user_login_http', key_new = 'user-login http')
        self.fw._is_key_exist(commands_static,kwargs, 'user_login_https',key_new = 'user-login https')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'shutdown-port')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'auto-discovery')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'multicast')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'cos-8021p')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'exclude-route')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'link-speed')# link-speed full 1000
        self.fw._is_key_exist(commands_static,kwargs, 'mac')# mac default/ mac override 00:11:22:33:44:55
        self.fw._is_key_exist(commands_static,kwargs, 'flow-reporting')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'mtu') #mtu:580..1500
        self.fw._is_key_exist(commands_static,kwargs, 'management-traffic-only')# true/false
        self.fw._is_key_exist(commands_static,kwargs, 'asymmertric-route') # true/false
        self.fw._is_key_exist(commands_static,kwargs, 'fqdn-assignment',key_new = 'management fqdn-assignment')#fqdn-assignment 'aaa.com'
       
        return commands_static

    def _get_interface_lan_transparent(self, **kwargs):
        commands_tp = []
        self.fw._is_key_exist(commands_tp, kwargs, 'transparent-range')
        self.fw._is_key_exist(commands_tp, kwargs, 'gratuitous-arp-wan-forwarding')
        self.fw._is_key_exist(commands_tp, kwargs, 'gratuitous-arp-wan-generation')
        commands_tp.append('exit')
        return commands_tp        

    def _get_interface_lan_l2bridge(self, **kwargs):
        commands_l2b = []
        self.fw._is_key_exist(commands_l2b, kwargs, 'bridge-to')
        self.fw._is_key_exist(commands_l2b, kwargs, 'block-non-ip')
        self.fw._is_key_exist(commands_l2b, kwargs, 'only-sniff')
        self.fw._is_key_exist(commands_l2b, kwargs, 'route-on-bridge-pair')
        if kwargs['zone'].lower() == 'lan':
            self.fw._is_key_exist(commands_l2b, kwargs, 'stateful-inspection')
            self.fw._is_key_exist(commands_l2b, kwargs, 'vlan-filtering-mode')
            if 'filter-vlans' in kwargs.keys(): 
                for each in kwargs['filter-vlans']:
                    commands_l2b.append('filtered-vlan ' + str(each))
            if 'no-filter-vlans' in kwargs.keys(): 
                for each in kwargs['no-filter-vlans']:
                    commands_l2b.append('no filtered-vlan ' + str(each))
        commands_l2b.append('exit')
        return commands_l2b 

    def _get_interface_lan_unnumber(self, **kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')            
            return False
        elif 'netmask' in kwargs.keys():
            commands_unm = ['ip ' + kwargs['ip'] + ' netmask ' + kwargs['netmask']]
        else:
            commands_unm = ['ip ' + kwargs['ip'] + ' netmask 255.255.255.0']
        self.fw._is_key_exist(commands_unm, kwargs, 'gateway')
        commands_unm.append('exit')
        return commands_unm

    def _get_interface_lan_portshield(self, **kwargs):
        commands_port = ['ip-assignment ' + kwargs['zone'] + ' ' + kwargs['mode'] + ' ' + kwargs['portsheild-to']]
        return commands_port

    def _get_interface_lan_native(self, **kwargs):
        commands_native = ['native-bridge ' + kwargs['bridge-to']]
        self.fw._is_key_exist(commands_native, kwargs, 'firewalling')
        return commands_native

    def _get_interface_vlan(self, **kwargs):
        if 'vlan-tag' not in kwargs.keys():
            kwargs['vlan-tag'] = '100'
        commands_vlan = ['interface ' + kwargs['if'] + ' ' + kwargs['type'] + ' ' + str(kwargs['vlan-tag'])]
        commands_if = self.config_interface(add_tag=True, **kwargs)
        del commands_if[1]
        del commands_if[0]
        commands_vlan.extend(commands_if)
        return commands_vlan

    def _get_interface_vpntunnel(self, **kwargs):
        if 'vpn-policy' not in kwargs.keys():
            logger.error('vpn-policy must be specified when add a vpn tunnel.')
        if 'tunnel-name' not in kwargs.keys():
            logger.info('tunnel-name is not specified, use test as default name.')
            kwargs['tunnel-name'] = 'vpn-testpolicy'
        commands_vpn = ['tunnel-interface vpn ' + kwargs['tunnel-name']]
        self.fw._is_key_exist(commands_vpn, kwargs, 'vpn-policy', key_new='policy', tag=True)
        if 'ip' in kwargs.keys():
            commands_vpn.append('ip-assignment VPN static')
            if 'netmask' in kwargs.keys():
                commands_vpn.append('ip ' + kwargs['ip'] + ' netmask ' + kwargs['netmask'])
            else:
                commands_vpn.append('ip ' + kwargs['ip'])
            commands_vpn.append('exit')
        self.fw._is_key_exist(commands_vpn, kwargs, 'flow-reporting')
        self.fw._is_key_exist(commands_vpn, kwargs, 'multicast')
        self.fw._is_key_exist(commands_vpn, kwargs, 'asymmetric-route')
        self.fw._is_key_exist(commands_vpn, kwargs, 'fragment-packets')
        self.fw._is_key_exist(commands_vpn, kwargs, 'ignore-df-bit')
        commands_vpn.extend(self._get_interface_user(**kwargs))
        commands_vpn.extend(self._get_interface_management(**kwargs))
        commands_vpn.extend(['end', 'commit', 'exit'])
        return commands_vpn

    def _get_tunnel_interface_manual(self, tag=True, **kwargs):
        commands_manual = []
        self.fw._is_key_exist(commands_manual, kwargs, 'zone')
        if not tag:
            self.fw._is_key_exist(commands_manual, kwargs, 'name-new', key_new='name')
        self.fw._is_key_exist(commands_manual, kwargs, 'comment')
        commands_manual.append('type manual')
        self.fw._is_key_exist(commands_manual, kwargs, 'bound-to')
        self.fw._is_key_exist(commands_manual, kwargs, 'ip', tag=tag)
        self.fw._is_key_exist(commands_manual, kwargs, 'prefix-length')
        self.fw._is_key_exist(commands_manual, kwargs, 'remote-ipv4', key_new='remote ipv4-address name', tag=tag)
        self.fw._is_key_exist(commands_manual, kwargs, 'remote-ipv6', key_new='remote ipv6-network', tag=tag)
        self.fw._is_key_exist(commands_manual, kwargs, 'link-mtu')
        commands_manual.append('exit')
        return commands_manual

    def _get_tunnel_interface_6rd(self, tag=True, **kwargs):
        commands_6rd = []
        if not tag:
            self.fw._is_key_exist(commands_6rd, kwargs, 'name-new', key_new='name')
        self.fw._is_key_exist(commands_6rd, kwargs, 'zone')
        commands_6rd.append('type 6rd')
        self.fw._is_key_exist(commands_6rd, kwargs, 'bound-to')
        self.fw._is_key_exist(commands_6rd, kwargs, 'ip', tag=tag)
        self.fw._is_key_exist(commands_6rd, kwargs, 'prefix-length')
        self.fw._is_key_exist(commands_6rd, kwargs, 'default-route')
        self.fw._is_key_exist(commands_6rd, kwargs, 'link-mtu')
        self.fw._is_key_exist(commands_6rd, kwargs, 'comment')

        if 'mode' in kwargs.keys():
            if kwargs['mode'] == 'manual':
                commands_6rd.append('no dynamic')
                self.fw._is_key_exist(commands_6rd, kwargs, '6rd-prefix', key_new='6rd prefix', tag=tag)
                self.fw._is_key_exist(commands_6rd, kwargs, '6rd-prefix-length', key_new='6rd prefix-length', tag=tag)
                self.fw._is_key_exist(commands_6rd, kwargs, 'border-relay-ipv4-address', tag=tag)
                self.fw._is_key_exist(commands_6rd, kwargs, 'mask-length', tag=tag)
            else:
                commands_6rd.append('dynamic')
        return commands_6rd

    def _get_tunnel_interface_6to4(self, tag=True, **kwargs):
        commands_6o4 = []
        self.fw._is_key_exist(commands_6o4, kwargs, 'zone')
        if not tag:
            self.fw._is_key_exist(commands_6o4, kwargs, 'name-new', key_new='name')
        self.fw._is_key_exist(commands_6o4, kwargs, 'comment')
        commands_6o4.append('type 6to4')
        self.fw._is_key_exist(commands_6o4, kwargs, 'bound-to')
        self.fw._is_key_exist(commands_6o4, kwargs, 'prefix-length')
        self.fw._is_key_exist(commands_6o4, kwargs, 'enable')
        self.fw._is_key_exist(commands_6o4, kwargs, 'link-mtu')
        commands_6o4.append('exit')
        return commands_6o4

    def _get_tunnel_interface_gre(self, tag=True, **kwargs):
        commands_manual = []
        self.fw._is_key_exist(commands_manual, kwargs, 'zone')
        if not tag:
            self.fw._is_key_exist(commands_manual, kwargs, 'name-new', key_new='name')
        self.fw._is_key_exist(commands_manual, kwargs, 'comment')
        commands_manual.append('type gre')
        self.fw._is_key_exist(commands_manual, kwargs, 'bound-to')
        self.fw._is_key_exist(commands_manual, kwargs, 'ip', tag=tag)
        self.fw._is_key_exist(commands_manual, kwargs, 'prefix-length')
        self.fw._is_key_exist(commands_manual, kwargs, 'remote-ipv4', key_new='remote ipv4-address name', tag=tag)
        self.fw._is_key_exist(commands_manual, kwargs, 'remote-ipv6', key_new='remote ipv6-network', tag=tag)
        commands_manual.append('exit')
        return commands_manual

    def _get_tunnel_interface_isatap(self, tag=True, **kwargs):
        commands_manual = []
        self.fw._is_key_exist(commands_manual, kwargs, 'zone')
        if not tag:
            self.fw._is_key_exist(commands_manual, kwargs, 'name-new', key_new='name')
        self.fw._is_key_exist(commands_manual, kwargs, 'comment')
        commands_manual.append('type isatap')
        self.fw._is_key_exist(commands_manual, kwargs, 'bound-to')
        self.fw._is_key_exist(commands_manual, kwargs, 'prefix')
        self.fw._is_key_exist(commands_manual, kwargs, 'link-mtu')
        commands_manual.append('exit')
        return commands_manual
        
    def _get_interface_wti(self, **kwargs):
        if 'tunnel-id' not in kwargs.keys():
            logger.error('tunnel-id must be specified when add a wlan tunnel.')
            kwargs['tunnel-id'] = '0'
        if 'tunnel-if' not in kwargs.keys():
            logger.error('tunnel-if must be specified when add a wlan tunnel.')
            kwargs['tunnel-if'] = 'X0'
        commands_wti = ['interface ' + kwargs['tunnel-if'] + ' tunnel ' + kwargs['tunnel-id']]
        kwargs['if'] = ''
        commands_if = self.config_interface(add_tag=True, **kwargs)
        del commands_if[1]
        del commands_if[0]   
        commands_wti.extend(commands_if)
        return commands_wti

    def _get_interface_4to6(self, **kwargs):
        if 'tunnel-name' not in kwargs.keys():
            logger.error('name must be specified when add a 4to6 tunnel.')
            kwargs['tunnel-name'] = 'test-4to6'
        commands_4to6 = ['tunnel-interface 4to6 ' + kwargs['tunnel-name']]
        if 'tunnel-type' in kwargs.keys():
            commands_4to6.append('type ' + kwargs['tunnel-type'])
            self.fw._is_key_exist(commands_4to6, kwargs, 'bound-to')
            self.fw._is_key_exist(commands_4to6, kwargs, 'local-ipv6', key_new='local')
            self.fw._is_key_exist(commands_4to6, kwargs, 'comment')
            if kwargs['tunnel-type'] == 'dslite':
                self.fw._is_key_exist(commands_4to6, kwargs, 'aftr-addr', key_new='remote')
                self.fw._is_key_exist(commands_4to6, kwargs, 'local-ipv4')
            elif kwargs['tunnel-type'] == 'gre4to6':
                self.fw._is_key_exist(commands_4to6, kwargs, 'ip-ipv4', key_new='ip')
                self.fw._is_key_exist(commands_4to6, kwargs, 'remote', key_new='remote ipv6')
            commands_4to6.append('exit')
        self.fw._is_key_exist(commands_4to6, kwargs, 'flow-reporting')
        self.fw._is_key_exist(commands_4to6, kwargs, 'fragment-packets')
        self.fw._is_key_exist(commands_4to6, kwargs, 'ignore-df-bit')
        self.fw._is_key_exist(commands_4to6, kwargs, 'send-icmp-fragmentation')

        commands_4to6.extend(['end', 'commit', 'exit'])
        return commands_4to6
    # add by cyuan
    def _get_tunnel_interface_4to6(self,**kwargs):
        commands_4to6 = []
        
        if kwargs['type'] == 'dslite':
            self.fw._is_key_exist(commands_4to6, kwargs, 'local-ipv4',tag=True)
        else:
            if 'ip'in kwargs.keys() and 'netmask' in kwargs.keys():
                commands_4to6.append('ip '+kwargs['ip']+' netmask '+kwargs['netmask'])
            else:
                logger.error('{} and {} must be specify.'.format('ip','netmask'))
        self.fw._is_key_exist(commands_4to6, kwargs, 'bound-if', key_new='bound-to interface',tag=True)
        self.fw._is_key_exist(commands_4to6, kwargs, 'local-ipv6', key_new = 'local', tag =True)
        self.fw._is_key_exist(commands_4to6, kwargs, 'remote', key_new='remote ipv6',tag=True)
        self.fw._is_key_exist(commands_4to6,kwargs, 'comment')
        commands_4to6.append('commit')
        commands_4to6.append('exit')
        self.fw._is_key_exist(commands_4to6,kwargs, 'flow-reporting')
        self.fw._is_key_exist(commands_4to6,kwargs, 'fragment-packets')
        self.fw._is_key_exist(commands_4to6,kwargs, 'ignore-df-bit')
        self.fw._is_key_exist(commands_4to6,kwargs, 'send-icmp-fragmentation') 
        return commands_4to6
        
    def _get_interface_lan_ipv6(self, **kwargs):
        commands_if = []
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_lan_static_ipv6(**kwargs)
        elif kwargs['mode'] == 'dhcpv6':
            commands_if = self._get_interface_dhcpv6(**kwargs)
        # elif kwargs['mode'] == 'wire-mode':
        #     commands_if = self._get_interface_wiremode_ipv6(**kwargs)
        # elif kwargs['mode'] == 'tap-mode':
        #     commands_if = self._get_interface_tapmode_ipv6(**kwargs)    
        # else:
            logger.error('Make sure lan mode {} is one of: static, dhcpv6, wire-mode, tap-mode.'.format(kwargs['mode']))
            return False 
        return commands_if

    def _get_interface_wan_ipv6(self, **kwargs):
        commands_if = []
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_wan_static_ipv6(**kwargs)
        elif kwargs['mode'] == 'dhcpv6':
            commands_if = self._get_interface_dhcpv6(**kwargs)
        elif kwargs['mode'] == 'auto':
            pass
        elif kwargs['mode'].lower() == 'pppoe6':
            commands_if = self._get_interface_wan_pppoe6(**kwargs)
        # elif kwargs['mode'] == 'wire-mode':
        #     commands_if = self._get_interface_wiremode_ipv6(**kwargs)
        # elif kwargs['mode'] == 'tap-mode':
        #     commands_if = self._get_interface_tapmode_ipv6(**kwargs)    
        else:
            logger.error('Make sure wan mode is one of: static, dhcpv6, pppoe6, auto, wire-mode, tap-mode.')
        return commands_if

    def _get_interface_wlan_ipv6(self, **kwargs):
        commands_if = []
        if kwargs['mode'] == 'static':
            commands_if = self._get_interface_lan_static(**kwargs)
        else:
            logger.error('Make sure lan mode {} is static.'.format(kwargs['mode']))
            return False
        return commands_if

    def _get_interface_wan_static_ipv6(self, **kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')            
            return False
        else:
            commands_static = ['ip ' + kwargs['ip']]
        if 'prefix-length' in kwargs.keys():
            commands_static.append('prefix-length ' + str(kwargs['prefix-length']))
        else:
            commands_static.append('prefix-length 64')
        self.fw._is_key_exist(commands_static, kwargs, 'gateway')
        self.fw._is_key_exist(commands_static, kwargs, 'dns1', key_new='dns primary')
        self.fw._is_key_exist(commands_static, kwargs, 'dns2', key_new='dns secondary')
        self.fw._is_key_exist(commands_static, kwargs, 'dns3', key_new='dns tertiary')
        self.fw._is_key_exist(commands_static, kwargs, 'subnet-prefix', key_new='advertise subnet-prefix')
        if 'router-advertisement' in kwargs.keys():
            commands_static.extend(self._get_router_advertisement(**kwargs))
        if 'add_address' in kwargs.keys():
            commands_static.extend(self._get_add_address(**kwargs))
        if 'del_address' in kwargs.keys():
            for each in kwargs['del_address']:
                commands_static.append('no extra-ip ' + each)
               
        commands_static.append('exit')
        return commands_static        

    def _get_interface_dhcpv6(self, **kwargs):
        commands_dhcpv6 = []
        if 'prefix-delegation' in kwargs.keys():
            if kwargs['prefix-delegation']:
                commands_dhcpv6.append('prefix-delegation')
                self.fw._is_key_exist(commands_dhcpv6, kwargs, 'preferred-send-hints', key_new='send-hints')
                if 'preferred-delegation-prefix' in kwargs.keys():
                    commands_dhcpv6.append('preferred ' + kwargs['preferred-delegation-prefix'])
                commands_dhcpv6.append('exit')
            else:
                commands_dhcpv6.append('no prefix-delegation')
        self.fw._is_key_exist(commands_dhcpv6, kwargs, 'rapid-commit')
        self.fw._is_key_exist(commands_dhcpv6, kwargs, 'send-hints')
        self.fw._is_key_exist(commands_dhcpv6, kwargs, 'dhcpv6-mode', key_new='mode')
        self.fw._is_key_exist(commands_dhcpv6, kwargs, 'info-only')
        self.fw._is_key_exist(commands_dhcpv6, kwargs, 'aftr-name-option')
        commands_dhcpv6.append('exit')
        return commands_dhcpv6
  
    def _get_interface_wan_pppoe6(self, **kwargs):
        commands_pppoe = []
        if 'pppoe-schedule' in kwargs.keys():
            rc = re.search(r"(.*) (\d{2}:\d{2})? to (\d{2}:\d{2})?", kwargs['pppoe-schedule'])
            if rc:
                commands_pppoe.append('schedule days ' + rc.group(1) + ' time ' + rc.group(2) + ' ' + rc.group(3))
            else:
                commands_pppoe.append('schedule ' + kwargs['pppoe-schedule']) 
        if 'mode-assignment' in kwargs:
            commands_pppoe.append('mode-assignment ' + kwargs['mode-assignment'])
            if kwargs['mode-assignment'] == 'dhcpv6':
                commands_pppoe.extend(self._get_interface_dhcpv6(**kwargs))
            elif kwargs['mode-assignment'] == 'static':
                commands_pppoe.extend(self._get_interface_wan_static_ipv6(**kwargs))
            else:
                pass     
        return commands_pppoe

    def _get_interface_lan_static_ipv6(self, **kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('Interface ip should be specified when static mode.')            
            return False
        else:
            commands_static = ['ip ' + kwargs['ip']]
        if 'prefix-length' in kwargs.keys():
            commands_static.append('prefix-length ' + str(kwargs['prefix-length']))
        else:
            commands_static.append('prefix-length 64')
        self.fw._is_key_exist(commands_static, kwargs, 'subnet-prefix', key_new='advertise subnet-prefix')
        if 'router-advertisement' in kwargs.keys():
            commands_static.extend(self._get_router_advertisement(**kwargs))
        if 'add_address' in kwargs.keys():
            commands_static.extend(self._get_add_address(**kwargs))
        if 'del_address' in kwargs.keys():
            for each in kwargs['del_address']:
                commands_static.append('no extra-ip ' + each)
        commands_static.append('exit')
        return commands_static 

    def _get_interface_wiremode_ipv6(self, **kwargs):
        pass

    def _get_interface_tapmode_ipv6(self, **kwargs):
        pass

    def _get_interface_management(self, **kwargs):
        commands_mgmt = []
        self.fw._is_key_exist(commands_mgmt, kwargs, 'mgmt-https', key_new='management https')
        self.fw._is_key_exist(commands_mgmt, kwargs, 'mgmt-http', key_new='management http')
        self.fw._is_key_exist(commands_mgmt, kwargs, 'mgmt-snmp', key_new='management snmp')
        self.fw._is_key_exist(commands_mgmt, kwargs, 'mgmt-ping', key_new='management ping')
        self.fw._is_key_exist(commands_mgmt, kwargs, 'mgmt-ssh', key_new='management ssh')
        return commands_mgmt

    def _get_interface_user(self, **kwargs):
        commands_user = []
        self.fw._is_key_exist(commands_user, kwargs, 'user-https', key_new='user-login https')
        self.fw._is_key_exist(commands_user, kwargs, 'user-http', key_new='user-login http') # edit by cyuan, correct the Spelling mistakes
        self.fw._is_key_exist(commands_user, kwargs, 'https-redirect')
        return commands_user

    def _get_advance(self, **kwargs):
        commands_adv = []
        # self.fw._is_key_exist(commands_adv, kwargs, 'link-speed', key_new='user-login https')
        if 'link-speed' in kwargs.keys():
            rc = re.search(r'(\d*)-(full|half)', kwargs['link-speed'])
            if rc:
                commands_adv.append('link-speed ' + rc.group(2) + ' ' + rc.group(1))
            else:
                commands_adv.append('link-speed auto')
        if 'mac' in kwargs.keys():
            if re.search(r':', kwargs['mac']):
                commands_adv.append('mac override ' + kwargs['mac'])
            else:
                commands_adv.append('mac default')
        self.fw._is_key_exist(commands_adv, kwargs, 'shutdown-port')
        self.fw._is_key_exist(commands_adv, kwargs, 'flow-reporting')
        self.fw._is_key_exist(commands_adv, kwargs, 'multicast')
        self.fw._is_key_exist(commands_adv, kwargs, '8021p', key_new='cos-8021p')
        self.fw._is_key_exist(commands_adv, kwargs, 'exclude-route')
        self.fw._is_key_exist(commands_adv, kwargs, 'asymmetric-route')
        if 'port' in kwargs.keys():
            if kwargs['port'] == 'aggregation':
                try:
                    commands_adv.append('port aggregation aggregate 1 ' + kwargs['port-aggregation'])
                except:
                    pass
            elif kwargs['port'] == 'redundancy':
                try:
                    commands_adv.append('port redundancy ' + kwargs['port-redundancy'])
                except:
                    pass
            else:
                commands_adv.append('no port redundancy-aggregation')
        self.fw._is_key_exist(commands_adv, kwargs, 'mtu')
        if kwargs['zone'].upper() == 'WAN':
            self.fw._is_key_exist(commands_adv, kwargs, 'fragment-packets')
            self.fw._is_key_exist(commands_adv, kwargs, 'ignore-df-bit')
            self.fw._is_key_exist(commands_adv, kwargs, 'send-icmp-fragmentation')
        elif kwargs['zone'].upper() == 'LAN' and kwargs['mode'] == 'static':
            self.fw._is_key_exist(commands_adv, kwargs, 'routed-mode')
        if kwargs['mode'] == 'dhcp':
            self.fw._is_key_exist(commands_adv, kwargs, 'force-discover-interval')
            self.fw._is_key_exist(commands_adv, kwargs, 'initiate-renewals-with-discover')
        self.fw._is_key_exist(commands_adv, kwargs, 'bwm-ingress', key_new='bandwidth-management ingress')
        self.fw._is_key_exist(commands_adv, kwargs, 'bwm-egress', key_new='bandwidth-management egress')
        return commands_adv

    def _get_advance_ipv6(self, **kwargs):
        commands_adv = []
        self.fw._is_key_exist(commands_adv, kwargs, 'ipv6-traffic')
        self.fw._is_key_exist(commands_adv, kwargs, 'listen-router-advertisement')
        self.fw._is_key_exist(commands_adv, kwargs, 'stateless-address-autoconfig')
        self.fw._is_key_exist(commands_adv, kwargs, 'duplicate-address-detection-transmits')
        self.fw._is_key_exist(commands_adv, kwargs, 'ndp-reachable-time', key_new='reachable-time')
        self.fw._is_key_exist(commands_adv, kwargs, 'ndp-size', key_new='max ndp-size')
        return commands_adv
 
    def _get_router_advertisement(self, **kwargs):
        commands_ra = ['router-advertisement']
        if kwargs['router-advertisement']:
            commands_ra.append('enable')
            self.fw._is_key_exist(commands_ra, kwargs, 'interval-min', key_new='interval min')
            self.fw._is_key_exist(commands_ra, kwargs, 'interval-max', key_new='interval max')
            self.fw._is_key_exist(commands_ra, kwargs, 'link-mtu')
            self.fw._is_key_exist(commands_ra, kwargs, 'reachable-time')
            self.fw._is_key_exist(commands_ra, kwargs, 'retransmit-timer')
            self.fw._is_key_exist(commands_ra, kwargs, 'current-hop-limit')
            self.fw._is_key_exist(commands_ra, kwargs, 'router-lifetime', key_new='router lifetime')
            self.fw._is_key_exist(commands_ra, kwargs, 'router-preference', key_new='router preference')
            self.fw._is_key_exist(commands_ra, kwargs, 'managed')
            self.fw._is_key_exist(commands_ra, kwargs, 'other-config')
            if 'add_prefix' in kwargs.keys():
                for each in kwargs['add_prefix']:
                    commands_ra.append('prefix ' + each)
                    self.fw._is_key_exist(commands_ra, kwargs[each], 'autonomou')
                    self.fw._is_key_exist(commands_ra, kwargs[each], 'on-link')
                    self.fw._is_key_exist(commands_ra, kwargs[each], 'valid-lifetime')
                    self.fw._is_key_exist(commands_ra, kwargs[each], 'preferred', key_new='preferred lifetime')
                    commands_ra.append('exit')
            if 'del_prefix' in kwargs.keys():
                for each in kwargs['del_prefix']:
                    commands_ra.append('no prefix ' + each)
            commands_ra.append('exit')
        else:
            commands_ra.append('no enable')
            commands_ra.append('exit')
        return commands_ra

    def _get_add_address(self, **kwargs):
        commands_aa = []
        for each in kwargs['add_address']:
            try:
                commands_aa.append('extra-ip ' + kwargs[each]['type'] + ' ' + kwargs[each]['ip'])
                if kwargs[each]['type'] == 'static':
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'ip', tag=True)
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'prefix-length', tag=True)
                    commands_aa.append('exit')
                elif kwargs[each]['type'] == 'prefix-delegation':
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'delegated-prefix', key_new='delegated-prefix name')
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'ip', key_new='preferred ip', tag=True)
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'prefix-length', key_new='preferred prefix-length', tag=True)
                    commands_aa.append('exit')
                elif kwargs[each]['type'] == '6rd':
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'ip', key_new='preferred ip', tag=True)
                    self.fw._is_key_exist(commands_aa, kwargs[each], 'prefix-length', key_new='preferred prefix-length', tag=True)
                    commands_aa.append('exit')
                self.fw._is_key_exist(commands_aa, kwargs[each], 'advertise')
            except KeyError as reason:
                logger.error('Make sure the parameter is specified:' + str(reason))
        return commands_aa

    def click_dhcp_release(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'dhcp']
        commands.append('release')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        
    
    def click_dhcp_renew(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'dhcp']
        commands.append('renew')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def click_dhcpv6_release(self, interface):
        commands = ['configure', 'interface ipv6 ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'dhcpv6']
        commands.append('release')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        
    
    def click_dhcpv6_renew(self, interface):
        commands = ['configure', 'interface ipv6 ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'dhcpv6']
        commands.append('renew')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def click_pptp_release(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'pptp']
        commands.append('release')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def click_pptp_renew(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'pptp']
        commands.append('renew')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def click_l2tp_release(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'l2tp']
        commands.append('release')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def click_l2tp_renew(self, interface):
        commands = ['configure', 'interface ' + interface, 'ip-assignment ' + 'WAN' + ' ' + 'l2tp']
        commands.append('renew')
        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_interface_status(self, interface=None, version=''):
        if not interface:
            commands = ['show interfaces ' + version]
        else:
            commands = ['show interface ' + version + ' ' + str(interface)]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output        

    def show_tunnel_status(self, type='', name=None, version=''):
        if type == 'manual' or type == '6to4' or type == 'gre' or type == '6rd' or type == 'isatap':
            version = 'ipv6'
            type = ''
        if not name:
            commands = ['show tunnel-interfaces ' + type]
        else:
            commands = ['show tunnel-interface ' + type + version + ' ' + name]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output  

    def show_tunnel_interface_status(self, type='', name=None, version=''):
        if type == 'manual' or type == '6to4' or type == 'gre' or type == '6rd' or type == 'isatap':
            version = 'ipv6'
            type = ''
        if not name:
            commands = ['show tunnel-interfaces ' + type]
        elif name and type == '4to6':
            commands = ['show tunnel-interface '+type+' '+name]
        else:
            commands = ['show tunnel-interface ' + type + version + ' ' + name]
        
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class FailoverLBCli:
    '''FailoverLBCli Class'''

    def __init__(self, fw):
        self.fw = fw

    def enable_Load_Balancing(self, **kwargs):
        commands = ['configure', 'failover-lb']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        if 'tcp_sync_port' in kwargs.keys():
            commands.append('respond-to-probes any-tcp-syn port ' + kwargs['tcp_sync_port'])
        elif 'tcp_sync' in kwargs.keys() and not kwargs['tcp_sync']:
            commands.append('respond-to-probes disable-any-tcp-syn')
        else:
            self.fw._is_key_exist(commands, kwargs, 'respond-to-probes')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_default_LB(self, **kwargs):
        commands = ['configure', 'failover-lb','enable']
        if 'version' in kwargs.keys() and kwargs['version'] == '6':
            commands.append('group ' + '" Default LB Group IPv6"')
        else:
            commands.append('group ' + '" Default LB Group"')
        self.fw._is_key_exist(commands, kwargs, 'type')
        if 'type' in kwargs.keys():
            if kwargs['type'] == 'basic':
                self.fw._is_key_exist(commands, kwargs, 'preempt')
            elif kwargs['type'] == 'ratio':
                self.fw._is_key_exist(commands, kwargs, 'address-binding')
                self.fw._is_key_exist(commands, kwargs, 'auto-adjust-ratio')
            elif kwargs['type'] == 'spillover':
                self.fw._is_key_exist(commands, kwargs, 'address-binding')
                self.fw._is_key_exist(commands, kwargs, 'spillover-bandwidth')
            elif kwargs['type'] == 'round-robin':
                self.fw._is_key_exist(commands, kwargs, 'address-binding')
            else:
                logger.error('type {} is not valid, please have a check.'.format(kwargs['type']))
                return False
        self.fw._is_key_exist(commands, kwargs, 'final-backup')
        if 'add-interfaces' in kwargs.keys():
            for interface in kwargs['add-interfaces']:
                commands.append('interface ' + interface.upper())
                commands.append('exit')
            if 'percentages' in kwargs.keys():
                for interface, percentage in zip(kwargs['add-interfaces'], kwargs['percentages']):
                    commands.append('percent ' + interface.upper() + ' ' + percentage)            
        if 'rem-interfaces' in kwargs.keys():
            for interface in kwargs['rem-interfaces'].split(','):
                commands.append('no interface ' + interface)
        if 'global-responder' in kwargs.keys() or 'health-check' in kwargs.keys() \
            or 'missed-intervals' in kwargs.keys() or 'successful-intervals' in kwargs.keys():
            commands.append('probing')
        self.fw._is_key_exist(commands, kwargs, 'global-responder')        
        self.fw._is_key_exist(commands, kwargs, 'health-check')        
        self.fw._is_key_exist(commands, kwargs, 'missed-intervals')        
        self.fw._is_key_exist(commands, kwargs, 'successful-intervals')     

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_groupmember(self, **kwargs):
        commands = ['configure', 'failover-lb','enable']
        if 'version' in kwargs.keys() and kwargs['version'] == '6':
            commands.append('group ' + '" Default LB Group IPv6"')
        else:
            commands.append('group ' + '" Default LB Group"')       
        self.fw._is_key_exist(commands, kwargs, 'interface', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'probe-type')
        self.fw._is_key_exist(commands, kwargs, 'probe-condition')

        if 'main_target_method' in kwargs.keys() and re.search('main|both|either', kwargs['probe-condition'], re.I):
            self.fw._is_key_exist(commands, kwargs, 'default-target')
            command = 'main-target '
            if 'main_target_method' in kwargs.keys():
                command += 'protocol ' + kwargs['main_target_method'] 
            if kwargs['main_target_method'] == 'tcp':
                if 'main_target_port' in kwargs.keys():
                    command += ' ' + kwargs['main_target_port'] 
                else:
                    logger.error('main_target_port must be specified when method is tcp!')
            else:
                pass
            if 'main_target_host' in kwargs.keys():
                command += ' host ' + kwargs['main_target_host'] 
            commands.append(command)
        if 'alter_target_method' in kwargs.keys() and re.search('both|either', kwargs['probe-condition'], re.I):
            command = 'alternate-target '
            if 'alter_target_method' in kwargs.keys():
                command += 'protocol ' + kwargs['alter_target_method'] 
            if kwargs['alter_target_method'] == 'tcp':
                if 'alter_target_port' in kwargs.keys():
                    command += ' ' + kwargs['alter_target_port'] 
                else:
                    logger.error('alter_target_port must be specified when method is tcp!')
            else:
                pass
            if 'alter_target_host' in kwargs.keys():
                command += ' host ' + kwargs['alter_target_host'] 
            commands.append(command)
        if 'main_target_method' in kwargs.keys() and kwargs['probe-condition'] == 'always':
            pass
        elif 'main_target_method' in kwargs.keys() and not re.search('main|always|both|either', kwargs['probe-condition'], re.I):
            logger.error('probe-condition {} should be one of always,both,main,either.Please have a check.'.format(kwargs['type']))
            return False   
        else:
            pass       
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result                

    def show_failover(self):
        commands = ['show failover-lb']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class NatpolicyCli:
    '''NatpolicyCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_natpolicy(self, **kwargs):
        commands = ['configure']
        command = NatpolicyCli._get_natpolicy(**kwargs)
        if command:
            commands.append(command)
        else:
            return False
        self.fw._is_key_exist(commands, kwargs, 'name')
        self.fw._is_key_exist(commands, kwargs, 'comment')
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'reflexive')
       
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_natpolicy(self, old_policy, new_policy):
        if not isinstance(old_policy, dict) or not isinstance(new_policy, dict):
            logger.error('Please pass your old policy and new policy as a dict.')
            return False
        commands = ['configure']
        command = NatpolicyCli._get_natpolicy(**old_policy)
        if command:
            commands.append(command)
        else:
            return False
        old_policy.update(new_policy)
        commands.extend(NatpolicyCli._get_natpolicy_edit(**old_policy))
        self.fw._is_key_exist(commands, old_policy, 'name') 
        self.fw._is_key_exist(commands, old_policy, 'comment') 
        self.fw._is_key_exist(commands, old_policy, 'enable') 
        self.fw._is_key_exist(commands, old_policy, 'reflexive')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_natpolicy_by_uuid(self, **kwargs):
        if 'version' in kwargs.keys() and 'uuid' in kwargs.keys():
            if kwargs['version'] == 'ipv6':
                command = 'nat-policy ipv6 uuid {}'.format(kwargs['uuid'])
            elif kwargs['version'] == 'nat64':
                command = 'nat-policy nat64 uuid {}'.format(kwargs['uuid'])
            else:
                command = 'nat-policy ipv4 uuid {}'.format(kwargs['uuid'])
            commands = ['configure']
            commands.append(command)
            commands.extend(self._get_natpolicy_edit(**kwargs))
            for command in ['commit', 'end', 'exit']:
                commands.append(command)
            result = self.fw.do_cli_commands(commands)
            return result
        else:
            logger.error('key version or uuid is not exist in kwargs.')
            return False

    def del_natpolicy(self, *params):
        commands = ['configure']
        if 'all' in params:
            commands.append('no nat-policies')
        else:        
            for entry in params:
                if isinstance(entry, dict):
                    command = NatpolicyCli._get_natpolicy(**entry)
                    if command:
                        commands.append('no ' + command)
                    else:
                        return False
                else:
                    (ver, type, value) = entry.split(":")
                    if type == 'name' or type == 'uuid':
                        # if ver='', nat-policy lacks 'ipv4' parameter , prompts error
                        # if ver.lower() == 'ipv4':
                        #     ver = ''
                        command = 'no nat-policy ' + ver + ' ' + type + ' ' + value
                        commands.append(command)
                    else:
                        logger.info('Make sure your delete entry defined like name:****** or uuid:******')

        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    #nat-policy nat64 inbound any outbound any source any translated-source X1 pref64 name nat64AO translated-destination embedded-ipv4-address service icmp-udp-tcp translated-service original
    ##
    def show_natpolicy(self, **kwargs):
        commands = []
        if ('version' in kwargs.keys() and 
            (kwargs['version'].lower() == 'ipv6' or kwargs['version'].lower() == 'nat64' or kwargs['version'].lower() == 'ipv4')):
            ver = kwargs['version'].lower() 
        else:
            ver = 'ipv4'
        if ('entries' in kwargs.keys() and kwargs['entries'] == 'all'):
            if 'type' in kwargs.keys():
                type = kwargs['type']
            else:
                type = ''    
            commands = ['show nat-policies ' + ver + ' ' + type]
        elif 'name' in kwargs.keys():
            name_command = 'show nat-policy ' + ver + ' name '
            self.fw._is_key_exist(commands, kwargs, 'name', key_new=name_command)
        elif 'uuid' in kwargs.keys():
            uuid_command = 'show nat-policy ' + ver + ' uuid '
            self.fw._is_key_exist(commands, kwargs, 'uuid', key_new=uuid_command)        
        else:
            command = NatpolicyCli._get_natpolicy(**kwargs)
            if command:
                # commands.append('show ' + command[:10] + ' ' + ver + command[10:])
                commands.append(command)
            else:
                logger.info('Please make sure your show command is correct.')
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output          

    @staticmethod
    def _get_natpolicy(**kwargs):
        ver = ''
        command = 'nat-policy '
        if ('version' in kwargs.keys() and
            (kwargs['version'].lower() == 'ipv6' or kwargs['version'].lower() == 'nat64')):
            ver = kwargs['version'].lower()
        elif 'version' not in kwargs.keys() or kwargs['version'] == 'ipv4':
            # if ver='', nat-policy lacks 'ipv4' parameter , prompts error
            ver = 'ipv4'
        else:
            logger.error('version must be one of ipv4,ipv6,nat64')
            return False
        command += ver + ' '     
        if ('inbound' in kwargs.keys() and kwargs['inbound']):
            command += 'inbound ' + kwargs['inbound'].upper() + ' '
        else:
            command += 'inbound ' + 'any '
        if ('outbound' in kwargs.keys() and kwargs['outbound']):
            command += 'outbound ' + kwargs['outbound'].upper() + ' '
        else:
            command += 'outbound ' + 'any '
        if ('orig_source_type' in kwargs.keys() and 
            (kwargs['orig_source_type'] != 'any' and kwargs['orig_source_type'])):
            if 'orig_source' in kwargs.keys() and kwargs['orig_source']:
                command += 'source ' + kwargs['orig_source_type'] + ' "' + kwargs['orig_source'] + '" '
            else:
                logger.error('Must specified orig_source when orig_source_type is not any.')
                return False
        if 'orig_source_type' in kwargs.keys() and kwargs['orig_source_type'] == 'any': #add by cyuan,'orig_source_type:any'
            command += 'source any '
        # translated parameter is 'original' instead of 'any'. new:'any' -> 'original'
        if ('trans_source_type' in kwargs.keys() and 
            (kwargs['trans_source_type'] != 'original' and kwargs['trans_source_type'])):
            if ('trans_source' in kwargs.keys() and kwargs['trans_source']):
                command += 'translated-source ' + kwargs['trans_source_type'] + ' "' + kwargs['trans_source'] + '" '
            else:
                logger.error('Must specified trans_source when trans_source_type is not original.')
                return False 
            
        if 'trans_source_type' in kwargs.keys() and (kwargs['trans_source_type'] == 'original'): #add by cyuan,'trans_source_type:original'
            command += 'translated-source original '
            
        if ver.lower() == 'nat64':
            if 'trans_source_type' in kwargs.keys() and kwargs['trans_source_type']: 
                if kwargs['trans_source_type'] == 'original':
                    logger.error("trans_source_type in nat64 policy can not be original")
                    return False
            if 'pref64_type' in kwargs.keys() and kwargs['pref64_type']: # 'pref64_type':'name', 'pref64':'Well-Known\ Pref64', 'pref64':'64:ffff::/96'
                if kwargs['pref64'] != 'any':
                    if 'pref64' in kwargs.keys() and kwargs['pref64']:
                        command += ' pref64 '+kwargs['pref64_type']+' '+kwargs['pref64']+' '
                else:
                    logger.error('pref64 can not be any')
            else:
                 logger.error("pref_64 must be specified.")
        else:                  
            if ('orig_dest_type' in kwargs.keys() 
                and (kwargs['orig_dest_type'] != 'any' and kwargs['orig_dest_type'])):
                if 'orig_dest' in kwargs.keys() and kwargs['orig_dest']:
                    command += 'destination ' + kwargs['orig_dest_type'] + ' "' + kwargs['orig_dest'] + '" '
                else:
                    logger.error('Must specified orig_dest when orig_dest_type is not any.')
                    return False
                
            if ('orig_dest_type' in kwargs.keys() and kwargs['orig_dest_type'] == 'any'):#add by cyuan, 'orig_dest_type':'any'
                command += 'destination any '
                
            # translated parameter is 'original' instead of 'any'. new:'any' -> 'original'
            if 'trans_dest_type' in kwargs.keys() and (kwargs['trans_dest_type'] != 'original' and kwargs['trans_dest_type']):
                if 'trans_dest' in kwargs.keys() and kwargs['trans_dest']:
                    command += 'translated-destination ' + kwargs['trans_dest_type'] + ' "' + kwargs['trans_dest'] + '" '
                else:
                    logger.error('Must specified trans_dest when trans_dest_type is not any.')
                    return False
            if 'trans_dest_type' in kwargs.keys() and kwargs['trans_dest_type'] == 'original': #add by cyuan, 'trans_dest_type':'original'
                command += 'translated-destination orginal '
                
            if 'orig_service_type' in kwargs.keys() and (kwargs['orig_service_type'] != 'any' and kwargs['orig_service_type']):
                if 'orig_service' in kwargs.keys() and kwargs['orig_service']:
                    if kwargs['orig_service_type'] == 'protocol':
                        command += 'service ' + kwargs['orig_service_type'] + ' ' + kwargs['orig_service'] + ' '
                    else:
                        command += 'service ' + kwargs['orig_service_type'] + ' "' + kwargs['orig_service'] + '" '
                else:
                    logger.error('Must specified orig_service when orig_service_type is not any.')
                    return False
            if 'orig_service_type' in kwargs.keys() and kwargs['orig_service_type'] == 'any': # add by cyuan, 'orig_service_type':'any'
                command += 'service any'  
                
            # translated parameter is 'original' instead of 'any'. new:'any' -> 'original'
            if 'trans_service_type' in kwargs.keys() and (kwargs['trans_service_type'] != 'original' and kwargs['trans_service_type']):
                if 'trans_service' in kwargs.keys() and kwargs['trans_service']:
                    if kwargs['trans_service_type'] == 'protocol':
                        command += 'service ' + kwargs['trans_service_type'] + ' ' + kwargs['trans_service']
                    else:
                        command += 'translated-service ' + kwargs['trans_service_type'] + ' "' + kwargs['trans_service'] + '" '
                else:
                    logger.error('Must specified trans_service when trans_service_type is not any.')
                    return False
            if 'trans_service_type' in kwargs.keys() and kwargs['trans_service_type'] == 'original':#add by cyuan, 'trans_service_type':'orginal'
                command += 'translated-service original '
        return command
        
    @staticmethod
    def _get_natpolicy_edit(**kwargs):
        commands = []
        if 'inbound_new' in kwargs.keys():
            commands.append('inbound ' + kwargs['inbound_new'])        
        if 'outbound_new' in kwargs.keys():
            commands.append('outbound ' + kwargs['outbound_new'])   
        if 'orig_source_new' in kwargs.keys():
            if 'orig_source_type_new' in kwargs.keys():
                commands.append('source ' + kwargs['orig_source_type_new'] + ' ' + kwargs['orig_source_new'])
            else:
                commands.append('source ' + kwargs['orig_source_type'] + ' ' + kwargs['orig_source_new'])
        if 'trans_source_new' in kwargs.keys():
            if 'trans_source_type_new' in kwargs.keys():
                # the commend of trans-source is 'translated-source' in CLI
                commands.append(
                    'translated-source ' + kwargs['trans_source_type_new'] + ' ' + kwargs['trans_source_new'])
            else:
                commands.append('translated-source ' + kwargs['trans_source_type'] + ' ' + kwargs['trans_source_new'])
        if 'orig_dest_new' in kwargs.keys():
            if 'orig_dest_type_new' in kwargs.keys():
                commands.append('destination ' + kwargs['orig_dest_type_new'] + ' ' + kwargs['orig_dest_new'])
            else:
                commands.append('destination ' + kwargs['orig_dest_type'] + ' ' + kwargs['orig_dest_new'])
        if 'trans_dest_new' in kwargs.keys():
            if 'trans_dest_type_new' in kwargs.keys():
                commands.append('translated-destination ' + kwargs['trans_dest_type_new'] + ' ' + kwargs['trans_dest_new'])
            else:
                commands.append('translated-destination ' + kwargs['trans_dest_type'] + ' ' + kwargs['trans_dest_new'])
        if 'orig_service_new' in kwargs.keys():
            if 'orig_service_type_new' in kwargs.keys():
                commands.append('service ' + kwargs['orig_service_type_new'] + ' ' + kwargs['orig_service_new'])
            else:
                commands.append('service ' + kwargs['orig_service_type'] + ' ' + kwargs['orig_service_new'])
        if 'trans_service_new' in kwargs.keys():
            if 'trans_service_type_new' in kwargs.keys():
                commands.append('translated-service ' + kwargs['trans_service_type_new'] + ' ' + kwargs['trans_service_new'])
            else:
                commands.append('translated-service ' + kwargs['trans_service_type'] + ' ' + kwargs['trans_service_new'])                
        if 'name_new' in kwargs.keys():
            commands.append('name ' + kwargs['name_new']) 
        if 'comment_new' in kwargs.keys():
            commands.append('comment ' + kwargs['comment_new'])
        if 'enable_new' in kwargs.keys():
            if kwargs['enable_new']:
                commands.append('enable')
            else:
                commands.append('no enable')             
        if 'reflexive_new' in kwargs.keys():
            if kwargs['reflexive_new']:
                commands.append('reflexive')
            else:
                commands.append('no reflexive')                               
        return commands


class DhcpServerCli:
    '''DhcpServerCli class'''
    def __init__(self, fw):
        self.fw = fw

    def add_dhcpserver_scope_v4(self, **kwargs):
        commands = ['configure', 'dhcp-server']
        command = DhcpServerCli._get_scope_v4(**kwargs)
        if command:
            commands.append(command)
        else:
            return False
        if kwargs['type'] == 'dynamic':
            self.fw._is_key_exist(commands, kwargs, 'allow-bootp')
        elif kwargs['type'] == 'static':
            self.fw._is_key_exist(commands, kwargs, 'name') 
        self.fw._is_key_exist(commands, kwargs, 'lease-time')
        self.fw._is_key_exist(commands, kwargs, 'gateway', key_new='default-gateway', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'netmask', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'domain-name')
        self.fw._is_key_exist(commands, kwargs, 'comment')
        self.fw._is_key_exist(commands, kwargs, 'inherit', key_new='dns server inherit')
        self.fw._is_key_exist(commands, kwargs, 'dns1', key_new='dns server static primary')
        self.fw._is_key_exist(commands, kwargs, 'dns2', key_new='dns server static secondary')
        self.fw._is_key_exist(commands, kwargs, 'dns3', key_new='dns server static tertiary')
        self.fw._is_key_exist(commands, kwargs, 'wins1', key_new='win primary')
        self.fw._is_key_exist(commands, kwargs, 'wins2', key_new='win secondary')
        self.fw._is_key_exist(commands, kwargs, 'voip1', key_new='call-manager primary')
        self.fw._is_key_exist(commands, kwargs, 'voip2', key_new='call-manager secondary')
        self.fw._is_key_exist(commands, kwargs, 'voip3', key_new='call-manager tertiary')
        self.fw._is_key_exist(commands, kwargs, 'boot-file', key_new='network-boot boot-file')
        self.fw._is_key_exist(commands, kwargs, 'next-server', key_new='network-boot next-server')
        self.fw._is_key_exist(commands, kwargs, 'server-name', key_new='network-boot server-name')
        self.fw._is_key_exist(commands, kwargs, 'always-send-option')
        if 'option-object' in kwargs.keys() and 'optoin-group' in kwargs.keys():
            logger.error('Only one of option-object or option-group can be defined.')
        else:
            self.fw._is_key_exist(commands, kwargs, 'option-object', key_new='generic-option object')
            self.fw._is_key_exist(commands, kwargs, 'option-group', key_new='generic-option group')
        
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_dhcpserver_scope_v6(self, **kwargs):
        pass

    def edit_dhcpserver_scope_v4(self, old_scope, new_scope):
        commands = ['configure', 'dhcp-server']
        if not isinstance(old_scope, dict) or not isinstance(new_scope, dict):
            logger.error('Please pass your old oscope and new scope as a dict.')
            return False 
        command = DhcpServerCli._get_scope_v4(**old_scope)
        if command:
            commands.append(command)
        else:
            return False
        if old_scope['type'] == 'dynamic':
            self.fw._is_key_exist(commands, old_scope, 'allow-bootp-new', key_new='allow-bootp')
            if 'start-new' in new_scope.keys() and 'end-new' in new_scope.keys():
                commands.append('range ' + new_scope['start-new'] + ' ' + new_scope['end-new'])
            elif 'start-new' in new_scope.keys() and 'end-new' not in new_scope.keys():
                commands.append('range ' + new_scope['start-new'] + ' ' + old_scope['end'])
            elif 'start-new' not in new_scope.keys() and 'end-new' in new_scope.keys():
                commands.append('range ' + old_scope['start'] + ' ' + new_scope['end-new'])
            else:
                pass
        elif old_scope['type'] == 'static':
            self.fw._is_key_exist(commands, old_scope, 'ip-new', key_new='ip') 
            self.fw._is_key_exist(commands, old_scope, 'mac-new', key_new='mac') 
            self.fw._is_key_exist(commands, old_scope, 'name-new', key_new='name') 
        self.fw._is_key_exist(commands, new_scope, 'lease-time-new', key_new='lease-time')
        self.fw._is_key_exist(commands, new_scope, 'gateway-new', key_new='default-gateway')
        self.fw._is_key_exist(commands, new_scope, 'netmask-new', key_new='netmask')
        self.fw._is_key_exist(commands, new_scope, 'domain-name-new', key_new='domain-name')
        self.fw._is_key_exist(commands, new_scope, 'comment-new', key_new='comment')
        self.fw._is_key_exist(commands, new_scope, 'inherit-new', key_new='dns server inherit')
        self.fw._is_key_exist(commands, new_scope, 'dns1-new', key_new='dns server static primary')
        self.fw._is_key_exist(commands, new_scope, 'dns2-new', key_new='dns server static secondary')
        self.fw._is_key_exist(commands, new_scope, 'dns3-new', key_new='dns server static tertiary')
        self.fw._is_key_exist(commands, new_scope, 'wins1-new', key_new='win primary')
        self.fw._is_key_exist(commands, new_scope, 'wins2-new', key_new='win secondary')
        self.fw._is_key_exist(commands, new_scope, 'voip1-new', key_new='call-manager primary')
        self.fw._is_key_exist(commands, new_scope, 'voip2-new', key_new='call-manager secondary')
        self.fw._is_key_exist(commands, new_scope, 'voip3-new', key_new='call-manager tertiary')
        self.fw._is_key_exist(commands, new_scope, 'boot-file-new', key_new='network-boot boot-file')
        self.fw._is_key_exist(commands, new_scope, 'next-server-new', key_new='network-boot next-server')
        self.fw._is_key_exist(commands, new_scope, 'server-name-new', key_new='network-boot server-name')
        self.fw._is_key_exist(commands, new_scope, 'always-send-option-new')
        if 'option-object-new' in new_scope.keys() and 'optoin-group-new' in new_scope.keys():
            logger.error('Only one of option-object-new or option-group-new can be defined.')
        else:
            self.fw._is_key_exist(commands, new_scope, 'option-object-new', key_new='generic-option object')
            self.fw._is_key_exist(commands, new_scope, 'option-group-new', key_new='generic-option group')
 
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        

    def edit_dhcpserver_scope_v6(self, **kwargs):
        pass

    def delete_dynmaic_scope(self, **kwargs):
        commands = ['configure']
        version = _get_version(kwargs)
        if version == 'ipv6':
            if 'name' not in kwargs.keys():
                logger.error('name must be defined when delete an {} server scope.'.format(version))
                return False  
        elif 'start' not in kwargs.keys() or 'end' not in kwargs.keys():
            logger.error('start or end must be defined.')
            return False                
        commands.append('dhcp-server ' + version)
        if version == 'ipv6':
            commands.append('no scope dynmic' + kwargs['name'])
        else:
            commands.append('no scope dynamic ' + kwargs['start'] + ' ' + kwargs['end'])
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def delete_all_scopes(self, **kwargs):
        commands = ['configure']
        version = _get_version(kwargs)
        commands.append('dhcp-server ' + version)
        if ('type' in kwargs.keys() and len(kwargs['type']) > 0 and kwargs['type'] != 'all'):
            commands.append('no scopes ' + kwargs['type'])
        else:
            commands.append('no scopes static')
            commands.append('no scopes dynamic')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def enable_dhcpserver(self, **kwargs):
        commands = ['configure']
        version = _get_version(kwargs)
        commands.append('dhcp-server ' + version)
        commands.append('enable')
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'conflict-detection')
        self.fw._is_key_exist(commands, kwargs, 'persistence')
        self.fw._is_key_exist(commands, kwargs, 'monitoring-interval', key_new='persistence monitoring-interval')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def disable_dhcpserver(self, **kwargs):
        commands = ['configure']
        version = _get_version(kwargs)
        commands.append('dhcp-server ' + version)
        commands.append('no enable')
        self.fw._is_key_exist(commands, kwargs, 'enable')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_option_object_v4(self, **kwargs):
        commands = ['configure', 'dhcp-server', 'enable']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='option object', tag=True)
        if not self.fw._is_key_exist(commands, kwargs, 'number', tag=True):
            logger.error('Option number must specified.')
            return False
        number = int(kwargs['number'])
        if number in [2, 24, 35, 38]:
            option_type = 'four-type'
        elif (number in range(3,12) or 
            number in [16, 21, 28, 32, 33, 41, 42, 44, 45, 48, 49, 54, 65, 85, 128, 138] or
            number in range(68,77)):
            option_type = 'ip'
        elif number in [12, 14, 15, 17, 18, 40, 47, 60, 62, 64, 66, 67, 86, 87]:
            option_type = 'string'
        elif number in [13, 22, 25, 26]:
            option_type = 'two-type'
        elif number in [19, 20, 27, 29, 30, 31, 34, 36, 39, 43, 119]:
            option_type = 'boolean'
        elif number in [23, 37, 46, 61, 63, 81, 82, 122]:
            option_type = 'one-type'
        elif (number in range(77,81) or 
            number in [83, 84, 88, 120, 121] or
            number in range(89,119) or
            number in range(123,128) or
            number in range(129,138) or
            number in range(139,255)):
            option_type = kwargs['type']
        elif number == 119:
            option_type = 'domain-name'
        else:
            logger.error('Option num is between 2-254.')
            return False
        self.fw._is_key_exist(commands, kwargs, 'value', key_new='value ' + option_type, tag=True)

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_option_object_v6(self, **kwargs):
        commands = ['configure', 'dhcp-server ipv6', 'enable']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='option object', tag=True)
        if not self.fw._is_key_exist(commands, kwargs, 'number', tag=True):
            logger.error('Option number must specified.')
            return False
        number = int(kwargs['number'])
        if number in [12, 22, 23, 27, 28, 31]:
            option_type = 'ip'
        elif number in [13, 24, 29, 30]:
            option_type = 'domain-name'
        elif number == 32:
            option_type = 'four-type'
        else:
            logger.error('Option num is one of 12, 13, 22, 23, 24, 27, 28, 29, 30, 31,32.')
            return False
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_option_group_v4(self, **kwargs):
        commands = ['configure', 'dhcp-server', 'enable']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='option group', tag=True)
        if 'objects' in kwargs.keys():
            for each in kwargs['objects']:
                commands.append('option object ' + each)
        if 'groups' in kwargs.keys():
            for each in kwargs['groups']:
                commands.append('option object ' + each)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_option_group_v6(self, **kwargs):
        commands = ['configure', 'dhcp-server ipv6', 'enable']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='option group', tag=True)
        if 'objects' in kwargs.keys():
            for each in kwargs['objects']:
                commands.append('option object ' + each)
        if 'groups' in kwargs.keys():
            for each in kwargs['groups']:
                commands.append('option object ' + each)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_option(self, **kwargs):
        version = _get_version(kwargs)
        commands = ['configure', 'dhcp-server '+ version]
        if 'objects' in kwargs.keys() and 'all' in kwargs['objects']:
            commands.append('no option objects')
        elif 'objects' in kwargs.keys():
            for each in kwargs['objects']:
                commands.append('no option object ' + each)
        else:
            pass
        if 'groups' in kwargs.keys() and 'all' in kwargs['groups']:
            commands.append('no option groups')
        elif 'groups' in kwargs.keys():
            for each in kwargs['groups']:
                commands.append('no option group ' + each)
        else:
            pass        
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        

    def show_dhcpserver_v4(self):
        commands = ['show dhcp-server ipv4']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output     

    def show_dhcpserver_v6(self):
        commands = ['show dhcp-server ipv6']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output     

    @staticmethod
    def _get_scope_v4(**kwargs):
        if 'type' in kwargs.keys() and kwargs['type'] == 'dynamic':
            if 'start' not in kwargs.keys() or 'end' not in kwargs.keys():
                logger.error('start or end must be defined.')
                return False
            else:
                command = 'scope dynamic ' + kwargs['start'] + ' ' + kwargs['end']
        elif 'type' in kwargs.keys() and kwargs['type'] == 'static':
            if 'ip' not in kwargs.keys() or 'mac' not in kwargs.keys():
                logger.error('start or end must be defined.')
                return False  
            else:
                command = 'scope static ' + kwargs['ip'] + ' ' + kwargs['mac']
        return command

    # @staticmethod
    # def _get_version(kwargs):
    #     ver = ''
    #     if 'version' in kwargs.keys() and kwargs['version'].lower() == 'ipv6':
    #         ver = 'ipv6'
    #     return ver        


class DNSCli:
    '''DNSCli class'''
    def __init__(self, fw):
        self.fw = fw

    def dns_setting(self, **kwargs):
        commands = ['configure' ]
        ver = ''
        if 'version' in kwargs.keys() and kwargs['version'] == '6':
            ver = 'ipv6'
        if 'type' in kwargs.keys() and kwargs['type'] == 'inherit':
            commands.append('dns server ' + ver + ' inherit')
        elif 'type' in kwargs.keys() and kwargs['type'] == 'static':
            if 'primary' in kwargs.keys():
                kwargs['dns server ' + ver + ' static primary'] = kwargs['primary']
                self.fw._is_key_exist(commands, kwargs, 'dns server' + ver + ' static primary')
            if 'secondary' in kwargs.keys():
                kwargs['dns server ' + ver + ' static secondary'] = kwargs['secondary']
                self.fw._is_key_exist(commands, kwargs, 'dns server' + ver + ' static secondary')
            if 'tertiary' in kwargs.keys():
                kwargs['dns server ' + ver + ' static tertiary'] = kwargs['tertiary']
                self.fw._is_key_exist(commands, kwargs, 'dns server' + ver + ' static tertiary')
        if ver == 'ipv6':
            if 'preferred' in kwargs.keys():
                kwargs['dns server ' + ver + ' preferred'] = kwargs['preferred']
                self.fw._is_key_exist(commands, kwargs, 'dns server ' + ver + ' preferred')
        self.fw._is_key_exist(commands, kwargs, 'dns fqdn-over-tcp-dns')
        if not ver:
            self.fw._is_key_exist(commands, kwargs, 'dns fqdn-binding')
            self.fw._is_key_exist(commands, kwargs, 'dns rebinding')
            self.fw._is_key_exist(commands, kwargs, 'dns rebinding action')
            self.fw._is_key_exist(commands, kwargs, 'dns rebinding allowed-domains')

        for command in ['commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result  

    def dns_sinkhole_service(self, **kwargs):
        commands = ['configure', 'dns-security', 'dns-sinkhole']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        if 'action-type' in kwargs.keys():
            if kwargs['action-type'] == '1':
                commands.append('action-type dropping-with-logs')       
            elif kwargs['action-type'] == '2':
                commands.append('action-type dropping-with-negative-dns-reply-to-source')
            elif kwargs['action-type'] == '3':
                if 'forged_ipv4' in kwargs.keys():
                    ipv4 = kwargs['forged_ipv4']
                else:
                    ipv4 = '127.0.0.1'
                if 'forged_ipv6' in kwargs.keys():
                    ipv6 = kwargs['forged_ipv6']
                else:
                    ipv6 = '::1'                
                commands.append('action-type dropping-with-dns-reply-of-forged-ip ' + ipv4 + ' ' + ipv6)
            else:
                logger.error('action-type only allow 1,2,3')
        else:
            pass
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result  

    def dns_tunnel_detection(self, **kwargs):
        commands = ['configure', 'dns-security', 'dns-tunnel']
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'block-all')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result  

    def add_custom_malicious_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-sinkhole', 'enable']
        for entry in entries:
            commands.append('custom-malicious-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def add_white_list_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-sinkhole', 'enable']
        for entry in entries:
            commands.append('white-list-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result                

    def add_tunnel_white_list_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-tunnel', 'enable']
        for entry in entries:
            commands.append('white-list-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result  

    def del_custom_malicious_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-sinkhole']
        if 'all' in entries:
            commands.append('no custom-malicious-entries')
        else:
            for entry in entries:
                commands.append('no custom-malicious-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_white_list_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-sinkhole']
        if 'all' in entries:
            commands.append('no white-list-entries')
        else:        
            for entry in entries:
                commands.append('white-list-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result                

    def del_tunnel_white_list_entry(self, *entries):
        commands = ['configure', 'dns-security', 'dns-tunnel']
        if 'all' in entries:
            commands.append('no white-list-entries')
        else:            
            for entry in entries:
                commands.append('white-list-entry ' + entry)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result  
        
    def show_dns(self, text='dns'):
        commands = ['show ' + text]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output
     

class ARPCli:
    def __init__(self, fw):
        self.fw =fw

    def add_arp_entry(self, **kwargs):
        commands = ['configure', 'arp']
        command = ARPCli._get_arp_entry(**kwargs)
        if command:
            commands.append(command)
        else:
            return False
        self.fw._is_key_exist(commands, kwargs, 'publish')
        self.fw._is_key_exist(commands, kwargs, 'bind-mac')
        if 'bind-mac' in kwargs.keys() and kwargs['bind-mac']:
            self.fw._is_key_exist(commands, kwargs, 'dynamic')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_arp_entry(self, old_entry, new_entry):
        commands = ['configure', 'arp']
        command = ARPCli._get_arp_entry(**old_entry)
        if command:
            commands.append(command)
        else:
            return False
        self.fw._is_key_exist(commands, new_entry, 'ip-new', key_new='ip')
        self.fw._is_key_exist(commands, new_entry, 'mac-new', key_new='mac')
        self.fw._is_key_exist(commands, new_entry, 'publish-new', key_new='publish')
        self.fw._is_key_exist(commands, new_entry, 'bind-mac-new', key_new='bind-mac')
        self.fw._is_key_exist(commands, new_entry, 'interface-new', key_new='interface')
        self.fw._is_key_exist(commands, new_entry, 'dynamic-new', key_new='dynamic')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_arp_entry(self, **kwargs):
        commands = ['configure', 'arp']
        command = ARPCli._get_arp_entry(**kwargs)
        if command:
            commands.append('no ' + command)
        else:
            return False
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def del_all_arp_entries(self):
        commands = ['configure', 'arp', 'no entries']
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def set_timeout(self, **kwargs):
        commands = ['configure', 'arp']
        self.fw._is_key_exist(commands, kwargs, 'timeout')
        self.fw._is_key_exist(commands, kwargs, 'glean')

        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def flush_arp_entry(self, *entries):
        commands = ['configure', 'arp']
        if 'all' in entries:
            commands.append('clear arp entries')
        else:
            for each in entries:
                commands.append('clear arp entry ' + each)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def show_arp_entry(self):
        commands = ['show arp entries']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output       

    def show_arp_cache(self):
        commands = ['show arp cache']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output 

    @staticmethod
    def _get_arp_entry(**kwargs):
        if 'ip' not in kwargs.keys():
            logger.error('ip must specified when add an arp entry')
            return False
        if 'mac' not in kwargs.keys():
            logger.error('mac must specified when add an arp entry')
            return False
        if 'interface' not in kwargs.keys():
            logger.error('interface must specified when add an arp entry')
            return False
        command = 'entry ' + kwargs['ip'] + ' ' + kwargs['mac'] + ' ' + kwargs['interface']
        return command


class IpHelperCli():
    '''IpHelper class'''

    def __init__(self, fw):
        self.fw = fw 

    def enable_IPhelper(self):
        commands = ['configure', 'ip-helper', 'enable']
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        

    def disable_IPhelper(self):
        commands = ['configure', 'ip-helper', 'no enable']
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_relay_protocol(self, **kwargs):
        commands = ['configure', 'ip-helper']
        if not self.fw._is_key_exist(commands, kwargs, 'name', key_new='protocol name', tag=True):
            return False
        if not self.fw._is_key_exist(commands, kwargs, 'port1', tag=True):
            return False
        if not self.fw._is_key_exist(commands, kwargs, 'port2', tag=True):
            return False
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'timeout')
        # self.fw._is_key_exist(commands, kwargs, 'mode')
        # self.fw._is_key_exist(commands, kwargs, 'multicast-ip')
        self.fw._is_key_exist(commands, kwargs, 'raw')
        self.fw._is_key_exist(commands, kwargs, 'source-translation')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def edit_ralay_protocol(self, old_relay, new_relay):
        commands = ['configure', 'ip-helper']
        if not self.fw._is_key_exist(commands, old_relay, 'name', key_new='protocol name', tag=True):
            return False
        self.fw._is_key_exist(commands, new_relay, 'port1-new', key_new='port1')
        self.fw._is_key_exist(commands, new_relay, 'port2-new', key_new='port2')
        self.fw._is_key_exist(commands, new_relay, 'enable-new', key_new='enable')
        self.fw._is_key_exist(commands, new_relay, 'timeout-new', key_new='timeout')
        # self.fw._is_key_exist(commands, new_relay, 'mode-new', key_new='mode')
        # self.fw._is_key_exist(commands, new_relay, 'multicast-ip-new', key_new='multicast-ip)
        self.fw._is_key_exist(commands, new_relay, 'raw-new', key_new='raw')
        self.fw._is_key_exist(commands, new_relay, 'source-translation-new', key_new='source-translation')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def del_relay_protocol(self, name=None):
        commands = ['configure', 'ip-helper']
        if name:
            if isinstance(name, str):
                commands.append('no protocol name ' + name)
            elif isinstance(name, list):
                for each in name:
                    commands.append('no protocol name ' + each)
        else:
            commands.append('no protocols')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def add_policy(self, **kwargs):
        # version = _get_version(kwargs)
        # commands = ['configure', 'ip-helper ' + version]
        version = ''
        if 'version' in kwargs.keys() and kwargs['version']=='ipv6':
            version = 'ipv6'
        commands = ['configure', 'ip-helper ' + version]
        command = IpHelperCli._get_policy(**kwargs)
        if not command:
            return False
        else:
            if version == 'ipv6':
                if 'egressif' in kwargs.keys() and kwargs['egressif']:
                    # commands.append(command + ' egressif ' + kwargs['egressif'])
                    commands.extend(command)
                    command.append('egressif ' + kwargs['egressif'])
            else:
                commands.extend(command)
        self.fw._is_key_exist(commands, kwargs, 'comment')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_policy(self, old_policy, new_policy):
        version = _get_version(old_policy)
        commands = ['configure', 'ip-helper ' + version]
        command = IpHelper._get_policy(**old_policy)
        if not command:
            return False
        else:
            if version == 'ipv6':
                if 'egressif' in old_policy.keys() and old_policy['egressif']:
                    commands.append(command + ' egressif ' + kwargs['egressif'])
        self.fw._is_key_exist(commands, new_policy, 'enable-new', key_new='enable')
        self.fw._is_key_exist(commands, new_policy, 'protocol-new', key_new='protocol')
        self.fw._is_key_exist(commands, new_policy, 'source-new', key_new='source')
        self.fw._is_key_exist(commands, new_policy, 'to-new', key_new='destination')
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result        

    def del_policy(self, **kwargs):
        version = _get_version(kwargs)
        commands = ['configure', 'ip-helper ' + version]
        command = IpHelper._get_policy(**kwargs)
        if not command:
            return False
        else:
            commands.append('no ' + command)
        for command in ['end', 'commit', 'exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands)
        return result 

    def show_policies(self):
        commands = ['show ip-helper policies']
        output = self.fw.do_cli_commands(commands,tag=1)[1]
        return output
    
    def show_relay_protocol(self, name=None):
        commands = []
        if name:
            command = 'show ip-helper protocol ' + name
        else:
            command = 'show ip-helper protocols'
        commands.append(command)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output        

    def show_dhcp_relay_lease(self):
        commands = ['show ip-helper dhcp-relay-leases']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output 

    def show_dhcpv6_relay_lease(self):
        commands = ['show ip-helper dhcpv6-relay-leases']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output   

    @staticmethod
    def _get_policy(**kwargs):
        command_if = []
        required_parameters = ['protocol', 'from', 'to']
        for each in required_parameters:
           if each not in kwargs.keys() or not kwargs[each]:
               logger.error(each + ' must be specified')
               return False
        command = 'policy protocol ' + kwargs['protocol']
        if kwargs['from'] in ['DMZ','LAN','WAN','WLAN','SSLVPN','VPN']:
            command += ' source zone '
        else:
            command += ' source interface '
        command += kwargs['from']
        command_if.append(command)
        command_if.append('destination '+ kwargs['to'])
        return command_if          


class DDNSCli():
    '''DDNS class'''

    def __init__(self, fw):
        self.fw = fw 
 
    def add_ddns_profile(self, **kwargs):
        # version = _get_version(kwargs)
        version = ''
        if 'version' in kwargs.keys() and kwargs['version'] == 'ipv6':
            version = 'ipv6'
        commands = ['configure']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='dynamic-dns profile ' + version, tag=True)
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'domain', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'password', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'provider')
        self.fw._is_key_exist(commands, kwargs, 'service-type')
        self.fw._is_key_exist(commands, kwargs, 'user-name', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'use-online')
        self.fw._is_key_exist(commands, kwargs, 'offline-settings')
        if 'online-settings' in kwargs.keys():
            if re.match(r'\d*\.\d*\.\d*\.\d*',kwargs['online-settings'], re.I):
                commands.append('online-settings manual ' + kwargs['online-settings'])
            else:
                commands.append('online-settings ' + kwargs['online-settings'])
        else:
            pass
        if 'bound-to' in kwargs.keys():
            if kwargs['bound-to'].lower() == 'any':
                commands.append('bound-to ' + kwargs['bound-to'])
            elif re.match(r'X\d*',kwargs['bound-to'], re.I):
                commands.append('bound-to interface ' + kwargs['bound-to'])
            else:
                logger.error('Make sure your bound-to is any or interface name.')
        else:
            pass
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result          

    def edit_ddns_profile(self, **kwargs):
        # version = _get_version(kwargs)
        version = ''
        if 'version' in kwargs.keys() and kwargs['version'] == 'ipv6':
            version = 'ipv6'
        commands = ['configure']
        self.fw._is_key_exist(commands, kwargs, 'name', key_new='dynamic-dns profile ' + version, tag=True)
        self.fw._is_key_exist(commands, kwargs, 'name-new', key_new='profile-name')
        self.fw._is_key_exist(commands, kwargs, 'enable-new', key_new='enable')
        self.fw._is_key_exist(commands, kwargs, 'domain-new', key_new='domain')
        self.fw._is_key_exist(commands, kwargs, 'password-new', key_new='password')
        self.fw._is_key_exist(commands, kwargs, 'provider-new', key_new='provider')
        self.fw._is_key_exist(commands, kwargs, 'service-type-new', key_new='service-type')
        self.fw._is_key_exist(commands, kwargs, 'user-name-new', key_new='user-name')
        self.fw._is_key_exist(commands, kwargs, 'use-online-new',key_new='user-online')
        self.fw._is_key_exist(commands, kwargs, 'bound-to-new', key_new='bound-to')

        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_ddns_profile(self, name=None, version=''):
        commands = ['configure']

        if isinstance(name, str):
            commands.append('no dynamic-dns profile ' + version + ' ' + name)
        elif isinstance(name, list):
            for each in name:
                commands.append('no dynamic-dns profile ' + version + ' ' + each)

        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_ddns_profiles(self, version=''):
        commands = ['configure', 'no dynamic-dns profiles ' + version, 'commit', 'exit']
        result = self.fw.do_cli_commands(commands)
        return result

    def show_ddns(self, version=''):
        commands = ['show dynamic-dns profiles ' + version]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output 


class NeighborDiscoveryCli():
    def __init__(self, fw):
        self.fw = fw

    def add_ndp_entry(self, **kwargs):
        commands = ['configure']
        command = self._get_ndp_entry(**kwargs)
        if not command:
            return False
        else:
            commands.append(command)
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result            

    def edit_ndp_entry(self, old_entry, new_entry):
        commands = ['configure']
        command = self._get_ndp_entry(**old_entry)
        if not command:
            return False
        else:
            commands.append(command)
        self.fw._is_key_exist(commands, new_entry, 'ip-new', key_new='ip')
        self.fw._is_key_exist(commands, new_entry, 'mac-new', key_new='mac')
        self.fw._is_key_exist(commands, new_entry, 'interface-new', key_new='interface')
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result 

    def del_ndp_entry(self, **kwargs):
        commands = ['configure']
        command = self._get_ndp_entry(**kwargs)
        if not command:
            return False
        else:
            commands.append('no ' + command)
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result 

    def del_ndp_entries(self):
        commands = ['configure', 'no ndp entries']
        result = self.fw.do_cli_commands(commands)
        commands.extend(['commit', 'exit'])
        return result

    @staticmethod
    def _get_ndp_entry(**kwargs):
        if 'ip' not in kwargs.keys() or 'mac' not in kwargs.keys() or 'interface' not in kwargs.keys():
            logger.error('ip,mac,interface must be specified.')  
            return False
        else:
            command = 'ndp entry ' + kwargs['ip'] + ' ' + kwargs['mac'] + ' ' + kwargs['interface']
            return command

    def set_reachable_time(self, time=30):
        commands =['configure', 'ndp reachable-time ' + str(time)]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_ndp_entries(self):
        commands = ['show ndp entries']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_ndp_caches(self):
        commands = ['show ndp cache']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class ZonesCli():
    def __init__(self, fw):
        self.fw = fw 

    def add_zone(self, **kwargs):
        commands =['configure']
        if not self.fw._is_key_exist(commands, kwargs, 'name', key_new='zone', tag=True):
            return False
        if not self.fw._is_key_exist(commands, kwargs, 'security-type', tag=True):
            return False
        commands.extend(self._get_general(**kwargs))
        if kwargs['security-type'].lower() != 'sslvpn':
            commands.extend(self._get_guestservice(**kwargs))
        if kwargs['security-type'].lower() == 'wireless':
            commands.extend(self._get_wireless(**kwargs))
            commands.extend(self._get_radius(**kwargs))
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_zone(self, **kwargs):
        commands =['configure']
        if not self.fw._is_key_exist(commands, kwargs, 'name', key_new='zone', tag=True):
            return False
        if kwargs['name'].upper() not in ['LAN', 'WAN', 'DMZ', 'MULTICAST', 'MGMT', 'VPN', 'SSLVPN', 'WLAN']:
            if not self.fw._is_key_exist(commands, kwargs, 'security-type', tag=True):
                return False            
        self.fw._is_key_exist(commands, kwargs, 'name-new', key_new='name')
        commands.extend(self._get_general(**kwargs))
        if kwargs['security-type'].lower() != 'sslvpn':
            commands.extend(self._get_guestservice(**kwargs))
        if kwargs['security-type'].lower() == 'wireless':
            commands.extend(self._get_wireless(**kwargs))
            commands.extend(self._get_radius(**kwargs, add_tag=False))
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_zone(self, *zones):
        commands =['configure']
        if not zones:
            commands.append('no zones')
        else:
            for each in zones:
                commands.append('no zone ' + each)
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_zones(self, zone=None):
        if not zone:
            commands = ['show zones']
        else:
            commands = ['show zone ' + zone]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def _get_general(self, **kwargs):
        commands_gel = []
        self.fw._is_key_exist(commands_gel, kwargs, 'interface-trust')
        self.fw._is_key_exist(commands_gel, kwargs, 'allow-from-higher', key_new='auto-generate-access-rules allow-from-higher')
        self.fw._is_key_exist(commands_gel, kwargs, 'allow-from-to-equal', key_new='auto-generate-access-rules allow-from-to-equal')
        self.fw._is_key_exist(commands_gel, kwargs, 'allow-to-lower', key_new='auto-generate-access-rules allow-to-lower')
        self.fw._is_key_exist(commands_gel, kwargs, 'deny-from-lower', key_new='auto-generate-access-rules deny-from-lower')
        self.fw._is_key_exist(commands_gel, kwargs, 'client-av', key_new='client anti-virus')
        self.fw._is_key_exist(commands_gel, kwargs, 'client-cfs', key_new='client content-filtering')

        self.fw._is_key_exist(commands_gel, kwargs, 'sslvpn-access')
        self.fw._is_key_exist(commands_gel, kwargs, 'create-group-vpn')
        self.fw._is_key_exist(commands_gel, kwargs, 'ssl-control')
        self.fw._is_key_exist(commands_gel, kwargs, 'gateway-anti-virus')
        self.fw._is_key_exist(commands_gel, kwargs, 'intrusion-prevention')
        self.fw._is_key_exist(commands_gel, kwargs, 'anti-spyware')
        self.fw._is_key_exist(commands_gel, kwargs, 'app-control')
        self.fw._is_key_exist(commands_gel, kwargs, 'dpi-ssl-client')
        self.fw._is_key_exist(commands_gel, kwargs, 'dpi-ssl-server')
        return commands_gel

    def _get_wireless(self, **kwargs):
        wireless_commands = []
        if 'wireless' in kwargs.keys() and kwargs['wireless']:
            wireless_commands.append('wireless')
            kwargs_wl = kwargs['wireless']
            if 'sslvpn-server' in kwargs_wl.keys() and 'sslvpn-service' in kwargs_wl.keys():
                wireless_commands.append('sslvpn-enforcement server ' + kwargs_wl['sslvpn-server'] + ' service ' + kwargs_wl['sslvpn-service'])
                self.fw._is_key_exist(wireless_commands, kwargs_wl, 'auto-channel-limitation')
                self.fw._is_key_exist(wireless_commands, kwargs_wl, 'only-sonicpoint-traffic')
                self.fw._is_key_exist(wireless_commands, kwargs_wl, 'sonicpoint-management')
                self.fw._is_key_exist(wireless_commands, kwargs_wl, 'sonicwave-online-registeration')
            for each in ['sonicpoit-ac', 'sonicpoit-n', 'sonicpoit-ndr', 'sonicpoit-wave2']:
                kwargs_each = kwargs_wl[each]
                ratio = each.split('-')[1]
                self.fw._is_key_exist(wireless_commands, kwargs_each, 'auto-provisioning', key_new='sonicpoint profile ' + ratio + ' auto-provisioning')
                self.fw._is_key_exist(wireless_commands, kwargs_each, 'profile', key_new='sonicpoint profile ' + ratio + ' profile-name ')
            wireless_commands.append('exit')
        return wireless_commands

    def _get_radius(self, add_tag=True, **kwargs): 
        radius_commands = []
        if 'local-radius' in kwargs.keys() and kwargs['local-radius']:
            kwargs_lr = kwargs['local-radius']
            radius_commands.append('local-radius-server')
            self.fw._is_key_exist(radius_commands, kwargs_lr, 'interface-server-numbers', tag=add_tag)
            self.fw._is_key_exist(radius_commands, kwargs_lr, 'port', tag=add_tag)
            self.fw._is_key_exist(radius_commands, kwargs_lr, 'client-password', tag=add_tag)
            self.fw._is_key_exist(radius_commands, kwargs_lr, 'tls-cache', tag=add_tag)
            self.fw._is_key_exist(radius_commands, kwargs_lr, 'tls-lifetime', key_new='tls-cache-lifetime', tag=add_tag)
            if 'database' in kwargs_lr and kwargs_lr['database']:
                kwargs_db = kwargs_lr['database']
                radius_commands.append('ldap-server')
                self.fw._is_key_exist(radius_commands, kwargs_db, 'server', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_db, 'base-dn', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_db, 'identity-dn', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_db, 'identity-dn-password', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_db, 'tls')
                self.fw._is_key_exist(radius_commands, kwargs_db, 'cache')
                self.fw._is_key_exist(radius_commands, kwargs_db, 'cache-lifetime')
                radius_commands.append('exit')
            if 'active-directory' in kwargs_lr and kwargs_lr['active-directory']:
                kwargs_ad = kwargs_lr['active-directory']
                radius_commands.append('active-directory-server')
                self.fw._is_key_exist(radius_commands, kwargs_ad, 'admin-name', key_new='admin-user-name', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_ad, 'admin-password', key_new='admin-user-password', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_ad, 'domain', tag=add_tag)
                self.fw._is_key_exist(radius_commands, kwargs_ad, 'full-name', tag=add_tag)
                radius_commands.append('exit')
        return radius_commands

    def _get_guestservice(self, **kwargs):
        guest_commands = []
        if 'guest-services' in kwargs.keys() and kwargs['guest-services']:
            guest_commands.append('guest-services')
            self.fw._is_key_exist(guest_commands, kwargs, 'inter-guest')
            self.fw._is_key_exist(guest_commands, kwargs, 'bypass-av', key_new='bypass client anti-virus')
            self.fw._is_key_exist(guest_commands, kwargs, 'bypass-cfs', key_new='bypass client content-filtering')

            # self.fw._is_key_exist(guest_commands, kwargs, 'external-auth')

            # self.fw._is_key_exist(guest_commands, kwargs, 'policy-page', key_new='policy-page-non-authentication')
            # self.fw._is_key_exist(guest_commands, kwargs, 'custom-auth-page')
            self.fw._is_key_exist(guest_commands, kwargs, 'post-auth')
            # self.fw._is_key_exist(guest_commands, kwargs, 'bypass-guest-auth', key_new='')
            if 'bypass-guest-auth' in kwargs.keys() and kwargs['bypass-guest-auth'] :
                if 'bypass-guest-auth-type' in kwargs.keys() and kwargs['bypass-guest-auth-type'] != None:
                    command_bypass = 'bypass-guest-auth ' + kwargs['bypass-guest-auth-type'] + ' '+ kwargs['bypass-guest-auth']
                    guest_commands.append(command_bypass)
                else:
                    logger.error("bypass-guest-auth-type must be specify.")
                    return False
            # self.fw._is_key_exist(guest_commands, kwargs, 'smtp-redirect')
            if 'smtp-redirect' in kwargs.keys() and kwargs['smtp-redirect']:#'smtp-redirect':'X0 IP', 'smtp-redirect-type':'name'
                if 'smtp-redirect-type' in kwargs.keys() and kwargs['smtp-redirect-type']:
                    command_smtp = 'smtp-redirect '+kwargs['smtp-redirect-type']+' "'+kwargs['smtp-redirect']+'"'
                    guest_commands.append(command_smtp)
                else:
                    logger.error('smtp-redirect-type must be specify')
            # self.fw._is_key_exist(guest_commands, kwargs, 'deny-networks', key_new='')
            if 'deny-networks' in kwargs.keys() and kwargs['deny-networks']:# 'deny-networks':'LAN Interface IP','deny-networks-type':'group'
                if 'version' in kwargs.keys() and kwargs['version'] == 'ipv6':
                    command_deny = 'deny-networks ipv6 '
                else: 
                    command_deny = 'deny-networks '
                if 'deny-networks-type' in kwargs.keys() and kwargs['deny-networks']:
                    command_deny += kwargs['deny-networks-type']+' "'+kwargs['deny-networks']+'"'
                    guest_commands.append(command_deny)
                else:
                    logger.error("deny-networks-type must be specify")
                    return False
            # self.fw._is_key_exist(guest_commands, kwargs, 'pass-networks', key_new='')
            if 'pass-networks' in kwargs.keys() and kwargs['pass-networks']:#'pass-networks':'All WAN IP', 'pass-networks-type':'group'
                if 'version' in kwargs.keys() and kwargs['version'] == 'ipv6':
                    command_pass = 'pass-networks ipv6 '
                else: 
                    command_pass = 'pass-networks '
                if 'pass-networks-type' in kwargs.keys() and kwargs['pass-networks']:
                    command_pass += kwargs['pass-networks-type']+' "'+kwargs['pass-networks']+'"'
                    guest_commands.append(command_pass)
                else:
                    logger.error("pass-networks-type must be specify")
                    return False
            self.fw._is_key_exist(guest_commands, kwargs, 'max-guests')
            self.fw._is_key_exist(guest_commands, kwargs, 'dynamic-address-translation')
            if 'external-auth' in kwargs.keys() and kwargs['external-auth']:
                guest_commands.extend(self._configure_external_auth(**kwargs['external-auth']))
            elif 'external-auth' in kwargs.keys() and not kwargs['external-auth']:
                guest_commands.append('no external-auth')
            else:
                pass
            if 'custom-auth-page' in kwargs.keys() and kwargs['custom-auth-page']:
                guest_commands.extend(self._configure_custom_auth_page(**kwargs['custom-auth-page']))
            elif 'custom-auth-page' in kwargs.keys() and not kwargs['custom-auth-page']:
                guest_commands.append('no custom-auth-page')
            else:
                pass 
            if 'policy-page-non-authentication' in kwargs.keys() and kwargs['policy-page-non-authentication']:
                guest_commands.extend(self._configure_policy_page(**kwargs['policy-page-non-authentication']))
            elif 'custom-auth-page' in kwargs.keys() and not kwargs['custom-auth-page']:
                guest_commands.append('no policy-page-non-authentication')
            else:
                pass  
        elif 'guest-services' in kwargs.keys() and not kwargs['guest-services']:
            guest_commands.append('no guest-services')
        else:
            pass
        return guest_commands        
        

    def _configure_external_auth(self, **kwargs):
        commands_external = []
        commands_external.append('external-auth')
        ###Genaral tab
        try:
            kwargs_gel = kwargs['general']
            print('kwargs_gel1')
            print(kwargs_gel)
            print('kwargs_gel1')
            if kwargs_gel:
                self.fw._is_key_exist(commands_external, kwargs_gel, 'client-redirect')
                self.fw._is_key_exist(commands_external, kwargs_gel, 'timeout', key_new='web-server timeout')
                if 'web-server1' in kwargs_gel.keys():
                    if 'protocol' not in kwargs_gel['web-server1'].keys() or\
                        'host' not in kwargs_gel['web-server1'].keys() or\
                        'port' not in kwargs_gel['web-server1'].keys():
                        logger.error('protocol, host, port must be specified.')
                    else:
                        commands_external.append('web-server-1 protocol ' + kwargs_gel['web-server1']['protocol'] + ' ' + kwargs_gel['web-server1']['host'] + ' port ' + kwargs_gel['web-server1']['port'])
                if 'web-server2' in kwargs_gel.keys():
                    if 'protocol' not in kwargs_gel['web-server2'].keys() or\
                        'host' not in kwargs_gel['web-server2'].keys() or\
                        'port' not in kwargs_gel['web-server2'].keys():
                        logger.error('protocol, host, port must be specified.')
                    else:
                        commands_external.append('web-server-2 protocol ' + kwargs_gel['web-server2']['protocol'] + ' ' + kwargs_gel['web-server2']['host'] + ' port ' + kwargs_gel['web-server2']['port'])
                if 'message-auth' in kwargs_gel.keys():
                    self.fw._is_key_exist(commands_external, kwargs_gel['message-auth'], 'method', key_new='message-auth method')
                    if 'secret' not in kwargs_gel['message-auth'].keys() or\
                        'confirm-secret' not in kwargs_gel['message-auth'].keys():
                        logger.error('secret, confirm-secret must be specified.')
                    else:
                        print('message-auth secret')
                        commands_external.append('message-auth shared-secret ' + kwargs_gel['message-auth']['secret'] + ' confirm-secret ' + kwargs_gel['message-auth']['confirm-secret'])
                        print(commands_external)
                        print('kwargs_gel')
                        print(kwargs_gel)
                        print('kwargs_gel')
                if 'social-network' in kwargs_gel.keys():
                    for each in kwargs_gel['social-network']:
                        commands_external.append('social-network ' + each)
                if 'wechat' in kwargs_gel.keys():
                    self.fw._is_key_exist(commands_external, kwargs_gel['wechat'], 'enable', key_new='wechat-qr-auth')
                    self.fw._is_key_exist(commands_external, kwargs_gel['wechat'], 'only-qr-auth', key_new='only-qr-auth')
                    self.fw._is_key_exist(commands_external, kwargs_gel['wechat'], 'qr-auth-page')
        except:
            logger.debug('{} not defined.'.format(kwargs['general']))           
        ####auth pages tab
        try:
            kwargs_auth = kwargs['auth-pages']
            print('auth-pages')
            print(kwargs_auth)
            print('auth-pages')
            if kwargs_auth and 'web-server1' in kwargs_auth.keys():
                print('webserver1')
                print(commands_external)
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server1'], 'login', key_new='auth-pages web-server-1 login')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server1'], 'expiration', key_new='auth-pages web-server-1 expiration')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server1'], 'timeout', key_new='auth-pages web-server-1 timeout')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server1'], 'max-sessions', key_new='auth-pages web-server-1 max-sessions')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server1'], 'traffic-exceeded', key_new='auth-pages web-server-1 traffic-exceeded')
            if kwargs_auth and 'web-server2' in kwargs_auth.keys():
                print('webserver2')
                print(commands_external)

                self.fw._is_key_exist(commands_external, kwargs_auth['web-server2'], 'login', key_new='auth-pages web-server-2 login')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server2'], 'expiration', key_new='auth-pages web-server-2 expiration')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server2'], 'timeout', key_new='auth-pages web-server-2 timeout')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server2'], 'max-sessions', key_new='auth-pages web-server-2 max-sessions')
                self.fw._is_key_exist(commands_external, kwargs_auth['web-server2'], 'traffic-exceeded', key_new='auth-pages web-server-2 traffic-exceeded')
        except:
            logger.debug('{} not defined.'.format(kwargs['auth-pages']))
       
        ####web content tab
        self.fw._is_key_exist(commands_external, kwargs['web-content'], 'redirect', key_new='web-content redirect')
        self.fw._is_key_exist(commands_external, kwargs['web-content'], 'server-down', key_new='web-content server-down')
        print('web content')
        print(commands_external)
        ####advanced tab
        try:
            kwargs_adv = kwargs['advanced']
            if kwargs_adv:
                self.fw._is_key_exist(commands_external, kwargs_adv['logout'], 'expire', key_new='logout-expired every')
                self.fw._is_key_exist(commands_external, kwargs_adv['logout'], 'cgi1', key_new='logout-expired cgi web-server-1')
                self.fw._is_key_exist(commands_external, kwargs_adv['logout'], 'cgi2', key_new='logout-expired cgi web-server-2')
                self.fw._is_key_exist(commands_external, kwargs_adv['status-check'], 'expire', key_new='status-check every')
                self.fw._is_key_exist(commands_external, kwargs_adv['status-check'], 'cgi1', key_new='status-check cgi web-server-1')
                self.fw._is_key_exist(commands_external, kwargs_adv['status-check'], 'cgi2', key_new='status-check cgi web-server-2')
                self.fw._is_key_exist(commands_external, kwargs_adv['session-sync'], 'expire', key_new='session-sync every')
                self.fw._is_key_exist(commands_external, kwargs_adv['session-sync'], 'cgi1', key_new='session-sync cgi web-server-1')
                self.fw._is_key_exist(commands_external, kwargs_adv['session-sync'], 'cgi2', key_new='session-sync cgi web-server-2')
        except:
            logger.debug('{} not defined.'.format(kwargs['advanced']))
        print('advanced')
        print(commands_external)            
        commands_external.append('exit')
        return commands_external
   
    def _configure_policy_page(self, **kwargs):
        commands_policy = []
        commands_policy.append('policy-page-non-authentication')
        self.fw._is_key_exist(commands_policy, kwargs, 'guest-usage-policy')
        if 'idle-timeout' in kwargs.keys():
            result = re.search(r'(\d*) (\w*)', kwargs['idle-timeout'], re.I)
            if result:
                num = result.group(1)
                unit = result.group(2)
                commands_policy.append('idle-timeout ' + num + ' unit ' + unit)
            else:
                logger.error('{} should follow like: 1 days(minutes/hours/seconds)'.format(kwargs['idle-timeout']))
        else:
            pass
        commands_policy.append('exit')
        return commands_policy

    def _configure_custom_auth_page(self, **kwargs):
        commands_custom = []
        commands_custom.append('custom-auth-page')
        try:
            kwargs_header = kwargs['header']
            if 'type' in kwargs_header.keys() and 'content' in kwargs_header.keys():
                commands_custom.append('custom-auth-page ' + kwargs_header['type'] + ' ' + kwargs_header['content'])
            else:
                pass
        except:
            logger.info('{} is not defined.'.format( kwargs['header']))
        try:
            kwargs_footer = kwargs['footer']
            if 'type' in kwargs_footer.keys() and 'content' in kwargs_footer.keys():
                commands_custom.append('custom-auth-page ' + kwargs_footer['type'] + ' ' + kwargs_footer['content'])
            else:
                pass 
        except:
            logger.info('{} is not defined.'.format( kwargs['footer'])) 
        commands_custom.append('exit')
        return commands_custom       

    def _get_zone_sslvpn(self, **kwargs):
        pass

    def _get_zone_wireless(self, **kwargs):
        pass


class RouteCli():
    def __init__(self, fw):
        self.fw = fw

    def add_route_policy(self, **kwargs):
        commands = ['configure']
        command = self._get_policy(**kwargs)
        if command:
            commands.append(command) 
        else:
            return False   
        self.fw._is_key_exist(commands, kwargs, 'name')
        self.fw._is_key_exist(commands, kwargs, 'path-selection-profile')
        self.fw._is_key_exist(commands,kwargs,'nexthop-number') # use to add multi-path route policy
        # self.fw._is_key_exist(commands, kwargs, 'interface')
        # self.fw._is_key_exist(commands, kwargs, 'metric')
        # self.fw._is_key_exist(commands, kwargs, 'service')
        self.fw._is_key_exist(commands, kwargs, 'comment')
        self.fw._is_key_exist(commands, kwargs, 'disable-on-interface-down')
        self.fw._is_key_exist(commands, kwargs, 'vpn-precedence')
        self.fw._is_key_exist(commands, kwargs, 'wxa-group')
        self.fw._is_key_exist(commands, kwargs, 'probe')
        self.fw._is_key_exist(commands, kwargs, 'default-probe-state-up')
        self.fw._is_key_exist(commands, kwargs, 'disable-when-probes-succeed')
        self.fw._is_key_exist(commands, kwargs, 'app')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result         

    def edit_route_policy(self, old_policy, new_policy):
        commands = ['configure']
        command = self._get_policy(**old_policy)
        if command:
            commands.append(command) 
        else:
            return False  
        self.fw._is_key_exist(commands, new_policy, 'if-new', key_new='interface')
        self.fw._is_key_exist(commands, new_policy, 'metric-new', key_new='metric')
        self.fw._is_key_exist(commands, new_policy, 'source-new', key_new='source')
        self.fw._is_key_exist(commands, new_policy, 'destination-new', key_new='destination')
        self.fw._is_key_exist(commands, new_policy, 'service-new', key_new='service')
        self.fw._is_key_exist(commands, new_policy, 'app-new', key_new='app')
        self.fw._is_key_exist(commands, new_policy, 'name-new', key_new='name')
        self.fw._is_key_exist(commands, new_policy, 'comment-new', key_new='comment')
        self.fw._is_key_exist(commands, new_policy, 'disable-on-interface-down-new', key_new='disable-on-interface-down')
        self.fw._is_key_exist(commands, new_policy, 'vpn-precedence-new', key_new='vpn-precedence')
        self.fw._is_key_exist(commands, new_policy, 'wxa-group-new', key_new='wxa-group')
        self.fw._is_key_exist(commands, new_policy, 'probe-new', key_new='probe')
        self.fw._is_key_exist(commands, new_policy, 'default-probe-state-up-new', key_new='default-probe-state-up')
        self.fw._is_key_exist(commands, new_policy, 'disable-when-probes-succeed-new', key_new='disable-when-probes-succeed')
        self.fw._is_key_exist(commands, new_policy, 'path-selection-profile-new',
                              key_new='path-selection-profile')  # added to change PSP of sdwan route policy
        self.fw._is_key_exist(commands, new_policy, 'tcp-acceleration',
                              key_new='tcp-acceleration')  # added to enable/disable tcp acceleration
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result
        
    def _get_policy(self, **kwargs):
        # version = _get_version(kwargs)
        # if not version:
        #     logger.error('Error! Get version failed!')
        #     return False
        # print('mark version:  {}'.format(version))
        command = 'route-policy '
        if 'version' not in kwargs.keys():
            command += 'ipv4 '
        else:
            command += kwargs['version']+' '
        if 'if' not in kwargs.keys() or 'metric' not in kwargs.keys():
            logger.error('interface and metric must be specified')
            return False
        command += 'interface ' + kwargs['if'] + ' metric ' + str(kwargs['metric']) + ' '
        # for each in ['source', 'destination', 'app', 'service']:
        for each in ['source','destination']:
            if each in kwargs.keys():
                command += each + ' ' + kwargs[each] + ' '
        
        if 'gateway' in kwargs.keys():
            command += 'gateway ' + kwargs['gateway'] +  ' '
        else:
            command += 'gateway default '
        return command    

    def del_route_policy(self, **kwargs):
        commands = ['configure']
        command = self._get_policy(**kwargs)
        if command:
            commands.append('no ' + command) 
        else:
            return False 
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_route_policies(self, version=''):
        commands =['configure', 'no route-policies ' + version] 
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_route_policies(self, version='', type=''):
        commands = ['show route-policies ' + version + ' ' + type]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_route_policy(self, **kwargs):
        version = _get_version(kwargs)
        if not version:
            version = 'ipv4'
        if 'if' not in kwargs.keys() or 'metric' not in kwargs.keys():
            logger.error('if and metric must be specified')
            return False
        command = 'route-policy ' + version + ' interface ' + kwargs['if'] + ' metric ' + str(kwargs['metric']) + ' '
        for each in ['source', 'destination', 'app', 'service']:
            if each in kwargs.keys():
                command += each + ' ' + kwargs[each] + ' '
        if 'gateway' in kwargs.keys():
            command += 'gateway ' + kwargs['gateway'] +  ' '
        else:
            command += 'gateway default '
        commands = ['show ' + command]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output  
                 
    def show_route_policy_by_name(self, version='ipv4',name=None):
        commands = ['show route-policy '+version+' name '+name]
        output = self.fw.do_cli_commands(commands,tag=1)[1]
        return output   
    
    def set_route(self, mode):
        commands = ['configure', 'routing', 'mode ' + mode]
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def config_ospf(self, **kwargs):
        commands = ['configure', 'routing', 'ospf', 'configure terminal']
        commands.append('router ospf')
        if 'redistribute' in kwargs.keys() and kwargs['redistribute']:
            commands.append('redistribute connected metric 1')
        else:
            commands.append('no redistribute connected') 
        if kwargs['type'].lower() == 'disable':
            try:
                commands.append('no network ' + kwargs['network'] + ' area ' + kwargs['area'])
            except:
                logger.error('network and area must specified when disable the ospf.')
                return False
        elif kwargs['type'].lower() == 'passive':
            if 'if' in kwargs.keys():
                commands.append('passive-interface ' + kwargs['if'])
            else:
                logger.error('if must be specified when set ospf passive')
                return False
        elif kwargs['type'].lower() == 'enable':
            try:
                commands.append('network ' + kwargs['network'] + ' area ' + kwargs['area'])
            except:
                logger.error('network and area must specified when disable the ospf.')
                return False
            if 'area-type' in kwargs.keys():
                if kwargs['area-type'] == 'stub':
                    commands.append('area ' + kwargs['area'] + ' stub')
                elif kwargs['area-type'] == 'totally-stub':
                    commands.append('area ' + kwargs['area'] + ' stub no-summary')
                elif kwargs['area-type'] == 'nssa':
                    commands.append('area ' + kwargs['area'] + ' nssa')
                elif kwargs['area-type'] == 'totally-nssa':
                    commands.append('area ' + kwargs['area'] + ' nssa no-summary')
                else:
                    logger.error('Make sure area type is one of stub,totally-stub,nssa,totally-nssa.')
            commands.append('exit')
            self.fw._is_key_exist(commands, kwargs, 'if', key_new='interface', tag=True)
            if 'auth' in kwargs.keys():
                if kwargs['auth'] == 'simple':
                    kwargs['auth'] = ''
                commands.append('ip ospf authentication ' + kwargs['auth'])  
            self.fw._is_key_exist(commands, kwargs, 'password',  key_new='ip ospf authentication-key ' + kwargs['password'])
            self.fw._is_key_exist(commands, kwargs, 'dead-interval',  key_new='ip ospf dead-interval')
            self.fw._is_key_exist(commands, kwargs, 'hello-interval',  key_new='ip ospf hello-interval')
            self.fw._is_key_exist(commands, kwargs, 'mtu-ignore', key_new='ip ospf mtu-ignore')
            self.fw._is_key_exist(commands, kwargs, 'priority', key_new='ip ospf priority')
            self.fw._is_key_exist(commands, kwargs, 'cost', key_new='ip ospf cost')

        commands.extend(['end', 'write terminal', 'exit', 'end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result
        
    def config_ospf3(self, **kwargs):
        commands = ['configure', 'routing', 'ospfv3', 'configure terminal']
        if 'if' not in kwargs.keys() or 'area' not in kwargs.keys():
            logger.error('if and area must be specified when config ospf3')
            return False
        if kwargs['type'].lower() == 'disable':
            commands.append('router ipv6 ospf')
            commands.append('no ipv6 router ospf area ' + kwargs['area'])
        elif kwargs['type'].lower() == 'passive':
            commands.append('router ipv6 ospf')
            commands.append('passive-interface ' + kwargs['if'])
        elif kwargs['type'].lower() == 'enable':
            commands.append('interface ' + kwargs['if'])
            commands.append('ipv6 router ospf area ' + kwargs['area'])
            self.fw._is_key_exist(commands, kwargs, 'dead-interval', key_new='ipv6 ospf dead-interval')
            self.fw._is_key_exist(commands, kwargs, 'hello-interval', key_new='ipv6 ospf hello-interval')
            self.fw._is_key_exist(commands, kwargs, 'priority', key_new='ipv6 ospf priority')
            self.fw._is_key_exist(commands, kwargs, 'cost', key_new='ipv6 ospf cost')
            commands.append('exit')
            commands.append('router ipv6 ospf')
            if 'area-type' in kwargs.keys():
                if kwargs['area-type'] == 'stub':
                    commands.append('area ' + kwargs['area'] + ' stub')
                elif kwargs['area-type'] == 'totally-stub':
                    commands.append('area ' + kwargs['area'] + ' stub no-summary')
                else:
                    logger.error('Make sure area type is one of stub,totally-stub.')

        commands.extend(['end', 'write terminal', 'exit', 'end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def config_ripng(self, **kwargs):
        commands = ['configure', 'routing', 'ripng', 'configure terminal']
        self.fw._is_key_exist(commands, kwargs, 'if', key_new='interface', tag=True)
        if kwargs['enable']:
            commands.append('ipv6 router rip')
        if kwargs['poison']:
            commands.append('ipv6 rip split-horizon poisoned')
        elif kwargs['split']:
            commands.append('ipv6 rip split-horizon')
        
        commands.extend(['end', 'write terminal', 'exit', 'end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def config_rip(self, **kwargs):
        commands = ['configure', 'routing', 'rip', 'configure terminal']
        if 'if' not in kwargs.keys() or 'network' not in kwargs.keys():
            logger.error('if and network must be specified when config rip')
            return False
        commands.append('router rip')
        if 'redistribute' in kwargs.keys() and kwargs['redistribute']:
            commands.append('redistribute connected metric 1')
        else:
            commands.append('no redistribute connected') 
        if 'redistribute_static' in kwargs.keys() and kwargs['redistribute_static']:
            commands.append('redistribute static')
        else:
            commands.append('no redistribute static')
        if kwargs['type'].lower() == 'disable':
            commands.append('no network ' + kwargs['network'])
        elif kwargs['type'].lower() == 'passive':
            commands.append('passive-interface ' + kwargs['if'])
        elif 'send' in kwargs['type'].lower() or 'receive' in kwargs['type'].lower():        
            commands.append('network ' + kwargs['network'])
            commands.append('exit')
            commands.append('interface ' + kwargs['if'])
            if 'send' in kwargs['type'].lower():
                try:
                    commands.append('ip rip send version ' + kwargs['send-version'])
                except:
                    logger.error('send-version must be specified when rip is {}'.format(kwargs['type']))
            if 'receive' in kwargs['type'].lower():
                try:
                    commands.append('ip rip receive version ' + kwargs['receive-version'])
                except:
                    logger.error('receive-version must be specified when rip is {}'.format(kwargs['type']))
            if kwargs['poison']:
                commands.append('ip rip split-horizon poisoned')
            elif kwargs['split']:
                commands.append('ip rip split-horizon')
            if 'password' in kwargs.keys() and kwargs['password']:
                commands.append('ip rip authentication string ' + kwargs['password'])

        commands.extend(['end', 'write terminal', 'exit', 'end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_rip(self):
        cmd = 'show routing rip database'
        commands = [cmd]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result  

    def conf_BGP(self, mode='on'): ### mode = 'on' or 'off'
        commands = ['configure', 'routing']
        if mode == 'on':
            commands.extend(['bgp', 'exit'])
        elif mode == 'off':
            commands.append('no bgp')
        commands.extend(['commit', 'end', 'end'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_BGP(self, mode=''): ### mode = '' | 'neighbor' | 'summary' | 'unicast'
        cmd = 'show routing bgp '
        if mode:
            cmd = cmd + str(mode)
        commands = [cmd]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result


    def show_ospf2(self, mode=''): ### mode = '' | 'neighbor' | 'database' | 'routes'        
        cmd = 'show routing ospf '        
        if mode:            
            cmd = cmd + str(mode)        
            commands = [cmd]
        result = self.fw.do_cli_commands(commands, tag=1)[1]
        return result


class PortShieldGroupCli():
    def __init__(self, fw):
        self.fw = fw

    def config_port(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('interface ' + kwargs['interface'])
            commands.append('ip-assignment LAN portshield ' + kwargs['portshield-to'])
            self.fw._is_key_exist(commands, kwargs, 'port-enable', key_new='shutdown-port')
            if 'link-speed' in kwargs.keys():
                rc = re.search(r'(\d*)-(full|half)', kwargs['link-speed'])
                if rc:
                    commands.append('link-speed ' + rc.group(2) + ' ' + rc.group(1))
                else:
                    commands.append('link-speed auto')
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason))
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result  
    
    
class MacIPAntiSproofCli():
    def __init__(self, fw):
        self.fw = fw

    def set_interface(self, **kwargs):
        ver = _get_version(kwargs)
        commands = ['configure', 'mac-ip-anti-spoof ' + ver]
        self.fw._is_key_exist(commands, kwargs, 'interface', tag=True)
        self.fw._is_key_exist(commands, kwargs, 'enable')
        self.fw._is_key_exist(commands, kwargs, 'allow-management')
        self.fw._is_key_exist(commands, kwargs, 'enforce-ingress')
        self.fw._is_key_exist(commands, kwargs, 'spoof-detection')
        if ver == 'ipv6':
            self.fw._is_key_exist(commands, kwargs, 'ndp-lock')
            self.fw._is_key_exist(commands, kwargs, 'static-ndp')
        else:
            self.fw._is_key_exist(commands, kwargs, 'static-arp')
            self.fw._is_key_exist(commands, kwargs, 'dhcp-relay')
            self.fw._is_key_exist(commands, kwargs, 'dhcp-server')
            self.fw._is_key_exist(commands, kwargs, 'arp-lock')
            self.fw._is_key_exist(commands, kwargs, 'arp-watch')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result    

    def resolve_detected_list(self, ver=''):
        commands = ['configure', 'mac-ip-anti-spoof ' + ver, 'resolve spoof-detected-list']
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def add_cache_entry(self, **kwargs):
        ver = _get_version(kwargs)
        commands = ['configure', 'mac-ip-anti-spoof ' + ver]
        if 'interface' not in kwargs.keys() or 'ip' not in kwargs.keys() or 'mac' not in kwargs.keys():
            logger.error('inteface, ip and mac must specified.')
            return False
        command = 'cache entry ' + kwargs['ip'] + ' ' + kwargs['mac'].replace(':','') + ' ' + kwargs['interface'] 
        commands.append(command)
        self.fw._is_key_exist(commands, kwargs, 'router')
        self.fw._is_key_exist(commands, kwargs, 'blacklisted')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_cache_entry(self, old_entry, new_entry):
        ver = _get_version(old_entry)
        commands = ['configure', 'mac-ip-anti-spoof ' + ver]
        if 'interface' not in old_entry.keys() or 'ip' not in old_entry.keys() or 'mac' not in old_entry.keys():
            logger.error('inteface, ip and mac must specified.')
            return False
        command = 'cache entry ' + old_entry['ip'] + ' ' + old_entry['mac'].replace(':','') + ' ' + old_entry['interface'] 
        commands.append(command)
        self.fw._is_key_exist(commands, new_entry, 'ip-new', key_new='ip')
        self.fw._is_key_exist(commands, new_entry, 'mac-new', key_new='mac')
        self.fw._is_key_exist(commands, new_entry, 'interface-new', key_new='interface')
        self.fw._is_key_exist(commands, new_entry, 'router-new', key_new='router')
        self.fw._is_key_exist(commands, new_entry, 'blacklisted-new', key_new='blacklisted')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_cache_entries(self, ver=''):
        commands = ['configure', 'mac-ip-anti-spoof ', 'no cache entries ' + ver]
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_cache_entry(self, **kwargs):
        ver = _get_version(kwargs)
        commands = ['configure', 'mac-ip-anti-spoof ' + ver]
        if 'interface' not in kwargs.keys() or 'ip' not in kwargs.keys() or 'mac' not in kwargs.keys():
            logger.error('inteface, ip and mac must specified.')
            return False
        command = 'cache entry ' + kwargs['ip'] + ' ' + kwargs['mac'].replace(':','') + ' ' + kwargs['interface'] 
        commands.extend([command, 'end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def clear_macip_detected_list(self, ver=''):
        commands = ['configure', 'mac-ip-anti-spoof ' + ver, 'clear cache statistics']
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def clear_macip_staticstics(self, ver=''):
        commands = ['configure', 'mac-ip-anti-spoof ' + ver, 'clear spoof-detected-list']
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_macip_detected_list(self, ver=''):
        commands = ['show mac-ip-anti-spoof ' + ver +  ' detected-list']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output        

    def show_macip_entries(self, ver=''):
        commands = ['show mac-ip-anti-spoof ' + ver + ' cache entries']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output      

    def show_macip_interaface(self, ver='', interface=''):
        if interface:
            commands = ['show mac-ip-anti-spoof ' + ver + ' interface ' + interface ]
        else:
            commands = ['show mac-ip-anti-spoof ' + ver + ' interfaces']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output  


class VlanTranslationCli():
    '''VlanTranslationCli'''

    def __init__(self, fw):
        self.fw = fw

    def add_vlan_translation(self, **kwargs):
        command = VlanTranslationCli._get_vlan_translation(kwargs)
        if not command:
            return False
        commands = ['configure', command]
        self.fw._is_key_exist(commands, kwargs, 'reverse')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result    

    def edit_vlan_translation(self, old_vt, new_vt):
        command = VlanTranslationCli._get_vlan_translation(old_vt)
        if not command:
            return False
        commands = ['configure', command]
        self.fw._is_key_exist(commands, new_vt, 'ingress-if-new', key_new='ingress interface')
        self.fw._is_key_exist(commands, new_vt, 'ingress-vlan-new', key_new='ingress vlan')
        self.fw._is_key_exist(commands, new_vt, 'egress-if-new', key_new='egress interface')
        self.fw._is_key_exist(commands, new_vt, 'egress-vlan-new', key_new='egress vlan')
        self.fw._is_key_exist(commands, new_vt, 'reverse-new', key_new='reverse')
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result 

    def del_vlan_translation(self, **kwargs):
        command = VlanTranslationCli._get_vlan_translation(kwargs)
        if not command:
            return False
        commands = ['configure', 'no ' + command]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_vlan_translation(self):
        commands = ['show vlan-translations']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output 

    @staticmethod
    def _get_vlan_translation(kwargs):
        if 'ingress-if' not in kwargs.keys():
            logger.error('ingress-if must be specified.')
            return False
        if 'ingress-vlan' not in kwargs.keys():
            logger.error('ingress-vlan must be specified.')
            return False
        if 'egress-if' not in kwargs.keys():
            logger.error('egress-if must be specified.')
            return False
        if 'egress-vlan' not in kwargs.keys():
            logger.error('egress-vlan must be specified.')
            return False
        command = 'vlan-translation ingress interface ' + kwargs['ingress-if'] + ' vlan ' + \
                str(kwargs['ingress-vlan']) + ' egress interface ' + kwargs['egress-if'] + ' vlan ' + str(kwargs['egress-vlan'])
        return command       


class NetworkMonitorCli():
    def __init__(self, fw):
        self.fw = fw

    def add_nm_policy(self, **kwargs):
        ver = _get_version(kwargs)
        commands = ['configure']
        if not self.fw._is_key_exist(commands, kwargs, 'name', key_new= 'network-monitor policy ' + ver):
            return False
        self.fw._is_key_exist(commands, kwargs, 'probe-target', key_new='probe target', tag=True)       
        if 'probe-type' in kwargs.keys():
            if 'tcp' in kwargs['probe-type']:
                if 'port' not in kwargs.keys() or not kwargs['port']:
                    logger.error('port must specified when probe type is tcp.')
                    return False
                commands.append('probe type ' + kwargs['probe-type'] + ' port ' + kwargs['port'])
            elif 'ping' in kwargs['probe-type']:
                commands.append('probe type ' + kwargs['probe-type'])
            else:
                pass
            if 'explicit' in kwargs['probe-type']:
                self.fw._is_key_exist(commands, kwargs, 'next-hop', tag=True)       
            else:
                pass
        self.fw._is_key_exist(commands, kwargs, 'outbound-interface')       
        self.fw._is_key_exist(commands, kwargs, 'intervel', key_new='probe interval')       
        self.fw._is_key_exist(commands, kwargs, 'reply-timeout')       
        self.fw._is_key_exist(commands, kwargs, 'down-after', key_new='interval missed')       
        self.fw._is_key_exist(commands, kwargs, 'up-after', key_new='interval successful')       
        self.fw._is_key_exist(commands, kwargs, 'must-respond')       
        self.fw._is_key_exist(commands, kwargs, 'rst-as-miss')    
        self.fw._is_key_exist(commands, kwargs, 'comment')       

        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_nm_policy(self, **kwargs):
        ver = _get_version(kwargs)
        commands = ['configure']
        if not self.fw._is_key_exist(commands, kwargs, 'name', key_new= 'network-monitor policy ' + ver):
            return False
        self.fw._is_key_exist(commands, kwargs, 'name-new', key_new='name')       
        self.fw._is_key_exist(commands, kwargs, 'probe-target', key_new='probe target')       

        if 'probe-type' in kwargs.keys():
            if 'tcp' in kwargs['probe-type']:
                if 'port' not in kwargs.keys() or not kwargs['port']:
                    logger.error('port must specified when probe type is tcp.')
                    return False
                commands.append('probe type ' + kwargs['probe-type'] + ' port ' + kwargs['port'])
            elif 'ping' in kwargs['probe-type']:
                commands.append('probe type ' + kwargs['probe-type'])
            else:
                pass
            if 'explicit' in kwargs['probe-type']:
                self.fw._is_key_exist(commands, kwargs, 'next-hop', tag=True)       
            else:
                pass
        self.fw._is_key_exist(commands, kwargs, 'outbound-interface')       
        self.fw._is_key_exist(commands, kwargs, 'intervel', key_new='probe interval')       
        self.fw._is_key_exist(commands, kwargs, 'reply-timeout')       
        self.fw._is_key_exist(commands, kwargs, 'down-after', key_new='interval missed')       
        self.fw._is_key_exist(commands, kwargs, 'up-after', key_new='interval successful')       
        self.fw._is_key_exist(commands, kwargs, 'must-respond')       
        self.fw._is_key_exist(commands, kwargs, 'rst-as-miss')    
        self.fw._is_key_exist(commands, kwargs, 'comment')       

        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_nm_policy(self, name=None, version=''):
        if version.lower() == 'ipv4':
            version = ''
        commands = ['configure', 'no network-monitor policy ' + version + ' ' + name]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_nm_policies(self, version=''):
        if version.lower() == 'ipv4':
            version = ''
        commands = ['configure', 'no network-monitor policies ' + version]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_nm_policies(self, version=''):
        commands = ['show network-monitor policies ' + version]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_nm_policy(self, name=None, version=''):
        if version.lower() == 'ipv4':
            version = ''
        commands = ['show network-monitor policy ' + version + ' ' + name]
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_nm_policies_status(self, version=''):
        commands = ['show network-monitor policies ' + version + ' status']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_nm_policy_status(self, version='', name=''):
        if version.lower() == 'ipv4':
            version = ''
        commands = ['show network-monitor policy ' + version + ' ' + name + ' status']
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class ServiceCli():
    '''ServiceCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_service_object(self, **kwargs):
        commands = ['configure']
        try:
            command = 'service-object ' + kwargs['name'] + ' ' + kwargs['protocol']
            if 'sub-type' in kwargs.keys():
                command += ' ' + kwargs['sub-type']
            if 'port' in kwargs.keys():
                command += ' ' + kwargs['port']
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason))
        commands.extend([command, 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_service_object(self, **kwargs):
        commands = ['configure', 'service-object ' + kwargs['name']]
        try:
            command = kwargs['protocol']
            if 'sub-type' in kwargs.keys():
                command += ' ' + kwargs['sub-type']
            if 'port' in kwargs.keys():
                command += ' ' + kwargs['port']
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason))
        # due to the crash on 7.1.0, add a commend 'end' before 'exit'
        commands.extend([command, 'commit', 'end', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_service_object(self, name=None):
        commands = ['configure']
        if not name:
            commands.append('no service-objects')
        else:
            commands.append('no service-object ' + name)
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def add_service_group(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('service-group ' + kwargs['name'])
            if 'add-group' in kwargs.keys():
                for each in kwargs['add-group']:
                    commands.append('service-group ' + each)
            if 'del-group' in kwargs.keys():
                for each in kwargs['del-group']:
                    commands.append('no service-group ' + each)
            if 'add-object' in kwargs.keys():
                for each in kwargs['add-object']:
                    commands.append('service-object ' + each)
            if 'del-object' in kwargs.keys():
                for each in kwargs['del-object']:
                    commands.append('no service-object ' + each)
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason))        
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_service_group(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('service-group ' + kwargs['name'])
            self.fw._is_key_exist(commands, kwargs, 'name-new', key_new='name')       
            if 'add-group' in kwargs.keys():
                for each in kwargs['add-group']:
                    commands.append('service-group ' + each)
            if 'del-group' in kwargs.keys():
                for each in kwargs['del-group']:
                    commands.append('no service-group ' + each)
            if 'add-object' in kwargs.keys():
                for each in kwargs['add-object']:
                    commands.append('service-object ' + each)
            if 'del-object' in kwargs.keys():
                for each in kwargs['del-object']:
                    commands.append('no service-object ' + each)
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason))        
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_service_group(self, name=None):
        commands = ['configure']
        if not name:
            commands.append('no service-groups')
        else:
            commands.append('no service-group ' + name)
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_service_group(self, name=None):
        commands = []
        if not name:
            commands.append('show service-groups')
        else:
            commands.append('show service-group ' + name)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def show_service_object(self, name=None):
        commands = []
        if not name:
            commands.append('show service-objects')
        else:
            commands.append('show service-object ' + name)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output


class AddressObjectCli():
    '''AddressObjectCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_address_object(self, **kwargs):
        commands = ['configure']
        try:
            if kwargs['type'] == 'mac':
                kwargs['version'] = ''
                sub_command = kwargs['type'] + ' ' + kwargs['name'] + ' ' + 'address ' + kwargs['address']
            elif kwargs['type'] == 'fqdn':
                kwargs['version'] = ''
                sub_command = kwargs['type'] + ' ' + kwargs['name'] + ' ' + 'domain ' + kwargs['domain']
            else:
                sub_command = kwargs['name'] + ' ' + kwargs['type'] + ' ' + kwargs[kwargs['type']]
            command = 'address-object ' + kwargs['version'] + ' ' + sub_command + ' zone ' + kwargs['zone']
            commands.append(command)
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason)) 
        if kwargs['type'] == 'mac':
            self.fw._is_key_exist(commands, kwargs, 'multi-homed') 
            commands.append('end')      
        elif kwargs['type'] == 'fqdn':
            self.fw._is_key_exist(commands, kwargs, 'dns-ttl')  
            commands.append('end')      
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_address_object(self, **kwargs):
        commands = ['configure']
        try:
            if 'type' in kwargs.keys() and (kwargs['type'] == 'mac' or kwargs['type'] == 'fqdn'):
                kwargs['version'] = ''
            else:
                kwargs['type'] = ''
            commands.append('address-object ' + kwargs['type'] + ' ' + kwargs['version'] + ' ' + kwargs['name'])
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason)) 
        self.fw._is_key_exist(commands, kwargs, 'name-new', key_new='name')       
        self.fw._is_key_exist(commands, kwargs, 'host-new', key_new='host')       
        self.fw._is_key_exist(commands, kwargs, 'network-new', key_new='network')       
        self.fw._is_key_exist(commands, kwargs, 'range-new', key_new='range')       
        self.fw._is_key_exist(commands, kwargs, 'address-new', key_new='address')       
        self.fw._is_key_exist(commands, kwargs, 'domain-new', key_new='domain')       
        self.fw._is_key_exist(commands, kwargs, 'multi-homed-new', key_new='multi-homed')       
        self.fw._is_key_exist(commands, kwargs, 'dns-ttl-new', key_new='dns-ttl')       
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result             

    def del_address_objects(self, type=''):
        commands= ['configure', 'no address-objects ' + type]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_address_object(self, **kwargs):
        commands = ['configure']
        if kwargs['type'] == 'mac' or kwargs['type'] == 'fqdn':
            kwargs['version'] = ''
        else:
            kwargs['type'] = ''
        try:
            commands.append('no address-object ' + kwargs['version'] + ' ' + kwargs['type'] + ' ' + kwargs['name'])
        except KeyError as reason:
            logger.error('Make sure the parameter is specified: ' + str(reason))
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def add_address_group(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('address-group ' + kwargs['version'] + ' ' + kwargs['name'])
            if 'objects' in kwargs.keys():
                for each in kwargs['objects']:
                    commands.append('address-object ' + each)
            if 'groups' in kwargs.keys():
                for each in kwargs['groups']:
                    commands.append('address-group ' + each)
        except KeyError as reason:
            logger.error('Make sure the parameter is specified: ' + str(reason))
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def edit_address_group(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('address-group ' + kwargs['version'] + ' ' + kwargs['name'])
        except KeyError as reason:
            logger.error('Make sure the parameter is specified:' + str(reason)) 
        if 'add_objects' in kwargs.keys():
            for each in kwargs['add_objects']:
                commands.append('address-object ' + each)
        if 'add_groups' in kwargs.keys():
            for each in kwargs['add_groups']:
                commands.append('address-group ' + each)
        if 'del_objects' in kwargs.keys():
            for each in kwargs['del_objects']:
                commands.append('no address-object ' + each)
        if 'del_groups' in kwargs.keys():
            for each in kwargs['del_groups']:
                commands.append('no address-group ' + each)
        commands.extend(['end', 'commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result  

    def del_address_groups(self, version=''):
        commands= ['configure', 'no address-groups ' + version]
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def del_address_group(self, **kwargs):
        commands = ['configure']
        try:
            commands.append('no address-group ' + kwargs['version'] + ' ' + kwargs['name'])
        except KeyError as reason:
            logger.error('Make sure the parameter is specified: ' + str(reason))
        commands.extend(['commit', 'exit'])
        result = self.fw.do_cli_commands(commands)
        return result

    def show_address_object(self, name=None, version='', type=''):
        commands = []
        if not name:
            commands.append('show address-objects ' + type)
        else:
            commands.append('show address-object ' + version + ' ' +type +' '+ name)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output         

    def show_address_group(self, name=None, version='', type=''):
        commands = []
        if not name:
            commands.append('show address-groups ' + type)
        else:
            commands.append('show address-group ' + version + ' ' + name)
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output      


class DNSfilteringCli:
    '''DNSfilteringCli class'''

    def __init__(self, fw):
        self.fw = fw

    def config_dns_filtering_base(self, tag=0, **kwargs):
        commands = ['configure', 'dns-security', 'dns-filtering']
        if 'forged-ip' in kwargs.keys():
            commands.append('forged-ip ' + kwargs['forged-ip'])
        else:
            logger.error('Must specify forged ip.') 
    
        for command in ['commit', 'end', 'exit']:
            commands.append(command)            
        result = self.fw.do_cli_commands(commands, tag=tag)
        return result


class ApplicationObjectCli(): #added to add application object -> sdwan app based route
    '''ApplicationCli class'''

    def __init__(self, fw):
        self.fw = fw

    def add_application_object(self, **kwargs):
        commands = ['configure']
        if 'type' in kwargs.keys() and kwargs['type']:
            commands.append('match-object ' + kwargs['name'])
            commands.append('type ' + kwargs['type'])
            commands.append('application category name ' + kwargs['app_category_name'] + ' app name ' + kwargs['app_name'])

        for command in ['commit', 'end', 'exit']:
            commands.append(command)
        res_edit_src = self.fw.do_cli_commands(commands)
        return res_edit_src