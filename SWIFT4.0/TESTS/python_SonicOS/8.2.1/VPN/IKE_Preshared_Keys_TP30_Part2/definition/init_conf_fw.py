from definition.settings import *


class TestConfigFW_Local(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    @repeat_method(10)
    def test_02_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_config_x2_to_wan(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.add_interface(**x2_vlan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_04_config_x3_to_dmz(self):
        logger.info("config x3 interface... ")
        rc = interfaceapi.config_interface(**x3_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")


class TestConfigFW_Remote(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        x1_wan_dict = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.REMOTE_X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': False,
            'mgmt_ping': True,
            'user_https': False,
            'mgmt-snmp': False,
        }
        rc = r_interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_x2_to_wan(self):
        logger.info("config x2 interface... ")
        rc = r_interfaceapi.add_interface(**r_x2_vlan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")


class TestinitRemoteFW(Test):
    uuid = 'NonTC'

    async def run_init_fw_script(self):
        logger.info('start Restore Remote FW in asyncio...\n'
                    'Restore Remote FW process will run in the background of the OS.')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X1 -zone=WAN ' \
                  f'-ip={Parameter.REMOTE_X1_IP} -restore=1'
        logger.info(f'run commands: {command}')
        await asyncio.create_subprocess_shell(f'{command} > /tmp/output.txt &')
        logger.info('End run Restore Remote FW script in asyncio...')

    def test_01_init_remote_fw_via_asyncio(self):
        start_time = time.time()
        running = self.run_init_fw_script()
        loop = asyncio.get_event_loop()
        task = loop.create_task(running)
        loop.run_until_complete(task)
        logger.info(f'setup asyncio task time: {time.time() - start_time}')
        Assertion.assert_equal(task.done(), True, "ERR: init Remote FW config via asyncio task failed")
