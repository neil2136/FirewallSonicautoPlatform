from definition.global_v import *

class TestConfigPC(Test):
    uuid = 'NonTC'

    def test_01_Setup_pptp_server_on_PC2(self):
        flag = False
        pptpd_conf    = '/etc/pptpd.conf';  
        options_pptpd = '/etc/ppp/options.pptpd';
        chap_secrets = '/etc/ppp/chap-secrets';
        pap_secrets  = '/etc/ppp/pap-secrets';
        PC2_login.send_command("mv {} {}.bak".format(pptpd_conf, pptpd_conf))
        PC2_login.send_command("mv {} {}.bak".format(options_pptpd, options_pptpd))
        PC2_login.send_command("mv {} {}.bak".format(chap_secrets, chap_secrets))
        PC2_login.send_command("mv {} {}.bak".format(pap_secrets, pap_secrets))
        for i in range(1,5):
            ret = PC2_login.send_command("cp -f {}pptpd.conf /etc/".format(confs_path))
            ret = ret + PC2_login.send_command("cp -f {}options.pptpd /etc/ppp/".format(confs_path))
            ret = ret + PC2_login.send_command("cp -f {}chap-secrets /etc/ppp/".format(confs_path))
            ret = ret + PC2_login.send_command("cp -f {}pap-secrets /etc/ppp/".format(confs_path))
            logger.info(ret)
            PC2_login.send_command("service pptpd restart-kill")
            PC2_login.send_command("service pptpd start")
            status = PC2_login.send_command("service pptpd status")
            logger.info(status)
            if re.search(r'is running', status, re.I):
                flag = True
                break
        Assertion.assert_equal(flag, True, "ERR: Start pptp server on PC2 failed")

    def test_01_Setup_dhcp_server_on_PC2(self):
        flag = False
        for i in range(1,5):
            conf_file = os.environ["PYTHON_SONICOS_HOME"] + '/Network/PPTP_Client/confs/dhcpd.conf';
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


