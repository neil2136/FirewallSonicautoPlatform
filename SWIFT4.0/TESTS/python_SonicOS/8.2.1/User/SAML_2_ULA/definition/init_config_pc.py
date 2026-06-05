from definition.settings import *


class Test_Config_PC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_route_on_pc(self):
        pc1_login.send_commands(['timedatectl set-ntp on', 'route add -net 12.12.1.0/24 gateway 192.168.168.168'])
        pc3_login.send_commands(['timedatectl set-ntp on', 'route add -net 12.12.1.0/24 gateway 192.168.168.168'])
        out1 = pc1_login.send_command('ping -c 2 12.12.1.169')
        out2 = pc3_login.send_command('ping -c 2 12.12.1.169')
        rc = '100% packet loss' not in out1 and '100% packet loss' not in out2
        Assertion.assert_equal(rc, True, 'ERR: config route on PC failed!!')

    def test_02_cp_xml_file_to_pc1(self):
        xml_file = suite_path + '/definition/file/saml_cyuan.xml'
        pc1_login.send_command(f'\cp {xml_file} /tmp')
        rc = os.path.exists('/tmp/saml_cyuan.xml')
        Assertion.assert_equal(rc, True, 'ERR: cp xml file FAILED!!')

    def test_03_setup_https_server_on_PC2(self):
        pc2_login.send_command('echo "cyuan test" > /root/index.html')
        pc2_login.send_command('systemctl restart httpd')
        out = pc2_login.send_command('curl -k https://12.12.1.169')
        rc = 'cyuan test' in out
        Assertion.assert_equal(rc, True, 'ERR: setup https server failed!!')
