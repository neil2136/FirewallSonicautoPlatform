from definition.settings import *

class TestConfigPC(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_define_custom_dhcp_options_on_pc2(self):
        cmds = [
                "echo 'option private1 code 230 = ip-address;' > /etc/dhcp/dhclient.conf",
                "echo 'option private2 code 231 = ip-address;' >> /etc/dhcp/dhclient.conf",
                "echo 'option tftp_150 code 150 = ip-address;' >> /etc/dhcp/dhclient.conf",
                "cat /etc/dhcp/dhclient.conf"
                ]
        checklist = ['private1', 'private2', 'tftp_150']
        res = PC2_Login.send_commands(cmds)
        logger.info(f'res is :{res}')
        flag = True if all(i in res for i in checklist) else False
        Assertion.assert_equal(flag, True, "ERR: define custom dhcp option on PC2 failed")




