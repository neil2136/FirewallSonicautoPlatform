from definition.settings import *
from bin.utils import Local_one_remote_LAN


@paramunittest.parametrized(
    {'MODE': 'NAT', 'TYPE': 'DMZ', 'SIDE': 0, 'LL': 'DMZ Subnets', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_dmz' , 'both':False,'uuid': '1754186', 'tcid': '1'},
    {'MODE': 'DHCP', 'TYPE': 'DMZ', 'SIDE': 0, 'LL': 'DMZ Subnets', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_dmz' , 'both':False,'uuid': '1754187', 'tcid': '2'},
    {'MODE': 'PPPoE', 'TYPE': 'DMZ', 'SIDE': 0, 'LL': 'DMZ Subnets', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_dmz' , 'both':False,'uuid': '1754188', 'tcid': '3'},
    {'MODE': 'Transparent', 'TYPE': 'DMZ', 'SIDE': 0, 'LL': 'DMZ Subnets', 'LR': 'remote_trans','RL': 'remote_trans', 'RR': 'local_dmz' , 'both':False,'uuid': '1754189', 'tcid': '4'},
    {'MODE': 'NAT', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'X4 Subnet', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_custom' , 'both':False,'uuid': '1754190', 'tcid': '5'},
    {'MODE': 'DHCP', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'X4 Subnet', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_custom' , 'both':False,'uuid': '1754191', 'tcid': '6'},
    {'MODE': 'PPPoE', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'X4 Subnet', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'local_custom' , 'both':False,'uuid': '1754192', 'tcid': '7'},
    {'MODE': 'Transparent', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'X4 Subnet', 'LR': 'remote_trans','RL': 'remote_trans', 'RR': 'local_custom' , 'both':False,'uuid': '1754193', 'tcid': '8'},
    {'MODE': 'NAT', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'local_gp', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'remote_gp' , 'both':True,'uuid': '1754194', 'tcid': '9'},
    {'MODE': 'DHCP', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'local_gp', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'remote_gp' , 'both':True,'uuid': '1754195', 'tcid': '10'},
    {'MODE': 'PPPoE', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'local_gp', 'LR': 'remote_net','RL': 'X0 Subnet', 'RR': 'remote_gp' , 'both':True,'uuid': '1754196', 'tcid': '11'},
    {'MODE': 'Transparent', 'TYPE': 'Custom', 'SIDE': 0, 'LL': 'local_gp', 'LR': 'remote_trans','RL': 'remote_trans', 'RR': 'remote_gp' , 'both':True,'uuid': '1754197', 'tcid': '12'},
    {'MODE': 'NAT', 'TYPE': 'DMZ', 'SIDE': 1, 'LL': 'DMZ Subnets', 'LR': 'remote_dmz','RL': 'DMZ Subnets', 'RR': 'local_dmz' , 'both':False,'uuid': '1754198', 'tcid': '13'},
    {'MODE': 'NAT', 'TYPE': 'Custom', 'SIDE': 1, 'LL': 'DMZ Subnets', 'LR': 'remote_custom','RL': 'X4 Subnet', 'RR': 'local_dmz' , 'both':False,'uuid': '1754199', 'tcid': '14'},
    {'MODE': 'NAT', 'TYPE': 'Custom', 'SIDE': 2, 'LL': 'X4 Subnet', 'LR': 'remote_custom','RL': 'X4 Subnet', 'RR': 'local_custom' , 'both':False,'uuid': '1754201', 'tcid': '16'},
    {'MODE': 'NAT', 'TYPE': 'Custom', 'SIDE': 1, 'LL': 'DMZ Subnets', 'LR': 'local_gp2','RL': 'remote_gp2', 'RR': 'local_dmz' , 'both':True,'uuid': '1754200', 'tcid': '15'},
)
class TestVPN_nonLAN_116_01(Test):

    def setParameters(self, MODE,TYPE,SIDE,LL,LR,RL,RR, both,uuid, tcid):
        self.mode = MODE
        self.type = TYPE
        self.side = SIDE
        self.LL = LL
        self.LR = LR
        self.RL = RL
        self.RR = RR
        self.both = both
        self.uuid = uuid
        self.tcid = tcid
        self.case = Local_one_remote_LAN(self.mode, self.type, self.side, self.LL, self.LR, self.RL, self.RR)
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_Config_remote_DUT_ENV(self):
        logger.info(" {} ".center(20, '-').format('Config remote DUT with {} mode'.format(self.mode)))
        rc = self.case.Setup_env()
        Assertion.assert_equal(rc, True, f"ERR: Config remote DUT with {self.mode} mode failed")

    def test_01_02_Add_VPN_Policy(self):
        logger.info(" {} ".center(20, '-').format('Add VPN Policy for DUT and Remote'))
        rc = self.case.Add_VPN_Policy()
        Assertion.assert_equal(rc, True, "ERR: Add VPN Policy for DUT and Remote failed")

    def test_01_03_Verify_Service_Ping(self):
        logger.info(" {} ".center(20, '-').format('Verify service ping'))
        rc = self.case.Verify(service='ping',action=2,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='ping',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service ping failed")

    @repeat_method(4)
    def test_01_04_Verify_Service_FTP(self):
        logger.info(" {} ".center(20, '-').format('Verify service FTP'))
        rc = self.case.Verify(service='FTP',action=2,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='FTP',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service FTP failed")
    
    @repeat_method(4)
    def test_01_05_Verify_Service_HTTP(self):
        logger.info(" {} ".center(20, '-').format('Verify service HTTP'))
        rc = self.case.Verify(service='HTTP',action=2,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='HTTP',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service HTTP failed")

    @repeat_method(4)
    def test_01_05_Renegotiate_on_local(self):
        logger.info(" {} ".center(20, '-').format('Renegotiate on local DUT'))
        rc = self.case.Renegotiate_on_local()
        if not rc:
            rc2 = self.case.Verify(service='ping',action=2,type=self.type)
            logger.info(f' ping active: {rc2}')
        Assertion.assert_equal(rc, True, "ERR: Renegotiate on local DUT failed")

    def test_01_06_Verify_Service_Ping_for_Renegotiate(self):
        logger.info(" {} ".center(20, '-').format('Verify service ping for Renegotiate '))
        rc = self.case.Verify(service='ping',action=2,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='ping',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service ping for Renegotiate  failed")

    def test_01_07_Disable_VPN_Policy_on_Local(self):
        logger.info(" {} ".center(20, '-').format('Disable VPN Policy on Local'))
        rc = self.case.Disable_VPN_Policy()
        Assertion.assert_equal(rc, True, "ERR: Disable VPN Policy on Local failed")

    def test_01_08_Verify_Ping_for_VPN_Disable(self):
        logger.info(" {} ".center(20, '-').format('Verify service ping for VPN Policy Disabled '))
        rc = self.case.Verify(service='ping',action=0,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='ping',action=0,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service ping for VPN Policy Disabled  failed")

    def test_01_09_reenable_VPN_Policy_on_Local(self):
        logger.info(" {} ".center(20, '-').format('re-enable VPN Policy on Local'))
        rc = self.case.Enable_VPN_Policy()
        Assertion.assert_equal(rc, True, "ERR: re-enable VPN Policy on Local failed")

    def test_01_10_Verify_Ping_for_VPN_Reenable(self):
        logger.info(" {} ".center(20, '-').format('Verify service ping for VPN Policy Reenable '))
        rc = self.case.Verify(service='ping',action=2,type=self.type)
        if self.both:
            rc &= self.case.Verify(service='ping',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service ping for VPN Policy Reenable  failed")

    def test_01_11_Test_Log_for_SA_expires(self):
        logger.info(" {} ".center(20, '-').format('Test log to verify VPN policy expires after lifetime runs out.'))
        rc = self.case.Test_Log_for_SA_expires()
        Assertion.assert_equal(rc, True, "ERR: Test log to verify VPN policy expires after lifetime runs out failed")

    def test_01_12_Verify_Ping_for_SA_expires(self):
        logger.info(" {} ".center(20, '-').format('Verify service ping for SA expires '))
        rc = self.case.Verify(service='ping',action=2, type=self.type)
        if self.both:
            rc &= self.case.Verify(service='ping',action=2,type='DMZ')
        Assertion.assert_equal(rc, True, "ERR: Verify service ping for SA expires  failed")

    def test_01_13_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        rc = self.case.Remove_VPN_Policy()
        rc &= self.case.Restore_env()
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")

