from definition.settings import *


class TestInitConfig(Test):
    uuid = 'NonTC'
   
    @repeat_method(3) 
    def test_01_setup_ipv4_dns_server(self):
        flag = False
        ret = True
        named_conf = '/etc/named.conf'
        
        PC2_login.send_command('service named stop')  
        PC2_login.send_command(f'rm -f {named_conf}.bak')  
        PC2_login.send_command(f'mv {named_conf} {named_conf}.bak')  
        ret = PC2_login.send_command(f'\\cp -f {confs_path}named.conf /etc/') 
        ret = ret +  PC2_login.send_command(f'\\cp -f {confs_path}named.ca /var/named/') 
        ret = ret + PC2_login.send_command(f'\\cp -f {confs_path}named.local /var/named/')  
        ret = ret + PC2_login.send_command(f'\\cp -f {confs_path}127.0.0.zone /var/named/')  
        ret = ret + PC2_login.send_command(f'\\cp -f {confs_path}limitFQDN.com.db /var/named/')  
        ret = ret + PC2_login.send_command(f'\\cp -f {confs_path}13.0.0.db /var/named/') 
        logger.info(ret)
        PC2_login.send_command("service named restart -kill") 
        PC2_login.send_command("service named start")
        status = PC2_login.send_command("service named status")
        logger.info(status)
        if re.search(r'is running', status, re.I):
            flag = True
        Assertion.assert_equal(flag, True, "ERR:Start dns server on PC2 failed") 
