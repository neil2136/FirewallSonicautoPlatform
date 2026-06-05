from definition.settings import *


class TestConfigFW(Test):
    uuid = 'NonTC'

    def test_01_Config_X1(self):
        logger.info("config x1 interface... ")
        res = interfacecfgapi.config_interface(**x1_static)
        logger.info('config X1 interface result: {}'.format(res))
        Assertion.assert_equal(res, True, "ERR: Config X1 to static failed")

    def test_02_add_address_object(self):
        reslist = []
        for ao in source_AO_dict.values():
            res = localaoapi.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add source ao {} result: {}'.format(ao, res))
        for ao in dest_AO_dict.values():
            res = localaoapi.config_addressobject(**ao)
            reslist.append(res)
            logger.info('add destination ao {} result: {}'.format(ao, res))
        res = all(value == 1 for value in reslist)
        Assertion.assert_equal(
            res, True, "ERR: Add source and destination AO failed")
