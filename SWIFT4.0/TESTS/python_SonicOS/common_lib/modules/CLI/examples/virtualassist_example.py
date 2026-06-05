import os,sys
root = ''
scriptPath = os.path.realpath(os.path.dirname(sys.argv[0]))
suite_absolute_path = (scriptPath.split('/'))
print('***************',suite_absolute_path)
script_list= ['mnt','c','modules', 'CLI']
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

import modules.CLI.virtualassist
from utm import Firewall
ip = '10.5.92.25'
port = '22'
fw = Firewall(ip,user='admin',password='password',supported_config_mode='cli-ssh')

vir_assist = modules.CLI.virtualassist.VirtualAssistCli(fw)

show_virtual={
	'command'='virtual-assist'
	}
virtual_show= vir_assist.show_virtual_assist(**show_virtual, tag=1)
print(virtual_show)

virtualassist_dict= {
    'assistance-code': '123456',
    'customer-access-link': 'https://abc.com',
    'support-without-invitation': False,
    'link-on-portal-login': True,
    'technician-email-list': 'abc',
    'invitation-subject': 'abhcjnj',
    'disclaimer': 'abchdfdf',
    'invitation - message': "An assistance invitation has been generated for you by: %EXPERTNAME%<br>%CUSTOMERMSG%<br>%SUPPORTLINK%<br>If you cannot access the link please request assistance by copying and pasting this link: <br>%ACCESSLINK%<br>Please do not reply.This message was automatically generated",
    ' max-requests': '10',
    'max-requests-one-ip':'5',
    'limit - message': 'Maximum queue size reached',
    'pending-request-expiration':'2',
    'host': ['1.1.1.1', '2.2.22.2', '3.3.3.3']
    #'network':['10.1.1.1 255.255.255.0', '10.2.2.1 255.255.255.0'],

    }
output1 = vir_assist.config_virtualassist(**virtualassist_dict, tag=1)
print(output1)

vir_assist1 = modules.CLI.virtualassist.virtualassistCli(fw)

delete_host_network_IP= {
    'del_host_ip': ['1.1.1.1', '2.2.22.2'],
    'del_network_ip':['10.1.1.1','10.2.2.1']
    }
#fw = Firewall(ip,user='admin',password='password',supported_config_mode='cli-ssh')

del_host_network_result= vir_assist1.delete_host_network(**delete_host_network_IP, tag=1)
print(del_host_network_result)