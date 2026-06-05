import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('/'))
print('***************',suite_absolute_path)
script_list= ['mnt','d','modules', 'CLI']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    print(os.chdir(scriptPath))
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../'
        print('+++++',root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)

import modules.CLI.sslvpn
from utm import Firewall
ip = '10.5.192.24'
port = '3035'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')


sslvpnserver = modules.CLI.sslvpn.SSLVPNServerSettingsCli(fw)
sslvpnportal = modules.CLI.sslvpn.SSLVPNPortalSettingsCli(fw)
sslvpnvirtual = modules.CLI.sslvpn.SSLVPNVirtualOfficeCli(fw)
sslvpnclient = modules.CLI.sslvpn.SSLVPNClientsettingsCli(fw)

########## Attribute keys used for SSLVPN Server:###############
'''
port 14
certificate 'use-self-signed'
user - domain LocalDomain
management web
no management ssh
session - timeout 10
download - url default
use - radius mschap
access LAN, WAN,WLAN,DMZ.
'''
def configure_serversettting():
    sslvpn_dict = {
            'port': '14',
            'management':['ssh'],
            'no management':['web'],
            'user-domain': 'LocalDomain1',
            'certificate':'ftp',
            'download-url':'default',
            'use-radius':'mschap',
            'session-timeout': 14,
            'access': ['LAN', 'DMZ'],
            'no access' :['WLAN']
    }


    output1 = sslvpnserver.config_server_settings(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')



def test_show_commands():
    commands=["server"]
    output=sslvpnserver.show_sslvpn_config(*commands)
    print("The sslvpn output----------------------------")
    print(output)

'''
Portal settings attributes
auto - launch
banner - title
cache - control
display - link
home - page - message
login - message
logo
site - title
'''
def configure_portalsettting():
    sslvpn_dict = {
            'site-title': 'newsite title',
            'banner-title':'ban-tittle',
            'home-page-message':'default',
            'login-message': 'default',
            'auto-launch': False,
            'cache-control':False,
            'display-link':False,
            'logo':'default'
            }


    output1 = sslvpnportal.config_portal_settings(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')

def configure_virtualofficerdp():
    sslvpn_dict = {
            'name': 'newsiterdp',
            'host':'10.10.10.10',
            'service':'rdp',
            'animation': False,
            'application-path': 'lkkfkdgfd',
            'auto-reconnection':False,
            'colors':'16bit',
            'screen-size':'full-screen',
            'desktop-background':False,
            'display-on-mobile':True,
            'start-in-folder':'nffjf',
            'window-drag':True,
            'automatic-login':'ssl-vpn',
            # 'custom-name':'kk',
            # 'password':'pkdfkd',
            # 'domain':'sv'
            }
    output1 = sslvpnvirtual.config_virtualoffice(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')

def configure_virtualofficessh():
    sslvpn_dict = {
        'name': 'newsitessh',
        'host': '10.10.10.10',
        'service': 'ssh',
        'automatic-accept-host-key':True,
        'display-on-mobile':True,
    }
    output1 = sslvpnvirtual.config_virtualoffice(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')

def configure_virtualofficetelnet():
    sslvpn_dict = {
        'name': 'newsitetelnet',
        'host': '10.10.10.10',
        'service': 'telnet',

    }
    output1 = sslvpnvirtual.config_virtualoffice(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')

def configure_virtualofficevnc():
    sslvpn_dict = {
        'name': 'newsitevnc',
        'host': '10.10.10.10',
        'service': 'vnc',
        'share-desktop': True,
        'view-only':True,
        'display-on-mobile':True
        }

    output1 = sslvpnvirtual.config_virtualoffice(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')



def edit_virtualofficevnc():
    sslvpn_dict = {
        'name': 'newsitevnc',
        'host': '10.10.10.100',
        'service': 'vnc',
        'share-desktop': True,
        'view-only':True,
        'display-on-mobile':True
        }

    output1 = sslvpnvirtual.edit_virtualoffice(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')
    # hh = sslvpnvirtual.del_bookmark('newsite')
    # del_all = sslvpnvirtual.del_all_bookmark()

def configure_devicepprofilebasicsettings():
    sslvpn_dict = {
        'ipv4': 'A',
        'ipv6': 'ipv6'
    }
    output1 = sslvpnclient.config_basic_settings(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')


def configure_devicepprofileclientsettings():
    sslvpn_dict = {
        'auto-update': True,
        'cache': 'credentials',
        # 'cache': 'user-name-only',
        'create-connection-profile':True,
        'exit-after-disconnect':True,
        'fingerprint-authentication':True,
        'netbios-over-sslvpn':True,
        'touch-id-authentication':True,
        'uninstall-after-exit':True,
        'inherit': True,
        'primary':'10.10.10.5',
        'secondary':'10.10.10.67',
        'search-list':['kk.com','ll.com'],
        'wins-primary':'1.1.1.1',
        'wins-secondary':'2.2.2.2'
        # 'no search-list':['kk.com']
        }

    output1 = sslvpnclient.config_client_settings(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')
    # del1 = sslvpnclient.del_search_list('kk.com', 'll.com')
    # del_all = sslvpnclient.del_all_search_list()


def configure_devicepprofileclientroutes():
    sslvpn_dict = {
        'name': ['fqdn_ttl1'],
        # 'ipv6_name': ['kk'],
        # 'group':['Addess_grpnew1]',
        # 'ipv6_group':['Address_fqdn2'],
        'tunnel-all' :True
    }

    output1 = sslvpnclient.config_client_routes(**sslvpn_dict)
    print('The output before commit')
    print(output1)
    print('The final out after commit changes')
# del_all_bookmark

# configure_serversettting()
# test_show_commands()
# configure_portalsettting()
# configure_virtualofficerdp()
# configure_virtualofficessh()
# configure_virtualofficetelnet()
# configure_virtualofficetelnet()
# configure_virtualofficevnc()
# edit_virtualofficevnc()
# configure_devicepprofilebasicsettings()
configure_devicepprofileclientsettings()
# configure_devicepprofileclientroutes()