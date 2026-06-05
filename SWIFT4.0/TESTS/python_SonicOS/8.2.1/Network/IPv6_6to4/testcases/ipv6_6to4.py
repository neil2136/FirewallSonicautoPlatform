from settings import *


class Test_05_Check_name(Test):
    uuid = "SOSAIOT-TC-56370"
    description= show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_05_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        ret = interface_v6.get_tunnel_interface(name='manual')
        rc &= interface_v6.delete_tunnel_interface(name='manual')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['name'], manual['name'], "ERR: verify manual tunnel interface.")


    def test_05_02_add_gre_tunnel(self):
        gre = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        ret = interface_v6.get_tunnel_interface(name='gre')
        rc &= interface_v6.delete_tunnel_interface(name='gre')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['name'], gre['name'], "ERR: verify gre tunnel interface.")

    def test_05_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        ret = interface_v6.get_tunnel_interface(name='6to4')
        rc &= interface_v6.delete_tunnel_interface(name='6to4')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['name'], tunnel_6to4['name'], "ERR: verify 6to4 tunnel interface.")


class Test_06_Check_comment(Test):
    uuid = "SOSAIOT-TC-56371"
    description= show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']

    def test_06_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_06_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'manual',
            'zone': 'WAN',
            'type': 'manual',
            'comment': 'TC6-gif',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        ret = interface_v6.get_tunnel_interface(name='manual')
        rc &= interface_v6.delete_tunnel_interface(name='manual')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['comment'], manual['comment'], "ERR: verify manual tunnel interface.")


    def test_06_02_add_gre_tunnel(self):
        gre = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'comment': 'TC6-gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        ret = interface_v6.get_tunnel_interface(name='gre')
        rc &= interface_v6.delete_tunnel_interface(name='gre')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['comment'], gre['comment'], "ERR: verify gre tunnel interface.")

    def test_06_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'comment': 'TC6-6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        ret = interface_v6.get_tunnel_interface(name='6to4')
        rc &= interface_v6.delete_tunnel_interface(name='6to4')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['comment'],tunnel_6to4['comment'], "ERR: verify 6to4 tunnel interface.")


class Test_07_Check_interface(Test):
    uuid = "SOSAIOT-TC-56372"
    description= show_testcase_info(Parameter.TESTPLAN, '7', description=True)['title']

    def test_07_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_07_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        ret = interface_v6.get_tunnel_interface(name='manual')
        rc &= interface_v6.delete_tunnel_interface(name='manual')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['zone'], manual['zone'], "ERR: verify manual tunnel interface.")

    def test_07_02_add_gre_tunnel(self):
        gre = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        ret = interface_v6.get_tunnel_interface(name='gre')
        rc &= interface_v6.delete_tunnel_interface(name='gre')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['zone'], gre['zone'], "ERR: verify gre tunnel interface.")

    def test_07_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        ret = interface_v6.get_tunnel_interface(name='6to4')
        rc &= interface_v6.delete_tunnel_interface(name='6to4')
        logger.info(ret)
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
        Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['zone'], tunnel_6to4['zone'], "ERR: verify 6to4 tunnel interface.")


