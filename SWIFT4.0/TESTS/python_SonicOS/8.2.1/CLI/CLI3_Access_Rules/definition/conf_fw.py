from settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        x1_static = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.X1_IP,
            'netmask': Parameter.MASK,
            'gateway': Parameter.X1_GW,
            'dns1': Parameter.X1_DNS1,
            'dns2': Parameter.X1_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        res = interfacecfg.config_interface(**x1_static)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_add_address_object(self):
        reslist = []
        for ao in source_ao_dict.values():
            res = localao.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add source ao {} result: {}'.format(ao, res))
        for ao in dest_ao_dict.values():
            res = localao.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add destination ao {} result: {}'.format(ao, res))
        res = all(value == 1 for value in reslist)
        Assertion.assert_equal(
            res, True, "ERR: Add source and destination AO failed")

    # @repeat_method(5)
    # def test_03_Register_fw(self):
    #     time.sleep(10)
    #     rc = lc.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")
