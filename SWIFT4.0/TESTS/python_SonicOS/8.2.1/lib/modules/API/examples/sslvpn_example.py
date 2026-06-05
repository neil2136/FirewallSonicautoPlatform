import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print('***************',suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../../'
        print('+++++',root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

from utm import Firewall
from modules.API.sslvpn import *

ip = '10.5.192.24'

fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
#SSLVPNServerSettingsAPI
server_url='/api/sonicos/ssl-vpn/server'
portal_url='/api/sonicos/ssl-vpn/portal'
serversetobj = SSLVPNServerSettingsAPI(fw)
portalsetobj = SSLVPNPortalSettingsAPI(fw)
virtualsetobj = SSLVPNVirtualOfficeAPI(fw)
clientsetobj = SSLVPNClientSettingsAPI(fw)
def put_server_settings():    # ssl_vpn= {    #         'server': {    #    #             'port':12,    #             'certificate': {    #                 'use_self_signed': True,    #             },    #             'use_radius': {    #                 'mschapv2': True,    #                 # 'mschap': True    #             }    #         }    #     }    ssl_vpn= {                'port': 12,                'use_self_signed': True,                'user_domain': 'LocalDomain',                'web': True,                'ssh': False,                'session_timeout': 13,                'default' : True,                'mschap': True,                'inactivity_check':True                }    put_response=serversetobj.edit_server_setting(**ssl_vpn)    print('The put update is %%%%%%%%%%%%% ',put_response)def get_server_settings():    get_server_set_resp = serversetobj.get_server_base_setting()    print(get_server_set_resp)def put_serveraccess_settings():    # 'ssl_vpn': {    #     'server': {    #         'access': [    #             {    #    #                 'enable': False,    #                 'zone': 'LAN'    #             },    #             {    #    #                 'enable': False,    #                 'zone': 'WAN'    #             },    #             {    #    #                 'enable': False,    #                 'zone': 'DMZ'    #             }    #         ]    #     }    # }    # }}    #     }    ssl_vpn= {               'LAN_enable' :True,                'WAN_enable':True,                'DMZ_enable':False,                }    put_response=serversetobj.edit_server_access_setting(**ssl_vpn)    print('The put update is ',put_response)def get_serveraccess_settings():    get_server_set_resp = serversetobj.get_server_access_setting()    print(get_server_set_resp)put_server_settings()put_serveraccess_settings()get_serveraccess_settings()get_server_settings()
#################################def put_portal_settings():        # ssl_vpn = {        #     'portal': {        #         'site_title': 'SonicWall - Virtual Office',        #         'banner_title': 'Virtual Office',        #         'home_page_message': {        #             'custom': '<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\'font-size:18px;\'><B> to the SonicWall Virtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\'line-height:115%;\'><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></sp'        #         },        #         'login_message': {        #             'custom': '<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\'font-size:18px;\'><B> to the SonicWall Virtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\'line-height:115%;\'><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></span></td></tr></table>'        #         },        #         'auto_launch': True,        #         'cache_control': True,        #         'display_link': True,        #         'logo': {        #             'custom': '/VirtualOffice.gif'        #         }        #     }        # }        ssl_vpn = {                'site_title': 'SonicWall - Virtual Office',                'banner_title': 'Virtual Office',                'home_custom': '<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\'font-size:18px;\'><B> to the SonicWall Virtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\'line-height:115%;\'><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></sp',                'login_custom': '<table cellspacing=0 cellpadding=0 border=0 valign=top><tr><td width=500 valign=top><font class=toolbar style=\'font-size:18px;\'><B> to the SonicWall Virtual Office</b></font><BR><img src=shim.gif width=1 height=6 border=0><BR><span style=\'line-height:115%;\'><font class=toolbar2>SonicWall Virtual Office provides secure Internet access for remote users to log in and access private network resources via SSLVPN technology.</font></span></td></tr></table>',                'auto_launch': True,                'cache_control': True,                'display_link': True,                'logo_custom': '/VirtualOffice.gif'        }        put_response=portalsetobj.edit_portal_setting(**ssl_vpn)        print('The put update is ',put_response)        response = portalsetobj.get_portal_setting()        print(response)def get_portal_settings():    get_portal_set_resp = portalsetobj.get_portal_setting()    print('*************',get_portal_set_resp)# get_portal_settings()# # put_portal_settings()##################################def create_virtual_settingsssh():    # ssl_vpn = {    #         'virtual_office': {    #             'bookmark': [    #                 {    #                     'name': 'SSH123',    #                     'host': '10.5.252.43',    #                     'service': {    #                         'sshv2': {    #                             'automatic_accept_host_key': False,    #                             'display_on_mobile': False    #                         }    #                     }    #                 }    #             ]    #         }    #     }    ssl_vpn = {                            'name': 'SSH12334',                            'host': '10.5.252.43',                            'service_type': 'sshv2',                            'ssl_type':'sshv2',                            'automatic_accept_host_key': False,                            'display_on_mobile': False            }    put_response=virtualsetobj.configure_bookmark(**ssl_vpn)    print('The put update is ',put_response)        # response = portalsetobj.get_portal_setting()        # print(response)create_virtual_settingsssh()def create_virtual_settingsrdp():    ssl_vpn = {                    'name': 'RDP1',                    'host': '10.5.252.115',                    'service_type':'rdp',                    'redirect_clipboard': True,                    'redirect_audio': False,                    'auto_reconnection': True,                    'desktop_background': False,                    'window_drag': False,                    'animation': False,                    'screen_size': 'full-screen',                    'colors': '16bit',                    'application_path': '',                    'start_in_folder': '',                    'automatic_login' : {},                    'display_on_mobile': False             }    put_response=virtualsetobj.configure_bookmark(**ssl_vpn)    print('The put update is ',put_response)create_virtual_settingsrdp()def create_virtual_settingstelnet():    ssl_vpn = {                   'name': 'telnet11',                    'host': '10.5.252.115',                    'service_type':'telnet',                    'display_on_mobile': True    }    create_response=virtualsetobj.configure_bookmark(**ssl_vpn)    print('The  create bookmark is ',create_response)create_virtual_settingstelnet()def create_virtual_settingsvnc():    ssl_vpn = {                    'name': 'vnc11',                    'host': '10.5.252.115',                    'service_type':'vnc',                    'view_only': False,                    'share_desktop': False,                    'display_on_mobile': False    }    put_response=virtualsetobj.configure_bookmark(**ssl_vpn)    print('The put update is ',put_response)create_virtual_settingsvnc()def create_virtual_settingsssh2():    ssl_vpn = {                'name': 'ssh_settings1',                'host': '10.5.252.115',                'service_type':'sshv2',                'display_on_mobile': False,                'automatic_accept_host_key': False,                'display_on_mobile': True    }    put_response=virtualsetobj.configure_bookmark(**ssl_vpn)    print('The put update is ',put_response)create_virtual_settingsssh2()def edit_virtual_settingsssh2():    ssl_vpn = {                'name': 'ssh_settings1',                'host': '10.5.252.116',                'service_type':'sshv2',                'display_on_mobile': False,                'automatic_accept_host_key': False,                'display_on_mobile': True    }    put_response=virtualsetobj.edit_bookmark(**ssl_vpn)    print('The put update is ',put_response)
def edit_virtual_settingsssh2():    ssl_vpn = {                'name': 'ssh_settings1',                'host': '10.5.252.116',                'service_type':'sshv2',                'display_on_mobile': False,                'automatic_accept_host_key': False,                'display_on_mobile': True    }    put_response=virtualsetobj.edit_bookmark(**ssl_vpn)    print('The put update is ',put_response)edit_virtual_settingsssh2()def delete_virtual_settingsssh2():    ssl_vpn = {                'name': 'ssh_settings1',                'host': '10.5.252.116',                'service_type':'sshv2',                'display_on_mobile': False,                'automatic_accept_host_key': False,                'display_on_mobile': True    }    put_response=virtualsetobj.delete_bookmark(**ssl_vpn)    print('The put update is ',put_response)delete_virtual_settingsssh2()
########CLIENT SETTINGS ##########################
def edit_client_settings():

    #                     'name': 'Default Device Profile',
    #                     'description': 'Default Device Profile',
    #                     'network_address': {
    #                         'ipv4': {
    #                             'name': {
    #                                 'name': 'B',
    #                                 'zone': 'SSLVPN'
    #                             }
    #                         },
    #                         'ipv6': {
    #                             'name': {
    #                                 'name': 'D',
    #                                 'zone': 'SSLVPN'
    #                             }
    #                         }
    #                     },
    #                     'client': {
    #                         'dns': {
    #                             'primary': '10.5.252.155',
    #                             'secondary': '10.5.252.115',
    #                             'search_list': [
    #                                 {
    #                                     'search_list': 'win2012.com'
    #                                 },
    #                                 {
    #                                     'search_list': 'tensa.com'
    #                                 }
    #                             ]
    #                         },
    #                         'wins': {
    #                             'primary': '0.0.0.0',
    #                             'secondary': '0.0.0.0'
    #                         },
    #
    #                     'routes': {
    #                         'tunnel_all': false,
    #                         'route': [
    #                             {
    #                                 'ipv4': {
    #                                     'group': 'LAN Subnets'
    #                                 }
    #                             }
    #                         ]
    #                     }
    #                 },

    ssl_vpn = {

                # 'name': 'Default Device Profile',
                # 'description': 'Default Device Profile',
                'ipv4_network_address_name': 'A',
                'ipv4_network_address_zone': 'SSLVPN',
                'dns_primary':'10.5.252.155',
                'dns_secondary':'10.5.252.115',
                'search_list':['win2012.com'],
                'wins_primary': '0.0.0.',
                'wins_secondary':'0.0.0.0',
                'auto_update': True,
                'exit_after_disconnect': True,
                'netbios_over_sslvpn': True,
                'touch_id_authentication': True,
                'fingerprint_authentication': True,
                'uninstall_after_exit': True,
                'create_connection_profile': True,
                'cache' :{},
                # 'user_name_only': True,
                # 'credentials' : True,
                'tunnel_all': False,
                'route_type': ' ',
                'route_ipv4': ['LAN Subnets'],
                 'route_ipv6' : ['Address_group2', 'X0 IPv6 Addresses'],
                # 'route_ipv6' :['X0 IPv6 Addresses']




            }




    put_response = clientsetobj.edit_default_device_profile(**ssl_vpn)
    print('The put update is ',put_response)
    # response = portalsetobj.get_default_device_profile()
    # print(response)

    # del_response = clientsetobj.delete_device_profile_client_dns(name = 'Default Device Profile', ip ='win2012.com')
    # print(del_response)


edit_client_settings()

def edit_client_settingsN():
    ssl_vpn = {
                'name_N': 'Default Device Profile for SonicPointN',
                'description_N': 'Default Device Profile for SonicPointN',
                'network_address_name_N': 'G',
                'network_address_zone_N':'SSLVPN',
                'tunnel_all_N': True,
                'route_type_N': ' ',
                'wlan_tunnel_interface': ''
    }

    put_response = clientsetobj.edit_device_profile_SonicPointN(**ssl_vpn)
    print('The put update is ',put_response)
edit_client_settingsN()