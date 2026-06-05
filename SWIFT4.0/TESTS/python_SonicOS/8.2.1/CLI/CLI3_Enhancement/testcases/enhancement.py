from definition.settings import *
from definition.utils import *


# smoke cases 03,05,08,14
class TestCLI_Enhancement_TC03(Test):
    uuid = "SOSAIOT-TC-48319"
    description = show_testcase_info(TESTPLAN, "3", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

# no need autopep8
    def test_01_add_service_object(self):
        addservobj = servicecli.add_service_object(**service_object_dict)
        logger.info('add service object result: {}'.format(addservobj))
        showresult = servicecli.show_service_object(service_object_dict['name'])
        output = True if 'UDP 1 80' in showresult else False
        logger.info(output)
        Assertion.assert_equal(output, True, "ERR: add service object failed!")


class TestCLI_Enhancement_TC01(Test):
    uuid = "SOSAIOT-TC-48307"
    description = show_testcase_info(TESTPLAN, "1", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_service_objects(self):
        checkres = servicecli.show_service_object()
        logger.info('show all service objects result: {}'.format(checkres))
        output = True if 'service-object {}'.format(service_object_dict['name']) in checkres else False
        Assertion.assert_equal(output, True, "ERR: show all service objects failed!")


class TestCLI_Enhancement_TC02(Test):
    uuid = "SOSAIOT-TC-48317"
    description = show_testcase_info(TESTPLAN, "2", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_service_object_name(self):
        checkres = servicecli.show_service_object(service_object_dict['name'])
        logger.info('show service object name result: {}'.format(checkres))
        output = True if 'service-object {}'.format(service_object_dict['name']) in checkres else False
        Assertion.assert_equal(output, True, "ERR: show service object name failed!")


class TestCLI_Enhancement_TC17(Test):
    uuid = "SOSAIOT-TC-48314"
    description = show_testcase_info(TESTPLAN, "17", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_service_object(self):
        modifyso = servicecli.edit_service_object(**edit_service_object_dict)
        logger.info('edit service object result: {}'.format(modifyso))
        checkres = servicecli.show_service_object(service_object_dict['name'])
        output = True if (f"service-object {service_object_dict['name']}" and "AH") in checkres else False
        Assertion.assert_equal(output, True, "ERR: modify service object failed!")


class TestCLI_Enhancement_TC18(Test):
    uuid = "SOSAIOT-TC-48315"
    description = show_testcase_info(TESTPLAN, "18", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_service_object(self):
        delso = servicecli.del_service_object(service_object_dict['name'])
        logger.info('edit service object result: {}'.format(delso))
        checkres = servicecli.show_service_object(service_object_dict['name'])
        output = True if 'No matching command found' in checkres else False
        Assertion.assert_equal(output, True, "ERR: delete service object failed!")


class TestCLI_Enhancement_TC06(Test):
    uuid = "SOSAIOT-TC-48319"
    description = show_testcase_info(TESTPLAN, "6", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_service_group(self):
        addsg = servicecli.add_service_group(**service_group_dict)
        logger.info('add service group result: {}'.format(addsg))
        checkres = servicecli.show_service_group(service_group_dict['name'])
        output = True if ('AutoAddSrvG' and 'service-group Ping' and 'service-object HTTPS') in checkres else False
        Assertion.assert_equal(output, True, "ERR: add service group failed!")


class TestCLI_Enhancement_TC04(Test):
    uuid = "SOSAIOT-TC-48320"
    description = show_testcase_info(TESTPLAN, "4", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_service_groups(self):
        checkres = servicecli.show_service_group()
        output = True if 'service-group {}'.format(service_group_dict['name']) in checkres else False
        Assertion.assert_equal(output, True, "ERR: show all service groups failed!")


class TestCLI_Enhancement_TC05(Test):
    uuid = "SOSAIOT-TC-48321"
    description = show_testcase_info(TESTPLAN, "5", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_service_group_name(self):
        checkres = servicecli.show_service_group(service_group_dict['name'])
        logger.info('show service group name result: {}'.format(checkres))
        output = True if 'service-group {}'.format(service_group_dict['name']) in checkres else False
        Assertion.assert_equal(output, True, "ERR: show service group name failed!")


class TestCLI_Enhancement_TC19(Test):
    uuid = "SOSAIOT-TC-48316"
    description = show_testcase_info(TESTPLAN, "19", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '19')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_service_group(self):
        modifysg = servicecli.edit_service_group(**edit_service_group_dict)
        logger.info('edit service group result: {}'.format(modifysg))
        checkres = servicecli.show_service_group(edit_service_group_dict['name-new'])
        output = True if ('AutoAddSrvG_new' and 'Ping6' and 'FTP') in checkres else False
        Assertion.assert_equal(output, True, "ERR: modify service group failed!")


class TestCLI_Enhancement_TC20(Test):
    uuid = "SOSAIOT-TC-48318"
    description = show_testcase_info(TESTPLAN, "20", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_service_group(self):
        delsg = servicecli.del_service_group(edit_service_group_dict['name-new'])
        logger.info('edit service group result: {}'.format(delsg))
        checkres = servicecli.show_service_group(edit_service_group_dict['name-new'])
        output = True if 'No matching command found' in checkres else False
        Assertion.assert_equal(output, True, "ERR: delete service group failed!")


# check nat uuid configure: nat ipv4 uuid...
# include case 07-10
class Test_NATUUIDTests(Test):
    uuid = 'NonTC'

    def test_01_add_nat_policy(self):
        addnat = natpolicycli.add_natpolicy(**nat_policy_dict)
        logger.info('add nat policy result: {}'.format(addnat))

        # check nat show
        logger.info(f"{' NAT:show test ':=^40}")
        checkres = natpolicycli.show_natpolicy(**show_nat_policy_dict)
        natuuid = get_uuid(checkres, nat_policy_dict['comment'])
        if natuuid == 'fail':
            Assertion.assert_equal(False, True, "error: can not get the uuid from nat policy.")
        else:
            g_nat_check_dict['show'] = True

        # storage the nat uuid to a dict
        nat_policy_uuid_dict['uuid'] = natuuid

        # check nat uuid
        logger.info(f"{' NAT:uuid add test ':=^40}")
        checkres = natpolicycli.show_natpolicy(**nat_policy_uuid_dict)
        g_nat_check_dict['uuid'] = True if f"comment {nat_policy_dict['comment']}" in checkres else False
        Assertion.assert_equal(g_nat_check_dict['uuid'], True, "ERR: add nat policy failed")

    def test_02_edit_nat_policy(self):
        if not g_nat_check_dict['uuid']:
            Assertion.assert_equal(False, True, "error: can not find nat uuid, skip all edit case.")

        # inbound test
        logger.info(f"{' NAT:inbound test ':=^40}")
        tempin = []
        inzones = ['any', 'X0', 'X1']
        for zone in inzones:
            nat_policy_uuid_dict['inbound_new'] = zone
            editres = natpolicycli.edit_natpolicy_by_uuid(**nat_policy_uuid_dict)
            logger.info('edit nat policy inbound result: {}'.format(editres))
            checkres = natpolicycli.show_natpolicy(**nat_policy_uuid_dict)
            if 'inbound ' + zone in checkres:
                tempin.append(1)
                logger.info('edit nat policy inbound {} successful.'.format(zone))
            else:
                tempin.append(0)
                logger.info('check nat policy inbound to {} failed'.format(zone))
        g_nat_check_dict['inbound'] = all(tempin)

        # init nat policy uuid dict
        del nat_policy_uuid_dict['inbound_new']

        # outbound test
        logger.info(f"{' NAT:outbound test ':=^40}")
        tempout = []
        outzones = ['any', 'X0', 'X1']
        for zone in outzones:
            nat_policy_uuid_dict['outbound_new'] = zone
            editres = natpolicycli.edit_natpolicy_by_uuid(**nat_policy_uuid_dict)
            logger.info('edit nat policy outbound result: {}'.format(editres))
            checkres = natpolicycli.show_natpolicy(**nat_policy_uuid_dict)
            if 'outbound ' + zone in checkres:
                tempout.append(1)
                logger.info('edit nat policy outbound {} successful.'.format(zone))
            else:
                tempout.append(0)
                logger.info('check nat policy outbound to {} failed'.format(zone))
        g_nat_check_dict['outbound'] = all(tempout)

        # init nat policy uuid dict
        del nat_policy_uuid_dict['outbound_new']

        # trans_source test
        logger.info(f"{' NAT:trans_source test ':=^40}")
        tempsource = []
        typelist = ['range', 'network', 'host']
        for type in typelist:
            nat_policy_uuid_dict['trans_source_type_new'] = type
            srcname = source_AO_dict[type]['name']
            srcvalue = source_AO_dict[type]['value']
            splitaddr = split_address(srcvalue)
            if splitaddr == 'fail':
                Assertion.assert_equal(False, True, "error: can not get the source address from address object.")
            else:
                nat_policy_uuid_dict['trans_source_new'] = splitaddr
            editres = natpolicycli.edit_natpolicy_by_uuid(**nat_policy_uuid_dict)
            logger.info('edit nat policy trans_source result: {}'.format(editres))
            checkres = natpolicycli.show_natpolicy(**nat_policy_uuid_dict)
            if 'translated-source name ' + srcname in checkres:
                tempsource.append(1)
                logger.info('edit nat policy trans_source {} successful.'.format(srcname))
            else:
                tempsource.append(0)
                logger.info('check nat policy trans_source to {} failed'.format(srcname))
        g_nat_check_dict['trans_source'] = all(tempsource)

        # init nat policy uuid dict
        del nat_policy_uuid_dict['trans_source_type_new']
        del nat_policy_uuid_dict['trans_source_new']

        g_nat_check_dict['modify'] = all(value == 1 for value in g_nat_check_dict.values())
        Assertion.assert_equal(g_nat_check_dict['modify'], True, "ERR: edit nat policy failed")

    def test_03_delete_restore_nat_policy(self):
        # delete nat policy
        g_nat_check_dict['delete'] = natpolicycli.del_natpolicy('{}:uuid:{}'.format(nat_policy_dict['version'], nat_policy_uuid_dict['uuid']))
        logger.info('delete nat policy result: {}'.format(g_nat_check_dict['delete']))

        # init the nat policy table
        initres = natpolicycli.del_natpolicy('all')
        logger.info('restore nat policy result: {}'.format(initres))

        Assertion.assert_equal(g_nat_check_dict['delete'], True, "ERR: delete nat policy failed")


class TestCLI_Enhancement_TC07(Test):
    uuid = "SOSAIOT-TC-48322"
    description = show_testcase_info(TESTPLAN, "7", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '7')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_nat_policy(self):
        logger.info('show nat policy result: {}'.format(g_nat_check_dict['show']))
        Assertion.assert_equal(g_nat_check_dict['show'], True, "ERR: show nat policy failed")


class TestCLI_Enhancement_TC08(Test):
    uuid = "SOSAIOT-TC-48323"
    description = show_testcase_info(TESTPLAN, "8", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_nat_policy(self):
        logger.info('add nat policy result: {}'.format(g_nat_check_dict['uuid']))
        Assertion.assert_equal(g_nat_check_dict['uuid'], True, "ERR: add nat policy failed")


class TestCLI_Enhancement_TC09(Test):
    uuid = "SOSAIOT-TC-48324"
    description = show_testcase_info(TESTPLAN, "9", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_nat_policy(self):
        logger.info('modify nat policy result: {}'.format(g_nat_check_dict['modify']))
        Assertion.assert_equal(g_nat_check_dict['modify'], True, "ERR: modify nat policy failed")


class TestCLI_Enhancement_TC10(Test):
    uuid = "SOSAIOT-TC-48324"
    description = show_testcase_info(TESTPLAN, "10", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_nat_policy(self):
        logger.info('delete nat policy result: {}'.format(g_nat_check_dict['delete']))
        Assertion.assert_equal(g_nat_check_dict['delete'], True, "ERR: delete nat policy failed")


# check acl uuid configure: access-rule ipv4 uuid...
# include case 11-16
class Test_ACLUUIDTests(Test):
    uuid = 'NonTC'

    def test_01_add_access_rule(self):
        addres = accessrulecli.add_access_rule(**access_rule_dict)
        logger.info('add a access rule result: {}'.format(addres))

        # check acl show
        logger.info(f"{' ACL:show test ':=^40}")
        checkres = accessrulecli.show_access_rules(**show_access_rule_dict)
        g_acl_check_dict['show'] = True if 'comment {}'.format(access_rule_dict['comment']) in checkres else False
        acluuid = get_uuid(checkres, access_rule_dict['comment'])
        if acluuid == 'fail':
            Assertion.assert_equal(False, True, "error: can not get the uuid from acl.")

        # storage the acl uuid to a dict
        access_rule_uuid_dict['uuid'] = acluuid

        # check acl uuid
        logger.info(f"{' ACL:uuid add test ':=^40}")
        show_access_rule_uuid_dict['type'] = 'uuid ' + acluuid
        checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
        g_acl_check_dict['uuid'] = True if 'comment {}'.format(access_rule_dict['comment']) in checkres else False

        Assertion.assert_equal(g_acl_check_dict['uuid'], True, "ERR: add access rule failed")

    def test_02_edit_access_rule(self):
        # init the acl table
        if not g_acl_check_dict['uuid']:
            initres = accessrulecli.restore_access_rule()
            logger.info('restore access rule result: {}'.format(initres))
            Assertion.assert_equal(False, True, "error: can not find acl uuid, skip all edit case.")

        # from test
        logger.info(f"{' ACL:from test ':=^40}")
        tempfrom = []
        fromzones = ['any', 'DMZ', 'WAN', 'WLAN', 'X0', 'LAN']
        for zone in fromzones:
            access_rule_uuid_dict['from_new'] = zone
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule to from result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'from ' + zone in checkres:
                tempfrom.append(1)
                logger.info('edit access rule from to {} successful.'.format(zone))
            else:
                tempfrom.append(0)
                logger.info('check access rule from to {} failed'.format(zone))
        g_acl_check_dict['from'] = all(tempfrom)

        # init acl uuid dict
        del access_rule_uuid_dict['from_new']

        # to test
        logger.info(f"{' ACL:to test ':=^40}")
        tempto = []
        tozones = ['any', 'DMZ', 'WLAN', 'WAN']
        for zone in tozones:
            access_rule_uuid_dict['to_new'] = zone
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule to to result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'to ' + zone in checkres:
                tempto.append(1)
                logger.info('edit access rule to to {} successful.'.format(zone))
            else:
                tempto.append(0)
                logger.info('check access rule to to {} failed'.format(zone))
        g_acl_check_dict['to'] = all(tempto)

        # init acl uuid dict
        del access_rule_uuid_dict['to_new']

        #  source test
        logger.info(f"{' ACL:source test ':=^40}")
        tempsource = []
        sourcelist = [
            source_AO_dict['range']['name'],
            source_AO_dict['network']['name'],
            source_AO_dict['host']['name']]
        for source in sourcelist:
            access_rule_uuid_dict['src_name_new'] = source
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule source result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'source address name ' + source in checkres:
                tempsource.append(1)
                logger.info('edit access rule source to {} successful.'.format(source))
            else:
                tempsource.append(0)
                logger.info('check access rule source to {} failed'.format(source))
        g_acl_check_dict['source'] = all(tempsource)

        # init acl uuid dict
        del access_rule_uuid_dict['src_name_new']

        # destination test
        logger.info(f"{' ACL:destination test ':=^40}")
        tempdest = []
        destinationlist = [
            dest_AO_dict['range']['name'],
            dest_AO_dict['network']['name'],
            dest_AO_dict['host']['name']]
        for destination in destinationlist:
            access_rule_uuid_dict['dst_name_new'] = destination
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule destination result: {}'.format(editres))

            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'destination address name ' + destination in checkres:
                tempdest.append(1)
                logger.info('edit access rule destination to {} successful.'.format(destination))
            else:
                tempdest.append(0)
                logger.info('check access rule destination to {} failed'.format(destination))
        g_acl_check_dict['destination'] = all(tempdest)

        # init acl uuid dict
        del access_rule_uuid_dict['dst_name_new']

        # Service test
        logger.info(f"{' ACL:service test ':=^40}")
        tempserv = []
        servicelist = ['SSH', 'HTTP', 'HTTPS']
        for service in servicelist:
            access_rule_uuid_dict['service_name_new'] = service
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule service result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'service name ' + service in checkres:
                tempserv.append(1)
                logger.info('edit access rule service to {} successful.'.format(service))
            else:
                tempserv.append(0)
                logger.info('check access rule service {} failed'.format(service))
        g_acl_check_dict['service'] = all(tempserv)

        # init acl uuid dict
        del access_rule_uuid_dict['service_name_new']

        # Action test
        logger.info(f"{' ACL:action test ':=^40}")
        actionname = []
        actionlist = ['allow', 'discard', 'deny']
        for action in actionlist:
            access_rule_uuid_dict['action_new'] = action
            editres = accessrulecli.edit_access_rule_by_uuid(**access_rule_uuid_dict)
            logger.info('edit access rule action result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(**show_access_rule_uuid_dict)
            if 'action ' + action in checkres:
                actionname.append(1)
                logger.info('edit access rule action to {} successful.'.format(action))
            else:
                actionname.append(0)
                logger.info('check access rule action to {} failed'.format(action))
        g_acl_check_dict['action'] = all(actionname)

        # init acl uuid dict
        del access_rule_uuid_dict['action_new']

        g_acl_check_dict['modify'] = all(value == 1 for value in g_acl_check_dict.values())
        Assertion.assert_equal(g_acl_check_dict['modify'], True, "ERR: edit access rule via uuid failed")

    def test_03_delete_restore_access_rule(self):
        # delete access rule
        g_acl_check_dict['delete'] = accessrulecli.del_access_rule(**access_rule_dict)
        logger.info('delete access rule result: {}'.format(g_acl_check_dict['delete']))

        # init the acl table
        initres = accessrulecli.restore_access_rule()
        logger.info('restore access rule result: {}'.format(initres))

        Assertion.assert_equal(g_acl_check_dict['delete'], True, "ERR: delete access rule failed")


class TestCLI_Enhancement_TC11(Test):
    uuid = "SOSAIOT-TC-48308"
    description = show_testcase_info(TESTPLAN, "11", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_show_access_rules(self):
        logger.info('show access rules result: {}'.format(g_acl_check_dict['show']))
        Assertion.assert_equal(g_acl_check_dict['show'], True, "ERR: show access rules failed")


class TestCLI_Enhancement_TC12(Test):
    uuid = "SOSAIOT-TC-48309"
    description = show_testcase_info(TESTPLAN, "12", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_access_rule_from(self):
        logger.info('access rule from test result: {}'.format(g_acl_check_dict['from']))
        Assertion.assert_equal(g_acl_check_dict['from'], True, "ERR: check access rule from failed")

    def test_01_edit_access_rule_to(self):
        logger.info('access rule to test result: {}'.format(g_acl_check_dict['to']))
        Assertion.assert_equal(g_acl_check_dict['to'], True, "ERR: check access rule to failed")


class TestCLI_Enhancement_TC13(Test):
    uuid = "SOSAIOT-TC-48310"
    description = show_testcase_info(TESTPLAN, "13", description=True)['title']
    jira = 'GEN7-36791'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_list_access_rule(self):
        acllist = accessrulecli.list_access_rule_cli()
        listres = True if ('ipv4' and 'ipv6' and 'restore-defaults') in acllist else False
        logger.info('acl list test result: {}'.format(listres))
        Assertion.assert_equal(listres, True, "ERR: access rule list failed")


class TestCLI_Enhancement_TC14(Test):
    uuid = "SOSAIOT-TC-48311"
    description = show_testcase_info(TESTPLAN, "14", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_access_rule(self):
        logger.info('access rule add result: {}'.format(g_acl_check_dict['uuid']))
        Assertion.assert_equal(g_acl_check_dict['uuid'], True, "ERR: add access rule failed")


class TestCLI_Enhancement_TC15(Test):
    uuid = "SOSAIOT-TC-48312"
    description = show_testcase_info(TESTPLAN, "15", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule(self):
        logger.info('acl modify test result: {}'.format(g_acl_check_dict['modify']))
        Assertion.assert_equal(g_acl_check_dict['modify'], True, "ERR: modify access rule failed")


class TestCLI_Enhancement_TC16(Test):
    uuid = "SOSAIOT-TC-48313"
    description = show_testcase_info(TESTPLAN, "16", description=True)['title']
    jira = 'GEN7-36791'

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_delete_access_rule(self):
        logger.info('acl delete test result: {}'.format(g_acl_check_dict['delete']))
        Assertion.assert_equal(g_acl_check_dict['delete'], True, "ERR: delete access rule failed")
