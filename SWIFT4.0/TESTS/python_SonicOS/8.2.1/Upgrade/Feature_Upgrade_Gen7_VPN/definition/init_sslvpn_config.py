from definition.settings import *


class TestSetup_sslvpn(Test):
    uuid = 'NonTC'
    sslvpn_ao_name = 'sslvpn2.100-105'

    def test_01_install_nx_Linux_remote(self):
        cpy_build = cp_nx.buildnx_linux_remote('-PC4')
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux_remote('-PC4')
        logger.info(inst)

    def test_02_create_sslvpn_address_object(self):
        address_object = {
            "object_type": "range",
            "name": self.sslvpn_ao_name,
            "zone": "SSLVPN",
            "value": "192.168.1.100,192.168.1.105"
        }
        output = aoapi.config_addressobject(**address_object)
        Assertion.assert_equal(output, True, "ERR: add sslvpn ao failed")

    def test_03_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        output = sslvpnserverapi.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(output, True, "Err: failed to config server settings")

    def test_04_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        output = sslvpnserverapi.edit_server_access_setting(**enable)
        Assertion.assert_equal(output, True, "Err: failed to config server access")

    def test_05_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': self.sslvpn_ao_name,
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        output = sslvpnclientapi.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(output, True, "Err: Client settings page is not configured successfully")

    def test_06_add_sslvpn_user(self):
        user_dict = {
            'action': 'add',
            'username': CaseParams.sslvpn_user_name,
            'userpassword': Params.G_NEW_PASSWORD,
            'vpn_client_access': ['LAN Subnets'],
            'member_of': ['Everyone', 'SSLVPN Services'],
        }
        output = userLocalapi.local_user(**user_dict)
        Assertion.assert_equal(output, True, "ERR: add a sslvpn user failed")

    def test_07_config_local_method_to_local(self):
        user_auth = {"auth_method": "local"}
        output = usersettingapi.user_method_authentication(**user_auth)
        Assertion.assert_equal(output, True, "ERR:locals method is not selected successfully")
