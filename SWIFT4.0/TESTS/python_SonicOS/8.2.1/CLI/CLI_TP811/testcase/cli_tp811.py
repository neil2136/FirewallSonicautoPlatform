from time import sleep
from definition.init_param import *
from definition.tools import *


class Test_CLI_1(Test):
    uuid='1713751'
    description= show_testcase_info(Parameter.TESTPLAN, '1713751', description=True)['title']

    def test_01_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713751')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_01_user_login_error(self):
        fw_cli_error = Firewall(Parameter.FIREWALL, user='test', password='test', supported_config_mode='cli-ssh')
        rc = fw_cli_error.cli_login()
        print(rc)
        logger.info("Sleep 5 minutes for ssh locked")
        sleep(305)
        Assertion.assert_equal(rc, False, "ERR: User can login with error user name and error password")

    def test_01_02_admin_login_error(self):
        rc = login(user="admin", ip= "192.168.168.168",password='test')
        logger.info("Sleep 5 minutes for ssh locked")
        sleep(305)
        Assertion.assert_equal(rc, False, "ERR: Admin user can login with error password")

    def test_01_03_admin_login_error(self):
        rc = login(user="admin", ip= "192.168.168.168",password='')
        logger.info("Sleep 5 minutes for ssh locked")
        sleep(305)
        Assertion.assert_equal(rc, False, "ERR: Admin user can login with empty password")

    def test_01_04_admin_login(self):
        rc = fw_cli.cli_login()
        Assertion.assert_equal(rc, True, "ERR: Admin user can not login failed")


class Test_CLI_12(Test):
    uuid='1713755'
    description= show_testcase_info(Parameter.TESTPLAN, '1713755', description=True)['title']

    def test_02_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713755')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_user_logout(self):
        rc,ssh = login(user="admin", ip= "192.168.168.168",password=Params.G_NEW_PASSWORD)
        rc = cli_logout(ssh)
        Assertion.assert_equal(rc, True, "ERR: Admin user can not logout")


