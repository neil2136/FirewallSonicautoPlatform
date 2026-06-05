from definition.settings import *


class TestConfigENV(Test):
    uuid = 'NonTC'
    goto_teardown = True

    def test_01_Config_Interface(self):
        rc = interfacev4api.config_interface(**x1_static)
        rc &= interfacev4api.config_interface(**x2_static)
        rc &= interfacev4api.add_interface(**x3_vlan)
        rc &= interfacev6api.config_interface_ipv6(**x0_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x1_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x2_ipv6)
        rc &= interfacev6api.config_interface_ipv6(**x3_ipv6)
        Assertion.assert_equal(rc, True, "ERR: Config Interface  failed")    

    @repeat_method(5)
    def test_02_register_fw(self):
        logger.info(" {} ".center(20, '-').format('Register firewall'))
        time.sleep(10)
        rc = license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")


    def test_03_config_LB_group(self):
        rc = failover_obj.config_failover_groups_by_multi(**lb_ipv4)
        Assertion.assert_equal(rc, True, "ERR: config LB group failed")

    def test_04_add_route(self):
        res1 = PC1.send_commands(pc1_route_cmds)
        res4 = PC_Server.send_commands(pc_server_route_cmds)
        if DUT_X1_NET_IPV6 in res1 and DUT_X2_NET_IPV6 in res1 and PC_Server_NET_IPV6 in res1 and \
             DUT_X1_NET_IPV6 in res4 and DUT_X2_NET_IPV6 in res4 :
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add route failed")

    def test_05_config_ipv6_forwarding_for_pc2_pc3(self):
        res1 = PC2.send_commands(forward_cmds)
        res2 = PC3.send_commands(forward_cmds)
        if 'net.ipv6.conf.all.forwarding = 1' in res1 and 'net.ipv6.conf.all.forwarding = 1' in res2:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: config pc ipv6 forwarding failed")

    def test_06_add_nat_policy(self):
        ref = copy.deepcopy(nat_policy1)
        ref['nat_policies'][0]['ipv6']['name'] = 'test2'
        ref['nat_policies'][0]['ipv6']['outbound'] = 'X2'
        ref['nat_policies'][0]['ipv6']['translated_source']['name'] = 'X2 IPv6 Primary Static Address'
        rc = nat_obj.add_nat_policy(**nat_policy1)
        rc &= nat_obj.add_nat_policy(**ref)
        Assertion.assert_equal(rc, True, "ERR: config nat policy failed")

    def test_07_check_traffic(self):
        rc = False
        for i in range(9):
            time.sleep(8)
            out = PC1.send_commands(traffic_cmd)
            if '100% packet loss' not in out:
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: check traffic failed")

