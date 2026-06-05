from definition.settings import *
from definition.utils import *


class TestInitFWConfig_Dut(Test):
    uuid = 'NonTC'

    def test_01_config_x1_interface(self):
        logger.info("Config DUT X1 Interface... ")
        rc = interface_api.config_interface(**dut_x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config DUT X1 interface Failed")

    def test_02_config_x2_interface(self):
        logger.info("Config DUT X2 Interface... ")
        rc = interface_api.config_interface(**dut_x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config DUT X2 interface Failed")

    def test_03_config_x3_interface(self):
        logger.info("Config DUT X3 Interface... ")
        rc = interface_api.config_interface(**dut_x3_static)
        Assertion.assert_equal(rc, True, "ERR: Config DUT X3 interface Failed")

    @parameterized.expand([(Parameter.R_X3_NET, 'LAN', 'network', f'{Parameter.R_X3_NET},{Parameter.MASK}'),
                           (Parameter.R_X2_IP, 'LAN', 'host', Parameter.R_X2_IP)])
    def test_04_add_ao_to_local_fw(self, name, zone, ao_type, value):
        logger.info(f'Add AO {name} To Local Firewall...')
        rc = add_ao(name, zone, ao_type, value)
        Assertion.assert_equal(rc, True, f"ERR: Add AO {name} To Local Fw Failed")
    
    @repeat_method(10)
    def test_05_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


class TestInitFWConfig_Remote(Test):
    uuid = 'NonTC'

    def test_01_inital_remote_fw(self):
        logger.info('Restore Remote FW...')
        path = os.environ["PYTHON_COMMON_HOME"] + \
               '/config/restore_gw_rmt_tel.py'
        command1 = (f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 '
                    f'-if=X1 -zone=WAN -ip={Parameter.R_X1_IP} -restore=1')
        confres = PC1_HOST.send_command(command1)
        logger.info(f"confres is {confres}")
        flag = True if confres else False
        Assertion.assert_equal(flag, True, "ERR: Intial Remote FW Failed")

    def test_02_configure_remote_fw_x2(self):
        logger.info('Configure Remote X2 Interface ..')
        rc = interface_api_remote.config_interface(**r_x2_config_dic)
        Assertion.assert_equal(rc, True, "ERR: Configure Remote X2 Interface Failed")

    @parameterized.expand([(Parameter.X0_NET, 'LAN', 'network', f'{Parameter.X0_NET},{Parameter.MASK}'),
                           (Parameter.X3_NET, 'LAN', 'network', f'{Parameter.X3_NET},{Parameter.MASK}'),
                           (Parameter.X2_IP, 'LAN', 'host', Parameter.X2_IP)])
    def test_03_add_ao_to_remote_fw(self, name, zone, ao_type, value):
        logger.info(f'Add AO {name} To Remote Firewall...')
        rc = add_ao(name, zone, ao_type, value, where="remote")
        Assertion.assert_equal(rc, True, f"ERR: Add AO {name} To Remote FW Failed")

    @parameterized.expand([(Parameter.X0_NET, Parameter.X2_IP),
                           (Parameter.X3_NET, Parameter.X2_IP)])
    def test_04_add_route_to_remote_fw(self, dest_name, gateway):
        logger.info(f"Add Static Route to {dest_name}.....")
        route_policy_dict["route_policies"][0]["ipv4"]["destination"]["name"] = dest_name
        route_policy_dict["route_policies"][0]["ipv4"]["gateway"]["name"] = gateway
        rc = route_api_remote.add_route_policy(**route_policy_dict)
        Assertion.assert_equal(rc, True, f"ERR: Add Static Route to {dest_name} Failed")

