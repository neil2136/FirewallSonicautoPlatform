from definition.global_v import *


class TestDHCP_Server_Options_01(Test):
    uuid = "SOSAIOT-TC-55926"
    description= show_testcase_info(TESTPLAN, '01', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_01) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_01) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed") 

    def test_03_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:90 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')

        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S254.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\s6f6f6f6f', str(out), re.I|re.DOTALL)
            if match2:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option failed")

    def test_04_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_05_Delete_the_DHCP_Option_Object(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")


class TestDHCP_Server_Options_02(Test):
    uuid = "SOSAIOT-TC-55928"
    description= show_testcase_info(TESTPLAN, '02', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_02) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_02) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed") 

    def test_03_Verify_the_DHCP_Option_for_not_requested(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:90 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')

        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S70.*POP3 Server[\s\S]*?Length:\s4[\s\S]*?POP3 Server:\s' + Object_ip1 + r'\s\S' + Object_ip1, str(out), re.I|re.DOTALL)
            if not match2:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option_for_not_requested failed")
    
    def test_04_Verify_the_DHCP_Option_for_requested(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:90 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(6)
        logger.info('dhclient -nw eth2 -R pop-server')
        os.system('dhclient -nw eth2 -R pop-server')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        out = os.popen('cat {} ' .format(FilePath)).read()
        logger.info(out)
        rc = re.search(r'Option:\s\S70.*POP3 Server[\s\S]*?Length:\s4[\s\S]*?POP3 Server:\s' + Object_ip1 + r'\s\S' + Object_ip1, str(out), re.I|re.DOTALL)
        if rc:
            flag = True
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option_for_requested failed")

    def test_05_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_06_Delete_the_DHCP_Option_Object(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")

 
class TestDHCP_Server_Options_03(Test):
    uuid = "SOSAIOT-TC-55929"
    description= show_testcase_info(TESTPLAN, '03', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_03) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_03) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed")      

    def test_03_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:120 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')

        logger.info('Define the DHCP option 150 in /etc/dhclient.conf')
        logger.info("echo 'option local-150 code 150 = ip-address;' > /etc/dhcp/dhclient.conf")
        os.system("echo 'option local-150 code 150 = ip-address;' > /etc/dhcp/dhclient.conf")
        out = os.popen('cat /etc/dhcp/dhclient.conf').read()
        logger.info("The file: /etc/dhclient.conf content is:{}". format(out))

        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        
        logger.info('dhclient -nw eth2 -R local-150')
        os.system('dhclient -nw eth2 -R local-150')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S150.*TFTP Server Address[\s\S]*?Length:\s4[\s\S]*?TFTP Server Address:\s' + Object_ip1 + r'\s\S' + Object_ip1, str(out), re.I|re.DOTALL)
            match3 = re.search(r'Option:\s\S150.*TFTP Server Address[\s\S]*?Length:\s4[\s\S]*?TFTP Server Address:\s' + Object_ip2 + r'\s\S' + Object_ip2, str(out), re.I|re.DOTALL)
            if match2 and match3:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option failed")
    
    def test_05_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_06_Delete_the_DHCP_Option_Object(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")

class TestDHCP_Server_Options_04(Test):
    uuid = "SOSAIOT-TC-55930"
    description= show_testcase_info(TESTPLAN, '04', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_04) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_04) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_03_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:120 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')

        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S70.*POP3 Server[\s\S]*?Length:\s4[\s\S]*?POP3 Server:\s' + Object_ip1 + r'\s\S' + Object_ip1, str(out), re.I|re.DOTALL)
            if match2:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option failed")

    def test_04_export_prefs(self):
        rc = setting_obj.export_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: Failed to export settings.")

    def test_05_reboot_fw(self):
        rc = setting_obj.boot_fw(mode=2)
        Assertion.assert_equal(rc, True, "ERR: Reboot FW failed.")

    def test_06_enable_api(self):
        ip = '192.168.168.168'
        fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
        admin = AdminCli(fw)
        api_dict = {
           'sonicos-api': True,
           'basic': True,
        }
        result = admin.sonicos_api(**api_dict)
        Assertion.assert_equal(result, True, "ERR: Enable api failed.")

    def test_07_import_prefs(self):
        time.sleep(5)
        rc = setting_obj.import_setting_exp(filepath='/tmp/preference_test.exp')
        Assertion.assert_equal(rc, True, "ERR: Failed to import settings.")

    def test_08_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:120 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(5)
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S70.*POP3 Server[\s\S]*?Length:\s4[\s\S]*?POP3 Server:\s' + Object_ip1 + r'\s\S' + Object_ip1, str(out), re.I|re.DOTALL)
            if match2:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option failed")

    def test_09_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_10_Delete_the_DHCP_Option_Object(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")


class TestDHCP_Server_Options_07(Test):
    uuid = "SOSAIOT-TC-55931"
    description= show_testcase_info(TESTPLAN, '07', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_0711) 
        ret &= dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_0722) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Option_group(self):
        ret = dhcp_obj.add_dhcp_server_option_group(**add_dhcp_server_option_group)
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_group failed.")

    def test_03_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_07) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_04_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:120 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(5)
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S231.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\sdededede', str(out), re.I|re.DOTALL)
            match3 = re.search(r'Option:\s\S230.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\s6f6f6f6f', str(out), re.I|re.DOTALL)
            if match2 and match3:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option  failed")

    def test_05_Delete_the_DHCP_Option_Object1(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")

    @repeat_method(5)
    def test_06_Verify_the_DHCP_Option_after_delete_option1(self):
        os.system('rm -rf /tmp/dhcpCapture.txt')
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:360 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(5)
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(350)
        out = os.popen('cat {} ' .format(FilePath)).read()
        match2 = re.search(r'Option:\s\S231.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\sdededede', str(out), re.I|re.DOTALL)
        match3 = re.search(r'Option:\s\S230.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\s6f6f6f6f', str(out), re.I|re.DOTALL)
        if match2 and not match3:
            flag = True
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option_after_delete_option1 failed")

    def test_07_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_08_Delete_the_DHCP_Option_Object(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname2, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")

    def test_09_delete_dhcp_server_option_group(self):
        rc = dhcp_obj.delete_dhcp_server_option_group(name=DHCP_Grp1)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_group failed")


class TestDHCP_Server_Options_08(Test):
    uuid = "SOSAIOT-TC-55927"
    description= show_testcase_info(TESTPLAN, '08', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_Add_a_DHCP_Option_Object(self):
        ret = dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_0711) 
        ret &= dhcp_obj.add_dhcp_server_option_object(**add_dhcp_server_option_object_0722) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_Object failed") 

    def test_02_Add_a_DHCP_Option_group(self):
        ret = dhcp_obj.add_dhcp_server_option_group(**add_dhcp_server_option_group)
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Option_group")

    def test_03_Add_a_DHCP_Scope_on_firewall_X2_Interface(self):
        ret = dhcp_obj.add_dhcp_server_scope_dynamic(**add_dhcp_server_scope_dynamic_07) 
        Assertion.assert_equal(ret, True, "ERR: Add_a_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_04_Verify_the_DHCP_Option(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:120 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('ip a flush dev eth2')
        os.system('ip a flush dev eth2')
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(5)
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        time.sleep(70)
        rc = os.popen('ip a show eth2').read()
        logger.info(rc)
        match1 = re.search(r'inet 172.16.2.\d\d\d.24', rc, re.I|re.DOTALL)
        if match1:
            out = os.popen('cat {} ' .format(FilePath)).read()
            logger.info(out)
            match2 = re.search(r'Option:\s\S231.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\sdededede', str(out), re.I|re.DOTALL)
            match3 = re.search(r'Option:\s\S230.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\s6f6f6f6f', str(out), re.I|re.DOTALL)
            if match2 and match3:
                flag = True
            else:
                logger.error('Capture DHCP packets failed2')
        else:
            logger.error('Capture DHCP packets failed1')
            flag = False
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option_for_not_requested failed")

    def test_05_Delete_the_DHCP_Option_Object1_and_option2(self):
        rc = dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname, version=4)
        rc &= dhcp_obj.delete_dhcp_server_option_object(name=DHCP_Optname2, version=4)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_Object failed")

    @repeat_method(5)
    def test_06_Verify_the_DHCP_Option_after_delete_option1_and_option2(self):
        flag = None
        logger.info("Start tshark to capture dhcp packets")
        cmd = "tshark -i eth2 -f 'udp dst port 67 or 68' -a duration:249 -V > {} &" .format(FilePath)
        os.system(cmd)
        time.sleep(2)
        logger.info('dhclient -r eth2')
        os.system('dhclient -r eth2')
        time.sleep(5)
        logger.info('dhclient -nw eth2')
        os.system('dhclient -nw eth2')
        out = os.popen('cat {} ' .format(FilePath)).read()
        match2 = re.search(r'Option:\s\S231.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\sdededede', str(out), re.I|re.DOTALL)
        match3 = re.search(r'Option:\s\S230.*Private[\s\S]*?Length:\s4[\s\S]*?Value:\s6f6f6f6f', str(out), re.I|re.DOTALL)
        if match2 or match3:
            flag = False
        else:
            logger.error('Capture DHCP packets failed1')
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Verify_the_DHCP_Option_after_delete_option1_and_option2 failed")

    def test_09_Delete_the_DHCP_Scope_on_firewall_X2_Interface(self):
        rc = dhcp_obj.delete_dhcp_server_scope_v4(scope='dynamic', p1=dynamic_start, p2=dynamic_end)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Scope_on_firewall_X2_Interface failed")

    def test_11_delete_dhcp_server_option_group(self):
        rc = dhcp_obj.delete_dhcp_server_option_group(name=DHCP_Grp1)
        Assertion.assert_equal(rc, True, "ERR: Delete_the_DHCP_Option_group failed")