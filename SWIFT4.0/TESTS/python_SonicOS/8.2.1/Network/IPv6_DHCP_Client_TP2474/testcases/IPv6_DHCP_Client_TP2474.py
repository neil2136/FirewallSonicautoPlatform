from definition.settings import *


@paramunittest.parametrized(
    {"RA":True,'M':True,'O':False},
    {"RA":True,'M':True,'O':True},
    {"RA":False,'M':False,'O':False},
    {"RA":True,'M':False,'O':True},
    {"RA":True,'M':False,'O':False},
)
class Test_IPv6_DHCP_01(Test):
    
    def setParameters(self, RA,M,O):
        self.RA = RA
        self.M = M
        self.O = O
        self.uuid = 'SOSAIOT-TC-56412'
        self.description = show_testcase_info(TESTPLAN, '1512423', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512423')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_01_01_config_dhcpserver_ra_mo(self):
        if not self.M and self.O:
            LPackageMonitObj.clear_packets()
            LPackageMonitObj.start_capture()
        else:
            logger.info('--not need start packet--')
        ref = copy.deepcopy(Rx1_ipv6)
        ref['router_adv'] = self.RA
        ref['managed'] = self.M
        ref['other_config'] =self.O
        rc = Rinterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config  failed")

    def test_01_02_check_packet(self):
        if not self.M and self.O:
            msg = Rinterface_ipv6.get_interface_address(name = 'x1')
            msg = msg['ip_address'].split(',')
            mac = msg[1].replace(' ','').split('/')[0]
            LPackageMonitObj.stop_capture()
            res = LPackageMonitObj.export_captured_packets()
            #LPackageMonitObj.export_captured_packets_pcapng()
            # res2 = PC1.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
            logger.info(f'-------{res}')
            res = (res.split("Packet number:"))[1:]
            rc = False
            for i in res:
                if mac  in i and 'ICMPV6' in i :
                    rc = True
                    break
            Assertion.assert_equal(rc, True, "ERR: check packet  failed")
        else:
            logger.info('--not need check packet--')
        
    @repeat_method(3)
    def test_01_03_get_x1_ipv6(self):
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc3 = True
            else:
                rc3 = False
        "when add manual mode, the M value is restricted to not get ip"
        if self.RA and not self.M:
            Assertion.assert_equal(rc and (not rc3), True, f"ERR: get x1 dhcpv6 ip failed")
        else:
            Assertion.assert_equal(rc and rc3, True, f"ERR: get x1 dhcpv6 ip failed")

    
class Test_IPv6_DHCP_02(Test):
    uuid = "SOSAIOT-TC-56414"
    description = show_testcase_info(TESTPLAN, '1512425', description=True)['title']

    def test_02_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512425')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_02_01_config_LB_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb)
        Assertion.assert_equal(rc, True, f"ERR: config LB group failed")
    
    def test_02_01_config_dhcpserver_ra_mo(self):
        rc = Rinterface_ipv6.config_interface_ipv6(**Rx1_ipv6)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config failed") 

    @repeat_method(3)
    def test_02_03_get_x1_ipv6(self):
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc &= True
            else:
                rc &= False
            Assertion.assert_equal(rc, True, f"ERR: get x1 dhcpv6 ip failed")

    def test_02_04_retore_env(self):
        ref = copy.deepcopy(lb)
        ref['failover_lb']['group'][0]['interface'][0]['name']='X1'
        ref['failover_lb']['group'][0]['interface'][1]['name']='X2'
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, f"ERR: config LB group failed")


