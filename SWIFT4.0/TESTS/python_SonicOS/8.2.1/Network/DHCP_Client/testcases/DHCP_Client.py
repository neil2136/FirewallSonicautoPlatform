from definition.initial_parameter import *


class TestDHCPClient_01(Test):
    uuid = "SOSAIOT-TC-55839"
    description= show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']
    address_x1 = '0.0.0.0'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
   
    def test_01_config_X1_dhcp(self):
        x1_dhcp = {
            'if': 'x1',
            'zone': 'wan',
            'mode': 'dhcp',
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        output = interface_obj.config_interface(**x1_dhcp)
        Assertion.assert_equal(output, True, "ERR: Configure X1 status to DHCP failed")

    @repeat_method(5)
    def test_02_get_X1_address(self):
        for i in range(0, 5):
            info_x1 = interface_obj.get_interface_address('X1')
            if info_x1['ip_address'] == '0.0.0.0':
                time.sleep(5)
            else:
                TestDHCPClient_01.address_x1 = info_x1['ip_address']
                break
        logger.info("X1 DHCP ip is {}".format(TestDHCPClient_01.address_x1))
        Assertion.assert_not_regular(TestDHCPClient_01.address_x1, '0.0.0.0', "ERR: X1 get dhcp address failed")
 
    def test_03_verify_ping_DUT_x1(self):
        ret = PC2_login.send_command("ping {} -c 5".format(TestDHCPClient_01.address_x1))
        Assertion.assert_not_regular(ret, '100% packet loss', "ERR: Ping X1 failed")

    def test_04_verify_ssh_DUT_x1(self):
        flag = False
        command = 'python3 ' +  bin_path + 'ssh_login_X1.py -i ' + TestDHCPClient_01.address_x1
        ret = PC2_login.send_command( command )
        logger.info(ret)
        if (r'True', ret):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: ssh X1 ip failed")

#    def test_04_verify_ssh_DUT_x1(self):
#        flag = False
#        ssh = paramiko.SSHClient()
#        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#        try:
#            ssh.connect(hostname=TestDHCPClient_01.address_x1, port=22, username='admin', password='password')
#        except:
#            logger.info("failed to ssh X1 ip")
#        else:
#            logger.info("ssh X1 ip successfully")
#            flag = True
#            stdin, stdout, stderr = ssh.exec_command("ls")
#            logger.info(stdout.read())
#            logger.info(stderr.read())
#        finally:
#            ssh.close()
#        Assertion.assert_equal(flag, True, "ERR: ssh X1 ip failed")

    def test_05_verify_https_DUT_x1(self):
        fw.api_logout()
        flag = False
        command = 'python3 ' +  bin_path + 'login_logout_DUT_from_X1.py -i ' + TestDHCPClient_01.address_x1 + ' -a login'
        ret = PC2_login.send_command( command )
        if re.search(r'True', ret):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: https X1 ip failed")

    #def test_05_verify_https_DUT_x1(self):
    #    command = "curl -k -i --basic -u admin:password -H 'Accept: application/json' \
    #        -H 'Content-Type: application/json' --data '{ \"override\":true }' \
    #        -X POST https://" + TestDHCPClient_01.address_x1 + "/api/sonicos/auth --max-time 60"
    #    ret = PC2_login.send_command( command ).decode("utf-8")
    #    Assertion.assert_regular(ret, "200 OK", "ERR: https X1 ip failed")

class TestDHCPClient_02(Test):
    uuid = "SOSAIOT-TC-55840"
    description= show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']
    address_x1 = '0.0.0.0'

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_release_X1_IP(self):
        flag = False
        TestDHCPClient_02.address_x1 = interface_obj.get_interface_address('X1')["ip_address"]
        logger.info(TestDHCPClient_02.address_x1)
        for i in range(0,5):
            ret = interface_obj.click_dhcp_release(name='X1')
            logger.info(ret)
            TestDHCPClient_02.address_x1 = interface_obj.get_interface_address('X1')["ip_address"]
            logger.info(TestDHCPClient_02.address_x1)
            if TestDHCPClient_02.address_x1 == '0.0.0.0' and ret == True:
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: release X1 DHCP failed")


class TestDHCPClient_03(Test):
    uuid = "SOSAIOT-TC-55841"
    description= show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
  
    def test_01_renew_X1_IP(self):
        flag = False
        ret = interface_obj.get_interface_address('X1')
        address_x1_ip = ret["ip_address"]
        logger.info(address_x1_ip)
        address_x1_time1 = ret["lease_expires"]
        logger.info(address_x1_time1)
        if address_x1_ip != '0.0.0.0':
            interface_obj.click_dhcp_release(name='X1')
        ret = interface_obj.click_dhcp_renew(name='X1')
        logger.info(ret)
        address_x1_time2 = interface_obj.get_interface_address('X1')["lease_expires"]
        logger.info(address_x1_time2)
        if address_x1_time1 != address_x1_time2 and ret == True:
            flag = True
        Assertion.assert_equal(flag, True, "ERR: renew X1 DHCP failed")

