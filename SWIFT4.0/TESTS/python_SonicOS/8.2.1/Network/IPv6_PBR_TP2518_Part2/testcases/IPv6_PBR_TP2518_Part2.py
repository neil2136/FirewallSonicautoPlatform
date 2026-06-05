from definition.settings import *


class Test_IPv6_PBR_01(Test):
    uuid = "SOSAIOT-TC-58547"
    description= show_testcase_info(TESTPLAN, '1532496', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1532496')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_route_policy(self):
        ####ipv4 addr can show UI but not API
        # ref1 = copy.deepcopy(ipv6_route)
        ref2 = copy.deepcopy(ipv6_route)
        # ref1['route_policies'][0]['ipv6']['name'] = 'test2'
        # ref1['route_policies'][0]['ipv6']['source']['name'] = 'ipv4_ao'
        # ref1['route_policies'][0]['ipv6']['destination']['name'] = 'ipv4_ao2'
        ref2['route_policies'][0]['ipv6']['name'] = 'test3'
        ref2['route_policies'][0]['ipv6']['source']['name'] = 'ipv6_ao1'
        ref2['route_policies'][0]['ipv6']['destination']['name'] = 'ipv6_ao3'
        # rc = route_obj.add_route_policy(**ref1)
        rc = route_obj.add_route_policy(**ref2)
        rc &= route_obj.add_route_policy(**ipv6_route)
        Assertion.assert_equal(rc, True, f"ERR: add route policy fail.")

    @repeat_method(3)
    def test_02_check_route_policy(self):
        res1 = route_obj.get_route_policy_by_name(name='test1',version='ipv6')
        # res2 = route_obj.get_route_policy_by_name(name='test2',version='ipv6')
        res3 = route_obj.get_route_policy_by_name(name='test3',version='ipv6')
        ref1 =res1['route_policies'][0]['ipv6']
        ref3 =res3['route_policies'][0]['ipv6']
        if ref1['source']['name']=='ipv6_ao2' and ref1['destination']['name']=='ipv6_ao1' and ref1['gateway']['name']=='ipv6_ao3' and\
            ref3['source']['name']=='ipv6_ao1' and ref3['destination']['name']=='ipv6_ao3' and ref3['gateway']['name']=='ipv6_ao3':
            rc = True
            logger.info('check route policy src/dst/gw success')
        else:
            rc =False
        Assertion.assert_equal(rc , True, f"ERR: check route policy src/dst/gw fail.")

##based 01
class Test_IPv6_PBR_02(Test):
    uuid = "SOSAIOT-TC-58543"
    description= show_testcase_info(TESTPLAN, '1510832', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1510832')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_route_policy(self):
        rc = route_obj.add_route_policy(**ipv4_route)
        Assertion.assert_equal(rc, True, f"ERR: add route policy fail.")

    def  test_02_check_filter_route_policy(self):
        res1 = route_obj.get_route_policy(version='v4')
        res2 = route_obj.get_route_policy(version='v6')
        count_v4 = 0
        count_v6 = 0
        logger.info(f'-----{res1}')
        logger.info(f'-----{res2}')
        for v4_policy in res1['route_policies']:
            if v4_policy['ipv4']['name'] == 'test_ipv4':
                count_v4 += 1
        for v6_policy in res2['route_policies']:
            if v6_policy['ipv6']['name'] == 'test1' or v6_policy['ipv6']['name'] == 'test3':
                count_v6 += 1
        logger.info(f'the count_v4 is {count_v4}, the count_v6 is {count_v6}')
        rc = True if count_v4==1 and count_v6==2 else False
        Assertion.assert_equal(rc, True, f"ERR: check filter route policy fail.")

    def test_03_delete_route_policy(self):
        rc = route_obj.del_route_policy_by_name(name='test_ipv4',version = 'v4')
        rc &= route_obj.del_route_policy_by_name(name='test1',version = 'v6')
        rc &= route_obj.del_route_policy_by_name(name='test3',version = 'v6')
        Assertion.assert_equal(rc, True, f"ERR: delete route policy fail.")


class Test_IPv6_PBR_03(Test):
    uuid = "SOSAIOT-TC-58550"
    description= show_testcase_info(TESTPLAN, '2617416', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2617416')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_invalid_input_route_settings(self):
        res1 = route_obj.config_route_settings(msg=True,metric = 0)
        res2 = route_obj.config_route_settings(msg=True,metric = "abc")
        res3 = route_obj.config_route_settings(msg=True,metric = "!@#~")
        if 'property \'default_route_metric\' can\'t be empty value' in res1[1]['status']['info'][0]['message'] and \
            'property \'default_route_metric\' expected: \'NUMBER\', found: \'"STRING..."\'' in res2[1]['status']['info'][0]['message'] \
             and 'expected: \'NUMBER\', found: \'"STRING..."\'' in res3[1]['status']['info'][0]['message']:
            rc = True
            logger.info("Invalid input shouldn't be saved.")
        else:
            rc = False
        logger.info('check Apply the following metric to IPv6 default routes')
        res4 = route_obj.get_route_settings()
        if res4['routing']['ipv6']['default_route_metric'] == 50:
            rc &= True
            logger.info('check default route metric is 50')
        else:
            rc &= False
        logger.info(f'------{res1}---{res2}--{res3}---{res4}--')
        Assertion.assert_equal(rc, True, f"ERR: set invalid input route settings and check it fail.")


class Test_IPv6_PBR_04(Test):
    uuid = "SOSAIOT-TC-58551"
    description= show_testcase_info(TESTPLAN, '2617440', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2617440')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_set_out_boundary_route_settings(self):
        res1 = route_obj.config_route_settings(msg=True,metric = 0)
        res2 = route_obj.config_route_settings(msg=True,metric = 256)
        if 'property \'default_route_metric\' can\'t be empty value' in res1[1]['status']['info'][0]['message'] and \
            'Value or string length(256) out of bounds' in res2[1]['status']['info'][0]['message'] :
            rc = True
            logger.info('check out boundary route setting')
        else:
            rc = False
        res4 = route_obj.get_route_settings()
        if res4['routing']['ipv6']['default_route_metric'] == 50:
            rc &= True
            logger.info('check default route metric is 50')
        else:
            rc &= False
        Assertion.assert_equal(rc, True, f"ERR: set out boundary route settings and check it fail.")

    def test_02_set_in_boundary_route_settings(self):
        res1 = route_obj.config_route_settings(msg=True,metric = 1)
        res2 = route_obj.get_route_settings()
        res3 = route_obj.config_route_settings(msg=True,metric = 255)
        res4 = route_obj.get_route_settings()
        if res1[0] and res2['routing']['ipv6']['default_route_metric'] == 1 and \
            res3[0] and  res4['routing']['ipv6']['default_route_metric'] == 255:
            rc = True
            logger.info('config  route metric and check it')
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: config  route metric and check it fail.")

    def test_03_restore_env(self):
        res1 = route_obj.config_route_settings(msg=True,metric = 50)
        res2 = route_obj.get_route_settings()
        if res1[0] and res2['routing']['ipv6']['default_route_metric'] == 50:
            rc = True
            logger.info('config default route metric and check it')
        else:
            rc = False
        Assertion.assert_equal(rc, True, f"ERR: restore env fail.")