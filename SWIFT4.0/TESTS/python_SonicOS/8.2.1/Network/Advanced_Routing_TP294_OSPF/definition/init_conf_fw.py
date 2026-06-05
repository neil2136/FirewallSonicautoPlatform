from definition.settings import *


class TestConfigFW_Local(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_config_x2_to_wan(self):
        x2_wan_dict = {
            'if': 'X2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '192.168.2.168',
            'netmask': Parameter.MASK,
            'gateway': '192.168.2.1',
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }

        rc = interfaceapi.config_interface(**x2_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to wan failed")

    def test_02_configure_dut_failover(self):
        wlb_conf_dict = {
            "failover_lb": {
                "group": [
                    {
                        "final_backup": "",
                        "interface": [
                            {
                                "name": "X2",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 1
                            },
                            {
                                "name": "X1",
                                "probe_condition": "always",
                                "probe_type": "physical",
                                "rank": 2
                            }
                        ],
                        "name": " Default LB Group",
                        "preempt": True,
                        "probing": {
                            "global_responder": False,
                            "health_check": 5,
                            "missed_intervals": 3,
                            "successful_intervals": 3
                        },
                        "type": "basic"
                    }
                ]
            }
        }
        res = failoverapi.config_failover_groups_by_multi(**wlb_conf_dict)
        Assertion.assert_equal(res, True, "ERR: Config DUT failover failed")

    @repeat_method(10)
    def test_03_Register_fw(self):
        time.sleep(20)
        rc = licensecli.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_config_x1_to_wan(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_05_config_x2_to_lan(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_06_config_x3_to_lan(self):
        logger.info("config x3 interface... ")
        rc = interfaceapi.config_interface(**x3_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")


class TestConfigFW_Remote(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(30, 20)
    def test_00_check_remote_x3_accessable(self):
        logger.info("check remote x3 accessable... ")
        output = PC1_login.send_command('ping -c 30 ' + Parameter.REMOTE_X3_IP)
        res = '30 received' in output
        Assertion.assert_equal(res, True, "ERR: Remote X3 interface is not accessable")

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

    def test_02_config_x2_to_lan(self):
        logger.info("config x2 interface... ")
        x2_lan_dict = {
            'if': 'X2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        rc = r_interfaceapi.config_interface(**x2_lan_dict)
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