class Test_08_Check_failover(Test):
    uuid = "SOSAIOT-TC-56373"
    description= show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_08_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'TC8',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        ret = failover.config_failover_groups_by_multi(**lb)
        rc &= interface_v6.delete_tunnel_interface(name='TC8')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret,False,  "ERR: verify manual tunnel interface.")        

    def test_08_02_add_gre_tunnel(self):
        gre = {
            'name': 'TC8',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        ret = failover.config_failover_groups_by_multi(**lb)
        rc &= interface_v6.delete_tunnel_interface(name='TC8')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")
        Assertion.assert_equal(ret,False, "ERR: verify gre tunnel interface.")        

    def test_08_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': 'TC8',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        ret = failover.config_failover_groups_by_multi(**lb)
        rc &= interface_v6.delete_tunnel_interface(name='TC8')
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
        Assertion.assert_equal(ret,False, "ERR: verify 6to4 tunnel interface.")        


class Test_09_Delete_Tunnel(Test):
    uuid = "SOSAIOT-TC-56374"
    description= show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_09_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        rc &= interface_v6.delete_tunnel_interface(name='manual')
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")

    def test_09_02_add_gre_tunnel(self):
        gre = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        rc &= interface_v6.delete_tunnel_interface(name='gre')
        Assertion.assert_equal(rc, True, "ERR: Add gre tunnel interface.")

    def test_09_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        rc &= interface_v6.delete_tunnel_interface(name='6to4')
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")


class Test_10_Edit_tunnel(Test):
    uuid = "SOSAIOT-TC-56351"
    description= show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_10_01_add_GIF_tunnel_interface(self):
        manual = {
            'name': 'manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
            'comment' : 'original',
        }
        logger.info('Add manual tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**manual)
        manual['name'] = 'manual-new'
        logger.info(f"change name to {manual['name']}")
        rc &= interface_v6.edit_tunnel_interface(**manual,tunnel_name='manual')
        manual['comment'] = 'new'
        logger.info(f"change commnet to {manual['comment']}")
        rc &= interface_v6.edit_tunnel_interface(**manual,tunnel_name=manual['name'])
        logger.info(f"change ipv4 and ipv6 address")
        manual['ipv4_address'] = {'name': Parameter.REMOTE_X2}
        manual['ipv6_address'] = {'name': Parameter.REMOTE_X0_IPv6_Network['6to4']}
        rc &= interface_v6.edit_tunnel_interface(**manual,tunnel_name=manual['name'])
        rc &= interface_v6.delete_tunnel_interface(name=manual['name'])
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")

    def test_10_02_add_gre_tunnel(self):
        gre = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
            'comment': 'original',
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre)
        gre['name'] = 'gre-new'
        logger.info(f"change name to {gre['name']}")
        rc &= interface_v6.edit_tunnel_interface(**gre,tunnel_name='gre',)
        gre['comment'] = 'new'
        logger.info(f"change commnet to {gre['comment']}")
        rc &= interface_v6.edit_tunnel_interface(**gre,tunnel_name=gre['name'])
        logger.info(f"change ipv4 and ipv6 address")
        gre['ipv4_address'] = {'name': Parameter.REMOTE_X2}
        gre['ipv6_address'] = {'name': Parameter.REMOTE_X0_IPv6_Network['6to4']}
        rc &= interface_v6.edit_tunnel_interface(**gre,tunnel_name=gre['name'])
        rc &= interface_v6.delete_tunnel_interface(name=gre['name'])
        Assertion.assert_equal(rc, True, "ERR: Add gre tunnel interface.")

    def test_10_03_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add tunnel_6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        tunnel_6to4['name'] = 'manual-new'
        logger.info(f"change name to {tunnel_6to4['name']}")
        rc &= interface_v6.edit_tunnel_interface(**tunnel_6to4, tunnel_name='6to4')
        tunnel_6to4['comment'] = 'new'
        logger.info(f"change commnet to {tunnel_6to4['comment']}")
        rc &= interface_v6.edit_tunnel_interface(**tunnel_6to4,tunnel_name=tunnel_6to4['name'])
        rc &= interface_v6.delete_tunnel_interface(name=tunnel_6to4['name'])
        Assertion.assert_equal(rc, True, "ERR: Add manual tunnel interface.")

class Test_11_Verify_Remote_IPv4_Address(Test):
    uuid = "SOSAIOT-TC-56375"
    description= show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_11_01_add_manual_tunnel(self):
        tunnel = {
            'name': 'TC11_manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }        
        rc = interface_v6.add_tunnel_interface(**tunnel)
        Assertion.assert_equal(rc, False, "ERR: should not add tunnel with non ipv4 address.")

    def test_11_02_add_manual_tunnel(self):
        tunnel = {
            'name': 'TC11_gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X0_IPv6_Network['gre']},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['gre']},
            'bound_to': {'interface':"X1"},# or any
        }        
        rc = interface_v6.add_tunnel_interface(**tunnel)
        Assertion.assert_equal(rc, False, "ERR: should not add tunnel with non ipv4 address.")


# class Test_12_Verify_Mcast_Bcast(Test):
#     uuid = '1512354'
#     description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

#     def test_12_00_show_testcase_info(self):
#         show_testcase_info(Parameter.TESTPLAN, '12')
#         Assertion.assert_equal(True, True, "ERR: show testcae info failed")

#     def test_12_01_add_manual_tunnel(self):
#         tunnel = {
#             'name': 'TC12_manual',
#             'zone': 'WAN',
#             'type': 'manual',
#             'ip': Parameter.TUNNEL_IP,
#             'prefix_length': 64,
#             'ipv4_address':{'name': Parameter.MCAST_V4},
#             'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
#             'bound_to': {'interface':"X1"},# or any
#         }        
#         rc = interface_v6.add_tunnel_interface(**tunnel)
#         tunnel['ipv4_address'] = {'name': Parameter.BCAST_V4}
#         rc |= interface_v6.add_tunnel_interface(**tunnel)
#         Assertion.assert_equal(rc, False, "ERR: should not add tunnel with mcast or bcast address.")

#     def test_12_02_add_manual_tunnel(self):
#         tunnel = {
#             'name': 'TC12_gre',
#             'zone': 'WAN',
#             'type': 'gre',
#             'ip': Parameter.TUNNEL_IP,
#             'prefix_length': 64,
#             'ipv4_address':{'name': Parameter.MCAST_V4},
#             'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['gre']},
#             'bound_to': {'interface':"X1"},# or any
#         }        
#         rc = interface_v6.add_tunnel_interface(**tunnel)
#         tunnel['ipv4_address'] = {'name': Parameter.BCAST_V4}
#         rc |= interface_v6.add_tunnel_interface(**tunnel)
#         Assertion.assert_equal(rc, False, "ERR: should not add tunnel with mcast or bcast address.")


# class Test_13_Verify_Mcast_Bcast(Test):
#     uuid = '1512354'
#     description= show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

#     def test_13_00_show_testcase_info(self):
#         show_testcase_info(Parameter.TESTPLAN, '13')
#         Assertion.assert_equal(True, True, "ERR: show testcae info failed")

#     def test_13_01_add_manual_tunnel(self):
#         tunnel = {
#             'name': 'TC3_manual',
#             'zone': 'WAN',
#             'type': 'manual',
#             'ip': Parameter.TUNNEL_IP,
#             'prefix_length': 64,
#             'ipv4_address':{'name': Parameter.REMOTE_X1},
#             'ipv6_network':{'name': Parameter.LOCAL_V6},
#             'bound_to': {'interface':"X1"},# or any
#         }        
#         rc = interface_v6.add_tunnel_interface(**tunnel)
#         tunnel['ipv6_address'] = {'name': Parameter.BCAST_V6}
#         rc |= interface_v6.add_tunnel_interface(**tunnel)
#         Assertion.assert_equal(rc, False, "ERR: should not add tunnel with ipv6 link-local or bcast address.")

#     def test_13_02_add_manual_tunnel(self):
#         tunnel = {
#             'name': 'TC13_gre',
#             'zone': 'WAN',
#             'type': 'gre',
#             'ip': Parameter.TUNNEL_IP,
#             'prefix_length': 64,
#             'ipv4_address':{'name': Parameter.REMOTE_X1},
#             'ipv6_network':{'name': Parameter.LOCAL_V6},
#             'bound_to': {'interface':"X1"},# or any
#         }        
#         rc = interface_v6.add_tunnel_interface(**tunnel)
#         tunnel['ipv6_address'] = {'name': Parameter.BCAST_V6}
#         rc |= interface_v6.add_tunnel_interface(**tunnel)
#         Assertion.assert_equal(rc, False, "ERR: should not add tunnel with ipv6 link-local or bcast address.")


@paramunittest.parametrized(
    {"tunnel_type": 'gre',"tc_id": "14", 'uuid':'1512356'},
    {"tunnel_type": 'manual',"tc_id":"15", 'uuid':'1512357'},
)

class Test_14_15_Verify_Multi_Tunnel(Test):
    def setParameters(self, tunnel_type, tc_id, uuid):
        '''parameter tunnel_type,tc_id uuid  must be same with the dict above'''
        self.tunnel_type = tunnel_type
        self.tc_id = tc_id
        self.uuid = uuid
        self.description = show_testcase_info(Parameter.TESTPLAN, tc_id, description=True)['title']

    def test_14_15_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tc_id)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_14_15_01_add_aos(self):
        nums = 6 
        rc =True
        for num in range(1,nums):
            ao_v4 ={
                "object_type": "host",
                "name": f"{num}." * 3 + str(num),
                "zone": "WAN",
                "value": f"{num}." * 3 + str(num),
            }
            ao_v6 = {
                'name': str(num) + '::' + str(num),
                'zone': 'WAN',
                'object_type': 'network',
                'subnet': str(num) + '::' + str(num),
                'mask': '/64',
            }
            rc &= ao.config_addressobject(**ao_v4)
            rc &= ao.config_ipv6_addressobject(**ao_v6)            
        Assertion.assert_equal(rc, True, "ERR: Add ao fail.")

    def test_14_15_02_add_tunnel(self):
        nums = 6 
        rc =True
        for num in range(1,nums):
            tunnel = {
                'name': self.tunnel_type + str(num),
                'zone': 'WAN',
                'type': self.tunnel_type,
                'ip': str(num) + ':1' + '::' + str(num),
                'prefix_length': 64,
                'ipv4_address':{'name': f"{num}." * 3 + str(num)},
                'ipv6_network':{'name': str(num) + '::' + str(num)},
                'bound_to': {'interface':"X1"},# or any
            }
            logger.info('Add manual tunnel interface.')
            rc &= interface_v6.add_tunnel_interface(**tunnel)     
        for num in range(1,nums):
            rc &= interface_v6.delete_tunnel_interface(name=self.tunnel_type + str(num))
        Assertion.assert_equal(rc, True, "ERR: Add multi tunnel fail.")

    def test_14_15_04_delete_aos(self):
        nums = 6 
        rc =True
        for num in range(1,nums):
        #     'ip_type': 'ipv6',/'ipv4'
        #     'name': 'test2',
            ao_v4 ={
                'ip_type': 'ipv4',
                "name": f"{num}." * 3 + str(num),
            }
            ao_v6 = {
                'name': str(num) + '::' + str(num),
                'ip_type': 'ipv6',
            }
            rc &= ao.del_addressobject(**ao_v4)
            rc &= ao.del_addressobject(**ao_v6)            
        Assertion.assert_equal(rc, True, "ERR: Delete ao fail.")


class Test_16_Verify_6to4_Multi_Tunnel(Test):
    uuid = "SOSAIOT-TC-56354"
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_16_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_16_01_add_tunnel(self):
        tunnel_6to4_1 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4_1',
            'bound_to': {'interface':"X1"},# or any
            'ip': '2::2',
            'prefix_length': 64,
            'enable': True,
        }
        tunnel_6to4_2 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4_2',
            'bound_to': {'interface':"X2"},# or any
            'ip': '3::3',
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 1st 6to4 tunnel interface.')
        rc1 = interface_v6.add_tunnel_interface(**tunnel_6to4_1)
        logger.info('Add 2nd 6to4 tunnel interface.')
        rc2 = interface_v6.add_tunnel_interface(**tunnel_6to4_2)
        rc1 &= interface_v6.delete_tunnel_interface(name='6to4_1')
        Assertion.assert_equal(rc1, True, "ERR: Add 1st 6to4 tunnel fail.")
        Assertion.assert_not_equal(rc2, True, "ERR: Add 2nd 6to4 tunnel fail.")


