from definition.settings import *


class TestConfigTB1(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    @repeat_method(5)
    def test_00_00_Config_Interface_and_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Config  ip address '))
        rc = Linterface.config_interface(**Lx1_r)
        time.sleep(10)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: Config ip address failed")
    
    def test_00_01_Add_Route_for_PC1_and_PC4(self):
        logger.info('-'*10+'add the route in PC1 and pc4 '+'-'*10)
        logger.info('send commands {}'.format(cmd_route))
        PC1.send_command(cmd_route)
        res1 = PC1.send_command('route')
        PC4.send_command(cmd_route)
        res2 = PC4.send_command('route')
        if '192.200.200.0' in res1 and '192.200.200.0' in res2:
            rc = True
        else:
            rc = False
            logger.info('pc1 route is {},pc4 route is {}'.format(res1,res2))
        Assertion.assert_equal(rc, True, 'add the route in PC1 and PC2 Failed.')

    def test_00_02_Config_DHCP_Server(self):
        logger.info('-'*10+'Config DHCP Server '+'-'*10)
        PC2.send_command('mv -f /etc/dhcp/dhcpd.conf /etc/dhcp/dhcpd.conf.bak')
        PC2.send_command('cp -f {} /etc/dhcp/dhcpd.conf'.format(dhcp_file))
        PC2.send_command('service dhcpd start')
        res = PC2.send_command('service dhcpd status')
        if 'is running' in res:
            rc = True
        else:
            rc = False
            logger.info(res)
        Assertion.assert_equal(rc, True, 'Config DHCP Server Failed.')

    def test_00_03_Config_PC3_as_DNS_Server(self):
        logger.info('-'*10+'Config PC3 as DNS  Server '+'-'*10)
        PC3.send_command('cp {} /var/named/chroot/var/named/'.format(dhcp_db))
        PC3.send_command('cp {} /var/named/chroot/etc/'.format(dhcp_name))
        res = PC3.send_command('service named restart')
        if 'Starting named: [  OK  ]' in res:
              rc = True
        else:
            rc = False
            logger.info(res)
        Assertion.assert_equal(rc, True, 'Config PC3 as DNS  Server Failed.')

    def test_00_04_Config_DNS_Server_for_UTM_and_PC2(self):
        logger.info('-'*10+'Config PC3 as DNS  Server '+'-'*10)
        PC1.send_command(f'echo "{cmd1}" > /etc/resolv.conf')
        PC2.send_command(f"echo '{cmd2}' > /etc/resolv.conf")
        PC5.send_command(f"echo '{cmd2}' > /etc/resolv.conf")
        logger.info('config dns server for UTM')
        rc = dnsObj.set_dns(**dns_dict)
        Assertion.assert_equal(rc, True, 'Config PC3 as DNS  Server Failed.')

    def test_00_05_Add_ACL(self):
        logger.info(" {} ".center(20, '-').format('Add ACL for WAN to LAN '))
        rule1 = copy.deepcopy(rule_opt)
        rule1['name'] = 'WAN_to_LAN'
        rule1['from'] = 'WAN'
        rule1['to']   = 'LAN'
        uuid = Laccess_rule_obj.get_access_rule_uuid(frm_rule = 'WAN',to_rule='LAN',action_rule='deny')
        rc = Laccess_rule_obj.put_accessrule(url=f"/access-rules/ipv4/uuid/{uuid}",**rule1)
        Assertion.assert_equal(rc, True, "ERR: Add ACL for WAN to LAN failed")
    
    def test_00_06_Config_WAN_Interface(self):
        logger.info(" {} ".center(20, '-').format('Config WAN for DHCP '))
        rc = Linterface.config_interface(**Lx1)
        Assertion.assert_equal(rc, True, "ERR: Config WAN for DHCP failed")
    
    def test_00_07_Add_AddObj(self):
        logger.info('-'*10+'Add  AddObj for DUT '+'-'*10)
        rc = LAddrOBJ.config_addressobject(**opt1)
        rc &= LAddrOBJ.config_addressobject(**opt2)
        rc &= LAddrOBJ.config_addressobject(**opt3)
        rc &= LAddrOBJ.config_addressobject(**opt4)
        rc &= LAddrOBJ.config_addressobject(**opt5)
        rc &= LAddrOBJ.config_addressobject(**opt6)
        rc &= LAddrOBJ.config_addressobject(**opt7)
        rc &= LAddrGroupOBJ.add_addressgroup(**opt8)
        rc &= LAddrGroupOBJ.add_addressgroup(**opt10)
        Assertion.assert_equal(rc, True, 'Add local  AddObj for DUT  Failed.')

    





   
