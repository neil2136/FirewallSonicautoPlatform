from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True
    
    def test_00_01_add_route(self):
        logger.info('-'*10+'add route'+'-'*10)
        out1 = PC1.send_commands(pc1_route_cmds)
        out3 = PC3.send_commands(pc3_route_cmds)
        if  f"{PC3_Network}/24 via {DUT_X2}" in out1 and \
            f'{PC1_Network_2}/24 via {DUT_X3}' in out3:
            rc = True
        else:
            rc = False
            logger.error(out1)
            logger.error(out2)
            logger.error(out3)
        Assertion.assert_equal(rc, True, 'add route Failed.')

    def test_00_02_config_interface(self):
        logger.info('-'*10+'config x1 and x2 x3 ip'+'-'*10)
        rc = Linterface.config_interface(**Lx3)
        rc &= Linterface.config_interface(**Lx1)
        rc &= Linterface.config_interface(**Lx2)
        Assertion.assert_equal(rc, True, 'config x1 and x2 x3 ip Failed.')

    def test_00_03_add_acl(self):
        rule3 = copy.deepcopy(rule_opt)
        rule3['name'] = 'WAN_to_LAN'
        rule3['from'] = 'WAN'
        rule3['to']   = 'LAN'
        uuid = Laccess_rule_obj.get_access_rule_uuid(frm_rule='WAN', to_rule='LAN', action_rule="deny")
        rc = Laccess_rule_obj.put_accessrule(url=f"/access-rules/ipv4/uuid/{uuid}",**rule3)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")
        
    def test_00_04_check_ftp_server(self):
        cmd = "ping {}  -w 3".format(pc3_ip)
        for i in range(10):
            logger.info("send the command {}".format(cmd))
            out = PC1.send_command(cmd)
            if '100% packet loss' not in str(out):
                logger.info('Send ping from pc1 to pc2 success')
                rc = True
                break
            elif i == 9:
                logger.info('Ping failed')
                rc = False
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")

