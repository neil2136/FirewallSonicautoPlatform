from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_config_x4_to_wan(self):
        x4_static_dict = {
            'if': 'X4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '66.66.66.168',
            'netmask': '255.255.255.0',
            'gateway': '66.66.66.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }

        res = interfacecfgapi.config_interface(**x4_static_dict)
        logger.info('config X4 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X4 to static wan failed")

    def test_02_configure_dut_failover(self):
        wlb_conf_dict = {
            "failover_lb": {
                "group": [
                    {
                        "final_backup": "",
                        "interface": [
                            {
                                "name": "X4",
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

    def test_04_config_x4_to_unasign(self):
        rc = interfacecfgapi.unassign_interface(interface='X4')
        Assertion.assert_equal(rc, True, "ERR: Config X4 to unassign failed")



class sslvpn_config(Test):
    uuid = 'NonTC'
    description = "configure sslvpn"
    goto_teardown = False

    def test_01_install_nx_Linux(self):
        cpy_build1 = nx_install.cpbuildnx_linux_local()
        logger.info(cpy_build1)
        inst1 = nx_install.install_nx_linux()
        logger.info(inst1)
        cpy_build2 = nx_install.buildnx_linux_remote('-PC3')
        logger.info(cpy_build2)
        inst2 = nx_install.install_nx_linux_remote('-PC3')
        logger.info(inst2)
        Assertion.assert_equal(inst1, 2, "ERR: Install NX failed")

    def test_02_Add_AO_X0_Subnet(self):
        sslvpn_ao = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.50,192.168.168.60",
        }
        rc = ao_api.config_addressobject(**sslvpn_ao)
        Assertion.assert_equal(rc, True, "ERR: Add SSLVPN address object failed.")

    def test_03_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': True,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        rc = sslvpn_server_api.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(rc, True, "Err: failed to config server settings")

    def test_04_enable_server_access(self):
        server_enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        rc = sslvpn_server_api.edit_server_access_setting(**server_enable)
        Assertion.assert_equal(rc, True, "Err: failed to config sslvpn server access")

    def test_05_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        rc = sslvpn_client_api.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(rc, True, "Err: Configure sslvpn Client settings fail")

    def test_06_add_sslvpn_user(self):
        sslvpn_user_dict = {
            'action': 'add',
            'username': 'sslvpntest',
            'userpassword': 'password',
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['SSLVPN Services', "SonicWALL Administrators"]
        }
        rc = user_api.local_user(**sslvpn_user_dict)
        Assertion.assert_equal(rc, True, "Err: Add a local user member of SSLVPN fail")
        
        
class Add_VPN_Policy(Test):
    uuid = "NonTC"
    # goto_teardown = False
    description= 'Config VPN policy'
    LObj1 = {
        'name': 'remote_net',
        'zone': 'VPN',
        'object_type': 'network',
        'value': '{},255.255.255.0'.format(Parameter.REMOTENET),
    }
    RObj1 = {
        'name': 'local_net',
        'zone': 'VPN',
        'object_type': 'network',
        'value': '{},255.255.255.0'.format(Parameter.LOCALNET),
    }


    def test_01_config_network(self):
        logger.info(" {} ".center(20, '-').format('Config network'))
        PC3_login = Host(PC3_IP, user='root', password='password')
        if Params.openstack == "1":
            cmd_list = ["cp {}/vpntestbed.com.db /var/named/chroot/var/named/".format(VPN_bin),
                        "cp {}/named.conf /var/named/chroot/etc/".format(VPN_bin),
                        "service named restart"]
            ret = ''
            rc = False
            for cmd in cmd_list:
                logger.info(cmd)
                ret = PC3_login.send_command(cmd)
                logger.info(ret)
                time.sleep(1)
            if 'Starting named: [  OK  ]' in ret:
                logger.info('config DNS PASS')
                rc = True
            else:
                logger.info('config DNS FAIL')

            cmd = " service smb restart;service nmb restart "
            ret  = PC2_login.send_command(cmd)
            logger.info(ret)
            if 'Starting SMB services: [  OK  ]' in ret and 'Starting NMB services: [  OK  ]' in ret:
                logger.info('service smb and service nmb restart successfully.')
            else:
                rc = False
            Assertion.assert_equal(rc, True, 'config Network FAIL')
        else:
            logger.info(Params.openstack)
            logger.info('Maybe something is wrong...')

    def test_02_add_address_object(self):
        logger.info(" {} ".center(20, '-').format('Prepare Environment 1'))
        rc = 0
        rc1 = ao_api.config_addressobject(msg=True, **self.LObj1)
        if rc1[0]:
            rc += 1
            logger.info('Add {} address objects success.'.format(self.LObj1['name']))
        elif 'Already exists' in rc1[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Local Address Object already exists')
        else:
            logger.info('Add {} Failed'.format(self.LObj1['name']))
        rc2 = RAddr_api.config_addressobject(msg=True, **self.RObj1)
        if rc2[0]:
            rc += 1
            logger.info('Add {} address objects success.'.format(self.RObj1['name']))
        elif 'Already exists' in rc2[1]['status']['info'][0]['message']:
            rc += 1
            logger.info('Remote Address Object already exists')
        else:
            logger.info('Add {} Failed'.format(self.RObj1['name']))

        Assertion.assert_equal(rc,2,'Add address objects Failed.')

    def test_03_add_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Add VPN Policy'))
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        Lvpn = {
            'type': 'site_to_site',
            'name': 'vpn1',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.REMOTEX1,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': Parameter.DUT,
            'peer_ike_id': Parameter.REMOTEX0,
            'local_net_type': 'name',
            'remote_net_type': 'name',
            'local_net_name': Parameter.LOCALSUBNET,
            'remote_net_name': self.LObj1['name'],
            'ike_exchange': 'main',
            'ike_encryption': 'aes-128',
            'ipsec_encryption': 'aes_128',
            'ike_lifetime': '120',
            'ipsec_lifetime': '120',
            'bound_to': ['zone', 'WAN'],
            'management_ssh': True,
            'keep_alive': True,
        }
        rc1 = Lvpn_api.add_vpn_policy(**Lvpn)
        if rc1:
            logger.info('Add Local VPN pass')
        else:
            logger.info('Add Local VPN failed')

        logger.info(" {} ".center(20, '*').format('Add Remote VPN Policy'))
        Rvpn = {
            'type': 'site_to_site',
            'name': 'vpn2',
            'enable': True,
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'pri_gate': Parameter.WANIP,
            'local_ike_type': 'ipv4',
            'peer_ike_type': 'ipv4',
            'local_ike_id': Parameter.REMOTEX0,
            'peer_ike_id': Parameter.DUT,
            'local_net_type': 'name',
            'remote_net_type': 'name',
            'local_net_name': Parameter.REMOTESUBNET,
            'remote_net_name': self.RObj1['name'],
            'ike_exchange': 'main',
            'ike_encryption': 'aes-128',
            'ipsec_encryption': 'aes_128',
            'ike_lifetime': '120',
            'ipsec_lifetime': '120',
            'bound_to': ['zone', 'WAN'],
            'keep_alive': True,
        }
        rc2 = Rvpn_api.add_vpn_policy(**Rvpn)
        if rc2:
            logger.info('Add Remote VPN pass')
        else:
            logger.info('Add Remote VPN failed')
        rc = rc1 and rc2
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')