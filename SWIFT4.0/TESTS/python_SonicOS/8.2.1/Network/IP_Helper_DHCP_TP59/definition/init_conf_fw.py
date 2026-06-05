from definition.settings import *
from definition.utils import *

class TestConfigFW(Test):
    uuid = 'NonTC'
    goto_teardown = True
    server_ao_name = "192.168.3.30"

    def test_01_config_static_ip_for_x1(self):
        logger.info("config x1 interface... ")
        rc = interfaceapi.config_interface(**x1_wan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_02_config_dmz_static_for_x2(self):
        logger.info("config x2 interface... ")
        rc = interfaceapi.config_interface(**x2_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_03_config_lan_static_for_x2(self):
        logger.info("config x3 interface... ")
        rc = interfaceapi.config_interface(**x3_lan_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X3 to static failed")

# Below are the same test steps for all the 3 cases:
    def test_04_disable_dhcpv4_server(self):
        logger.info("Disable the DHCPv4 server of the firewall... ")
        dhcp_server_opt = {
            "dhcp_server": {
                "ipv4": {
                    "enable": False
                    , "conflict_detection": True
                    , "persistence": True
                    , "persistence_monitoring_interval": 5
                    , "trusted_relay_agents": ""
                    , "recycle_expired_lease": 0
                }
            }
        }
        rc = dhcp_obj.config_dhcp_server_settings(**dhcp_server_opt)
        Assertion.assert_equal(rc, True, "ERR: Disable dhcpv4 server on firewall failed!")

    def test_05_enable_ip_helper(self):
        logger.info("Enable the Global IP Helper button... ")
        rc = iphelper_obj.enable_iphelper()
        Assertion.assert_equal(rc, True, "ERR: Enable ip helper failed!")

    def test_06_enable_dhcp_support_of_ip_helper(self):
        logger.info("Enable the DHCP option of IP Helper... ")
        dhcp_protocol_opt = {
            'protocol': 'DHCP',
            'enable': True
        }
        rc = iphelper_obj.edit_iphelper_protocol(**dhcp_protocol_opt)
        Assertion.assert_equal(rc, True, "ERR: Enable the DHCP option of IP Helper failed!")

    def test_07_configure_interface_x2_to_dmz_static(self):
        logger.info("Make sure the X2 is DMZ zone... ")
        rc = interfaceapi.config_interface(**x2_dmz_dict)
        Assertion.assert_equal(rc, True, "ERR: Configure X2 to DMZ failed")

    def test_08_create_address_object_for_dhcp_server(self):
        logger.info("Add an AO for DHCP server which we will set in the IP Helper Policy... ")
        ao_dict = {
            "object_type": "host",
            "name": self.server_ao_name,
            "zone": "LAN",
            "value": self.server_ao_name
        }
        (res, aomsg) = address_obj.config_addressobject(msg=True, **ao_dict)
        if res is False:
            res = True if 'Already exists' in str(aomsg) else False
        Assertion.assert_equal(res, True, "ERR: Add an AO for DHCP server which we will set in the IP Helper Policy failed")
