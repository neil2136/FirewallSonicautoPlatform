from definition.settings import *


@paramunittest.parametrized(
    {'FromZone': 'LAN','ToZone':'LAN',  'uuid': 'SOSAIOT-TC-51583', 'tcid': '4'},
    {'FromZone': 'DMZ','ToZone':'DMZ',  'uuid': 'SOSAIOT-TC-51580', 'tcid': '5'},
    {'FromZone': 'CST','ToZone':'CST',  'uuid': 'SOSAIOT-TC-51581', 'tcid': '6'},
    {'FromZone': 'LAN','ToZone':'DMZ',  'uuid': 'SOSAIOT-TC-51582', 'tcid': '7'},
    # {'FromZone': 'LAN','ToZone':'CST',  'uuid': '', 'tcid': '7'},
    # {'FromZone': 'DMZ','ToZone':'LAN',  'uuid': '', 'tcid': '7'},
    # {'FromZone': 'DMZ','ToZone':'CST',  'uuid': '', 'tcid': '7'},
    # {'FromZone': 'CST','ToZone':'LAN',  'uuid': '', 'tcid': '7'},
    # {'FromZone': 'CST','ToZone':'DMZ',  'uuid': '1704901', 'tcid': '7'},
)
class TestVPN_DNS_Loopback_340(Test):

    def setParameters(self, FromZone,ToZone, uuid, tcid):
        self.FromZone = FromZone
        self.ToZone = ToZone
        self.uuid = uuid
        self.tcid = tcid
        self.description = 'test'
        self.description = show_testcase_info(TESTPLAN, self.tcid, description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_01_01_Add_Nat_Policy(self):
        if self.FromZone == 'LAN':
            os = 'X0 Subnet'
        elif self.FromZone == 'DMZ':
            os = 'X2 Subnet'
        elif self.FromZone == 'CST':
            os = 'X3 Subnet'
        if self.ToZone == "LAN":
            td = 'HTTP_Private_LAN'
        elif self.ToZone == "DMZ":
            td = 'HTTP_Private_DMZ'
        elif self.ToZone == "CST":
            td = 'HTTP_Private_CST'
        ref = copy.deepcopy(nat_opts)
        opt = ref['nat_policies'][0]['ipv4']
        opt['source']['name'] = os
        opt['translated_destination']['name'] = td
        logger.info(" {} ".center(20, '-').format('Add Nat Rule for DUT'))
        rc = natPolicyObj.add_nat_policy(**ref)
        Assertion.assert_equal(rc, True, f"ERR: Add Nat Rule for DUT failed")
        
    def test_01_02_Add_ACL(self):
        logger.info(" {} ".center(20, '-').format('Add ACL '))
        rule1 = copy.deepcopy(rule_opt)
        rule1['name'] = 'my_acl'
        rule1['from'] = self.FromZone
        rule1['to']   = self.ToZone
        rule1['service']   = {"name":"HTTP"}
        rc = Laccess_rule_obj.config_accessrule(**rule1)
        Assertion.assert_equal(rc, True, "ERR: Add ACL failed")
        
    def test_01_03_config_HTTP_Server(self):
        logger.info(" {} ".center(20, '-').format('config HTTP Server '))
        if self.ToZone == "LAN":
            ip = DUT_X0
            device = 'eth1'
        elif self.ToZone == "DMZ":
            ip = DUT_X2
            device = 'eth2'
        elif self.ToZone == "CST":
            ip = DUT_X3
            device = 'eth3'
        logger.info(f'send command :ip r a {DUT_X1} via {ip} dev {device}')
        http_server.send_command(f'ip r a {DUT_X1} via {ip} dev {device}')
        out = http_server.send_command('route')
        if DUT_X1 in str(out):
            rc = True
            logger.info(f"add route {DUT_X1} via {ip} dev {device} success")
        else:
            rc = False
            logger.error(f"add route {DUT_X1} via {ip} dev {device} failed")
        Assertion.assert_equal(rc, True, "ERR: config HTTP Server failed")
        
    def test_01_04_login_HTTP_Server(self):
        logger.info(" {} ".center(20, '-').format('config HTTP Server '))
        if self.FromZone == "LAN":
            ip = DUT_X0
            server =  Host(PC1_LAN, user='root', password='password')
        elif self.FromZone == "DMZ":
            ip = DUT_X2
            server =  Host(PC3_DMZ, user='root', password='password')
        elif self.FromZone == "CST":
            ip = DUT_X3
            server =  Host(PC4_CST, user='root', password='password')
        cmd1 = f"sed -i '1inameserver {PC_DNS2}' /etc/resolv.conf"
        cmd2 = f'ip r a {PC_HTTP} via {ip} dev eth1'
        cmd3 = f'ip r a {PC_DNS2} via {ip} dev eth1'
        cmd4 = f'ip r d {PC_HTTP} via {ip} dev eth1'
        cmd5 = f'ip r d {PC_DNS2} via {ip} dev eth1'
        logger.info(f'send command :{cmd1}')
        server.send_command(cmd1)
        logger.info(f'send command :{cmd2}')
        server.send_command(cmd2)
        logger.info(f'send command :{cmd3}')
        server.send_command(cmd3)
        server.send_command('service httpd start')
        out1 = server.send_command('cat /etc/resolv.conf')
        out2 = server.send_command('route')
        if PC_DNS2 in str(out1) and 'PC-HTTP' in str(out2) and PC_DNS2 in str(out2):
            rc = True
            logger.info('add route and config dns success!!')
        else:
            rc = False
            logger.error('add route and config dns failed!!')
        for i in range(9):
            out = server.send_command(f'nslookup {http_domain}')
            if http_domain in str(out)  and (PC_DNS2 in str(out) or  Params.G_DNS1 in str(out) or "69.167.164.199" in str(out) or "127.0.0.1" in str(out) ):
                rc &= True
                logger.info(f"dns resolves {http_domain} successful!!!")
                break
            elif i == 8:
                rc &= False
                logger.error(f"dns resolves {http_domain} failed")
        logger.info(f'send command :{cmd4}')
        server.send_command(cmd4)
        logger.info(f'send command :{cmd5}')
        server.send_command(cmd5)
        server.send_command('sed -i "1d" /etc/resolv.conf')
        out3 = server.send_command('route')
        out4 = server.send_command('cat /etc/resolv.conf')
        if  PC_HTTP not in str(out3) and PC_DNS2 not in str(out3) and PC_DNS2 not in str(out4):
            rc &= True
            logger.info('del route  success!!')
        else:
            rc &= False
            logger.error('del route failed!!')
        Assertion.assert_equal(rc, True, "ERR: config HTTP Server failed")
        
    def test_01_05_Restore_Env(self):
        logger.info(" {} ".center(20, '-').format('Restore env'))
        logger.info('delete nat policy')
        rc = natPolicyObj.del_nat_policy_by_name(name = 'tc_nat_rule')
        logger.info('delete acl')
        rc &= Laccess_rule_obj.delete_accessrule_by_name('my_acl')
        logger.info(f'delete ip route,send command: ip r d {DUT_X1}')
        http_server.send_command(f' ip r d {DUT_X1}')
        out = http_server.send_command('route')
        if DUT_X1 not in str(out):
            rc &= True
            logger.info(f"del route success")
        else:
            rc &= False
            logger.error(f"del route {DUT_X1}  failed")
        Assertion.assert_equal(rc, True, "ERR: Restore env failed")