class Test_CLI_22(Test):
    uuid='1713766'
    description= show_testcase_info(Parameter.TESTPLAN, '1713766', description=True)['title']

    def test_02_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713766')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_show_interface(self):
        flage = False
        flage = show_interface(fw_cli =fw_cli,flage=flage,start=0,end=6)
        Assertion.assert_equal(flage, True, "ERR: show interface info failed")

    def test_02_02_config_interface(self):
        flage = False
        for i in range(1,6):
            if i ==1:
                command = ["configure", "interface x1","ip-assignment WAN static","ip 192.168.161.168","commit","end"]
            else:
                command = ["configure", "interface x{0}".format(i),"ip-assignment LAN static","ip 192.168.16{0}.168".format(i),"commit","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flage = True
            else:
                flage = False
                break
        Assertion.assert_equal(flage, True, "ERR: config interface failed")

    def test_02_03_show_interface_ip(self):
        flage = False
        flage = show_interface_ip(fw_cli =fw_cli,flage=flage,start=1,end=6)
        Assertion.assert_equal(flage, True, "ERR: show interface ip info failed")
            
class Test_CLI_23(Test):
    uuid='1713767'
    description= show_testcase_info(Parameter.TESTPLAN, '1713767', description=True)['title']

    def test_03_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713767')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_config_interface_to_WLAN(self):
        flage = False
        for i in range(2,5):
            sleep(2)
            command = ["configure", "interface x{0}".format(i),"ip-assignment WLAN static","ip 172.168.1{0}8.168".format(i),"netmask 255.255.248.0","commit","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flage = True
            else:
                flage = False
                break
        Assertion.assert_equal(flage, True, "ERR: config interface to WLAN failed")

    def test_03_02_check_WLAN(self):
        flage = False
        flage = show_interface_zone(fw_cli=fw_cli,flage=flage,start=2,end=5,zone="WLAN")
        Assertion.assert_equal(flage, True, "ERR: show WALN info failed")

    def test_03_03_config_interface_to_DMZ(self):
        flage = False
        for i in range(2,6):
            sleep(1)
            command = ["configure", "interface x{0}".format(i),"ip-assignment DMZ static","commit","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flage = True
            else:
                flage = False
                break
        Assertion.assert_equal(flage, True, "ERR: config interface to DMZ failed")

    def test_03_04_check_DMZ(self):
        flage = False
        flage = show_interface_zone(fw_cli=fw_cli,flage=flage,start=2,end=6,zone="DMZ")
        Assertion.assert_equal(flage, True, "ERR: show DMZ failed")

    def test_03_05_config_interface_to_LAN(self):
        flage = False
        for i in range(2,6):
            sleep(2)
            command = ["configure", "interface x{0}".format(i),"ip-assignment LAN static","commit","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flage = True
            else:
                flage = False
                break
        Assertion.assert_equal(flage, True, "ERR: config interface to LAN failed")

    def test_03_06_check_LAN(self):
        flage = False
        flage = show_interface_zone(fw_cli=fw_cli,flage=flage,start=2,end=6,zone="LAN")
        Assertion.assert_equal(flage, True, "ERR: show LAN info failed")

    def test_03_07_config_X0(self):
        command = ["configure", "interface x0","ip-assignment WAN static","commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], False, "ERR: config X0 failed")

    def test_03_08_config_X1_to_LAN(self):
        command = ["configure", "interface x1","ip-assignment LAN static","commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], False, "ERR: config X1 to LAN failed")

    def test_03_09_config_X1_to_DMZ(self):
        command = ["configure", "interface x1","ip-assignment DMZ static","commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], False, "ERR: config X1 to DMZ failed")

    def test_03_10_config_X1_to_LAN(self):
        command = ["configure", "interface x1","ip-assignment LAN static","commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], False, "ERR: config X1 to LAN failed")

    def test_03_11_config_X1_to_WLAN(self):
        command = ["configure", "interface x1","ip-assignment WLAN static","ip 172.168.118.168","netmask 255.255.254.0","commit","end"]
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], False, "ERR: config X1 to WLAN failed")


class Test_CLI_26(Test):
    uuid='1713770'
    description= show_testcase_info(Parameter.TESTPLAN, '1713770', description=True)['title']

    def test_04_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713770')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_04_01_config_interface_to_WLAN(self):
        flage = False
        for i in range(2,6):
            sleep(2)
            command = ["configure", "interface x{0}".format(i),"ip-assignment WAN static","ip 172.168.1{0}8.168".format(i),"netmask 255.255.248.0","commit","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if "Changes made" in rc[1] or "changes made" in rc[1]:
                flage = True
            else:
                flage = False
                break
        Assertion.assert_equal(flage, True, "ERR: config interface to WLAN failed")

    def test_04_02_check_WLAN(self):
        flage = False
        flage = show_interface_zone(fw_cli=fw_cli,flage=flage,start=2,end=6,zone="WAN")
        Assertion.assert_equal(flage, True, "ERR: show WALN info failed")


class Test_CLI_27(Test):
    uuid='1713771'
    description= show_testcase_info(Parameter.TESTPLAN, '1713771', description=True)['title']

    def test_05_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713771')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_05_01_config_interface_to_LAN(self):
        flage = False
        for i in range(2,6):
            sleep(2)
            command = ["configure", "interface x{0}".format(i),"ip-assignment LAN static","end"]
            rc = fw_cli.do_cli_commands(command,tag=1)
            if rc[1]:
                flage = True
            else:
                flage = False
        Assertion.assert_equal(flage, True, "ERR: config interface to LAN failed")

    def test_05_02_check_LAN(self):
        flage = False
        flage = show_interface_zone(fw_cli=fw_cli,flage=flage,start=2,end=6,zone="WAN")
        Assertion.assert_equal(flage, True, "ERR: show LAN info failed")


class Test_CLI_40(Test):
    uuid='1713786'
    description= show_testcase_info(Parameter.TESTPLAN, '1713786', description=True)['title']

    def test_06_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713786')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_config_web_manage(self):
        command = [
            'configure',
            'interface x0',
            'no management https',
            'user-login https',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config management https failed")

    def test_06_02_check_https_login(self):
        rc = fw.api_login()
        Assertion.assert_regular(rc, r"(Administrator login not allowed from here|Response is Service disabled over HTTPS)", 'ERR: Check management https info failed')

    def test_06_03_config_web_manage(self):
        command = [
            'configure',
            'interface x0',
            'management https',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config management https failed")

    def test_06_04_check_https_login(self):
        rc = fw.api_login()
        Assertion.assert_equal(rc, True, "ERR: Check management https login failed")


class Test_CLI_41(Test):
    uuid='1713787'
    description= show_testcase_info(Parameter.TESTPLAN, '1713787', description=True)['title']

    def test_07_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713787')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_07_01_config_security_type(self):
        command = [
            'configure',
            'zone test',
            'security-type trusted',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: config security-type trusted failed")
    
    def test_07_02_check_zone_test(self):
        command = [
            'show zone test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_regular(rc[1], r"security-type trusted", "ERR: Check zone info failed")

    def test_07_03_config_zone(self):
        command = [
            'configure',
            'zone test',
            'dpi-ssl-server',
            "intrusion-prevention",
            "gateway-anti-virus",
            "anti-spyware",
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config zone test failed")

    def test_07_04_check_zone_test(self):
        flage = False
        command = [
            'show zone test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "no gateway-anti-virus" not in rc[1] and "no intrusion-prevention" not in rc[1] and "no anti-spyware" not in rc[1] and "no dpi-ssl-server" not in rc[1]:
            flage = True
        Assertion.assert_equal(flage, True, "ERR: Check zone test info failed")

    def test_07_05_config_zone(self):
        command = [
            'configure',
            'zone test',
            'no dpi-ssl-server',
            "no intrusion-prevention",
            "no gateway-anti-virus",
            "no anti-spyware",
            'cancel']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config zone test failed")

    def test_07_06_check_zone_test(self):
        flage = False
        command = [
            'show zone test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        if "no gateway-anti-virus" not in rc[1] and "no intrusion-prevention" not in rc[1] and "no anti-spyware" not in rc[1] and "no dpi-ssl-server" not in rc[1]:
            flage = True
        Assertion.assert_equal(flage, True, "ERR: Check zone test info failed")

    def test_07_07_config_zone_security_type(self):
        command = [
            'configure',
            'zone test',
            'security-type public',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config zone test security type failed")

    def test_07_08_check_zone_test(self):
        command = [
            'show zone test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_regular(rc[1], r"security-type public", "ERR: Check zone test info failed")


class Test_CLI_47(Test):
    uuid='1713793'
    description= show_testcase_info(Parameter.TESTPLAN, '1713793', description=True)['title']

    def test_08_00_show_testcase_info(slef):
        show_testcase_info(Parameter.TESTPLAN,'1713793')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_08_01_config_address_object(self):
        command = [
            'configure',
            'address-object ipv4 test',
            'host 192.168.1.168',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config address object failed")

    def test_08_02_check_address_object_test(self):
        command = [
            'show address-object ipv4 test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_regular(rc[1], r"address-object ipv4 test", "ERR: Check address object info failed")

    def test_08_03_config_address_object_test_zone(self):
        command = [
            'configure',
            'address-object ipv4 test',
            'zone WAN',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config address object failed")

    def test_08_04_check_address_object_test_zone(self):
        command = [
            'show address-object ipv4 test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_regular(rc[1], r"zone WAN", "ERR: Check address object info failed")

    def test_08_05_config_address_object_test_network(self):
        command = [
            'configure',
            'address-object ipv4 test',
            'network 192.168.1.0 255.255.255.0',
            'commit']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_equal(rc[0], True, "ERR: Config address object failed")

    def test_08_06_check_address_object_test_network(self):
        command = [
            'show address-object ipv4 test']
        rc = fw_cli.do_cli_commands(command,tag=1)
        Assertion.assert_regular(rc[1], r"network 192.168.1.0 255.255.255.0", "ERR: Check address object info failed")