@paramunittest.parametrized(
    {"RA":True,'M':True,'O':True},
    {"RA":True,'M':True,'O':False},
    {"RA":False,'M':False,'O':False},
    {"RA":True,'M':False,'O':True},
    {"RA":True,'M':False,'O':False},
    
)
class Test_IPv6_DHCP_03(Test):
    def setParameters(self, RA,M,O):
        self.RA = RA
        self.M = M
        self.O = O
        self.uuid = 'SOSAIOT-TC-56415'
        self.description = show_testcase_info(TESTPLAN, '1512426', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512423')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_03_01_config_dhcpserver_ra_mo(self):
        if not self.M and self.O:
            LPackageMonitObj.clear_packets()
            LPackageMonitObj.start_capture()
        else:
            logger.info('--not need start packet--')
        ref = copy.deepcopy(Rx1_ipv6)
        ref['router_adv'] = self.RA
        ref['managed'] = self.M
        ref['other_config'] =self.O
        rc = Rinterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config  failed")

    def test_03_02_check_packet(self):
        if not self.M and self.O:
            msg = Rinterface_ipv6.get_interface_address(name = 'x1')
            msg = msg['ip_address'].split(',')
            mac = msg[1].replace(' ','').split('/')[0]
            LPackageMonitObj.stop_capture()
            res = LPackageMonitObj.export_captured_packets()
            res = (res.split("Packet number:"))[1:]
            rc = False
            for i in res:
                if mac  in i and 'ICMPV6' in i :
                    rc = True
                    break
            Assertion.assert_equal(rc, True, "ERR: check packet  failed")
        else:
            logger.info('--not need check packet--')
        
    @repeat_method(3)
    def test_03_03_get_x1_ipv6(self):
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc3 = True
            else:
                rc3 = False
        "when add manual mode, the M value is restricted to not get ip"
        if self.RA and not self.M:
            Assertion.assert_equal(rc and (not rc3), True, f"ERR: get x1 dhcpv6 ip failed")
        else:
            Assertion.assert_equal(rc and rc3, True, f"ERR: get x1 dhcpv6 ip failed")


class Test_IPv6_DHCP_04(Test):
    uuid = 'NonTC'

    def test_04_01_config_LB_group(self):
        ref = copy.deepcopy(lb)
        ref['failover_lb']['group'][0]['interface'][1]['name']='X2'
        ref['failover_lb']['group'][0]['interface'][1]['rank']=1
        ref['failover_lb']['group'][0]['interface'].pop(0)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        rc &= failover_obj.config_failover_groups_by_multi(**lb_ipv4)
        Assertion.assert_equal(rc, True, f"ERR: config LB group failed")

    def test_04_02_add_custom_zone(self):
        rc = Lzone_obj.add_zone_object(**zone_dict)
        Assertion.assert_equal(rc, True, f"ERR: add zone failed")


@paramunittest.parametrized(
    {"RA":True,'M':True,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':True,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":False,'M':False,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    
    {"RA":True,'M':True,'O':True,"Zone":"DMZ",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':True,'O':False,"Zone":"DMZ",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":False,'M':False,'O':False,"Zone":"DMZ",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':True,"Zone":"DMZ",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':False,"Zone":"DMZ",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    
    {"RA":True,'M':True,'O':True,"Zone":"test",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':True,'O':False,"Zone":"test",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":False,'M':False,'O':False,"Zone":"test",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':True,"Zone":"test",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    {"RA":True,'M':False,'O':False,"Zone":"test",'Stateless':False,'ListenRA':True,'rapid_commit':False,"uuid":'SOSAIOT-TC-56416'},
    
    {"RA":True,'M':True,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56419'},
    {"RA":True,'M':True,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56419'},
    {"RA":False,'M':False,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56419'},
    {"RA":True,'M':False,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56419'},
    {"RA":True,'M':False,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56419'},
    
    {"RA":True,'M':True,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56417'},
    {"RA":True,'M':True,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56417'},
    {"RA":False,'M':False,'O':False,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56417'},
    {"RA":True,'M':False,'O':True,"Zone":"LAN",'Stateless':False,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56417'},
    
    {"RA":True,'M':True,'O':False,"Zone":"LAN",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    {"RA":False,'M':False,'O':False,"Zone":"LAN",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    {"RA":True,'M':False,'O':True,"Zone":"LAN",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    
    {"RA":True,'M':True,'O':False,"Zone":"DMZ",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    {"RA":False,'M':False,'O':False,"Zone":"DMZ",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    {"RA":True,'M':False,'O':True,"Zone":"DMZ",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56418'},
    
    {"RA":True,'M':True,'O':False,"Zone":"test",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56423'},
    {"RA":False,'M':False,'O':False,"Zone":"test",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56423'},
    {"RA":True,'M':False,'O':True,"Zone":"test",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56423'},
    
    {"RA":True,'M':True,'O':True,"Zone":"LAN",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56432'},
    {"RA":True,'M':True,'O':True,"Zone":"DMZ",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56432'},
    {"RA":True,'M':True,'O':True,"Zone":"test",'Stateless':True,'ListenRA':True,'rapid_commit':True,"uuid":'SOSAIOT-TC-56432'},
)
class Test_IPv6_DHCP_05(Test):
    
    def setParameters(self, RA,M,O,Zone,Stateless,ListenRA,rapid_commit,uuid):
        self.RA = RA
        self.M = M
        self.O = O
        self.zone = Zone
        self.stateless = Stateless
        self.listenRA = ListenRA
        self.rapid_commit = rapid_commit
        self.uuid = uuid
        self.description = show_testcase_info(TESTPLAN, self.uuid, description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 

    def test_05_01_config_x1_zone(self):
        ref = copy.deepcopy(Lx1_ipv6)
        ref['zone'] = self.zone
        ref['stateless_address_autoconfig']=self.stateless
        ref['listen_router_advertisement'] = self.listenRA
        ref['dhcpv6']['rapid_commit'] = self.rapid_commit
        dict = {
            'if': 'x1',
            'zone': self.zone,
            'mode': 'static',
            'ip': DUT_X1,
            'mgmt_https': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'mgmt_ssh': True,
        } 
        rc = Linterface.config_interface(**dict)
        rc &= Linterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, 'config x1  zone Failed.')
    
    def test_05_02_config_dhcpserver_ra_mo(self):
        if not self.M and self.O:
            LPackageMonitObj.clear_packets()
            LPackageMonitObj.start_capture()
        else:
            logger.info('--not need start packet--')
        ref = copy.deepcopy(Rx1_ipv6)
        ref['router_adv'] = self.RA
        ref['managed'] = self.M
        ref['other_config'] =self.O
        rc = Rinterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config  failed")

    def test_05_03_check_packet(self):
        if not self.M and self.O:
            msg = Rinterface_ipv6.get_interface_address(name = 'x1')
            msg = msg['ip_address'].split(',')
            mac = msg[1].replace(' ','').split('/')[0]
            LPackageMonitObj.stop_capture()
            res = LPackageMonitObj.export_captured_packets()
            res = (res.split("Packet number:"))[1:]
            rc = False
            for i in res:
                if mac  in i and 'ICMPV6' in i :
                    rc = True
                    break
            Assertion.assert_equal(rc, True, "ERR: check packet  failed")
        else:
            logger.info('--not need check packet--')
        
    @repeat_method(3)
    def test_05_04_get_x1_ipv6(self):
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc3 = True
            else:
                rc3 = False
        "when add manual mode, the M value is restricted to not get ip"
        if self.RA and not self.M:
            Assertion.assert_equal(rc and (not rc3), True, f"ERR: get x1 dhcpv6 ip failed")
        else:
            Assertion.assert_equal(rc and rc3, True, f"ERR: get x1 dhcpv6 ip failed")



class Test_IPv6_DHCP_06(Test):
    uuid = 'NonTC'

    def test_06_01_config_Lx1(self):
        ref = copy.deepcopy(Lx1_ipv6)
        ref['stateless_address_autoconfig']=True
        rc = Linterface.config_interface(**Lx1_ipv4)
        rc &= Linterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, 'config x1  Failed.')

    def test_06_02_config_LB_group(self):
        ref = copy.deepcopy(lb)
        ref['failover_lb']['group'][0]['interface'][1]['name']='X1'
        ref['failover_lb']['group'][0]['interface'][1]['rank']=1
        ref['failover_lb']['group'][0]['interface'].pop(0)
        rc = failover_obj.config_failover_groups_by_multi(**ref)
        Assertion.assert_equal(rc, True, f"ERR: config LB group failed")


@paramunittest.parametrized(
    {"RA":True,'M':True,'O':False},
    {"RA":False,'M':False,'O':False},
    {"RA":True,'M':False,'O':True},
    {"RA":True,'M':False,'O':False},
    {"RA":True,'M':True,'O':True},
)
class Test_IPv6_DHCP_07(Test):
    
    def setParameters(self, RA,M,O):
        self.RA = RA
        self.M = M
        self.O = O
        self.uuid = 'SOSAIOT-TC-56423'
        self.description = show_testcase_info(TESTPLAN, '1512434', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512423')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  
    
    def test_07_01_config_dhcpserver_ra_mo(self):
        if not self.M and self.O:
            LPackageMonitObj.clear_packets()
            LPackageMonitObj.start_capture()
        else:
            logger.info('--not need start packet--')
        ref = copy.deepcopy(Rx1_ipv6)
        ref['router_adv'] = self.RA
        ref['managed'] = self.M
        ref['other_config'] =self.O
        rc = Rinterface_ipv6.config_interface_ipv6(**ref)
        Assertion.assert_equal(rc, True, "ERR: config dhcp server x1 ipv6 ra managed and other-config  failed")

    def test_07_02_check_packet(self):
        if not self.M and self.O:
            msg = Rinterface_ipv6.get_interface_address(name = 'x1')
            msg = msg['ip_address'].split(',')
            mac = msg[1].replace(' ','').split('/')[0]
            LPackageMonitObj.stop_capture()
            res = LPackageMonitObj.export_captured_packets()
            res = (res.split("Packet number:"))[1:]
            rc = False
            for i in res:
                if mac  in i and 'ICMPV6' in i :
                    rc = True
                    break
            Assertion.assert_equal(rc, True, "ERR: check packet  failed")
        else:
            logger.info('--not need check packet--')
        
    @repeat_method(3)
    def test_07_03_get_x1_ipv6(self):
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc3 = True
            else:
                rc3 = False
        "when add manual mode, the M value is restricted to not get ip"
        if self.RA and not self.M:
            Assertion.assert_equal(rc and (not rc3), True, f"ERR: get x1 dhcpv6 ip failed")
        else:
            Assertion.assert_equal(rc and rc3, True, f"ERR: get x1 dhcpv6 ip failed")


class Test_IPv6_DHCP_08(Test):
    uuid = "SOSAIOT-TC-56431"
    description = show_testcase_info(TESTPLAN, '1512443', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512443')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    @repeat_method(3)
    def test_08_01_get_ip_and_check_packet(self):
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc3 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc3[0]:
            logger.info('unstable renew')
            logger.info(rc3[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc &= True
            else:
                rc &= False
            LPackageMonitObj.stop_capture()
            res = LPackageMonitObj.export_captured_packets()
            res = (res.split("Packet number:"))[1:]
            logger.info(f'-------{res}')
            rc2 = False
            for i in res:
                if 'in:X1'  in i and 'Received' in i :
                    rc2 = True
                    break
            Assertion.assert_equal(rc&rc2, True, "ERR: check packet  failed")


class Test_IPv6_DHCP_09(Test):
    uuid = "SOSAIOT-TC-56439"
    description = show_testcase_info(TESTPLAN, '1512454', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512454')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    def test_09_01_config_x1_dhcpv6(self):
        rc = Linterface_ipv6.config_interface_ipv6(**Lx1_ipv6)
        Assertion.assert_equal(rc, True, 'config x1  Failed.')

    def test_09_02_restar_and_check_x1(self):
        rc = Lrestart.restart_now()
        res = Linterface_ipv6.get_ipv6_interface_base(name = 'x1')
        logger.info(f'------{res}')
        if res["interfaces"][0]['ipv6']['ip_assignment']['mode']['dhcpv6']['rapid_commit'] and res["interfaces"][0]['ipv6']['listen_router_advertisement'] \
            and not res["interfaces"][0]['ipv6']['stateless_address_autoconfig']:
            rc &= True
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: restart dut and check x1 failed")


class Test_IPv6_DHCP_10(Test):
    uuid = "SOSAIOT-TC-56441"
    description = show_testcase_info(TESTPLAN, '1512456', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512456')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")  

    @repeat_method(3)
    def test_10_01_get_x1_ip(self):
        LPackageMonitObj.clear_packets()
        LPackageMonitObj.start_capture()
        rc = Linterface.click_dhcp_release(name = 'X1',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = 'X1',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(5)
            res = Linterface_ipv6.get_interface_address(name = 'x1')
            logger.info(f'------{res}')
            if "2023::" in res["ip_address"] :
                rc &= True
            else:
                rc &= False
            Assertion.assert_equal(rc, True, f"ERR: get x1 dhcpv6 ip failed")

    def test_10_02_check_packet(self):
        LPackageMonitObj.stop_capture()
        LPackageMonitObj.export_captured_packets_pcapng()
        res = PC1.send_commands(['tshark -V -r /tmp/packet-c.pcapng'])
        logger.info(f'-------{res}')
        if 'Rapid Commit'  in res :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check packet  failed")


class Test_IPv6_DHCP_11(Test):
    uuid = "SOSAIOT-TC-56430"
    description = show_testcase_info(TESTPLAN, '1512442', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1512442')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed") 

    def test_11_01_add_dhcp_scope(self):
        rc = Rdhcp_obj.add_dhcp_server_scope_dynamic(**dhcp_scope_dyn_v6_x3)
        Assertion.assert_equal(rc, True, "ERR: add dhcp scope  failed")

    def test_11_02_unassign_Lx1_ipv6(self):
        rc = Linterface_ipv6.unassign_ipv6_interface(interface='X1')
        Assertion.assert_equal(rc, True, "ERR: config unassign Lx1  failed")

    def test_11_03_config_Rx3_ipv6(self):
        rc = Rinterface.config_interface(**Rx3_ipv4)
        rc &= Rinterface_ipv6.config_interface_ipv6(**Rx3_ipv6)
        time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: config  Rx3 ipv6  failed")

    @repeat_method(3)
    def test_11_04_config_Lx2_vlan(self):
        logger.info('--------config Lx2 vlan-----------')
        rc = Linterface.add_interface(**Lx2_vlan)
        rc &= Linterface_ipv6.config_interface_ipv6(**Lx2_vlan_ipv6)
        rc &= Rdhcp_obj.edit_dhcp_server_scope_v6(scope='dynamic',name ='dyn_ipv6',**dhcp_scope_dyn_v6_x3_modify)
        logger.info('--------get_vlan_interface_ip-----------')
        rc &= Linterface.click_dhcp_release(name = f'X2:V{vlan_tag}',version = 'v6')
        rc2 = Linterface.click_dhcp_renew(name = f'X2:V{vlan_tag}',version = 'v6',msg=True)
        if not rc2[0]:
            logger.info('unstable renew')
            logger.info(rc2[1])
        else:
            time.sleep(15)
            res = Linterface.get_interface_address(f'X2:V{vlan_tag}',version='v6')
            _,res = fw_cli.do_cli_commands(commands=show_ips,tag = 1)
            logger.info(f'------{res}')
            if "2024::" in res:
                rc &= True
            else:
                rc &= False
            logger.info('--------restore_env-----------')
            rc &= Linterface.del_interface(**Lx2_vlan)
            Assertion.assert_equal(rc, True, "ERR: restore env failed")


class Test_IPv6_DHCP_12(Test):
    uuid = 'NonTC'

    def test_12_00_restore_remote_dut(self):
        logger.info('Restore Remote FW...')
        path = cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device={} -if=X2 -zone=WAN -ip=12.12.2.201 -restore=1'.format(path, Params.testbed, rm_device)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)
        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(DHCPV6_X2)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote is unreachable.')
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")




    

