from definition.settings import *

class TestConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_setup_dhcp_server_on_pc2(self):
        flag = False
        for i in range(3):
            conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/Network/DHCP_Client_TP54/definition/script/dhcpd.conf'
            pc2login.send_command("mv /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak")
            pc2login.send_command("cp -f {} /etc/dhcp/dhcpd.conf".format(conf_file))
            pc2login.send_command("service dhcpd restart")
            dhcpres = pc2login.send_command("service dhcpd status")
            logger.info(dhcpres)
            if re.search(r'is running', dhcpres, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Start dhcp server on PC2 failed")