class Test_17_Check_interface(Test):
    uuid = "SOSAIOT-TC-56355"
    description= show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_17_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_17_01_add_gre_tunnel(self):
        ao_v4 ={
            "object_type": "host",
            "name": '17.17.17.17',
            "zone": "WAN",
            "value": '17.17.17.17',
        }
        ao_v6 = {
            'name': '17::17',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '17::17',
            'mask': '/64',
        }

        gre1 = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '1::1',
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        gre2 = {
            'name': 'gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '2::2',
            'prefix_length': 64,
            'ipv4_address': {'name': '17.17.17.17'},
            'ipv6_network': {'name': '17::17'},
            'bound_to': {'interface':"X1"},# or any
        }
        rc = ao.config_addressobject(**ao_v4)
        rc &= ao.config_ipv6_addressobject(**ao_v6)        
        logger.info('Add gre tunnel interface.')
        rc &= interface_v6.add_tunnel_interface(**gre1)
        ret = interface_v6.add_tunnel_interface(**gre2)
        rc &= interface_v6.delete_tunnel_interface(name='gre')
        Assertion.assert_equal(rc, True, "ERR: Add gre tunnel interface failed.")
        Assertion.assert_not_equal(ret, True, "ERR: Add identical gre tunnel interface should not be successful.")


