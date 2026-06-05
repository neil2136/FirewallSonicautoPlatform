from definition.settings import *


@paramunittest.parametrized(
    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': None, \
         'uuid': '1714229', 'tcid': '1714229'},
    {'remote_net_type': 'pool', 'remote_net_name': rm_range, 'edit_para': None, \
         'uuid': '1714229', 'tcid': '1714229'},

    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'name', \
         'uuid': '1714240', 'tcid': '1714240'},
    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'any', \
         'uuid': '1714240', 'tcid': '1714240'},

    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'main', \
         'uuid': '1714251', 'tcid': '1714251'},
    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'aggressive', \
         'uuid': '1714251', 'tcid': '1714251'},

    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'main', \
         'uuid': '1714252', 'tcid': '1714252'},
    {'remote_net_type': 'pool', 'remote_net_name': rm_net, 'edit_para': 'aggressive', \
         'uuid': '1714252', 'tcid': '1714252'},
 )
class TestMOBIKE_TP2581_TC3_4_5_6(Test):
    def setParameters(self, remote_net_type, remote_net_name, edit_para, uuid, tcid):
        self.remote_net_type = remote_net_type
        self.remote_net_name = remote_net_name
        self.edit_para = edit_para
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

    def test_03_add_vpn_policy(self):
        ref1 = copy.deepcopy(Lvpn)
        ref1['remote_net_type'] = self.remote_net_type
        ref1['remote_net_name'] = self.remote_net_name['name']
        logger.info(" {} ".center(20, '*').format('Add Local VPN Policy'))
        rc = Lvpn_obj.add_vpn_policy(**ref1)
        Assertion.assert_equal(rc, True, 'Add VPN Policy Failed.')

    def test_04_edit_vpn_policy_for_remote_net_type(self):
        if self.tcid == '1714240':
            logger.info(" {} ".center(20, '*').format('edit vpn policy for remote net type'))
            edit_ref = {
                'type': 'site_to_site',
                'name': 'vpn',
                'edit_network': True,
                'remote_net_type': self.edit_para,
                'remote_net_name': 'remote_net',
            }
            if self.edit_para == 'any':
                del edit_ref['remote_net_name']
            rc = Lvpn_obj.edit_vpn_policy(**edit_ref)
            Assertion.assert_equal(rc, True, 'edit VPN Policy for remote net type Failed.')
        else:
            logger.info("testcase {} skip this step".format(self.tcid))
            Assertion.assert_equal(True, True, 'edit VPN Policy for remote net type Failed.')

    def test_05_edit_vpn_policy_for_exchange_mode(self):
        if self.tcid == '1714251':
            logger.info(" {} ".center(20, '*').format('edit vpn policy for exchange mode'))
            edit_ref = {
                'type': 'site_to_site',
                'name': 'vpn',
                'auth_mode': 'shared_secret',
                'edit_proposal': True,
                'ike_exchange': self.edit_para,
            }
            resp = Lvpn_obj.edit_vpn_policy(**edit_ref, msg=True)
            Assertion.assert_regular(str(resp), 'Remote Network not selected', 'edit VPN Policy for exchange mode Failed.')
        else:
            logger.info("testcase {} skip this step".format(self.tcid))
            Assertion.assert_equal(True, True, 'edit VPN Policy for exchange mode Failed.')

    def test_06_edit_vpn_policy_for_rm_net_and_exchange_mode(self):
        if self.tcid == '1714252':
            logger.info(" {} ".center(20, '*').format('edit vpn policy for rm net and exchange mode'))
            edit_ref = {
                'type': 'site_to_site',
                'name': 'vpn',
                'auth_mode': 'shared_secret',
                'edit_network': True,
                'remote_net_type': 'name',
                'remote_net_name': 'remote_net',
                'edit_proposal': True,
                'ike_exchange': self.edit_para,
            }
            rc = Lvpn_obj.edit_vpn_policy(**edit_ref)
            Assertion.assert_equal(rc, True, 'edit VPN Policy for rm net and exchange mode Failed.')
        else:
            logger.info("testcase {} skip this step".format(self.tcid))
            Assertion.assert_equal(True, True, 'edit VPN Policy Failed.')

    def test_06_remove_vpn_policy(self):
        logger.info(" {} ".center(20, '-').format('Delete S2S VPN'))
        rc = Lvpn_obj.del_s2svpn_policy(**Lvpn)
        Assertion.assert_equal(rc, True, 'Remove VPN Policy Failed.')

    def test_07_delete_addObj(self):
        logger.info('-'*10+'delete ao'+'-'*10)
        rc = LAddrOBJ.del_ao_by_name(name=self.remote_net_name['name'], version='ipv4')
        Assertion.assert_equal(rc, True, 'delete AO Failed.')
