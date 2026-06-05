import os, sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('\\'))
print(suite_absolute_path)
script_list= ['modules', 'API']
for folder in script_list:
    root = ''
    os.chdir(scriptPath)
    for i in range(suite_absolute_path.index(folder)-1, len(suite_absolute_path)-1):
        root = root + '../../'
        print(root)
    os.chdir(root)
    dir = os.path.abspath(os.curdir)
    sys.path.append(dir)
print(sys.path)
from utm import Firewall
from modules.API.virtualassist import SettingApi
ip = '10.5.92.25'
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
print(fw)
url = 'api/sonicos/virtual-assist/settings'
vaobj = SettingApi(fw)
def virtualAssist1():
    json_put1 = {
            'assistance_code': '1234',
            'support_without_invitation': False,
            'disclaimer': '',
            'customer_access_link': '',
            'link_on_portal_login': False,
            'technician_email_list': '',
            'invitation_subject': '%EXPERTNAME% has sent you a support invitation',
            'invitation_message': 'An assistance invitation has been generated for you by: %EXPERTNAME%<br>%CUSTOMERMSG%<br>%SUPPORTLINK%<br>If you cannot access the link please request assistance by copying and pasting this link: <br>%ACCESSLINK%<br>Please do not reply.This message was automatically generated',
            'max_requests': 5,
            'limit_message': 'Maximum queue size reached, please try again later',
            'max_requests_one_ip': 0,
            'pending_request_expiration': 0,
            'host': ['4.4.4.4','5.5.5.5', '6.6.6.6'],
            'network':[{'net': ['10.10.10.10'],'mask':['255.255.255.0']}]

    }
    rc=vaobj.config_virtual_assist(**json_put1)
    print(rc)

virtualAssist1()