from definition.init_param import *


class TestConfigTB_01(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_config_interface_x1(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': '255.255.255.0',
            'gateway': Parameter.X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_snmp': True,
            'mgmt_https': True,
        }
        rc = interface_obj.config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    def test_02_config_interface_x0_ipv6(self):
        logger.info("config x0 interface ipv6... ")
        x0_ipv6 = {'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.X0_IPv6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': False,
            'adv_pref': False,
            'ra_min': 20,
            'ra_max': 30
        }
        rc = interface_ipv6_Obj.config_interface_ipv6(**x0_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config x0 interface ipv6 failed")    

    def test_03_config_interface_x1_ipv6(self):
        logger.info("config x1 interface ipv6... ")
        x1_ipv6 = {'name': 'X1',
            'mode': 'static',
            'zone': 'WAN',
            'ip': Parameter.X1_IPv6,
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ssh':True,
            'router_adv': True,
            'adv_pref': True,
            'ra_min': 20,
            'gateway':Parameter.X1_IPv6_GW,
            'ra_max': 30
            }
        rc = interface_ipv6_Obj.config_interface_ipv6(**x1_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config x1 interface ipv6 failed")    



class TestConfigTB_02(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_01_install_nmap(self):
        logger.info("install nmap... ")
        flag = False
        cmd = f'yum localinstall -y {os.environ["PYTHON_SONICOS_HOME"]}/Network/IPv6_Port_Scanning_TP766/definition/nmap-7.98-1.x86_64.rpm'
        # local_host.send_command(cmd)
        pc2_ssh.send_command(cmd)
        # output1 = local_host.send_command('nmap -version')
        output2 = pc2_ssh.send_command('nmap -version')
        if re.search(r'Nmap version\s+\d.\d+', str(output2), re.I|re.DOTALL):
            flag =True
        Assertion.assert_equal(flag, True, "ERR: install nmap failed")
