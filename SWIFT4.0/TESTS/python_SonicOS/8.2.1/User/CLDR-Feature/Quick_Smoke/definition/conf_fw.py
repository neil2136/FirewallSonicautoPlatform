from definition.settings import *


class TestConfigTB(Test):
	uuid = 'NonTC'

	def test_00_Config_X1(self):
		x1_static = {
			'if': 'X1',
			'zone': 'WAN',
			'mode': 'static',
			'ip': Parameter.X1_IP,
			'netmask': '255.255.255.0',
			'gateway': Parameter.X1_GW,
			'dns1': Params.G_DNS1,
			'dns2': Params.G_DNS2,
			'dns3': Params.G_DNS3,
			'mgmt_https': True,
			'user_https': True
		}
		rc = interface.config_interface(**x1_static)
		Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

	def test_01_Config_X2(self):
		x2_static = {
			'if': 'X2',
			'zone': 'DMZ',
			'mode': 'static',
			'ip': '23.0.0.100',
			'netmask': '255.255.255.0',
			'mgmt_https': True,
			'user_https': True,
		}
		rc = interface.config_interface(**x2_static)
		Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

	def test_02_Config_X0(self):
		x0_interface = {
			'if': 'X0',
			'zone': 'LAN',
			'ip': '192.168.168.168',
			'mgmt_ping': True,
			'mgmt_https': True,
			'mgmt_ssh': True
		}
		rc = interface.config_interface(**x0_interface)
		Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")