class Test_18_Same_IPv6_Network(Test):
    uuid = "SOSAIOT-TC-56356"
    description= show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_18_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_18_01_add_gre_tunnel(self):
        gre1 = {
            'name': 'gre1',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '1::1',
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        gre2 = {
            'name': 'gre2',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '2::2',
            'prefix_length': 64,
            'ipv4_address': {'name': '17.17.17.17'},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
    
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre1)
        rc &= interface_v6.add_tunnel_interface(**gre2)
        rc &= interface_v6.delete_tunnel_interface(name='gre1')
        rc &= interface_v6.delete_tunnel_interface(name='gre2')
        Assertion.assert_equal(rc, True, "ERR: Add same ipv6 network gre tunnel interface failed.")


class Test_19_Same_IPv4_Network(Test):
    uuid = "SOSAIOT-TC-56357"
    description= show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']

    def test_19_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_19_01_add_gre_tunnel(self):
        gre1 = {
            'name': 'gre1',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '1::1',
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        gre2 = {
            'name': 'gre2',
            'zone': 'WAN',
            'type': 'gre',
            'ip': '2::2',
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network': {'name': '17::17'},
            'bound_to': {'interface':"X1"},# or any
        }
    
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**gre1)
        ret = interface_v6.add_tunnel_interface(**gre2)
        rc &= interface_v6.delete_tunnel_interface(name='gre1')
        Assertion.assert_equal(rc, True, "ERR: Add 1st network gre tunnel interface failed.")
        Assertion.assert_not_equal(ret, True, "ERR: Add same ipv4 network gre tunnel interface failed.")

#need add rule manually
# class Test_20_Change_Zone(Test):
#     uuid = '1512362'
#     description= show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

#     def test_20_00_show_testcase_info(self):
#         show_testcase_info(Parameter.TESTPLAN, '20')
#         Assertion.assert_equal(True, True, "ERR: show testcae info failed")

#     def test_20_01_add_6to4_tunnel(self):
#         tunnel_6to4 = {
#             'type': '6to4',
#             'zone': 'WAN',
#             'name': '6to4',
#             'bound_to': {'interface':"X1"},# or any
#             'ip': Parameter.TUNNEL_IP,
#             'prefix_length': 64,
#             'enable': True,
#         }
#         logger.info('Add 6to4 tunnel interface.')
#         rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
#         ret = acl_ipv6.get_accessrule_ipv6()
#         # rc &= interface_v6.delete_tunnel_interface(name='6to4')
#         logger.info(ret)
#         Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
#         Assertion.assert_equal(ret['tunnel_interfaces'][0]['ipv6']['name'], tunnel_6to4['name'], "ERR: verify 6to4 tunnel interface.")

#     def test_20_02_delete_tunnel(self):
#         rc = interface_v6.delete_tunnel_interface(name='6to4')
#         Assertion.assert_equal(rc, True, f"ERR: Delete tunnels failed.")


class Test_21_Check_Route(Test):
    uuid = "SOSAIOT-TC-56358"
    description= show_testcase_info(Parameter.TESTPLAN, '21', description=True)['title']

    def test_21_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_21_01_add_6to4_tunnel(self):
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': '6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'enable': True,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        ret = acl_ipv6.get_accessrule_ipv6()
        routes = route.get_default_route_policy_v6()
        rc &= interface_v6.delete_tunnel_interface(name='6to4')
        ret = False
        for r in routes:
            if r['interface'] == '6to4':
                logger.info('Got auto added route.')
                ret = True
                break
        Assertion.assert_equal(rc, True, "ERR: Add 6to4 tunnel interface.")
        Assertion.assert_equal(ret, True, "ERR: verify auto added route fail.")


@paramunittest.parametrized(
    {"tunnel_type": 'gre',"tc_id": "22", "zones":'','uuid':'1512364'},
    {"tunnel_type": 'manual',"tc_id":"23", "zones":'','uuid':'1704942'},
    {"tunnel_type": '6to4',"tc_id":"24", "zones":'','uuid':'1512365'},
    {"tunnel_type": 'gre',"tc_id": "25", "zones":'LAN,DMZ','uuid':'1704943'},
    {"tunnel_type": 'manual',"tc_id":"26", "zones":'LAN,DMZ','uuid':'1512366'},
    {"tunnel_type": '6to4',"tc_id":"27", "zones":'LAN,DMZ','uuid':'1512367'},
)

class Test_22_23_24_Verify_Multi_Tunnel(Test):
    def setParameters(self, tunnel_type, tc_id, zones, uuid):
        '''parameter tunnel_type,tc_id,zones, uuid  must be same with the dict above'''
        self.tunnel_type = tunnel_type
        self.tc_id = tc_id
        self.zones = zones
        self.uuid = uuid
        self.description = show_testcase_info(Parameter.TESTPLAN, tc_id, description=True)['title']
        self.tunnel = {
            'name': self.tunnel_type,
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        self.rem_tunnel = {
            'name': self.tunnel_type,
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X1_IP},
            'ipv6_network':{'name': Parameter.DUT_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }

    def test_22_23_24_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tc_id)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_22_23_24_01_config_X0(self):
        x0_v6 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X0_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_v6)  
        time.sleep(5)    
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x0_v6)         

        Assertion.assert_equal(rc, True, "ERR: Config X0 IPV6 fail.")

    @repeat_method(2)
    def test_22_23_24_02_add_tunnel_interface(self):
        logger.info(f'Add {self.tunnel_type} tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**self.tunnel)
        time.sleep(5)    
        rc &= rem_interface_v6.add_tunnel_interface(**self.rem_tunnel)
        Assertion.assert_equal(rc, True, "ERR: Add  tunnel interface.")

    def test_22_23_24_03_config_PC1_IP_and_Route(self):
        rc1 = pc1.config_IPv6_ip(ip=Parameter.PC1_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        rc2 = pc1.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_22_23_24_04_config_PC2_IP_and_Route(self):
        rc1 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc2 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    @repeat_method(2)
    def test_22_23_24_05_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6[self.tunnel_type])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6[self.tunnel_type]) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_22_23_24_06_change_zone(self):
        rc =True
        ret = True
        acl_opt_v6=  {
            "uuid": '1',
            "name": "rule4",
            "enable": True,
            "from": "WAN",
            "to": "LAN",
            "action": "Allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                    "group": 'Ping6'
            },
            "destination": {
                "address": {
                    "any": True,
                }
            },
            "schedule": {
                "always_on": True
            },
            "users": {
                "included": {
                    "all": True
                },
                "excluded": {
                    "none": True
                }
            },
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": True,
            "h323": True,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "block": {
                "countries": {
                    "unknown": False
                }
            },
            "packet_monitoring": False,
            "management": False,
            "max_connections": 100,
            "tcp": {
                "timeout": 15,
                "urgent": False
            },
            "icmp": {
                "timeout": 30
            },
            "connection_limit": {
                "source": {},
                "destination": {}
            },
            "dpi": True,
            "dpi_ssl": {
                "client": True,
                "server": True
            },
            "redirect_unauthenticated_users_to_log_in": True,
            "quality_of_service": {
                "class_of_service": {},
                "dscp": {
                    "preserve": True
                }
            },
        }
        if self.zones:
            for zone in self.zones.split(','):
                logger.info(f'change tunnel zone to {zone}')
                self.tunnel['zone'] = zone
                self.rem_tunnel['zone'] = zone
                acl_opt_v6['from'] = zone
                rc&= interface_v6.edit_tunnel_interface(**self.tunnel)
                rc&= rem_interface_v6.edit_tunnel_interface(**self.rem_tunnel)
                rc &= acl_ipv6.config_accessrule_ipv6(**acl_opt_v6)   
                ret &=pc2.ping6(Parameter.PC1_X0_IPv6[self.tunnel_type])
                del_acl={'from':zone,'to':'LAN','service':'Ping6','destination':'any'}
                uuid = acl_ipv6.get_ipv6_accessrule_uuid(**del_acl)
                rc &= acl_ipv6.delete_accessrule_ipv6(url=f'/access-rules/ipv6/uuid/{uuid}') 
        Assertion.assert_equal(rc, True, "ERR: change zone and access rule fail.")
        Assertion.assert_equal(rc, True, "ERR: ping from pc2 to pc1 fail after change to zone.")
          
    def test_22_23_24_07_delete_tunnel_interface(self):
        logger.info(f'Delete {self.tunnel_type} tunnel interface.')
        rc = interface_v6.delete_tunnel_interface(name=self.tunnel_type)
        rc &= rem_interface_v6.delete_tunnel_interface(name=self.tunnel_type)
        Assertion.assert_equal(rc, True, "ERR: Delete tunnel interface.")

    def test_22_23_24_08_reset_PC1_IP_and_Route(self):
        rc1 = pc1.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6[self.tunnel_type])
        rc2 = pc1.delete_IPv6_ip(ip=Parameter.PC1_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_22_23_24_09_reset_PC2_IP_and_Route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6[self.tunnel_type])
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC2_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")


