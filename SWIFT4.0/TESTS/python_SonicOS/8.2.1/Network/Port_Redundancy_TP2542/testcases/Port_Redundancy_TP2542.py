from definition.settings import *
import re
class Test_Port_Redundancy_01_TC01(Test):
    uuid = "SOSAIOT-TC-57052"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_config_and_check_redundant_port(self):
        logger.info(" {} ".center(20, '-').format('Configuration of Redundant Port and check Redundant interface is not editable.'))
        ref1 = copy.deepcopy(redundant_port)
        ref2 = copy.deepcopy(Lx0)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        res = Linterface.config_interface(msg=True,**Lx4)
        logger.info(res)
        
        pattern = r'["\']?X4["\']?\s+(is\s+)?not\s+a\s+reasonable\s+value\.?'
        # if not res[0] and '"X4" is not a reasonable value' in str(res[1]):
        if not res[0] and re.search(pattern, str(res[1])) :
            rc &= True
        else:
            rc &= False
            logger.info(f'check Redundant interface failed and the res is:{res} ')
        Assertion.assert_equal(rc, True, f"ERR: Configuration of Redundant Port and check Redundant interface is not editable failed")


class Test_Port_Redundancy_02_TC02(Test):
    uuid = "SOSAIOT-TC-57063"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_02_01_remove_and_check_redundant_port(self):
        logger.info(" {} ".center(20, '-').format('Removing Redundant Port and check Redundant interface is  editable.'))
        ref1 = copy.deepcopy(Lx0)
        ref2 = copy.deepcopy(remove_redundancy)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        rc &= Linterface.config_interface(**Lx4)
        Assertion.assert_equal(rc, True, f"ERR: Removing Redundant Port and check Redundant interface is  editable failed")

    def test_02_02_restore(self):
        logger.info(" {} ".center(20, '-').format('restore Local X4 unassign'))
        rc = Linterface.unassign_interface(interface="X4")
        Assertion.assert_equal(rc, True, f"ERR: restore Local X4 unassign failed")


class Test_Port_Redundancy_04_TC11(Test):
    uuid = "SOSAIOT-TC-57054"
    description = show_testcase_info(TESTPLAN, '11', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_04_01_config_X2(self):
        logger.info(" {} ".center(20, '-').format('Configuration X2 Redundant Port and disable X2.'))
        ref1 = copy.deepcopy(redundant_port)
        ref2 = copy.deepcopy(Lx2)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: Configuration X2 Redundant Port and disable X2 failed")

    def test_04_02_check_Redundant_interface_with_FTP(self):
        logger.info(" {} ".center(20, '-').format('check FTP traffic from LAN to WAN'))
        rc = my_ftp.login()
        rc &= my_ftp.download_file(local_file = local_file,remote_file=rmt_file)
        Assertion.assert_equal(rc, True, f"ERR: check FTP traffic from LAN to WAN failed")

    def test_04_03_restore(self):
        logger.info(" {} ".center(20, '-').format('restore x2 remove Redundant port'))
        ref1 = copy.deepcopy(Lx2)
        ref2 = copy.deepcopy(remove_redundancy)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        rc &= Linterface.unassign_interface(interface="X4")
        Assertion.assert_equal(rc, True, f"ERR: restore x2 remove Redundant port failed")


class Test_Port_Redundancy_05_TC12(Test):
    uuid = "SOSAIOT-TC-57055"
    description = show_testcase_info(TESTPLAN, '12', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_05_01_config_Redundant_Port_X3(self):
        logger.info(" {} ".center(20, '-').format('redundant port configured WAN for X3.'))
        ref1 = copy.deepcopy(redundant_port)
        ref2 = copy.deepcopy(Lx3)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: redundant port configured WAN for X3 failed")

    def test_05_02_check_Redundant_interface_with_FTP(self):
        logger.info(" {} ".center(20, '-').format('check FTP traffic from LAN to WAN'))
        rc = my_ftp.login()
        rc &= my_ftp.download_file(local_file = local_file,remote_file=rmt_file)
        Assertion.assert_equal(rc, True, f"ERR: check FTP traffic from LAN to WAN failed")

    def test_05_03_restore(self):
        logger.info(" {} ".center(20, '-').format('restore x3 remove Redundant port'))
        ref1 = copy.deepcopy(Lx3)
        ref2 = copy.deepcopy(remove_redundancy)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        rc &= Linterface.unassign_interface(interface="X4")
        Assertion.assert_equal(rc, True, f"ERR: restore x3 remove Redundant port failed")


class Test_Port_Redundancy_06_TC42(Test):
    uuid = "SOSAIOT-TC-57088"
    description = show_testcase_info(TESTPLAN, '42', description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '42')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_06_01_config_interface_link_speed(self):
        logger.info(" {} ".center(20, '-').format('config interface x2 and x4 same link speed,check x2 can be configured for port redundancy .'))
        ref1 = copy.deepcopy(redundant_port)
        ref2 = copy.deepcopy(Lx2)
        ref3 = copy.deepcopy(link_speed1)
        ref2.update(ref1)
        ref2.update(ref3)
        rc = Linterface.unassign_interface(interface="X4",**link_speed2)
        rc = Linterface.config_interface(**ref2)
        Assertion.assert_equal(rc, True, f"ERR: config interface x2 and x4 same link speed,check x2 can be configured for port redundancy  failed")

    def test_06_02_restore(self):
        logger.info(" {} ".center(20, '-').format('restore x2 remove Redundant port'))
        ref1 = copy.deepcopy(Lx2)
        ref2 = copy.deepcopy(remove_redundancy)
        ref2.update(ref1)
        rc = Linterface.config_interface(**ref2)
        rc &= Linterface.unassign_interface(interface="X4")
        Assertion.assert_equal(rc, True, f"ERR: restore x2 remove Redundant port failed")


