from definition.settings import *


class Test_init_RemoteFW(Test):
    uuid = 'NonTC'
    goto_teardown = True

    async def run_init_fw_script(self):
        logger.info('start Restore Remote FW in asyncio...\n'
                    'Restore Remote FW process will run in the background of the OS.')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN7 -if=X1 -zone=WAN ' \
                  f'-ip={Parameter.REMOTE_X1_IP} -restore=1'
        logger.info(command)
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


# pc1(eth1)---x0(FW)x1---x1(fw2)x0---(eth1)pc2
class Test_SetupVPN(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(30, 20)
    def test_00_check_remote_x3_accessable(self):
        logger.info("check remote x3 accessable... ")
        output = PC1_login.send_command('ping -c 30 ' + Parameter.REMOTE_X3_IP)
        res = '30 received' in output
        Assertion.assert_equal(res, True, "ERR: Remote X3 interface is not accessable")

    def test_02_add_fw_aos(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "LAN",
            "value": Parameter.REMOTE_X0_NET + ',255.255.255.0'
        }
        remote_ao_dict = {
            "object_type": "network",
            "name": "local_vpn_net",
            "zone": "LAN",
            "value": f'{Parameter.X0_SUBNET},{Parameter.MASK}'
        }
        localres, msg1 = l_aoapi.config_addressobject(msg=True, **local_ao_dict)
        if 'Already exists' in str(msg1):
            localres = True
        remoteres, msg2 = r_aoapi.config_addressobject(msg=True, **remote_ao_dict)
        if 'Already exists' in str(msg2):
            remoteres = True
        Assertion.assert_equal(localres & remoteres, True, "ERR: Add local ti vpn policy failed.")

    def test_03_add_ti_local_vpn_local(self):
        delallvpnres = l_vpnbasesettingapi.del_all_vpn_policies()
        addvpnres = l_vpnapi.add_vpn_policy(**ti_vpn_dict)
        logger.info(f'delallvpnres: {delallvpnres}, addvpnres: {addvpnres}')
        Assertion.assert_equal(addvpnres, True, "ERR: Add local ti vpn policy failed.")

    def test_04_add_ti_remote_vpn(self):
        vpn_dict = copy.deepcopy(ti_vpn_dict)
        vpn_dict.update({
            'name': VPNParams.remote_vpn1_name,
            'pri_gate': Parameter.X1_IP,
        })
        delallvpnres = r_vpnbasesettingapi.del_all_vpn_policies()
        addvpnres = r_vpnapi.add_vpn_policy(**vpn_dict)
        logger.info(f'delallvpnres: {delallvpnres}, addvpnres: {addvpnres}')
        Assertion.assert_equal(addvpnres, True, "ERR: Add local ti vpn policy failed.")

    def test_05_add_local_ti_route_policy(self):
        local_route_dict = {"route_policies": [{"ipv4": l_route_base_dict}]}
        output, msg = l_routepolicyapi.add_route_policy(msg=True, **local_route_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: Add local ti to route policy failed")

    def test_06_add_remote_ti_route_policy(self):
        remote_route_dict = {"route_policies": [{"ipv4": r_route_base_dict}]}
        output, msg = r_routepolicyapi.add_route_policy(msg=True, **remote_route_dict)
        if 'Already exists' in str(msg):
            output = True
        Assertion.assert_equal(output, True, "ERR: Add local ti to route policy failed")

    @repeat_method(5)
    def test_07_check_ping_form_local_to_remote_network(self):
        logger.info("start verify ping from pc1 eth1 to remote host pc4 eth1... ")
        time.sleep(20)
        pingres = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: ping from pc1 eth1 to remote host pc4 eth1 failed")

