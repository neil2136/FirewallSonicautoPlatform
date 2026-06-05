from definition.settings import *


class Test_init_RemoteFW(Test):
    uuid = 'NonTC'

    async def run_init_fw_script(self):
        logger.info('start Restore Remote FW in asyncio...\n'
                    'Restore Remote FW process will run in the background of the OS.')
        path = os.environ["PYTHON_COMMON_HOME"] + '/config/restore_gw_rmt_tel.py'
        command = f'python3 {path} -os=1 --testbed={Params.testbed} -device=RemoteGEN5 -if=X1 -zone=WAN ' \
                  f'-ip={Parameter.REMOTE_X1_IP} -restore=1'
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


# pc1(eth1)---x0(FW)x1---x1(fw2)x0---(eth1)pc4
class Test_SetupVPN(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_02_check_remote_fw_connection(self):
        res = False
        for count in range(10):
            logger.info(f'time {count}: start verify ping from pc1 eth2 to remote fw x3...')
            pingres = PC1_login.ping_from_eth(ip=Parameter.REMOTE_X3_IP, eth='eth2')
            if pingres:
                res = True
                break
            else:
                time.sleep(30)
        Assertion.assert_equal(res, True, "ERR: ping from pc1 eth2 to remote fw x3 failed")

    def test_03_add_s2s_local_vpn_local(self):
        local_ao_dict = {
            "object_type": "network",
            "name": "remote_vpn_net",
            "zone": "LAN",
            "value": Parameter.REMOTE_X0_NET + ',255.255.255.0'
        }
        vpn_dict = {
            'type': 'site_to_site',
            'name': 'localvpn',
            'pri_gate': Parameter.REMOTE_X1_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '2.2.2.2',

            'local_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'remote_vpn_net',

            'ike_exchange': 'main',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 12000,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 12000,

            'keep_alive': True,
        }
        delallvpnres = l_vpnbasesettingapi.del_all_vpn_policies()
        addaores = l_aoapi.config_addressobject(**local_ao_dict)
        addvpnres = l_vpnapi.add_vpn_policy(**vpn_dict)
        logger.info(f'delallvpnres: {delallvpnres}, addaores: {addaores}, addvpnres: {addvpnres}')
        vpnentry = l_vpnapi.show_s2svpnpolicy()
        Assertion.assert_regular(str(vpnentry), vpn_dict['name'], "ERR: Add local vpn policy failed.")

    def test_04_add_s2s_remote_vpn(self):
        remote_ao_dict = {
            "object_type": "network",
            "name": "local_vpn_net",
            "zone": "LAN",
            "value": f'{Parameter.LOCAL_X0_NET},{Parameter.MASK}'
        }
        vpn_dict = {
            'type': 'site_to_site',
            'name': 'remotevpn',
            'pri_gate': Parameter.X1_IP,
            'auth_mode': 'shared_secret',
            'secret': '123456',
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': '2.2.2.2',
            'peer_ike_id': '2.2.2.2',

            'local_net_type': 'name',
            'local_net_name': 'X0 Subnet',
            'remote_net_type': 'name',
            'remote_net_name': 'local_vpn_net',

            'ike_exchange': 'main',
            'ike_dh_group': '14',
            'ike_encryption': 'aes-256',
            'ike_auth': 'sha-256',
            'ike_lifetime': 12000,
            'ipsec_protocol': 'esp',
            'ipsec_encryption': 'aes_256',
            'ipsec_auth': 'sha_256',
            'ipsec_lifetime': 12000,
            'keep_alive': True,
        }
        delallvpnres = r_vpnbasesettingapi.del_all_vpn_policies()
        addaores = r_aoapi.config_addressobject(**remote_ao_dict)
        addvpnres = r_vpnapi.add_vpn_policy(**vpn_dict)
        logger.info(f'delallvpnres: {delallvpnres}, addaores: {addaores}, addvpnres: {addvpnres}')
        vpnentry = r_vpnapi.show_s2svpnpolicy()
        Assertion.assert_regular(str(vpnentry), vpn_dict['name'], "ERR: Add local vpn policy failed.")

    @repeat_method(5)
    def test_05_check_ping_form_local_to_remote_newtork(self):
        time.sleep(20)
        logger.info("start verify ping from pc1 eth1 to remote host pc4 eth1... ")
        pingres = PC1_login.ping_from_eth(ip=PC4_ETH1_IP, eth='eth1')
        Assertion.assert_equal(pingres, True, "ERR: ping from pc1 eth1 to remote host pc4 eth1 failed")
