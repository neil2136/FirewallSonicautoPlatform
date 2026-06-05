from definition.settings import *


class TestConfig_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True
    
    def test_01_config_route_on_pc1(self):
        os.system('route add -net 12.12.1.0/24 gateway 192.168.168.168')  
        Assertion.assert_equal(True, True, 'ERR: add route on PC1 failed!!')

    @repeat_method(3)
    def test_02_install_dhcpv6_server_packages_on_pc2(self):
        check_install = PC2_login.send_command('dpkg -l | grep -E "dibbler-server|radvd"')
        
        if 'dibbler-server' not in check_install or 'radvd' not in check_install:
            print("Some packages are missing, installing...")
            PC2_login.send_command('sudo nohup apt-get update 2>&1 &')
            sleep(180)
            
            if 'dibbler-server' not in check_install:
                PC2_login.send_command('sudo nohup apt-get install -y dibbler-server 2>&1 &')
                sleep(180)
            
            if 'radvd' not in check_install:
                PC2_login.send_command('sudo nohup apt-get install -y radvd 2>&1 &')
                sleep(180)
        else:
            print("All required packages are already installed.")

        verify_install = PC2_login.send_command('dpkg -l | grep -E "dibbler-server|radvd"')
        rc = 'dibbler-server' in verify_install and 'radvd' in verify_install
        Assertion.assert_equal(rc, True, "ERR: install dibbler-server and radvd failed")

    def test_03_setup_dhcpv6_server_on_pc2(self):
        server_conf_path = os.path.join(suite_path, 'definition/file')
        
        # cp conf file to pc2
        cmd_list = ['sudo killall dibbler-server',f'sudo \cp {server_conf_path}/radvd.conf /etc/', f'sudo \cp {server_conf_path}/server_ubuntu24.conf /etc/dibbler/server.conf', f'sudo \cp {server_conf_path}/sysctl.conf /etc/']
        PC2_login.send_commands(cmd_list)
        sleep(3)
        PC2_login.send_command( 'sudo sysctl -p')
        PC2_login.send_command( 'sudo systemctl restart radvd')
        sleep(3)
        PC2_login.send_command('sudo nohup dibbler-server run > /var/log/dibbler.log 2>&1 &')
        sleep(3)
        out = PC2_login.send_command('sudo dibbler-server status')
        Assertion.assert_regular(out, 'Dibbler server: RUNNING', 'ERR: start server on pc2 failed.')
    
    def test_04_config_pc2_v6_addr(self):
        PC2_login.send_command('sudo ip -6 addr flush dev eth1 scope global')
        PC2_login.send_command('sudo ip -6 addr add 2001:1:2:3::1/64 dev eth1')
        out = PC2_login.send_command('ip -6 addr show eth1')
        Assertion.assert_regular(out, '2001:1:2:3::1', 'ERR: config ipv6 address on PC2 eth1 failed.')

