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

from modules.API.security_services import *



ip = '192.168.168.168'



fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')

print(fw)

#SSLVPNServerSettingsAPI


servicebase = SecurityServicesBase(fw)


def put_securityservices_base():
    base= {
                'security': 'maximum',
                'reduce_isdn_antivirus_traffic': False,
                'drop_packets_at_reload': False,
                'web': True,
                'http_clientless_notification_timeout': 86400,
                'proxy_enable': True,
                'host' : '1.1.1.1',
                'port': 30,
                'enable_auth':True,
				'user_name': 'abhi',
				'password': 'sonicwall'
                }


    put_response=servicebase.configure_services_base(**base)


def get_security_services_settings():
    get_server_set_resp = servicebase.get_security_services_base()
    logger.info(get_server_set_resp)

