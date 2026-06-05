from definition.settings import *


@paramunittest.parametrized(
    {'ike_exchange': 'ikev2', 'remote_net_type': 'pool', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'ikev2', 'remote_net_type_2': 'pool', 'remote_net_name_2': rm_net, \
     'uuid': '1714253', 'tcid': '1714253'},
    {'ike_exchange': 'main', 'remote_net_type': 'name', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'ikev2', 'remote_net_type_2': 'pool', 'remote_net_name_2': rm_net, \
     'uuid': '1714254', 'tcid': '1714254'},
    {'ike_exchange': 'aggressive', 'remote_net_type': 'name', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'ikev2', 'remote_net_type_2': 'pool', 'remote_net_name_2': rm_net, \
     'uuid': '1714254', 'tcid': '1714254'},

    {'ike_exchange': 'ikev2', 'remote_net_type': 'pool', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'main', 'remote_net_type_2': 'name', 'remote_net_name_2': rm_net, \
     'uuid': '1714208', 'tcid': '1714208'},
    {'ike_exchange': 'ikev2', 'remote_net_type': 'pool', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'aggressive', 'remote_net_type_2': 'name', 'remote_net_name_2': rm_net, \
     'uuid': '1714208', 'tcid': '1714208'},
    {'ike_exchange': 'ikev2', 'remote_net_type': 'pool', 'remote_net_name': rm_net, \
     'ike_exchange_2': 'ikev2', 'remote_net_type_2': 'name', 'remote_net_name_2': rm_net, \
     'uuid': '1714208', 'tcid': '1714208'},

)
class TestMOBIKE_TP2581_TC7_8_10(Test):
    def setParameters(self, ike_exchange, remote_net_type, remote_net_name, \
                      ike_exchange_2, remote_net_type_2, remote_net_name_2, \
                      uuid, tcid):
        self.ike_exchange = ike_exchange
        self.remote_net_type = remote_net_type
        self.remote_net_name = remote_net_name
        self.ike_exchange_2 = ike_exchange_2
        self.remote_net_type_2 = remote_net_type_2
        self.remote_net_name_2 = remote_net_name_2
        self.uuid = uuid
        self.tcid = tcid
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_add_addObj(self):
        logger.info('-'*10+'Add AO for DUT'+'-'*10)
        rc = LAddrOBJ.config_addressobject(**self.remote_net_name)
        Assertion.assert_equal(rc, True, 'Add AO for DUT Failed.')

    def test_03_add_first_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['ike_exchange'] = self.ike_exchange
        ref1['remote_net_type'] = self.remote_net_type
        ref1['remote_net_name'] = self.remote_net_name['name']
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add first VPN Policy Failed.')

    def test_04_add_second_vpn_policy(self):
        ref_2 = copy.deepcopy(Lvpn_2)
        ref_2['ike_exchange'] = self.ike_exchange_2
        ref_2['remote_net_type'] = self.remote_net_type_2
        ref_2['remote_net_name'] = self.remote_net_name_2['name']
        logger.info(" {} ".center(20, '*').format('Add secondry VPN Policy'))
        resp = Lvpn_obj.add_vpn_policy(**ref_2, msg=True)
        match = 'IKEv2 IP pool is overlap with'
        if self.tcid == '1714208':
            match = 'Address object remote_net has overlapping networks'
        Assertion.assert_regular(str(resp), match, 'Add sec VPN Policy Failed.')

    def test_05_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_06_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(name=self.remote_net_name['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')
