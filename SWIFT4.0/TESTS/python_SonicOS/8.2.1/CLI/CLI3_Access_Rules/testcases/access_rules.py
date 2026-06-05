from settings import *
from utils import *


# check acl uuid configure: access-rule ipv4 uuid...
# include case 17,02,01,05,07,08,09,10
class Test_ACLUUIDTests(Test):
    uuid = 'NonTC'

    def test_01_add_access_rule(self):
        addres = accessrulecli.add_access_rule(**access_rule_dict)
        logger.info('add a access rule result: {}'.format(addres))

        # check acl comment
        checkres = accessrulecli.show_access_rules(**show_access_rule_dict)
        acluuid = get_acl_uuid(checkres, access_rule_dict['comment'])
        if acluuid == 'fail':
            Assertion.assert_equal(
                False, True, "error: can not get the uuid from acl.")
        else:
            check_uuid_cfg_dict['comment'] = True

        # storage the acl uuid to a dict
        access_rule_uuid_dict['uuid'] = acluuid

        # check acl uuid
        show_access_rule_uuid_dict['type'] = 'uuid ' + acluuid
        checkres = accessrulecli.show_access_rules(
            **show_access_rule_uuid_dict)
        check_uuid_cfg_dict['uuid'] = True if 'Access Rule not found' not in checkres else False

        Assertion.assert_equal(
            check_uuid_cfg_dict['uuid'], True, "ERR: add access rule failed")

    def test_02_edit_access_rule(self):
        if not check_uuid_cfg_dict['uuid']:
            # init the acl table
            initres = accessrulecli.restore_access_rule()
            logger.info('restore access rule result: {}'.format(initres))
            Assertion.assert_equal(
                False, True, "error: can not find acl uuid, skip all edit case.")

        # form test
        tempfrom = []
        fromzones = ['any', 'DMZ', 'WAN', 'WLAN', 'X0', 'LAN']
        for zone in fromzones:
            access_rule_uuid_dict['from_new'] = zone
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info('edit access rule to from result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'from ' + zone in checkres:
                tempfrom.append(1)
                logger.info(
                    'edit access rule from to {} successful.'.format(zone))
            else:
                tempfrom.append(0)
                logger.info('check access rule from to {} failed'.format(zone))
        check_uuid_cfg_dict['from'] = all(tempfrom)
        # init acl uuid dict
        del access_rule_uuid_dict['from_new']

        # to test
        tempto = []
        tozones = ['any', 'DMZ', 'WLAN', 'WAN']
        for zone in tozones:
            access_rule_uuid_dict['to_new'] = zone
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info('edit access rule to to result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'to ' + zone in checkres:
                tempto.append(1)
                logger.info(
                    'edit access rule to to {} successful.'.format(zone))
            else:
                tempto.append(0)
                logger.info('check access rule to to {} failed'.format(zone))
        check_uuid_cfg_dict['to'] = all(tempto)
        # init acl uuid dict
        del access_rule_uuid_dict['to_new']

        #  source test
        tempsource = []
        sourcelist = [
            source_ao_dict['range']['name'],
            source_ao_dict['network']['name'],
            source_ao_dict['host']['name']]
        for source in sourcelist:
            access_rule_uuid_dict['src_name_new'] = source
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info('edit access rule source result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'source address name ' + source in checkres:
                tempsource.append(1)
                logger.info(
                    'edit access rule source to {} successful.'.format(source))
            else:
                tempsource.append(0)
                logger.info(
                    'check access rule source to {} failed'.format(source))
        check_uuid_cfg_dict['source'] = all(tempsource)
        # init acl uuid dict
        del access_rule_uuid_dict['src_name_new']

        # destination test
        tempdest = []
        destinationlist = [
            dest_ao_dict['range']['name'],
            dest_ao_dict['network']['name'],
            dest_ao_dict['host']['name']]
        for destination in destinationlist:
            access_rule_uuid_dict['dst_name_new'] = destination
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info(
                'edit access rule destination result: {}'.format(editres))

            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'destination address name ' + destination in checkres:
                tempdest.append(1)
                logger.info(
                    'edit access rule destination to {} successful.'.format(destination))
            else:
                tempdest.append(0)
                logger.info(
                    'check access rule destination to {} failed'.format(destination))
        check_uuid_cfg_dict['destination'] = all(tempdest)
        # init acl uuid dict
        del access_rule_uuid_dict['dst_name_new']

        # Service test
        tempserv = []
        servicelist = ['SSH', 'HTTP', 'HTTPS']
        for service in servicelist:
            access_rule_uuid_dict['service_name_new'] = service
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info('edit access rule service result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'service name ' + service in checkres:
                tempserv.append(1)
                logger.info(
                    'edit access rule service to {} successful.'.format(service))
            else:
                tempserv.append(0)
                logger.info(
                    'check access rule service {} failed'.format(service))
        check_uuid_cfg_dict['service'] = all(tempserv)
        # init acl uuid dict
        del access_rule_uuid_dict['service_name_new']

        # Action test
        actionname = []
        actionlist = ['allow', 'discard', 'deny']
        for action in actionlist:
            access_rule_uuid_dict['action_new'] = action
            editres = accessrulecli.edit_access_rule_by_uuid(
                **access_rule_uuid_dict)
            logger.info('edit access rule action result: {}'.format(editres))
            checkres = accessrulecli.show_access_rules(
                **show_access_rule_uuid_dict)
            if 'action ' + action in checkres:
                actionname.append(1)
                logger.info(
                    'edit access rule action to {} successful.'.format(action))
            else:
                actionname.append(0)
                logger.info(
                    'check access rule action to {} failed'.format(action))
        check_uuid_cfg_dict['action'] = all(actionname)
        # init acl uuid dict
        del access_rule_uuid_dict['action_new']

        # init the acl table
        initres = accessrulecli.restore_access_rule()
        logger.info('restore access rule result: {}'.format(initres))
        Assertion.assert_equal(
            all(check_uuid_cfg_dict),
            True,
            "ERR: eidt access rule via uuid failed")


class Test_17_access_rule_comment_check(Test):
    uuid = "SOSAIOT-TC-48419"
    description = show_testcase_info(TESTPLAN,
                                     "17", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_access_rule_comment(self):
        logger.info(
            'acl comment test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['comment']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['comment'], True, "ERR: modify comment failed")


class Test_02_access_rule_uuid_check(Test):
    uuid = "SOSAIOT-TC-48409"
    description = show_testcase_info(TESTPLAN,
                                     "02", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_access_rule(self):
        logger.info(
            'acl uuid test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['uuid']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['uuid'], True, "ERR: check uuid failed")


class Test_01_access_rule_from_check(Test):
    uuid = "SOSAIOT-TC-48405"
    description = show_testcase_info(TESTPLAN,
                                     "01", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_access_rule_from(self):
        logger.info(
            'acl from test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['from']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['from'],
            True,
            "ERR: check access rule from failed")


class Test_05_access_rule_to_check(Test):
    uuid = "SOSAIOT-TC-48412"
    description = show_testcase_info(TESTPLAN,
                                     "05", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_edit_access_rule_to(self):
        logger.info(
            'acl to test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['to']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['to'],
            True,
            "ERR: check access rule to failed")


class Test_07_access_rule_source_check(Test):
    uuid = "SOSAIOT-TC-48414"
    description = show_testcase_info(TESTPLAN,
                                     "07", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '07')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule_source(self):
        logger.info(
            'acl source test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['source']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['source'],
            True,
            "ERR: modify access rule source failed")


class Test_08_access_rule_destination_check(Test):
    uuid = "SOSAIOT-TC-48415"
    description = show_testcase_info(TESTPLAN,
                                     "08", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule_destination(self):
        logger.info(
            'acl destination test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['destination']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['destination'],
            True,
            "ERR: modify destination failed")


class Test_09_access_rule_service_check(Test):
    uuid = "SOSAIOT-TC-48416"
    description = show_testcase_info(TESTPLAN,
                                     "09", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '09')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_access_rule_service(self):
        logger.info(
            'acl service test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['service']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['service'], True, "ERR: modify service failed")


class Test_10_access_rule_action_check(Test):
    uuid = "SOSAIOT-TC-48406"
    description = show_testcase_info(TESTPLAN,
                                     "10", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_access_rule_action(self):
        logger.info(
            'acl action test by uuid cmd result: {}'.format(
                check_uuid_cfg_dict['action']))
        Assertion.assert_equal(
            check_uuid_cfg_dict['action'],
            True,
            "ERR: modify access rule action failed")


# execute independently to avoid conflicts with other configurations
class Test_11_access_rule_user_check(Test):
    uuid = "SOSAIOT-TC-48407"
    description = show_testcase_info(TESTPLAN,
                                     "11", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_add_access_rule(self):
        addres = accessrulecli.add_access_rule(**access_rule_dict)
        Assertion.assert_equal(addres, True, "ERR: add a access rule failed")

    def test_02_check_access_rule_users(self):
        userres = True
        userlist = ['guests', 'administrator', 'group Everyone']
        for include in userlist:
            edit_access_rule_dict['users_included'] = include
            editres = accessrulecli.edit_access_rule(**edit_access_rule_dict)
            logger.info('edit access rule result: {}'.format(editres))

            showres = accessrulecli.show_access_rules(
                **show_access_rule_dict)
            splitres = filter_access_rule(showres, access_rule_dict['comment'])
            if 'users included ' + include in splitres:
                logger.info('modify access rule users included successful.')
            else:
                userres = False
                logger.info(
                    'check access rule users included {} failed'.format(userres))
        # init users included to all
        edit_access_rule_dict['users_included'] = 'all'
        for exclude in userlist:
            edit_access_rule_dict['users_excluded'] = exclude
            editres = accessrulecli.edit_access_rule(**edit_access_rule_dict)
            logger.info('edit access rule result: {}'.format(editres))

            showres = accessrulecli.show_access_rules(
                **show_access_rule_dict)
            splitres = filter_access_rule(showres, access_rule_dict['comment'])
            if 'users excluded ' + exclude in splitres:
                logger.info('modify access rule users excluded successful.')
            else:
                userres = False
                logger.info(
                    'check access rule users excluded {} failed'.format(userres))

        # init the acl table
        initres = accessrulecli.restore_access_rule()
        logger.info('restore access rule result: {}'.format(initres))
        Assertion.assert_equal(
            userres, True, "ERR: modify access rule user failed")


# check non uuid configure:  access-rule ipv4 from LAN to WAN action deny...
# include case 18,04,13,15,16,06,03
class Test_ACLNonUUIDTests(Test):
    uuid = 'NonTC'

    def test_01_add_access_rule(self):
        initres = accessrulecli.restore_access_rule()
        logger.info('restore access rule result: {}'.format(initres))

        addres = accessrulecli.add_access_rule(**access_rule_dict)
        Assertion.assert_equal(addres, True, "ERR: add a access rule failed")

    def test_02_edit_access_rule(self):
        # enable test
        tempenable = []
        enablelist = ['no enable', 'enable']
        for newenable in enablelist:
            edit_access_rule_dict['new_enable'] = newenable
            editres = accessrulecli.edit_access_rule(**edit_access_rule_dict)
            logger.info('edit access rule result: {}'.format(editres))

            showres = accessrulecli.show_access_rules(
                **show_access_rule_dict)
            splitres = filter_access_rule(showres, access_rule_dict['comment'])
            if newenable in splitres:
                tempenable.append(1)
                logger.info(
                    'modify access rule enable to {} successful.'.format(newenable))
            else:
                tempenable.append(0)
                logger.info(
                    'check access rule enable to {} failed'.format(newenable))
        check_nonuuid_cfg_dict['enable'] = all(tempenable)
        # init access_rule_dict
        edit_access_rule_dict['new_enable'] = ''

        # modify test
        edit_access_rule_dict['action_new'] = 'allow'
        edit_access_rule_dict['flow-reporting'] = True
        edit_access_rule_dict['packet-monitoring'] = True
        edit_access_rule_dict['botnet-filter'] = True
        edit_access_rule_dict['priority'] = 42
        editres = accessrulecli.edit_access_rule(**edit_access_rule_dict)
        logger.info('edit access rule result: {}'.format(editres))

        checkres = accessrulecli.show_access_rules(**show_access_rule_dict)
        splitres = filter_access_rule(checkres, access_rule_dict['comment'])
        logger.info('check the accesss rule result: {}'.format(splitres))
        check_nonuuid_cfg_dict['action'] = True if 'action allow' in splitres else False
        check_nonuuid_cfg_dict['flowreport'] = True if 'no flow-reporting' not in splitres else False
        check_nonuuid_cfg_dict['packetmonitor'] = True if 'no packet-monitoring' not in splitres else False
        check_nonuuid_cfg_dict['botnetfilter'] = True if 'no botnet-filter' not in splitres else False
        check_nonuuid_cfg_dict['priority'] = True if 'priority manual 42' in splitres else False

        # restore default test
        res = accessrulecli.restore_access_rule()
        logger.info('restore access rule result: {}'.format(res))
        showres = accessrulecli.show_access_rules(**show_access_rule_dict)
        if access_rule_dict['comment'] not in showres:
            check_nonuuid_cfg_dict['restore'] = True

        check_nonuuid_cfg_dict['modify'] = all(
            value == 1 for value in check_nonuuid_cfg_dict.values())
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['modify'],
            True,
            "ERR: edit access rule failed")


class Test_18_access_rule_enable_check(Test):
    uuid = "SOSAIOT-TC-48408"
    description = show_testcase_info(TESTPLAN,
                                     "18", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_check_access_rule_enable(self):
        logger.info(
            'acl enable test result: {}'.format(
                check_nonuuid_cfg_dict['enable']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['enable'],
            True,
            "ERR: modify enable failed")


class Test_04_access_rule_modify_check(Test):
    uuid = "SOSAIOT-TC-48411"
    description = show_testcase_info(TESTPLAN,
                                     "04", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '04')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule(self):
        logger.info(
            'acl modify test result: {}'.format(
                check_nonuuid_cfg_dict['modify']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['modify'],
            True,
            "ERR: modify access rule failed")


class Test_13_access_rule_flow_report_check(Test):
    uuid = "SOSAIOT-TC-48417"
    description = show_testcase_info(TESTPLAN,
                                     "13", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule_flow_report(self):
        logger.info(
            'acl flow report test result: {}'.format(
                check_nonuuid_cfg_dict['flowreport']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['flowreport'],
            True,
            "ERR: modify flow-reporting failed")


class Test_15_access_rule_botnet_filter_check(Test):
    uuid = "SOSAIOT-TC-48418"
    description = show_testcase_info(TESTPLAN,
                                     "15", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule_botnet_filter(self):
        logger.info(
            'acl botnet filter test result: {}'.format(
                check_nonuuid_cfg_dict['botnetfilter']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['botnetfilter'],
            True,
            "ERR: modify botnet-filter failed")


class Test_16_access_rule_packet_monitoring_check(Test):
    uuid = '1088349'
    description = show_testcase_info(TESTPLAN,
                                     "16", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_access_rule_packet_monitoring(self):
        logger.info(
            'acl packet monitoring test result: {}'.format(
                check_nonuuid_cfg_dict['packetmonitor']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['packetmonitor'],
            True,
            "ERR: modify packet-monitoring failed")


class Test_06_access_rule_priority_check(Test):
    uuid = "SOSAIOT-TC-48413"
    description = show_testcase_info(TESTPLAN,
                                     "06", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_modify_priority_to_manual(self):
        logger.info(
            'acl priority test result: {}'.format(
                check_nonuuid_cfg_dict['priority']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['priority'],
            True,
            "error: modify acl priority failed")


class Test_03_access_rule_restore_defaults_check(Test):
    uuid = "SOSAIOT-TC-48410"
    description = show_testcase_info(TESTPLAN,
                                     "03", description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_01_restore_access_rule(self):
        logger.info('acl restore test result: {}'.format(
            check_nonuuid_cfg_dict['restore']))
        Assertion.assert_equal(
            check_nonuuid_cfg_dict['restore'],
            True,
            "error: acl restore-defaults test failed")
