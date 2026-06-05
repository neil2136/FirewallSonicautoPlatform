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

import modules.CLI.antispyware
from utm import Firewall
ip = '10.5.192.32'
port = '22'
fw = Firewall(ip,user='admin',password='password',supported_config_mode='cli-ssh')

vir_assist = modules.CLI.antispyware.antispywareCli(fw)
#dpisslclient = modules.CLI.dpissl.ClientsslCli(fw)
# enable_ssh
virtualassist_dict= {
    'enable': True,
    'prevent-all_hd': True

    }
output1 = vir_assist.config_antispyware(**virtualassist_dict, tag=1)
print(output1)

