from definition.settings import *

class Test_1_Configure_Link_Aggregation(Test):
    uuid = "SOSAIOT-TC-"
    description = '''Verify that a link aggregation can be configured.'''

    def test_1_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_1_Step02_Config_X1_with_Aggregation_Port(self):
        logger.info("config x1 interface... ")
        rc = interface_api.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 with aggregation failed")

    def test_1_Step03_Config_X2_with_Aggregation_Port(self):
        logger.info("config x2 interface... ")
        rc = interface_api.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 with aggregation failed")

    def test_1_Step04_Check_Settings(self):
        out1 = interface_api.get_interface_status("X1")
        out2 = interface_api.get_interface_status("X2")
        rc = False
        try:
            if out1['interfaces'][0]['ipv4']['port']['aggregation']['aggregate'][0]['interface'] == 'X4' and \
               out2['interfaces'][0]['ipv4']['port']['aggregation']['aggregate'][0]['interface'] == 'X3':
                rc = True
            else:
                logger.error(out1)
                logger.error(out2)
        except:
            logger.error("May get X1/X2 port information failed.")
        Assertion.assert_equal(rc, True, "ERR: Config X1/X2 with aggregation port failed")


class Test_3_Management_on_LAG_Interface(Test):
    uuid = "SOSAIOT-TC-"
    description = '''Management (ping/https/http/ssh) on LAG interface.'''

    def test_3_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_3_Step02_Try_SSH_on_X2(self):
        out = system_cli.show_status()
        rc = False
        if re.search(r'Serial Number', out, re.I):
            rc = True 
        Assertion.assert_equal(rc, True, "ERR: Verify X2 SSH management failed")

    def test_3_Step03_Try_PING_on_X2(self):
        out = os.popen("ping {} -c 3".format(X2_IP)).read()
        rc = False
        if re.search(r' 0% packet loss', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify X2 PING management failed")

    def test_3_Step04_Try_HTTPS_on_X2(self):
        os.system("rm -rf /tmp/login.html")
        time.sleep(1)
        os.system("wget https://{} --no-check-certificate -O /tmp/login.html".format(X2_IP))
        rc = False
        out = ""
        try:
            out = os.popen("cat /tmp/login.html").read()
        except Exception as e:
            print("The got login.html may be a gzip package.")
            print(e)
        if not rc:
            os.system("rm -rf /tmp/login.gz")
            os.system("mv /tmp/login.html /tmp/login.gz")
            os.system("gunzip -c /tmp/login.gz > /tmp/login.html")
            out = os.popen("cat /tmp/login.html").read()

        if re.search(r'SonicWall Network Security Login', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify X2 HTTPS management failed")

    def test_3_Step05_Cut_X2_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X2', 'disable')
        Assertion.assert_equal(rc, True, "ERR: Cut X2 link failed")

    def test_3_Step06_Try_SSH_on_X2_Again(self):
        out = system_cli.show_status()
        rc = False
        if re.search(r'Serial Number', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify X2 SSH management failed")

    def test_3_Step07_Try_PING_on_X2_Again(self):
        out = os.popen("ping {} -c 3".format(X2_IP)).read()
        rc = False
        if re.search(r' 0% packet loss', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify X2 PING management failed")

    def test_3_Step08_Try_HTTPS_on_X2_Again(self):
        os.system("rm -rf /tmp/login.html")
        time.sleep(1)
        os.system("wget https://{} --no-check-certificate -O /tmp/login.html".format(X2_IP))
        rc = False
        out = ""
        try:
            out = os.popen("cat /tmp/login.html").read()
        except Exception as e:
            print("The got login.html may be a gzip package.")
            print(e)
        if not rc:
            os.system("rm -rf /tmp/login.gz")
            os.system("mv /tmp/login.html /tmp/login.gz")
            os.system("gunzip -c /tmp/login.gz > /tmp/login.html")
            out = os.popen("cat /tmp/login.html").read()

        if re.search(r'SonicWall Network Security Login', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify X2 HTTPS management failed")

    def test_3_Step09_Reconnect_X2_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X2', 'enable')
        Assertion.assert_equal(rc, True, "ERR: Reconnect X2 link failed")


class Test_11_Traffic_Across_Aggregation_LAN(Test):
    uuid = "SOSAIOT-TC-"
    description = '''Traffic Across the aggregation LAN.'''

    def test_11_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_Step02_Cut_X2_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X2', 'disable')
        Assertion.assert_equal(rc, True, "ERR: Cut X2 link failed")

    def test_11_Step03_FTP_Traffic_From_WAN_to_LAN(self):
        file = '/tmp/ftp_index.html'
        os.system('rm -rf {}'.format(file))
        os.system('wget ftp://root:password@{}:21/index.html -O {}'.format(X1_PC, file))
        out = os.popen('cat {}'.format(file)).read()
        rc = False
        if re.search(r'Hello World', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify FTP traffic from LAN to WAN failed")

    def test_11_Step04_Reconnect_X2_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X2', 'enable')
        Assertion.assert_equal(rc, True, "ERR: Reconnect X2 link failed")


class Test_12_Traffic_Across_Aggregation_WAN(Test):
    uuid = "SOSAIOT-TC-"
    description = '''Traffic Across the aggregation WAN.'''

    def test_12_Step01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_12_Step02_Cut_X1_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X1', 'disable')
        Assertion.assert_equal(rc, True, "ERR: Cut X1 link failed")

    def test_12_Step03_FTP_Traffic_From_WAN_to_LAN(self):
        file = '/tmp/ftp_index.html'
        os.system('rm -rf {}'.format(file))
        os.system('wget ftp://root:password@{}:21/index.html -O {}'.format(X1_PC, file))
        out = os.popen('cat {}'.format(file)).read()
        rc = False
        if re.search(r'Hello World', out, re.I):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Verify FTP traffic from LAN to WAN failed")

    def test_12_Step04_Reconnect_X1_Link(self):
        rc = os_obj.set_node_interface_state('UTM','X1', 'enable')
        Assertion.assert_equal(rc, True, "ERR: Reconnect X1 link failed")