@paramunittest.parametrized(
    {"tunnel_type": '6to4',"tc_id": "28", 'uuid':'1512368'},
    {"tunnel_type": 'manual',"tc_id":"29", 'uuid':'1704944'},
    {"tunnel_type": 'gre',"tc_id":"30", 'uuid':'1512369'},
)

class Test_28_29_30_Verify_Multi_Tunnel(Test):
    def setParameters(self, tunnel_type, tc_id, uuid):
        '''parameter tunnel_type,tc_id uuid  must be same with the dict above'''
        self.tunnel_type = tunnel_type
        self.tc_id = tc_id
        self.uuid = uuid
        self.description = show_testcase_info(Parameter.TESTPLAN, tc_id, description=True)['title']

    def test_28_29_30_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tc_id)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_28_29_30_01_config_X0(self):
        x0_v6 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X0_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_v6)      
        time.sleep(5)
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x0_v6)         
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPV6 fail.")

    def test_28_29_30_02_config_X3(self):
        x3_v6 = {
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X3_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rem_x3_v6 ={
            'name': 'X3',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X3_IPv6[self.tunnel_type],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x3_v6)     
        time.sleep(5) 
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x3_v6)         
        Assertion.assert_equal(rc, True, "ERR: Config X3 IPV6 fail.")

    def test_28_29_30_03_add_tunnel_interface(self):
        tunnel_1 = {
            'name': self.tunnel_type + '_1',
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        rem_tunnel_1 = {
            'name': self.tunnel_type + '_1',
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X1_IP},
            'ipv6_network':{'name': Parameter.DUT_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        tunnel_2 = {
            'name': self.tunnel_type + '_2',
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP_2,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X2},
            'ipv6_network':{'name': Parameter.REMOTE_X3_IPv6_Network['manual']},
            'bound_to': {'interface':"X2"},# or any
        }
        rem_tunnel_2 = {
            'name': self.tunnel_type + '_2',
            'zone': 'WAN',
            'type': self.tunnel_type,
            'ip': Parameter.TUNNEL_IP_2,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X2_IP},
            'ipv6_network':{'name': Parameter.DUT_X3_IPv6_Network['manual']},
            'bound_to': {'interface':"X2"},# or any
        }
        logger.info('Add 1st {self.tunnel_type} tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_1)
        time.sleep(5)
        rc &= rem_interface_v6.add_tunnel_interface(**rem_tunnel_1)
        if self.tunnel_type != '6to4':
            rc &= interface_v6.add_tunnel_interface(**tunnel_2)
            time.sleep(5)
            rc &= rem_interface_v6.add_tunnel_interface(**rem_tunnel_2)
        Assertion.assert_equal(rc, True, "ERR: Add  tunnel interface.")

    def test_28_29_30_04_config_PC1_IP_and_Route(self):
        rc1 = pc1.config_IPv6_ip(ip=Parameter.PC1_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        rc2 = pc1.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_28_29_30_05_config_PC2_IP_and_Route(self):
        rc1 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc2 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_28_29_30_06_config_PC3_IP_and_Route(self):
        rc1 = pc3.config_IPv6_ip(ip=Parameter.PC3_X3_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC3_INTERFACE)
        rc2 = pc3.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X3_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc3 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc3 fail.")

    def test_28_29_30_07_config_PC4_IP_and_Route(self):
        rc1 = pc4.config_IPv6_ip(ip=Parameter.PC4_X3_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC4_INTERFACE)
        rc2 = pc4.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X3_IPv6[self.tunnel_type])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc4 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc4 fail.")

    def test_28_29_30_08_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6[self.tunnel_type])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6[self.tunnel_type]) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_28_29_30_09_ping_from_pc3_to_pc4(self):
        if self.tunnel_type != '6to4':
            pc4.ping6(Parameter.PC3_X3_IPv6[self.tunnel_type])
            rc = pc3.ping6(Parameter.PC4_X3_IPv6[self.tunnel_type]) 
            Assertion.assert_equal(rc, True, "ERR: ping from pc3 to pc4 failed.")

    def test_28_29_30_10_delete_tunnel_interface(self):
        logger.info('Delete {self.tunnel_type} tunnel interface.')
        rc = interface_v6.delete_tunnel_interface(name=self.tunnel_type + '_1')
        rc &= rem_interface_v6.delete_tunnel_interface(name=self.tunnel_type + '_1')
        if self.tunnel_type != '6to4':
            rc &= interface_v6.delete_tunnel_interface(name=self.tunnel_type + '_2')
            rc &= rem_interface_v6.delete_tunnel_interface(name=self.tunnel_type + '_2')    
        Assertion.assert_equal(rc, True, "ERR: Delete tunnel interface.")

    def test_28_29_30_11_reset_PC1_IP_and_Route(self):
        rc1 = pc1.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6[self.tunnel_type])
        rc2 = pc1.delete_IPv6_ip(ip=Parameter.PC1_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_28_29_30_12_reset_PC2_IP_and_Route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6[self.tunnel_type])
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC2_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_28_29_30_13_reset_PC3_IP_and_Route(self):
        rc1 = pc3.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X3_IPv6[self.tunnel_type])
        rc2 = pc3.delete_IPv6_ip(ip=Parameter.PC3_X3_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC3_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc3 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc3 fail.")

    def test_28_29_30_14_reset_PC4_IP_and_Route(self):
        rc1 = pc4.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X3_IPv6[self.tunnel_type])
        rc2 = pc4.delete_IPv6_ip(ip=Parameter.PC4_X3_IPv6[self.tunnel_type], prefix='64', interface=Parameter.PC4_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")


class Test_31_6to4_relay(Test):
    uuid = "SOSAIOT-TC-56365"


    def test_31_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    @repeat_method(3)
    def test_31_01_config_X0(self):
        x0_v6 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X0_IPv6['6to4-relay'],
            'mgmt_ping': True,
        }
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6['6to4-relay'],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_v6)      
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x0_v6)         
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPV6 fail.")

    def test_31_02_add_tunnel_interface(self):
        tunnel = {
            'name': 'TC31_relay',
            'zone': 'WAN',
            'type': '6to4',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface':"X1"},# or any
        }
        rem_tunnel = {
            'name': 'TC31_relay',
            'zone': 'WAN',
            'type': '6to4',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X1_IP},
            'ipv6_network':{'name': Parameter.DUT_X0_IPv6_Network['manual']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel)
        rc &= rem_interface_v6.add_tunnel_interface(**rem_tunnel)
        Assertion.assert_equal(rc, True, "ERR: Add  tunnel interface.")

    def test_31_03_config_PC1_IP_and_Route(self):
        rc1 = pc1.config_IPv6_ip(ip=Parameter.PC1_X0_IPv6['6to4-relay'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        rc2 = pc1.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['6to4-relay'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_31_04_config_PC2_IP_and_Route(self):
        rc1 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6['6to4-relay'], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc2 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['6to4-relay'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_31_05_add_static_route(self):
        ao_v6 = {
            'name': 'TC31-relay',
            'zone': 'WAN',
            'object_type': 'host',
            'ip': Parameter.REMOTE_X0_IPv6['6to4'],
        }
        rc = ao.config_ipv6_addressobject(**ao_v6)
        route_policy = {
            "route_policies": [
                {
                    "ipv6": {
                        "interface": "TC31_relay",
                        "metric": 1,
                        "source": {"any": True},
                        'destination': {"any": True},
                        'gateway':{'name':'TC31-relay'},
                        "distance": {"auto": True},
                        "name": "route_policy_tc31",
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": {"tag1": "","tag2": "","tag3": ""}
                    }
                }
            ]
        }
        rc = route.add_route_policy(**route_policy)
        Assertion.assert_equal(rc, True, "ERR: add route policy failed")            

    @repeat_method(2)
    def test_31_06_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6["6to4-relay"])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6["6to4-relay"]) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_31_07_delete_tunnel_interface(self):
        logger.info('Delete tunnel interface.')
        rc = interface_v6.delete_tunnel_interface(name='TC31_relay')
        rc &= rem_interface_v6.delete_tunnel_interface(name='TC31_relay')
        Assertion.assert_equal(rc, True, "ERR: Delete tunnel interface.")

    def test_31_08_reset_PC1_IP_and_Route(self):
        rc1 = pc1.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['6to4-relay'])
        rc2 = pc1.delete_IPv6_ip(ip=Parameter.PC1_X0_IPv6['6to4'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_31_09_reset_PC2_IP_and_Route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['6to4-relay'])
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6["6to4-relay"], prefix='64', interface=Parameter.PC2_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")


class Test_34_Modify_Remote_Object(Test):
    uuid = "SOSAIOT-TC-56366"

    def test_34_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '34')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed") 

    @repeat_method(2)
    def test_34_01_config_X0(self):
        x0_v6 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X0_IPv6['gre'],
            'mgmt_ping': True,
        }
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6['gre'],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_v6)      
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x0_v6)         
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPV6 fail.")

    def test_34_02_add_tunnel_interface(self):
        tunnel_1 = {
            'name': 'TC34',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['gre']},
            'bound_to': {'interface':"X1"},# or any
        }
        rem_tunnel_1 = {
            'name': 'TC34',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X1_IP},
            'ipv6_network':{'name': Parameter.DUT_X0_IPv6_Network['gre']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_1)
        rc &= rem_interface_v6.add_tunnel_interface(**rem_tunnel_1)
        Assertion.assert_equal(rc, True, "ERR: Add  tunnel interface.")

    def test_34_03_config_PC1_IP_and_Route(self):
        rc1 = pc1.config_IPv6_ip(ip=Parameter.PC1_X0_IPv6['gre'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        rc2 = pc1.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['gre'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_34_04_config_PC2_IP_and_Route(self):
        rc1 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6['gre'], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc2 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['gre'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_34_05_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6['gre'])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6['gre']) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_34_06_add_aos(self):
        ao_new_v4 ={ 
            "object_type": "host",
            "name": Parameter.REMOTE_X1_IP_new,
            "zone": "WAN",
            "value": Parameter.REMOTE_X1_IP_new,
        }
        ao_new_v6 ={ 
            "zone": "WAN",
            "name": Parameter.REMOTE_X0_IPv6_Network_new,
            'object_type': 'network',
            'subnet': Parameter.REMOTE_X0_IPv6_Network_new,
            'mask': '/64',
        }  
        tunnel_new= {
            'name': 'TC34',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1_IP_new},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network_new},
            'bound_to': {'interface':"X1"},# or any
        }    
 
        rc = ao.config_addressobject(**ao_new_v4)
        rc &= ao.config_ipv6_addressobject(**ao_new_v6)    
        rc &= interface_v6.edit_tunnel_interface(**tunnel_new,tunnel_name='TC34')
        Assertion.assert_equal(rc, True, "ERR: Add new ao failed.")

    def test_34_07_update_remote_X1(self):
        rem_x1_static_dict = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X1_IP_new,
            'netmask': Parameter.NETMASK,
            'mgmt_https': True,
        } 
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6_new,
            'mgmt_ping': True,
        }
        rc = rem_interface_api.config_interface(**rem_x1_static_dict)
        rc &= rem_interface_v6_new.config_interface_ipv6(**rem_x0_v6)      
        Assertion.assert_equal(rc, True, "ERR: Update remote X1 failed.")

    def test_34_08_update_PC2_route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['6to4-relay'])
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6["gre"], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc3 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6_new, prefix='64', interface=Parameter.PC2_INTERFACE)
        rc4 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.rem_gw_new)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc2 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc2 fail.")    
        Assertion.assert_not_equal(rc3, False, "ERR: add new ipv6 route on pc2 fail.")
        Assertion.assert_not_equal(rc4, False, "ERR: add new ipv6 route on pc2 fail.")  

    def test_34_09_ping_from_pc1_to_pc2(self):
        rc = pc1.ping6(Parameter.PC2_X0_IPv6_new) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_34_10_reset_PC1_IP_and_Route(self):
        rc1 = pc1.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['gre'])
        rc2 = pc1.delete_IPv6_ip(ip=Parameter.PC1_X0_IPv6['gre'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_34_11_reset_PC2_IP_and_Route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.rem_gw_new)
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6_new, prefix='64', interface=Parameter.PC2_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_34_12_reset_interface(self):
        rem_x1_static_dict = {
            'if': 'x1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': Parameter.REMOTE_X1,
            'netmask': Parameter.NETMASK,
            'mgmt_https': True,
        }         
        rc = rem_interface_new.config_interface(**rem_x1_static_dict)
        logger.info('Delete tunnel interface.')
        rc &= interface_v6.delete_tunnel_interface(name='TC34')
        rc &= rem_interface_v6.delete_tunnel_interface(name='TC34')
        Assertion.assert_equal(rc, True, "ERR: Delete tunnel interface.")

class Test_35_VPN_Check(Test):
    uuid = "SOSAIOT-TC-56367"

    def test_35_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '35')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")      

    def test_35_01_config_X0(self):
        x0_v6 = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.DUT_X0_IPv6['gre'],
            'mgmt_ping': True,
        }
        rem_x0_v6 ={
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': Parameter.REMOTE_X0_IPv6['gre'],
            'mgmt_ping': True,
        }
        rc = interface_v6.config_interface_ipv6(**x0_v6)      
        rc &= rem_interface_v6.config_interface_ipv6(**rem_x0_v6)         
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPV6 fail.")


    def test_35_03_add_tunnel_interface(self):
        tunnel_1 = {
            'name': 'TC35-gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.REMOTE_X1},
            'ipv6_network':{'name': Parameter.REMOTE_X0_IPv6_Network['gre']},
            'bound_to': {'interface':"X1"},# or any
        }
        rem_tunnel_1 = {
            'name': 'TC35-gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name': Parameter.DUT_X1_IP},
            'ipv6_network':{'name': Parameter.DUT_X0_IPv6_Network['gre']},
            'bound_to': {'interface':"X1"},# or any
        }
        logger.info('Add gre tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_1)
        rc &= rem_interface_v6.add_tunnel_interface(**rem_tunnel_1)
        Assertion.assert_equal(rc, True, "ERR: Add  tunnel interface.")

    def test_35_04_add_vpn(self):
        vpn_dict ={
            'ipversion':'ipv6',
            'type': 'site_to_site',
            'name': 'local_vpn_1',
            'pri_gate': Parameter.TUNNEL_IP,
            'sec_gate': '0::0',
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'local_ike_type': 'ipv6',
            'peer_ike_type': 'ipv6',
            'local_ike_id': '1::1',
            'peer_ike_id': '2::2',
            'local_net_type': 'group',
            'local_net_group': 'LAN IPv6 Subnets',
            'remote_net_type': 'name',
            'remote_net_name': Parameter.REMOTE_X0_IPv6_Network['gre'],
            'keep_alive': True,
        } 
        rem_vpn_dict = {
            'ipversion':'ipv6',
            'type': 'site_to_site',
            'name': 'local_vpn_1',
            'pri_gate': Parameter.TUNNEL_IP,
            'sec_gate': '0::0',
            'auth_mode': 'shared_secret',
            'secret': 'password',
            'local_ike_type': 'ipv6',
            'peer_ike_type': 'ipv6',
            'local_ike_id': '1::1',
            'peer_ike_id': '2::2',
            'local_net_type': 'group',
            'local_net_group': 'LAN IPv6 Subnets',
            'remote_net_type': 'name',
            'remote_net_name': Parameter.DUT_X0_IPv6_Network['gre'],
            'keep_alive': True,
        } 
        rc = Lvpn.add_ipv6_vpn_policy(**vpn_dict)
        logger.info(" {} ".center(20, '*').format('Add VPN Policy'))
        rc &= rem_vpn.add_ipv6_vpn_policy(**rem_vpn_dict)
        Assertion.assert_equal(rc, True, "ERR: Add vpn policy failed.")

    def test_35_05_config_PC1_IP_and_Route(self):
        rc1 = pc1.config_IPv6_ip(ip=Parameter.PC1_X0_IPv6['gre'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        rc2 = pc1.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['gre'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_35_06_config_PC2_IP_and_Route(self):
        rc1 = pc2.config_IPv6_ip(ip=Parameter.PC2_X0_IPv6['gre'], prefix='64', interface=Parameter.PC2_INTERFACE)
        rc2 = pc2.config_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['gre'])
        Assertion.assert_not_equal(rc1, False, "ERR: config ipv6 on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: add ipv6 route on pc1 fail.")

    def test_35_07_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6['gre'])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6['gre']) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_35_08_add_route(self):
        route_policy = {
            "route_policies": [
                {
                    "ipv6": {
                        "interface": "TC35-gre",
                        "metric": 1,
                        "source": {"any": True},
                        'destination': {"name": Parameter.REMOTE_X0_IPv6_Network['gre']},
                        'gateway':{'default':True},
                        "distance": {"auto": True},
                        "name": "route_policy_tc35",
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": True,
                        "probe": "",
                        "ticket": {"tag1": "","tag2": "","tag3": ""}
                    }
                }
            ]
        }        
        rem_route_policy = {
            "route_policies": [
                {
                    "ipv6": {
                        "interface": "TC35-gre",
                        "metric": 1,
                        "source": {"any": True},
                        'destination': {"name": Parameter.DUT_X0_IPv6_Network['gre']},
                        'gateway':{'default':True},
                        "distance": {"auto": True},
                        "name": "route_policy_tc35",
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": True,
                        "probe": "",
                        "ticket": {"tag1": "","tag2": "","tag3": ""}
                    }
                }
            ]
        } 
        rc = route.add_route_policy(**route_policy)
        rc &= rem_route.add_route_policy(**rem_route_policy)
        Assertion.assert_equal(rc, True, "ERR: Add route failed.")

    def test_35_09_ping_from_pc1_to_pc2(self):
        pc2.ping6(Parameter.PC1_X0_IPv6['gre'])
        rc = pc1.ping6(Parameter.PC2_X0_IPv6['gre']) 
        Assertion.assert_equal(rc, True, "ERR: ping from pc1 to pc2 failed.")

    def test_35_10_delete_tunnel_interface(self):
        logger.info('Delete tunnel interface.')
        rc = interface_v6.delete_tunnel_interface(name='TC35-gre')
        rc &= rem_interface_v6.delete_tunnel_interface(name='TC35-gre')
        Assertion.assert_equal(rc, True, "ERR: Delete tunnel interface.")

    def test_35_11_reset_PC1_IP_and_Route(self):
        rc1 = pc1.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.DUT_X0_IPv6['gre'])
        rc2 = pc1.delete_IPv6_ip(ip=Parameter.PC1_X0_IPv6['gre'], prefix='64', interface=Parameter.PC1_INTERFACE['LAN'])
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")

    def test_35_12_reset_PC2_IP_and_Route(self):
        rc1 = pc2.delete_IPv6_route(route='0::0',prefix='0', gw=Parameter.REMOTE_X0_IPv6['gre'])
        rc2 = pc2.delete_IPv6_ip(ip=Parameter.PC2_X0_IPv6["gre"], prefix='64', interface=Parameter.PC2_INTERFACE)
        Assertion.assert_not_equal(rc1, False, "ERR: delete ipv6 route on pc1 fail.")
        Assertion.assert_not_equal(rc2, False, "ERR: unset ipv6 on pc1 fail.")


