# this file to config VPN testenv, such as DUT/GW/REMOTE interfaces and route
#

from bin.global_settings import *

interface = network.InterfaceIPv4Api(fw)
localhost = Host('localhost')
access_rule_obj = firewall.AccessRuleApi(fw)
log_set = log.LogCategoryApi(fw)
ui_obj = FWPage()
license_obj = LicenseCli(fw_cli)

class TestConfigTB(Test):
    uuid = 'NonTC'
    goto_teardown = True
    description = "initial testbed"

    @repeat_method(5)
    def test_00_00_00_intial_register_fw(self):
        ipstrlist = Parameter.WANIP.strip().split('.')
        GW = '.'.join(ipstrlist[0:3]) + '.1'
        x1_static = {
            'if'     : 'X1',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.WANIP,
            'mask'   : '255.255.255.0',
            'gateway': GW,
            'dns1'   : Params.G_DNS1,
            'dns2'   : Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
        }
        rc = interface.config_interface(**x1_static)
        time.sleep(3)
        rc &= license_obj.register("online")
        Assertion.assert_equal(rc, True, "ERR: Config X1 and register fw failed")

    def test_00_00_Get_All_PC_Nodes(self):
        PC_list = []
        for node in node_list:
            if re.match('PC\d+', node):
                PC_list.append(node)
        logger.info('PC_list:{}'.format(PC_list))
        for pc_node in PC_list:
            eth1_ip = OpenS.get_node_interface_ip(pc_node, 'eth1')
            logger.info('{}_eth1_IP: {}'.format(pc_node,eth1_ip))
    
    def test_00_01_Configure_Interface(self):
        x1_static = {
            'if'     : 'X1',
            'zone'   : 'WAN',
            'mode'   : 'static',
            'ip'     : Parameter.WANIP,
            'mask'   : '255.255.255.0',
            'gateway': Parameter.WANGW,
            'dns1'   : Parameter.DNSSERVER,
            'mgmt_https': True,
            'mgmt_ssh'  : True,
            'mgmt_ping' : True,
            'fragment_packets': True,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")
    
    def test_00_02_Add_Access_Rule_between_VPN_and_LAN(self):
        rule1 = copy.deepcopy(rule_opt)
        rule2 = copy.deepcopy(rule_opt)
    
        rule1['name'] = 'VPN_to_LAN'
        rule1['from'] = 'VPN'
        rule1['to']   = 'LAN'
    
        rule2['name'] = 'LAN_to_VPN'
        rule2['from'] = 'LAN'
        rule2['to']   = 'VPN'
    
        rc = access_rule_obj.config_accessrule(**rule1)
        rc = rc and access_rule_obj.config_accessrule(**rule2)
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: add access rule between VPN to LAN failed")
    
    def test_00_03_Config_Log_Settings(self):
        logger.info('-'*10+'Enable all VPN log'+'-'*10)
        rc = log_set.enable_all_log_category()
        logger.info('-' * 10 + 'Set the level of LOG as Debug' + '-' * 10)
        rc = rc and log_set.logging_level(level='debug')
    
        logger.info(rc)
        Assertion.assert_equal(rc, True, "ERR: Config log settings failed.")
    
    # def test_00_04_Check_GW_R2_Alive(self):
    #     logger.info('111111GW:')
    #     logger.info(GW)
    #     if (GW == 0):
    #         logger.info('no GW, skip this step')
    #         return()
    #     rc = False
    #     path = cfg_path + 'cfg_if_tel.py'
    #     cmd = 'python3 {} -os=1 --testbed={} -device=VPNGW -if=X0 -zone=LAN -ip=11.11.11.101 -exp=1'.format(path, Params.testbed )
    #     logger.info(cmd)
    #     out = os.popen(cmd).read()
    #     logger.info(out)
    #     if ' Change FW Pass' in out:
    #         rc = True
    #     for i in range(10):
    #         out = os.popen('ping {} -c 2'.format(Parameter.WANGW)).read()
    #         logger.info(out)
    #         if ('100% packet loss' not in out):
    #             logger.info('GW is alive.')
    #             rc = True
    #             break
    #         elif i == 9:
    #             logger.info('GW is not alive.')
    #             rc = False
    #     logger.info(rc)
    #     Assertion.assert_equal(rc, True, "ERR: Check GW R2 Alive failed")
    
    # def test_00_05_restore_GW(self):
    #     if (GW == 0):
    #         logger.info('no GW, skip this step')
    #         return()
    #     logger.info(" {} ".center(20, '-').format('Restore Gateway'))
    #     rc = False
    #     # path = cfg_path + 'restore_gw_rmt_tel.py'
    #     # cmd = 'python3 {} -os=1 --testbed={} -device=VPNGW -if=X0 -zone=LAN -ip=11.11.11.101 -restore=1'.format(path, Params.testbed)
    #     cmd1 = " /SWIFT4.0/COMMON/bin/soniccli.pl -fw 11.11.11.101 -verbatim \
    #     -p refresh_page=netInterfaces.html -p iface_ifnum=0 -p iface_type=6 \
    #     -p iface_name=X0 -p iface_http_mgmt=0 -p iface_https_mgmt=1 \
    #     -p iface_ping_mgmt=1 -p iface_snmp_mgmt=0 -p iface_ssh_mgmt=1 \
    #     -p iface_http_usrLogin=0 -p iface_https_usrLogin=1 \
    #     -p iface_http_redirect_rule=1 -p interface_Zone=LAN \
    #     -p iface_lan_ip=11.11.11.101 -p iface_lan_mask=255.255.255.0 \
    #     -p iface_lan_default_gw=11.11.11.200 "
    #     cmd2 = " curl -A SGMS/2.0libwww-perl/6.13 --cookie 'SessId=BD7471B626D93C829AB22C90881BE4C8' -F 'firmware=@/SWIFT4.0/COMMON/data/prefs/GW/OS_GW.exp' --max-time 30 https://11.11.11.101/import.cgi  --insecure"
    #     logger.info(cmd1)
    #     resp1 = os.popen(cmd1).read()
    #     logger.info(cmd2)
    #     resp2 = os.popen(cmd2).read()
    #     logger.info(resp2)
    #     reg = re.search('restarting_now.*restarting_now', resp2, re.I|re.M)
    #     if reg:
    #         logger.info("import GW Pref file passed, wait for gw restart")
    #         for i in range(10):
    #             time.sleep(10)
    #             out = os.popen('ping {} -c 2'.format(Parameter.WANGW)).read()
    #             logger.info(out)
    #             if ('100% packet loss' not in out):
    #                 logger.info('Ping GW success.')
    #                 rc = True
    #                 break
    #             elif i == 9:
    #                 logger.info('GW is unreachable.')
    #                 rc = False
    #     else:
    #         rc = False
    #         logger.info("import GW Pref file failed")
    #     logger.info(rc)
    #     Assertion.assert_equal(rc, True, "ERR: Restore GW failed")

    def test_00_05_restore_GW(self):
        if (GW == 0):
            logger.info('no GW, skip this step')
            return()
        logger.info(" {} ".center(20, '-').format('Restore Gateway'))
        rc = False
        path = cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device=VPNGW -if=X0 -zone=LAN -ip=11.11.11.101 -restore=1'.format(path, Params.testbed)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(10):
            out = os.popen('ping {} -c 2'.format(Parameter.WANGW)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping GW success.')
                rc = True
                break
            elif i == 9:
                rc = False
                logger.info('Remote GW unreachable.')
        
        logger.info(rc)        
        Assertion.assert_equal(rc, True, "ERR: Restore GW failed")

    def test_00_06_Restore_Remote_FW(self):
        logger.info("check Remote FW alive")
        for i in range(10):
            time.sleep(5)
            out = os.popen('ping {} -c 1 -w 1'.format(Parameter.REMOTEX1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                break
            elif i == 9:
                logger.info('Remote DUT is unreachable. Check the network configuration.')
                ret = os.popen('route -n').read()
                logger.info(ret)

        logger.info('Restore Remote FW...')
        path = cfg_path + 'restore_gw_rmt_tel.py'
        cmd = 'python3 {} -os=1 --testbed={} -device={} -if=X1 -zone=WAN -ip=12.12.1.201 -restore=1'.format(path, Params.testbed, rm_device)
        logger.info(cmd)
        out = os.popen(cmd).read()
        logger.info(out)

        rc = False
        for i in range(30):
            out = os.popen('ping {} -c 2'.format(Parameter.REMOTEX1)).read()
            logger.info(out)
            if ('100% packet loss' not in out):
                logger.info('Ping Remote success.')
                rc = True
                break
            elif i == 29:
                time.sleep(5)
                rc = False
                logger.info('Remote is unreachable.')
        Assertion.assert_equal(rc, True, "ERR: Restore Remote FW failed")
    
    @repeat_method(3)
    def test_00_07_Enable_remote_api_basic(self):
        logger.info(" {} ".center(20, '-').format('Enable Remote Api Basic'))
        logger.info('time sleep 10 sec.')
        time.sleep(10)
        remote = AdminCli(rmt)
        api_dict = {'sonicos-api': True, 'basic': True,}
        try:
            result = remote.sonicos_api(**api_dict)
            if result:
                logger.info('Success enable remote api basic')
            else:
                logger.info('Failed enable remote api basic')
        except KeyError:
            logger.error('Failed enable remote api basic')


