from settings import *

ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceIPv4Api(fw)
interface_v6 = network.InterfaceIPv6Api(fw)
license_obj = LicenseCli(fw_cli)
ao = network.AddressobjectsApi(fw)
if Params.openstack:
    osstack = Openstack(Params.testbed)
    consvr, conport = osstack.get_console_info(dut='RemoteGEN7')
rem_fw = Firewall(Parameter.REMOTE_X1, user='admin', password='password', console_ip=consvr, console_port=conport, supported_config_mode = 'cli-console')
rem_interface = InterfaceCli(rem_fw)
rem_dhcp = DhcpServerCli(rem_fw)

class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True
    pc3 = Host(Params.testbed + '-PC3')

    def test_00_01_start_PPPoE_server_on_PC3(self):
        rc = self.pc3.start_PPPoE_server(interface=Parameter.PPPOE_ETH, local_ip=Parameter.PPPOE_SERVER, assign_ip=Parameter.PPPOE_ASSIGH, ppp_secrets=Parameter.PPP_FILE, pppoe_option=Parameter.PPPOE_OPTION)
        Assertion.assert_equal(rc, True, "ERR: Start PPPoE Server on PC2 failed")    

    def test_00_02_config_dhcp_server_on_PC2(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=RemoteGEN7 -if=X1 -zone={} -ip={} -restore=1'.\
              format(path, Params.testbed,'WAN', Parameter.REMOTE_X1)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        ping = trafficGen.ping(Parameter.REMOTE_X1)

        rc = True
        if not ping:
            logger.info(f'config remote X1 to {Parameter.REMOTE_X1}')
            x1_static_dict = {
                'if': 'x1',
                'zone': 'WAN',
                'mode': 'static',
                'ip': Parameter.REMOTE_X1,
                'gateway': Parameter.REMOTE_X1_GW,
                'netmask': Parameter.NETMASK,
                'mgmt-https': True,
            }
            rc &= rem_interface.config_interface(**x1_static_dict)
        logger.info('config dhcp server scope on X2')
        x2_static_dict = {
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X2,
            'netmask': Parameter.NETMASK,
            'mgmt-https': True,
        }   
        rc &= rem_interface.config_interface(**x2_static_dict)
        object_option_v4 = {
            'name': 'for6rd',
            'number': '212',
            'type': 'hex-string',# ip, domain-name, boolean, one-type, two-type, four-type,string, hex-string
            'value': '18106868000000000000000000000000000004040404',#IPv4 mask length = 24, 6rd prefix length = 16, 6rd prefix = 6868::, BR iopv4 address = 4.4.4.4
            'array': True,
        }
        rem_dhcp.add_option_object_v4(**object_option_v4)
        dynamic_scope = {
            'enable': True,
            'type': 'dynamic',
            'start': Parameter.DUT_X2_IP,
            'end': Parameter.DUT_X2_IP,
            'netmask': Parameter.NETMASK,
            'gateway': Parameter.REMOTE_X2,
            'lease-time': '100',
            'option-object': 'for6rd'
        }
        rc &= rem_dhcp.add_dhcpserver_scope_v4 (**dynamic_scope)
        Assertion.assert_equal(rc, True, "ERR: Start PPPoE Server on PC2 failed")    

    @repeat_method(10, 10)
    def test_00_03_register_fw(self):
        rc = interface.config_interface(**Lx1)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestUnconfigENV(Test):
    uuid = 'NonTC'

    def test_01_01_config_dhcp_scope(self):
        dynamic_scope = {
            'enable': True,
            'type': 'dynamic',
            'start': Parameter.DUT_X2_IP,
            'end': Parameter.DUT_X2_IP,
            'netmask': Parameter.NETMASK,
            'gateway': Parameter.REMOTE_X2,
            'lease-time': '1',
            'option-object': 'for6rd'
        }
        rc = rem_dhcp.delete_dynmaic_scope(**dynamic_scope)
        Assertion.assert_equal(rc, True, "ERR: Start PPPoE Server on PC2 failed")  