class Test_36_37_39_Add_AOs(Test):
    uuid = 'NonTC'
    def test_36_37_39_add_aos(self):
        ao_v4_1 ={
            "object_type": "host",
            "name": 'tc36_37_39_1',
            "zone": "WAN",
            "value": '4.4.4.4',
        }
        ao_v4_2 ={
            "object_type": "host",
            "name": 'tc36_37_39_2',
            "zone": "WAN",
            "value": '5.5.5.5',
        }
        ao_v6_1 = {
            "name": 'tc36_37_39_3',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '4::4',
            'mask': '/64',
        }
        ao_v6_2 = {
            "name": 'tc36_37_39_4',
            'zone': 'WAN',
            'object_type': 'network',
            'subnet': '5::5',
            'mask': '/64',
        }
        rc = ao.config_addressobject(**ao_v4_1)
        rc &= ao.config_addressobject(**ao_v4_2)
        rc &= ao.config_ipv6_addressobject(**ao_v6_1)
        rc &= ao.config_ipv6_addressobject(**ao_v6_2)
        Assertion.assert_equal(rc, True, "ERR: Add ao failed.")


@paramunittest.parametrized(
    {"action": 'reboot',"tc_id": "36", 'uuid':'1704945'},
    {"action": 'tsr',"tc_id":"37", 'uuid':'1512373'},
    {"action": 'pref',"tc_id":"39", 'uuid':'1512374'},
)

