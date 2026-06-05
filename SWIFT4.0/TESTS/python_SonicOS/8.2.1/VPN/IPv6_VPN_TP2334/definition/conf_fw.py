from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    @repeat_method(3)
    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        rc &= interfacev4api.config_interface(**x2_static)
        res1= interfacev4api.add_interface(msg = True,**x3_vlan)
        rc &= interfacev6api.config_interface_ipv6(**x0_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x1_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x2_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x3_ipv6)
        rc &= Rinterfacev6api.config_interface_ipv6(**r_x0_ipv6)
        rc &= Rinterfacev6api.config_interface_ipv6(**r_x1_ipv6)
        rc &= Rinterfacev6api.config_interface_ipv6(**r_x2_ipv6)
        rc &= Rinterfacev4api.config_interface(**r_x4_static)
        rc &= Rinterfacev6api.config_interface_ipv6(**r_x4_ipv6)
        rc &= Rinterfacev4api.config_interface(**r_x0_static)
        rc &= Rinterfacev4api.config_interface(**r_x2_static)
        res2= Rinterfacev4api.add_interface(msg=True,**r_x3_vlan)
        rc &= Rinterfacev6api.config_interface_ipv6(**r_x3_ipv6)
        pattern = r'already exists'
        if (res1[0] or re.search(pattern, str(res1[1]), re.IGNORECASE)) and (res2[0] or re.search(pattern, str(res2[1]), re.IGNORECASE)):
            rc &= True
            logger.info("add vlan x3 success.")
        else:
            rc &= False
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    # @repeat_method(5)
    # def test_02_register_fw(self):
    #     logger.info(" {} ".center(20, '-').format('Register firewall'))
    #     time.sleep(10)
    #     rc = license_obj.register("online")
    #     Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_03_add_nat_policy(self):
        rc = nat_obj.add_nat_policy(**nat_policy1)
        rc &= Rnat_obj.add_nat_policy(**nat_policy1)
        Assertion.assert_equal(rc, True, "ERR: config nat policy failed")

    def test_04_add_addObj(self):
        logger.info('-'*10+'Add remote AddObj for DUT and Remote DUT'+'-'*10)
        logger.info('-'*10+'Add remote AddObj for DUT '+'-'*10)
        res1 = LAddrOBJ.config_addressobject(msg=True,**local_r)
        res3 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_r_ipv6)
        res5 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_test_ipv6)
        res6 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_l_host)
        res7 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_r_host)
        res10 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_l_x0)
        res11 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_r_x4)
        res16 = LAddrOBJ.config_ipv6_addressobject(msg=True,**local_r_net)
        logger.info('-'*10+'Add remote AddObj for Remote DUT'+'-'*10)
        res2 = RAddrOBJ.config_addressobject(msg=True,**remote_r)
        res4 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_r_ipv6)
        res8 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_l_host)
        res9 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_r_host)
        res12 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_l_x0)
        res13 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_l_x4)
        res17 = RAddrOBJ.config_ipv6_addressobject(msg=True,**remote_l_net)
        res14 = Laddrgroup.add_addressgroup(msg=True,**local_r_group)
        res15 = Raddrgroup.add_addressgroup(msg=True,**remote_l_group)
        logger.info(f'----------{res1}------{res2}---{res3}-------{res4}-----')
        
        pattern = r'already exists'
        if (res1[0] or re.search(pattern, str(res1[1]), re.IGNORECASE) ) and (res2[0] or re.search(pattern, str(res2[1]), re.IGNORECASE)) \
            and (res3[0] or re.search(pattern, str(res3[1]), re.IGNORECASE)) and (res4[0] or re.search(pattern, str(res4[1]), re.IGNORECASE)) \
            and (res5[0] or re.search(pattern, str(res5[1]), re.IGNORECASE))  and (res6[0] or re.search(pattern, str(res6[1]), re.IGNORECASE)) \
            and (res7[0] or re.search(pattern, str(res7[1]), re.IGNORECASE)) and (res8[0] or re.search(pattern, str(res8[1]), re.IGNORECASE)) \
            and (res9[0] or re.search(pattern, str(res9[1]), re.IGNORECASE)) and (res10[0] or re.search(pattern, str(res10[1]), re.IGNORECASE)) \
            and (res11[0] or re.search(pattern, str(res11[1]), re.IGNORECASE)) and (res12[0] or re.search(pattern, str(res12[1]), re.IGNORECASE)) \
            and (res13[0] or re.search(pattern, str(res13[1]), re.IGNORECASE)) and (res14[0] or re.search(pattern, str(res14[1]), re.IGNORECASE)) \
            and (res15[0] or re.search(pattern, str(res15[1]), re.IGNORECASE)) and (res16[0] or re.search(pattern, str(res16[1]), re.IGNORECASE)) \
            and (res17[0] or re.search(pattern, str(res17[1]), re.IGNORECASE)) :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, 'Add local and remote AddObj for DUT  Failed.')

    def test_06_add_acl(self):
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
        rule3 = copy.deepcopy(rule_opt)
        rule4 = copy.deepcopy(rule_opt)
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
        rule3['name'] = 'VPN_to_LAN_ipv6'
        rule3['from'] = 'VPN'
        rule3['to']   = 'LAN'
        rule4['name'] = 'LAN_to_VPN_ipv6'
        rule4['from'] = 'LAN'
        rule4['to']   = 'VPN'
        res1 = Laccess_rule_obj.config_accessrule(msg=True,**rule1)
        res2 = Laccess_rule_obj.config_accessrule(msg=True,**rule2)
        res3 = Laccess_rule_obj.config_accessrule(msg=True,url="/access-rules/ipv6",**rule3)
        res4 = Laccess_rule_obj.config_accessrule(msg=True,url="/access-rules/ipv6",**rule4)
        res5 = Raccess_rule_obj.config_accessrule(msg=True,url="/access-rules/ipv6",**rule3)
        res6 = Raccess_rule_obj.config_accessrule(msg=True,url="/access-rules/ipv6",**rule4)
        pattern = r'already exists'
        if (res1[0] or re.search(pattern, str(res1[1]), re.IGNORECASE) ) and (res2[0] or re.search(pattern, str(res2[1]), re.IGNORECASE) )\
            and (res3[0] or re.search(pattern, str(res3[1]), re.IGNORECASE) ) and (res4[0] or re.search(pattern, str(res4[1]), re.IGNORECASE) ) \
            and (res5[0] or re.search(pattern, str(res5[1]), re.IGNORECASE) ) and (res6[0] or re.search(pattern, str(res6[1]), re.IGNORECASE) ):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN in DUT2 failed")

    def test_07_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out = PC1.send_commands([f'ping6 -c 3 {Remote_X1_IPV6}'])
            if '100% packet loss' not in out:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")



class TestConfigNETENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_00_add_route(self):
        logger.info('-'*10+'add route'+'-'*10)
        out1 = PC1.send_commands(pc1_route_cmds)
        out2 = PC2.send_commands(pc2_route_cmds)
        out3 = PC3.send_commands(pc3_route_cmds)
        if DUT_X1_NET_IPV6 in out1 and DUT_X2_NET_IPV6 in out1 and DUT_X3_NET_IPV6 in out1 and Remote_X4_NET_IPV6 in out1 and\
            Remote_X0_NET_IPV6 in out1 and  DUT_X1_NET_IPV4 in out1 and DUT_X2_NET_IPV4 in out1 and \
            Remote_X0_NET_IPV4 in out1 and DUT_X1_NET_IPV6 in out2 and DUT_X2_NET_IPV6 in out2 and DUT_X3_NET_IPV6 in out2\
             and DUT_X0_NET_IPV6 in out2 and DUT_X1_NET_IPV4 in out2 and DUT_X2_NET_IPV4 in out2\
             and DUT_X0_NET_IPV4 in out2 and DUT_X1_NET_IPV6 in out3 and DUT_X2_NET_IPV6 in out3 \
             and DUT_X0_NET_IPV6 in out3:
            rc = True
        else:
            rc = False
            logger.error(out1)
            logger.error(out2)
            logger.error(out3)
        Assertion.assert_equal(rc, True, 'add route Failed.')