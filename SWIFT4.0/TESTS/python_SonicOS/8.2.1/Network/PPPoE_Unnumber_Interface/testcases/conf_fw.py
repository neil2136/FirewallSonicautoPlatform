from settings import *

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
ao = network.AddressobjectsApi(fw)
snmp_obj = system.SNMPApi(fw)
license_obj = LicenseCli(fw_cli)


class TestConfigENV(Test):
    uuid = 'NonTC'
    pc2 = Host(Parameter.PC2_SERVER)

    def test_00_01_start_PPPoE_server_on_PC2(self):
        rc = self.pc2.start_PPPoE_server(interface=Parameter.PPPOE_ETH, local_ip=Parameter.PC2_ETH1, \
        assign_ip=Parameter.PPPOE_ASSIGH, ppp_secrets=Parameter.PPP_FILE, pppoe_option=Parameter.PPPOE_OPTION)
        Assertion.assert_equal(rc, True, "ERR: Start PPPoE Server on PC2 failed")    

    def test_00_02_Start_HTTPS_Server_on_PC2(self):
        rc = self.pc2.start_HTTPS_server(conf_path=os.environ['PYTHON_SONICOS_HOME'] + "/Network/PPPoE_Unnumber_Interface/confs")
        Assertion.assert_equal(rc, True, "ERR: Start HTTPS Server on PC2 failed")

    def test_00_03_start_FTP_server_on_PC2(self):
        self.pc2.send_command('service vsftpd start')
        rc = self.pc2.send_command('service vsftpd status')
        Assertion.assert_regular(rc, 'running', "ERR: Start FTP Server on PC2 failed")
    
    def test_00_04_config_snmp(self):
        advance = {'mandatory': False}
        rc = snmp_obj.snmp_advance_settings(**advance)
        config_snmp_dict = {
            "enable":True,
            "system_name": "SonicwallTest",
            "system_contact": "test@test.com",
            "system_location": "Shanghai",
            "asset_number": "1234567",
            "get_community_name": "public",
            "trap_community_name": "admin",
            "host_1": Parameter.PC1_ETH1,
        }
        rc &= snmp_obj.snmp_base_settings(**config_snmp_dict)
        Assertion.assert_equal(rc, True, "ERR: config snmp failed.")

    @unittest.skipIf(Params.product!='TZ80-PROTOTYPE','skip register if not TZ80-PROTOTYPE')
    def test_00_05_register(self):
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '13.0.12.100',
            'gateway': '13.0.12.1',
            'dns1': Params.G_DNS1,
        }
        rc = interface.config_interface(**x1_static)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register firewall failed")