class Test_36_37_39_Inter_Test(Test):
    def setParameters(self, action, tc_id, uuid):
        '''parameter action,tc_id uuid  must be same with the dict above'''
        self.action = action
        self.tc_id = tc_id
        self.uuid = uuid
        self.description = show_testcase_info(Parameter.TESTPLAN, tc_id, description=True)['title']    

    def test_36_37_39_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tc_id)
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")  

    def test_36_37_39_01_add_tunnel(self):
        manual = {
            'name': 'TC36_37_39_manual',
            'zone': 'WAN',
            'type': 'manual',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'ipv4_address':{'name':'tc36_37_39_1'},
            'ipv6_network':{'name':'tc36_37_39_3'},
            'bound_to': {'interface':"X1"},# or any
        }
        gre = {
            'name': 'TC36_37_39_gre',
            'zone': 'WAN',
            'type': 'gre',
            'ip': Parameter.TUNNEL_IP_2,
            'prefix_length': 64,
            'ipv4_address':{'name': 'tc36_37_39_2'},
            'ipv6_network':{'name': 'tc36_37_39_4'},
            'bound_to': {'interface':"X1"},# or any
        }
        tunnel_6to4 = {
            'type': '6to4',
            'zone': 'WAN',
            'name': 'TC36_37_39_6to4',
            'bound_to': {'interface':"X1"},# or any
            'ip': Parameter.TUNNEL_IP_3,
            'prefix_length': 64,
        }
        logger.info('Add 6to4 tunnel interface.')
        rc = interface_v6.add_tunnel_interface(**tunnel_6to4)
        logger.info('Add gre tunnel interface.')
        rc &= interface_v6.add_tunnel_interface(**manual)    
        logger.info('Add manual tunnel interface.')
        rc &= interface_v6.add_tunnel_interface(**gre)    
        Assertion.assert_equal(rc, True, "ERR: Add tunnels failed.")

    def test_36_37_39_02_take_action(self):
        if self.action == 'reboot':
            rc = setting.boot_fw(1)
        elif self.action == 'pref':
            rc = setting.export_setting_exp('/tmp/tunnel.exp')
            rc &= setting.boot_fw(2)
            rc &= setting.import_setting_exp('/tmp/tunnel.exp')
        elif self.action == 'tsr':
            rc =True
        Assertion.assert_equal(rc, True, f"ERR: Take action {self.action} failed.")

    def test_36_37_39_03_verify_action(self):
        tsr = diag.get_tsr_part('Network','Interfaces')
        Assertion.assert_regular(tsr, 'TC36_37_39_manual', f"ERR: tunnel TC36_37_39_manual not in tsr.")
        Assertion.assert_regular(tsr, 'TC36_37_39_gre', f"ERR: tunnel TC36_37_39_gre not in tsr.")
        Assertion.assert_regular(tsr, 'TC36_37_39_6to4', f"ERR: tunnel TC36_37_39_6to4 not in tsr.")

    def test_36_37_39_04_delete_tunnel(self):
        rc = interface_v6.delete_tunnel_interface(name='TC36_37_39_manual')
        rc &= interface_v6.delete_tunnel_interface(name='TC36_37_39_gre')
        rc &= interface_v6.delete_tunnel_interface(name='TC36_37_39_6to4')
        Assertion.assert_equal(rc, True, f"ERR: Delete tunnels failed.")


