from definition.initial_parameter import *


class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_Setup_dhcp_server_on_PC2(self):
        flag = False
        for i in range(1,5):
            conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Client/conf/dhcpd.conf';
            ret = PC2_login.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
            ret = ret + PC2_login.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
            ret = ret + PC2_login.send_command("service dhcpd restart")
            logger.info(ret)
            status = PC2_login.send_command("service dhcpd status")
            logger.info(status)
            if re.search(r'is running', status, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC2 failed")
