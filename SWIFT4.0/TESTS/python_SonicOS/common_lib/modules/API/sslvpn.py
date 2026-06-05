import copy
import json
import urllib3
import requests
from runner.settings import logger
from runner.utils.assertion import Assertion
from requests.auth import HTTPBasicAuth
from requests_toolbelt.adapters import source


class SSLVPNServerSettingsAPI:
    '''Server Settings class'''
    default_options = {
        'port': 4433,
        'certificate': None,
        'user_domain': 'LocalDomain',
        'management': None,
        'web': False,
        'ssh': False,
        'session_timeout': 0,
        'download_url': None,
        'use_radius': None,
        'access': None

    }

    default_options1 = {
        'enable': True,
        'zone': None

    }

    def __init__(self, fw):
        self.fw = fw
        self.base_url = 'api/sonicos/ssl-vpn/server/base'
        self.access_url = 'api/sonicos/ssl-vpn/server/accesses'
        self.initial_json_serverbaseset = {
            'ssl_vpn': {
                'server': {
                    'port': 4433,
                    'certificate': {
                        'use_self_signed': True
                    },
                    'use_radius': {},
                    'user_domain': "LocalDomain",
                    'management': {
                        'web': False,
                        'ssh': False
                    },
                    'session_timeout': 10,
                    #'download_url': {},
                    'inactivity_check': False

                }
            }
        }

        self.initial_json_serveraccess = {

            'ssl_vpn': {
                'server': {
                    'access': [
                        {

                            'enable': False,
                            'zone': 'LAN'
                        },
                        {

                            'enable': False,
                            'zone': 'WAN'
                        },
                        {

                            'enable': False,
                            'zone': 'DMZ'
                        },
                        {

                            'enable': False,
                            'zone': 'WLAN'
                        }
                    ]
                }
            }
        }

    # Build json for server settings Page
    def build_json_server_set(self, **kwargs):
        json_input = {}
        access_list = []
        json_input = copy.deepcopy(self.initial_json_serverbaseset)
        logger.info("The json input is {}".format(json_input))
        try:
            if 'port_ssl' in kwargs.keys():
                json_input['ssl_vpn']['server']['port'] = kwargs['port_ssl']
            if 'user_domain' in kwargs.keys():
                json_input['ssl_vpn']['server']['user_domain'] = kwargs['user_domain']
            if 'session_timeout' in kwargs.keys():
                json_input['ssl_vpn']['server']['session_timeout'] = kwargs['session_timeout']
            if 'auth_type' in kwargs:
                json_input['ssl_vpn']['server']['auth_type'] = kwargs['auth_type']
            try:
                if 'use_self_signed' in kwargs.keys():
                    json_input['ssl_vpn']['server']['certificate']['use_self_signed'] = kwargs['use_self_signed']
                elif 'certificat_name' in kwargs.keys():
                    json_input['ssl_vpn']['server']['certificate'] = {}
                    json_input['ssl_vpn']['server']['certificate']['name'] = kwargs['certificat_name']
                if 'web' in kwargs.keys():
                    json_input['ssl_vpn']['server']['management']['web'] = kwargs['web']
                if 'ssh' in kwargs.keys():
                    json_input['ssl_vpn']['server']['management']['ssh'] = kwargs['ssh']
                if 'default' in kwargs.keys():
                    json_input['ssl_vpn']['server']['download_url'] = {}
                    json_input['ssl_vpn']['server']['download_url']['default'] = kwargs['default']
                if 'mschapv2' in kwargs.keys():
                    json_input['ssl_vpn']['server']['use_radius']['mschapv2'] = kwargs['mschapv2']
                if 'mschap' in kwargs.keys():
                    json_input['ssl_vpn']['server']['use_radius']['mschap'] = kwargs['mschap']
                if 'inactivity_check' in kwargs.keys():
                    json_input['ssl_vpn']['server']['inactivity_check'] = kwargs['inactivity_check']

                else:
                    raise KeyError
            except KeyError as ke:
                logger.info('Missing use_radius attribute under SSL-VPN Server')
        except KeyError:
            logger.error('Error: In creating JSON for SSLVPN Server settings')
            logger.info(json_input)
        return json_input

    def build_json_server_access_set(self, **kwargs):
        json_input = {}
        json_input = copy.deepcopy(self.initial_json_serveraccess)
        logger.info("The json input is {}".format(json_input))
        try:
            if 'LAN_enable' in kwargs.keys():
                json_input['ssl_vpn']['server']['access'][0]['enable'] = kwargs['LAN_enable']
            if 'WAN_enable' in kwargs.keys():
                json_input['ssl_vpn']['server']['access'][1]['enable'] = kwargs['WAN_enable']
            if 'DMZ_enable' in kwargs.keys():
                json_input['ssl_vpn']['server']['access'][2]['enable'] = kwargs['DMZ_enable']
            if 'WLAN_enable' in kwargs.keys():
                json_input['ssl_vpn']['server']['access'][3]['enable'] = kwargs['WLAN_enable']

        except KeyError as ke:
            logger.error('Missing server access under SSL-VPN Server')
        except KeyError:
            logger.error('Error: in creating JSON for SSLVPN Server settings')
            logger.info(json_input)

        return json_input

    def get_server_base_setting(self):
        get_response = self.fw.api_get(self.base_url)
        return get_response

    def get_server_access_setting(self):
        get_response = self.fw.api_get(self.access_url)
        return get_response

    def edit_server_setting(self, msg=False, **kwargs):
        self.options = dict(SSLVPNServerSettingsAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_server_set(**kwargs)
        logger.info('the json input build is', json_input)
        sslserver_resp = self.fw.api_put(self.base_url, msg, data=json_input)
        return sslserver_resp

    def edit_server_access_setting(self, msg=False, **kwargs):
        self.options = dict(SSLVPNServerSettingsAPI.default_options1)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_server_access_set(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        sslserver_resp = self.fw.api_put(self.access_url, msg, data=json_input)
        return sslserver_resp

    def sslvpn_server_logout(self, ip):
        url = 'api/sonicos/ssl-vpn/server-logout/' + str(ip)
        resp = self.fw.api_post(url)
        return resp

class SSLVPNPortalSettingsAPI:
    '''Portal Settings class'''
    default_options = {
        'site_title': "SonicWall - Virtual Office",
        'banner_title': "Virtual Office",
        'home_page_message': None,
        'home_custom': "<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\"font-size:18px;\"><B>Welcome to the SonicWallVirtual Office</b></font><BR>                                            <BR><span style=\"line-height:115%;\"><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.<BR>                                            <BR>Click a pre-configured bookmark or create your own to gain secure Internet access to internal corporate resources.<BR>                                            <BR>Launch NetExtender to create an SSLVPN tunnel to your corporate network for full network access.</font></span></td></tr></table>'",
        'login_message': None,
        'login_custom': "<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\"font-size:18px;\"><B>Welcome to the SonicWall Virtual Office</b></font><BR>                                            <BR><span style=\"line-height:115%;\"><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></span></td></tr></table>",
        'auto_launch': False,
        'cache_control': False,
        'virtual_office': True,
        'display_link': False,
        'logo': None,
        'logo_custom': "/VirtualOffice.gif"
    }

    def __init__(self, fw):
        self.fw = fw
        self.portal_url = 'api/sonicos/ssl-vpn/portal'
        self.initial_json_portal_set ={
            'ssl_vpn' : {
                'portal': {
                    'site_title': None,
                    'banner_title': None,
                    'home_page_message': {
                        'custom': "<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\"font-size:18px;\"><B>Welcome to the SonicWallVirtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\"line-height:115%;\"><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.<BR><img src=shim.gif width=1 height=6 border=0><BR>Click a pre-configured bookmark or create your own to gain secure Internet access to internal corporate resources.<BR><img src=shim.gif width=1 height=6 border=0><BR>Launch NetExtender to create an SSLVPN tunnel to your corporate network for full network access.</font></span></td></tr></table>"
                    },
                    'login_message': {
                        "custom": "<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\"font-size:18px;\"><B>Welcome to the SonicWall Virtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\"line-height:115%;\"><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></span></td></tr></table>"
                    },
                    'auto_launch': False,
                    'cache_control': False,
                    'virtual_office': True,
                    'display_link': False,
                    'logo': {}
                }
            }
        }
    #Build json for portal settings Page
    def build_json_portal_set(self, **kwargs):

        json_input = copy.deepcopy(self.initial_json_portal_set)
        logger.info('The json input is {}'.format(json_input))
        try:
            if 'site_title' in kwargs.keys():
                json_input['ssl_vpn']['portal']['site_title'] = kwargs['site_title']
            if 'banner_title' in kwargs.keys():
                json_input['ssl_vpn']['portal']['banner_title'] = kwargs['banner_title']

            if 'home_custom' in kwargs.keys():
                json_input['ssl_vpn']['portal']['home_page_message']['custom'] = kwargs['home_custom']

            try:
                if 'login_custom' in kwargs.keys():
                    json_input['ssl_vpn']['portal']['login_message']['custom'] = kwargs['login_custom']
                else:
                    raise KeyError
            except KeyError as ke:
                logger.error('Login message is not defined')
            try:
                if 'auto_launch' in kwargs.keys():
                    json_input['ssl_vpn']['portal']['auto_launch'] = kwargs['auto_launch']
                else:
                    raise KeyError
            except KeyError as ke:
                logger.error('Error: Undefined auto launch for portal ssl vpn setting is : {}'.format(ke))

            if 'cache_control' in kwargs.keys():
                json_input['ssl_vpn']['portal']['cache_control'] = kwargs['cache_control']
            if 'display_link' in kwargs.keys():
                json_input['ssl_vpn']['portal']['display_link'] = kwargs['display_link']
            if 'virtual_office' in kwargs.keys():
                json_input['ssl_vpn']['portal']['virtual_office'] = kwargs['virtual_office']
            if 'logo_custom' in kwargs.keys():
                json_input['ssl_vpn']['portal']['logo']['custom'] = kwargs['logo_custom']

        except KeyError:
            logger.error('Error: in creating JSON for SSLVPN Portal settings Page')
            logger.info(json_input)
        return json_input

    def get_portal_setting(self):
        get_response = self.fw.api_get(self.portal_url)
        return get_response

    def edit_portal_setting(self, msg=False, **kwargs):
        self.options = dict(SSLVPNPortalSettingsAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_portal_set(**kwargs)
        logger.info('the json input build is',json_input)
        sslportal_resp = self.fw.api_put(self.portal_url, msg, data=json_input)
        return sslportal_resp
    
    def config_portal_setting(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        resp = self.fw.api_put(self.portal_url, msg, data=json_input)
        return resp


class SSLVPNVirtualOfficeAPI:
    '''SSLVPN VIrtual Office
	options used as we have service_type as rdp, ssh, vnc.
		'name': '',
        'host': '',
        'service_type': 'rdp', #rdp, ssh,telnet,vnc
        'redirect_clipboard': True,
        'redirect_audio': False,
        'auto_reconnection': True,
        'desktop_background': False,
        'window_drag': False,
        'animation': False,
        'screen_size': '',
        'colors': '16bit',
        'application_path': '',
        'start_in_folder': '',
        'automatic_login': {}, # {} for disable and 'automatic_login' : True - for ssl_vpn:True
        'custom': {},
        'view_only': False,
        'share_desktop': False,
        'automatic_accept_host_key': False,
        'display_on_mobile': False,
	'''

    default_options = {
        'name': '',
        'host': '',
        'service_type': 'rdp', #rdp, ssh,telnet,vnc
        'redirect_clipboard': True,
        'redirect_audio': False,
        'auto_reconnection': True,
        'desktop_background': False,
        'window_drag': False,
        'animation': False,
        'screen_size': 'full-screen',
        'colors': '16bit',
        'application_path': '',
        'start_in_folder': '',
        'automatic_login': {}, # {} for disable and 'automatic_login' : True - for ssl_vpn:True
        'custom': {}


    }
    def __init__(self, fw):
        self.fw = fw
        self.bookmark_url = 'api/sonicos/ssl-vpn/bookmarks'
        self.initial_json_virtual_office_rdp = {
            'ssl_vpn':{
                'virtual_office':{
                    'bookmark': [
                        {
                            'name': '',
                            'host': '',
                            'service':{
                                'rdp': {
                                    'redirect_clipboard': False,
                                    'redirect_audio': False,
                                    'auto_reconnection': False,
                                    'desktop_background': False,
                                    'window_drag': False,
                                    'animation': False,
                                    'screen_size': '1280x1024',
                                    'colors': '32bit',
                                    'application_path': '',
                                    'start_in_folder': '',
                                    'automatic_login': {},
                                    'display_on_mobile': False
                                }
                            }
                        }
                    ]
                }
            }
        }
        self.initial_json_virtual_office_ssh = {'ssl_vpn': {'virtual_office': {'bookmark': [{'name': '','host': '','service': {'sshv2': {}}}]}}}
        self.initial_json_virtual_office_telnet = {'ssl_vpn': {'virtual_office': {'bookmark': [{'name': '','host': '','service': {'telnet': {}}}]}}}
        self.initial_json_virtual_office_vnc = {'ssl_vpn': {'virtual_office': {'bookmark': [{'name': '','host': '','service': {'vnc': {}}}]}}}


    def build_json_virtual_office(self, **kwargs):
        json_input = {}
        try:
            if(kwargs['service_type'] == 'rdp'):

                json_input = copy.deepcopy(self.initial_json_virtual_office_rdp)
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['name'] = kwargs['name']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['host'] = kwargs['host']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['screen_size'] = kwargs['screen_size']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['colors'] = kwargs['colors']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['redirect_clipboard'] = kwargs['redirect_clipboard']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['redirect_audio'] = kwargs['redirect_audio']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['auto_reconnection'] = kwargs['auto_reconnection']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['desktop_background'] = kwargs['desktop_background']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['window_drag'] = kwargs['window_drag']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['animation'] = kwargs['animation']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['application_path'] = kwargs['application_path']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['start_in_folder'] = kwargs['start_in_folder']
                if(kwargs['automatic_login'] == True):
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['automatic_login']['ssl_vpn'] = kwargs['automatic_login']
                if('custom' in kwargs.keys() and kwargs['custom'] != {}):
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['automatic_login']['custom']['name'] = kwargs['custom']['name']
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['automatic_login']['custom']['password'] = kwargs['custom']['password']
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['automatic_login']['custom']['domain'] = kwargs['custom']['domain']
                if(kwargs['automatic_login'] == {}):
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['automatic_login'] = kwargs['automatic_login']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['rdp']['display_on_mobile'] = kwargs['display_on_mobile']

            if (kwargs['service_type'] == 'sshv2'):
                json_input = copy.deepcopy(self.initial_json_virtual_office_ssh)
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['sshv2']['automatic_accept_host_key'] = kwargs['automatic_accept_host_key']
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['sshv2']['display_on_mobile'] = kwargs['display_on_mobile']
            if (kwargs['service_type'] == 'telnet'):
                json_input = copy.deepcopy(self.initial_json_virtual_office_telnet)
                json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['telnet']['display_on_mobile'] = kwargs['display_on_mobile']
            if (kwargs['service_type'] == 'vnc'):
                json_input = copy.deepcopy(self.initial_json_virtual_office_vnc)
                try:
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['vnc']['view_only'] = kwargs['view_only']
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['vnc']['share_desktop'] = kwargs['share_desktop']
                    json_input['ssl_vpn']['virtual_office']['bookmark'][0]['service']['vnc']['display_on_mobile'] = kwargs['display_on_mobile']

                except KeyError as ke:
                    logger.info('Json paramters failed is {}'.format(ke))

            json_input['ssl_vpn']['virtual_office']['bookmark'][0]['name'] = kwargs['name']
            json_input['ssl_vpn']['virtual_office']['bookmark'][0]['host'] = kwargs['host']

        except KeyError:
            logger.error('Error: in creating JSON for SSLVPN Server settings')
            logger.info('The json input is {}'.format(json_input))

        return json_input

    def get_virtual_office(self):
        get_response = self.fw.api_get(self.bookmark_url)
        return get_response

    #Create bookmark method
    def configure_bookmark(self, msg=False, **kwargs):
        self.options = dict(SSLVPNVirtualOfficeAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_virtual_office(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        sslbookmark_resp = self.fw.api_post(self.bookmark_url, msg, data=json_input)
        return sslbookmark_resp

    def edit_bookmark(self, msg=False, **kwargs):
        self.options = dict(SSLVPNVirtualOfficeAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_virtual_office(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        url = self.bookmark_url + '/name/' + json_input['ssl_vpn']['virtual_office']['bookmark'][0]['name']
        sslbookmark_resp = self.fw.api_put(url, msg, data=json_input)
        # sslbookmark_resp = self.fw.api_put(self.bookmark_url, msg, data=json_input)
        return sslbookmark_resp
        
    def add_bookmark(self, msg=False, **kwargs):
        json_input = copy.deepcopy(kwargs)
        logger.info(json_input)
        resp = self.fw.api_post(self.bookmark_url, msg, data=json_input)
        return resp

    def delete_bookmark(self, msg=False, **kwargs):
        self.options = dict(SSLVPNVirtualOfficeAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_virtual_office(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        sslbookmark_resp = self.fw.api_delete(self.bookmark_url, msg, data=json_input)
        return sslbookmark_resp
        
    def delete_bookmark_by_name(self, name):
        url = self.bookmark_url + '/name/' + name
        sslbookmark_resp = self.fw.api_delete(url)
        return sslbookmark_resp


class SSLVPNClientSettingsAPI:
    '''SSLVPN Client Settings'''
    default_options = {
        'name': 'Default Device Profile',
        'description': 'Default Device Profile',
        # 'ipv4_network_address_name': '',
        # 'ipv4_network_address_zone': '',
        # 'ipv6_network_address_name': '',
        # 'ipv6_network_address_zone': '',
        # 'dns_primary': '',
        # 'dns_secondary': '',
        # 'search_list': [],
        # 'wins_primary': '',
        # 'wins_secondary': '',
        'auto_update': False,
        'exit_after_disconnect': False,
        'netbios_over_sslvpn': False,
        'touch_id_authentication': False,
        'fingerprint_authentication': False,
        'uninstall_after_exit': False,
        'create_connection_profile': False,
        #'cache' :'',        # 'credentials': True, user_name_only :True
        'tunnel_all': False,
        # 'route_ipv4': ' ',
        # 'route_ipv6' :' '

    }
    default_options_SonicPointN = {
        'name': 'Default Device Profile for SonicPointN',
        'description': 'Default Device Profile for SonicPointN',
        'network_address_name': '',
        'network_address_zone': '',
        'tunnel_all': False,
        'route_type': ' ',
        'wlan_tunnel_interface': ''

    }
    def __init__(self, fw):
        self.fw = fw
        self.deviceprofile_url = 'api/sonicos/ssl-vpn/device-profiles'
        self.logout_vpn = 'api/sonicos/ssl-vpn/logout'
        self.device_route_url = 'api/sonicos/ssl-vpn/device-profile-routes'
        self.device_client_dns = 'api/sonicos/ssl-vpn/device-profile-client-dns'
        self.initial_json_default_device_profile = {
            'ssl_vpn': {
                'profile': {
                    'device_profile':[
                        {
                            'name': 'Default Device Profile',
                            'description': 'Default Device Profile',
                            'network_address': {
                                'ipv4': {
                                    'name': {}
                                },
                                'ipv6': {
                                    'name' :{}
                                }
                            },
                            'client': {
                                'dns': {
                                    'primary':{
                                        #'value':None
                                    },
                                    'secondary': {
                                       # 'value':None
                                    },
                                    'search_list': [
                                        {
                                            'search_list': None
                                        }
                                    ]
                                },
                                'wins': {
                                    'primary': {
                                        #'value':None
                                    },
                                    'secondary': {
                                       # 'value':None
                                    }
                                },
                                'auto_update': False,
                                'exit_after_disconnect': False,
                                'netbios_over_sslvpn': False,
                                'touch_id_authentication': False,
                                'fingerprint_authentication': False,
                                'uninstall_after_exit': False,
                                'create_connection_profile': False,
                                'cache': {},
                            },
                            'routes': {
                                'tunnel_all': False,
                                'route':[]
                            }
                        }
                    ]
                }
            }
        }


        self.initial_json_device_profile_SonicPointN = {
            'ssl_vpn': {
                'profile': {
                    'device_profile':[
                       {
                        'name': 'Default Device Profile for SonicPointN',
                        'description': 'Default Device Profile for SonicPointN',
                        'network_address': {
                            'ipv4': {
                                'name': {
                                   'name':None,
                                   'zone': None
                                     }
                            }
                        },

                        'routes': {
                            'tunnel_all': True,
                            'route':[]
                        },
                        'wlan_tunnel_interface': ''
                        }
                    ]
                }
            }

        }


    def build_json_default_device_profile(self, **kwargs):
        json_input = {}
        search_new = []
        route_new = []
        try:
            json_input = copy.deepcopy(self.initial_json_default_device_profile)
            if 'ipv4_network_address_name' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['name'] = kwargs['ipv4_network_address_name']
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['zone'] =kwargs['ipv4_network_address_zone']
            else:

                del json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']

            if 'ipv6_network_address_name' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']['name'] = kwargs['ipv6_network_address_name']
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']['zone'] =kwargs['ipv6_network_address_zone']
            else:
                del json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv6']['name']


            if 'dns_primary' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['primary']['value'] = kwargs['dns_primary']
            if 'dns_secondary' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['secondary']['value'] = kwargs['dns_secondary']
            if 'search_list' in kwargs.keys():
                for search in kwargs['search_list']:
                    search_gt = {'search_list': search}
                    search_new.append(search_gt)
                    logger.info('The search list appended is {}'.format(search_new))
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['dns']['search_list'] = search_new
            if 'wins_primary' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['wins']['primary']['value'] = kwargs['wins_primary']
            if 'wins_secondary' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['wins']['secondary']['value'] = kwargs['wins_secondary']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['auto_update'] = kwargs['auto_update']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['exit_after_disconnect'] = kwargs['exit_after_disconnect']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['netbios_over_sslvpn'] = kwargs['netbios_over_sslvpn']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['touch_id_authentication'] = kwargs['touch_id_authentication']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['fingerprint_authentication'] = kwargs['fingerprint_authentication']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['uninstall_after_exit'] = kwargs['uninstall_after_exit']
            json_input['ssl_vpn']['profile']['device_profile'][0]['client']['create_connection_profile'] = kwargs['create_connection_profile']
            if 'tunnel_all' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['routes']['tunnel_all'] = kwargs['tunnel_all']
            if 'route_ipv4' in kwargs.keys():
                for route_list in kwargs['route_ipv4']:
                    if 'route_name' in kwargs.keys() and kwargs['route_name']:
                        group_append = {'name': route_list}
                    else:
                        group_append = {'group' : route_list}
                    ipv4_append = { 'ipv4' : group_append}
                    route_new.append(ipv4_append)
                    logger.info('The route appended is {}'.format(route_new))
                json_input['ssl_vpn']['profile']['device_profile'][0]['routes']['route'] = route_new
            if 'route_ipv6' in kwargs.keys():
                for route_list in kwargs['route_ipv6']:
                    if 'route_name' in kwargs.keys() and kwargs['route_name']:
                        group_append = {'name': route_list}
                    else:
                        group_append = {'group' : route_list}
                    ipv6_append = { 'ipv6' : group_append}
                    route_new.append(ipv6_append)
                    logger.info('The route appended is {}'.format(route_new))
                json_input['ssl_vpn']['profile']['device_profile'][0]['routes']['route'] = route_new
            else:
                pass

            if 'credentials' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['credentials'] = kwargs['credentials']
            elif 'user_name_only' in kwargs.keys():
                #del json_input['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['credentials']
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['user_name_only'] = kwargs['user_name_only']
            else:
                #del json_input['ssl_vpn']['profile']['device_profile'][0]['client']['cache']['credentials']
                json_input['ssl_vpn']['profile']['device_profile'][0]['client']['cache'] = kwargs['cache']
        except KeyError as e:
            logger.error('Error: in creating JSON for SSLVPN Server settings : {}'.format(e))
            logger.info('The json input is {}'.format(json_input))

        return json_input

    def build_json_device_profile_SonicPointN(self, **kwargs):
        json_input = {}
        try:
            json_input = copy.deepcopy(self.initial_json_device_profile_SonicPointN)
            if 'network_address_name_N' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['name'] = kwargs['network_address_name_N']
            if 'network_address_zone_N' in kwargs.keys():
                json_input['ssl_vpn']['profile']['device_profile'][0]['network_address']['ipv4']['name']['zone'] = kwargs['network_address_zone_N']
        except KeyError as e:
            logger.error('Error: in creating JSON for SSLVPN Server settings : {}'.format(e))
            logger.info('The json input is {}'.format(json_input))

        return json_input

    def get_default_device_profile(self):
        get_response = self.fw.api_get(self.deviceprofile_url)
        return get_response

    def logout_sslvpn_session(self,sslvpnclientip,msg=False):
        if not sslvpnclientip:
            logger.info('pls enter sslvpnclientip')
            return False
        else:
            url = self.logout_vpn + '/' + sslvpnclientip
            status = self.fw.api_post(url,msg)
        return status

    def edit_default_device_profile(self, msg=False, **kwargs):
        self.options = dict(SSLVPNClientSettingsAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_default_device_profile(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        deviceprofile_resp = self.fw.api_put(self.deviceprofile_url, msg, data=json_input)
        return deviceprofile_resp

    def delete_device_profile_client_dns(self, name, ip, msg=False):

        url = self.device_client_dns + '/' + name + '/'  + 'search-list' + '/' + ip
        client_dns_resp = self.fw.api_delete(url, msg)
        return client_dns_resp

    def edit_device_profile_SonicPointN(self, msg=False, **kwargs):
        self.options = dict(SSLVPNClientSettingsAPI.default_options)
        self.options.update(kwargs)
        kwargs = self.options
        json_input = self.build_json_device_profile_SonicPointN(**kwargs)
        logger.info('The json input build is {}'.format(json_input))
        profile_n_resp = self.fw.api_put(self.deviceprofile_url, msg, data=json_input)
        return profile_n_resp

    def delete_device_profile_route(self, name, ip_type, msg=False):

        url = self.device_route_url + '/' + name + '/' + 'route' + '/' + ip_type
        device_route_resp = self.fw.api_delete(url, msg)
        return device_route_resp

    def get_sslvpn_sessions(self):
        url = 'api/sonicos/reporting/ssl-vpn/sessions'
        resp = self.fw.api_get(url)
        return resp
        
    def get_sslvpn_bookmarks_sessions(self):
        url = 'api/sonicos/reporting/ssl-vpn/bookmarks/sessions'
        resp = self.fw.api_get(url)
        return resp


class VirtualOfficeAPI:
    def __init__(self):
        urllib3.disable_warnings()

    def user_login(self, ipaddr, username, password):
        s = requests.Session()
        url = f"https://{ipaddr}:4433/api/sonicos/auth"
        payload = {"domain": "LocalDomain", "override": 'false', "snwl": 'true'}
        data = json.dumps(payload)
        header = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
        }
        try:
            requests.packages.urllib3.disable_warnings()
            response = s.post(url, auth=HTTPBasicAuth(username, password), headers=header, data=data, verify=False)
            response.raise_for_status()
            if response.status_code == 200:
                return f"Login successful for {username}."
        except requests.exceptions.RequestException as e:
            return f"Login error for {username}, message: {e}"
