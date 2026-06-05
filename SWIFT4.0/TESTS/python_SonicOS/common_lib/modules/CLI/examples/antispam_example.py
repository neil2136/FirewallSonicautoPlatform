import os,sys,time
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

import modules.CLI.anti_spam
from utm import Firewall
ip = '10.5.192.119'
port = '22'
fw = Firewall(
    ip,
    user='admin',
    password='password',
    supported_config_mode='cli-ssh')


antispam = modules.CLI.anti_spam.AntiSpamCLI(fw)
def test_show_commands():
    commands=" ","allow-list","reject-list","status","statistics"
    output=antispam.show_anti_spam_config(*commands)
    print("the output----------------------------")
    print(output)
def test_configure_commands_actions():
    for values in ["delete","filtering-off","store","tag"]:
        commands={
                "definite-phishing":values,
                "definite-spam":values,
                "definite-virus":values,
                "likely-phishing":values,
                "likely-spam":values,
                "likely-virus":values
        
                }
        output=antispam.config_settings(**commands)
        print("the output----------------------------")
        print(output)
        time.sleep(5)
def test_configure_commands():
    commands={

                "allow-list":"1.1.1.1",
                #"allow-list_fqdn":"1.com",
                #"allow-list_host":"2.2.2.2",
                #"allow-list_range":"3.3.3.3 3.3.3.4", 
                #"reject-list_fqdn":"4.com",
                #"reject-list_host":"5.5.5.5",
                #"reject-list_range":"6.6.6.6 6.6.6.7",
                "system-detection":True,
                "destination-mail-address-as-junk-store":True,
                #"enable":True,
                "service-down":"allow",
                "junk-box":"delete",
                "junk-store-ip":"30.30.30.30",
                "failure-threshold":"3",
                "success-threshold":"3",
                "probe_interval":"4",
                "probe_timeout":"41"
                # "mail-server_public":"41.41.41.41",
                # "mail-server_private":"42.42.42.42",
                # "mail-server_port":"43"                    

                }
    output=antispam.config_settings(**commands)
    print("the output----------------------------")
    print(output)

def delete_config_commands():
    commands={

                "allow-list":"1.1.1.1",
                #"allow-list_fqdn":"1.com",
                #"allow-list_host":"2.2.2.2",
                #"allow-list_range":"3.3.3.3 3.3.3.4", 
                #"reject-list_fqdn":"54.com",
                #"reject-list_host":"5.5.5.5",
                #"reject-list_range":"6.6.6.6 6.6.6.7",
                "system-detection":False,
                "destination-mail-address-as-junk-store":False,
                #"enable":False,
                "mail-server_public":None,
                "mail-server_private":None,
                "mail-server_port":None                    

                }
    output=antispam.del_config(**commands)
    print("the output----------------------------")
    print(output)









test_configure_commands()
test_configure_commands_actions()
test_show_commands()
delete_config_commands()

##################################RBL##################################

rbl=modules.CLI.Rbl.RblCli(fw)

def rbl_test_show_commands():
    commands=" ", "blacklist", ["service", "sbl-xbl.spamhaus.org"],"services","whitelist","statistics"
    output=rbl.show_rbl_config(*commands)
    print("the output----------------------------")
    print(output)

def rbl_test_configure_commands():
    commands={
                
                #"enable":False,
                #"whitelist":"X11\ IP",
                #"whitelist_fqdn":"12.com",
                "service":["domain abc.com","blocked-responses open-relay"],
                #"service":["enable dnsbl.sorbs.net"],
                #"service":["domain dnsbl.sorbs.net","no blocked-responses block-all"],
                #"service":["domain dnsbl.sorbs.net","blocked-responses open-relay"],
                #"service":["domain dnsbl.sorbs.net","domain dnsbl.sorbs.net1"],
                #"dns":["inherit"],
                #"dns":["static primary 4.4.8.8"],
                #"dns":["static secondary 8.8.8.8"],
                #"service":["domain dnsbl.sorbs.net","enable"]
                #"service":["domain dnsbl.sorbs.net","no enable"]
                
                

                }
    output=rbl.config_settings(**commands)
    print("the output----------------------------")
    print(output)

def rbl_test_remove_config_commands():
    commands={
        #"whitelist":"X11\ IP",
        #"dns":["static secondary 8.8.8.8"],
        #"service":["domain dnsbl.sorbs.net1","blocked-responses open-relay"],
        "service":["enable dnsbl.sorbs.net1"],
        "dns":["static primary"],
        "service":["domain abc.com"],
    }
    output=rbl.delete_config(**commands)
    print("the output----------------------------")
    print(output)

#rbl_test_show_commands()
#rbl_test_configure_commands()
rbl_test_remove_config_commands()
