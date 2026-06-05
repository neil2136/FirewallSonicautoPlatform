from definition.settings import *


class Test_init_LocalFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_Config_X2(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_Config_X3(self):
        logger.info("config x3 interface... ")
        rc = interfaceapi.config_interface(**x3_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

    def test_04_add_aos(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "LAN",
            "value": Parameter.R_X0_NET + ',255.255.255.0'
        }
        output1, msg1 = aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            output1 = True

        remote_ao_dict = {
            "object_type": "network",
            "name": "local_vpn_net",
            "zone": "LAN",
            "value": f'{Parameter.X0_SUBNET},{Parameter.MASK}'
        }
        output2, msg2 = r_aoapi.config_addressobject(msg=True, **remote_ao_dict)
        if 'Already exists' in str(msg2):
            output2 = True
        logger.info(f'add aos result: {output1}, {output2}')
        Assertion.assert_equal(output1 & output2, True, "ERR: add aos failed")


class Test_init_RemoteFW(Test):
    uuid = 'NonTC'

    async def run_init_fw_script(self):
        logger.info('start Restore Remote FW in asyncio...\n'
                    'Restore Remote FW process will run in the background of the OS.')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X1 -zone=WAN ' \
                  f'-ip={Parameter.R_X1_IP} -restore=1'
        # await asyncio.create_subprocess_shell('sleep 20')
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





