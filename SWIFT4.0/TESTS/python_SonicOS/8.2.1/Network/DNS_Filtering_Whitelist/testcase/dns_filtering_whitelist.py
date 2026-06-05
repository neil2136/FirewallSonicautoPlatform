from definition.initial_param import *


class Test_dns_filtering_whitelist_01(Test):
    uuid = '1521173'
    description = show_testcase_info(Parameter.TESTPLAN, "01", description=True)['title']
    goto_teardown = True

    def test_01_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '01')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_02_config_x1_interface(self):
        logger.info("config x1 interface... ")
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '172.16.1.10',
            'netmask': '255.255.255.0',
            'gateway': '172.16.1.1',
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': False,
            'mgmt_ssh': False,
            'mgmt_ping': False,
        }
        rc = interface_v4 .config_interface(**x1)
        Assertion.assert_equal(rc, True, "ERR: Config X1 IPv4 failed")

    @repeat_method(5)
    def test_03_register_fw(self):
        license = LicenseCli(fw_cli)
        rc = license.register("online")
        Assertion.assert_equal(rc, True, "ERR: register fw failed")

    def test_04_add_dns_policy(self):
        rc = dnspolicy.add_dns_policy(**Parameter.dns_policy_dict)
        Assertion.assert_equal(rc, True, 'ERR: Add dns policy failed!')


class Test_dns_filtering_whitelist_02(Test):
    uuid = '1521174'
    description = show_testcase_info(Parameter.TESTPLAN, "02", description=True)['title']
    goto_teardown = True

    def test_02_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '02')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_02_01_check_default_settings(self):
        rc = dnsfilter.check_dns_filtering_global_settings()
        Assertion.assert_equal(rc['dns_security']['dns_filtering']['use_whitelist'], True, 'ERR: Default dns filtering disable the whitelist!')


@paramunittest.parametrized(
    {'uuid': '1521175', 'tcid': '03', 'enable': True, 'err': 'Enable'},
    {'uuid': '1521176', 'tcid': '04', 'enable': False, 'err': 'Disable'},
)
class Test_dns_filtering_whitelist_03(Test):
    goto_teardown = True

    def setParameters(self, uuid, tcid, enable, err):
        self.uuid = uuid
        self.tcid = tcid
        self.enable = enable
        self.err = err
        self.description = show_testcase_info(Parameter.TESTPLAN, self.tcid, description=True)['title']


    def test_03_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_03_01_enable_whitelist(self):
        opt['dns_security']['dns_filtering']['use_whitelist'] = self.enable
        rc = dnsfilter.config_whitelist(**opt)
        Assertion.assert_equal(rc, True, 'ERR: {} DNS filtering whitelist failed!'.format(self.err))


class Test_dns_filtering_whitelist_06(Test):
    uuid = '1521178'
    description = show_testcase_info(Parameter.TESTPLAN, "06", description=True)['title']
    goto_teardown = True

    def test_06_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '06')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_06_01_enable_whitelist(self):
        opt['dns_security']['dns_filtering']['use_whitelist'] = True
        rc = dnsfilter.config_whitelist(**opt)
        Assertion.assert_equal(rc, True, 'ERR: Enable DNS filtering whitelist failed!')

    def test_06_02_add_whitelist(self):
        rc = dnsfilter.add_dns_whitelist(name='*.ea.com')
        Assertion.assert_equal(rc, True, 'ERR: Add whitelist failed!')

    def test_06_03_check_tsr(self):
        #delete file
        localhost.send_command('rm -f /tmp/mytsr.txt')
        # download tsr
        tsr.download_tsr(filepath='/tmp/mytsr.txt')
        sleep(10)
        flag = False
        cmd = "cat /tmp/mytsr.txt | grep '*.ea.com'"
        if '*.ea.com' in localhost.send_command(cmd):
            flag = True
        Assertion.assert_equal(flag, True, 'ERR: Check TSR failed!')


class Test_dns_filtering_whitelist_10(Test):
    uuid = '1521182'
    description = show_testcase_info(Parameter.TESTPLAN, "10", description=True)['title']
    goto_teardown = True

    def test_10_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_10_01_add_whitelist(self):
        cli_cmds = ['configure', 'dns-security', 'white-list-entry {}'.format(Parameter.white_list), 'commit', 'exit', 'exit']
        rc = fw_cli.do_cli_commands(cli_cmds)
        Assertion.assert_equal(rc, True, 'ERR: Add whitelist by cli command failed!')

    def test_10_02_check_whitelist(self):
        output = dnsfilter.show_whitelist()
        rc = False
        for whitelist in output['dns_security']['white_list_entry']:
            if whitelist['name'] == Parameter.white_list:
                rc = True
        Assertion.assert_equal(rc, True, 'ERR: Added whitelist not found!')

    def test_10_03_delete_whitelist(self):
        cli_cmds = ['configure', 'dns-security', 'no white-list-entry {}'.format(Parameter.white_list), 'commit', 'exit', 'exit']
        rc = fw_cli.do_cli_commands(cli_cmds)
        Assertion.assert_equal(rc, True, 'ERR: Delete whitelist by cli command failed!')

    def test_10_04_check_whitelist(self):
        output = dnsfilter.show_whitelist()
        flag = False
        if Parameter.white_list in str(output):
            flag = True
        Assertion.assert_equal(flag, False, 'ERR: Deleted whitelist is found!')


