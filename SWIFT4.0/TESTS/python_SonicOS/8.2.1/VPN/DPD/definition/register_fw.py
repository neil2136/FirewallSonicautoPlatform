from definition.settings import *


class TestRegisterFW(Test):
    uuid = 'NonTC'
    description = "initial config x1 and register fw"
    goto_teardown = True

def test_00_config_x1_interface(self):
        logger.info("config x1 interface... ")
        # x1 ip should be in a same network with PC3_eth0
        ipstrlist = Parameter.WANIP.strip().split('.')
        gateway = '.'.join(ipstrlist[0:3]) + '.1'
        logger.info(gateway)
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.WANIP,
            'mask': '255.255.255.0',
            'gateway': gateway,
            'dns1': Params.G_DNS1,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'fragment_packets': True,
        }
        rc = LintfaceObj.config_interface(**x1_static)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 and register fw failed")