@paramunittest.parametrized(
    {'uuid': '1521183', 'tcid': '11', 'enable': False, 'err': 'Disable', 'cli_cmd': 'use-whitelist', 'flag': True},
    {'uuid': '1521184', 'tcid': '12', 'enable': True, 'err': 'Enable', 'cli_cmd': 'no use-whitelist', 'flag': False},
)
class Test_dns_filtering_whitelist_11(Test):
    goto_teardown = True

    def setParameters(self, uuid, tcid, enable, err, cli_cmd, flag):
        self.uuid = uuid
        self.tcid = tcid
        self.enable = enable
        self.err = err
        self.cli_cmd = cli_cmd
        self.flag = flag
        self.description = show_testcase_info(Parameter.TESTPLAN, self.tcid, description=True)['title']
   
    def test_11_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, self.tcid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_11_01_config_whitelist(self):
        opt['dns_security']['dns_filtering']['use_whitelist'] = self.enable
        rc = dnsfilter.config_whitelist(**opt)
        Assertion.assert_equal(rc, True, 'ERR: {} DNS filtering whitelist failed!'.format(self.err))

    def test_11_02_config_whitelist_cli(self):
        sleep(10)
        cli_cmds = ['configure', 'dns-security', 'dns-filtering', self.cli_cmd, 'commit', 'exit', 'exit', 'exit']
        rc = fw_cli.do_cli_commands(cli_cmds)
        Assertion.assert_equal(rc, True, 'ERR: Config DNS filtering whitelist by cli failed!')

    def test_11_03_check_whitelist(self):
        rc = dnsfilter.check_dns_filtering_global_settings()
        Assertion.assert_equal(rc['dns_security']['dns_filtering']['use_whitelist'], self.flag, 'ERR:  Whitelist is not same as cli configuration!')


class Test_dns_filtering_whitelist_13(Test):
    uuid = '1521185'
    description = show_testcase_info(Parameter.TESTPLAN, "13", description=True)['title']
    goto_teardown = True

    def test_13_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_13_01_add_whitelists(self):
        for whitelist in Parameter.whitelists:
            rc = dnsfilter.add_dns_whitelist(name=whitelist)
            Assertion.assert_equal(rc, True, 'ERR: Add {} whitelist failed!'.format(whitelist))

    def test_13_02_check_whitelists_cli(self):
        # need debug
        cli_cmds = ['configure', 'show dns-security white-list-entries', 'exit']
        output = fw_cli.do_cli_commands(cli_cmds, 1)[1]
        flag = True
        for whitelist in Parameter.whitelists:
            if whitelist not in str(output):
                flag = False
                break
        Assertion.assert_equal(flag, True, 'ERR: Cli command not fount added whitelist')


class Test_dns_filtering_whitelist_14(Test):
    uuid = '1521186'
    description = show_testcase_info(Parameter.TESTPLAN, "14", description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_14_01_enable_whitelist(self):
        opt['dns_security']['dns_filtering']['use_whitelist'] = True
        rc = dnsfilter.config_whitelist(**opt)
        Assertion.assert_equal(rc, True, 'ERR: Enable DNS filtering whitelist failed!')

    def test_14_02_check_status_cli(self):
        cmd = ['show dns-security dns-filtering base']
        output = fw_cli.do_cli_commands(cmd, 1)[1]
        Assertion.assert_regular(str(output), r'use-whitelist', 'ERR: use_whitelist status shows wrong in cli command!')

    def test_14_03_disable_whitelist(self):
        opt['dns_security']['dns_filtering']['use_whitelist'] = False
        rc = dnsfilter.config_whitelist(**opt)
        Assertion.assert_equal(rc, True, 'ERR: Disable DNS filtering whitelist failed!')

    def test_14_04_check_status_cli(self):
        cmd = ['show dns-security dns-filtering base']
        output = fw_cli.do_cli_commands(cmd, 1)[1]
        Assertion.assert_regular(str(output), r'no use-whitelist', 'ERR: use_whitelist status shows wrong in cli command!')