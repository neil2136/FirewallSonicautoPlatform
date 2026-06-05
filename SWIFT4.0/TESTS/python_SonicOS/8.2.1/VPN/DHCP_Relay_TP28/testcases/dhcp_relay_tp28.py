from definition.settings import *
from definition.utils import *


# Excepted: External dhcp server is used,client can obtain a lease
class TestBaseFun_TC1(Test):
    uuid = "SOSAIOT-TC-54245"
    description = show_testcase_info(TESTPLAN, '1', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_central_dhcp_over_vpn(self):
        logger.info("Central Gateway, Eternal DHCP server")
        central_dict = {
            'internal_dhcp': False,
            'global_vpn': False,
            'remote': False,
            'relay_ip': '0.0.0.0',
            'send_requests': True,
            'dhcp_server_ip_list': [Parameter.LAN_PC],
        }
        rc = dhcpovervpnapi.config_dhcpvpn_centralgw(**central_dict)
        Assertion.assert_equal(rc, True, "ERR: Config central DHCP over VPN failed.")

    def test_03_config_remote_dhcp_over_vpn(self):
        remotegw_dict = {
            'bound_to': 'X0',
            'accept_bridged_wlan_request': True,
            'relay_ip': Parameter.RELAY_IP,
            'management_ip': Parameter.MGMT_IP,
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2',
            # 'static_device_ip_list': ['1.1.1.10','10.1.1.10'],
            # 'static_device_mac_list': ['a112412124da','acbda5115514'],
            # 'excluded_device_mac_list': ['b11231d521c5','ca123456d2f1'],
        }
        rc = rdhcpovervpnapi.config_dhcpvpn_remotegw(**remotegw_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    def test_04_disable_and_enable_central_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_05_check_vpn_status_is_up(self):
        time.sleep(10)
        (res, msg) = centralvpnapi.get_vpn_status('centralvpn')
        logger.info(f'get vpn status res is: {res},msg is: {msg}')
        flag = True if res and msg == 'up' else False
        Assertion.assert_equal(flag, True, "ERR: Config central DHCP over VPN failed.")

    @repeat_method(2)
    def test_06_get_lease_on_client_PC(self):
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        logger.info(f'release result is {res}')
        ParamCases.TC01fw_time = lotimeapi.show_time()
        time.sleep(10)
        ParamCases.TC01dhcplease = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info("Remote PC get IP {} from central LAN PC.".format(ParamCases.TC01dhcplease))
        flag = True if ParamCases.TC01dhcplease else False
        Assertion.assert_equal(flag, True, "ERR: Remote PC gets DHCP lease failed.")

    def test_07_check_central_system_log_event_about_get_lease_through_dhcp_over_vpn(self):
        time.sleep(10)
        getlogres = logmonitorapi.get_log(id=225)
        res = check_log_by_time(ParamCases.TC01fw_time, getlogres, event_id=225)
        Assertion.assert_equal(res, True, "ERR: check log message failed.")

    def test_08_check_central_current_dhcp_over_vpn_leases(self):
        check_lease_dict_TC01_TC02['dhcpleaseip'] = ParamCases.TC01dhcplease
        logger.info(check_lease_dict_TC01_TC02['dhcpleaseip'])
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC01_TC02)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if leasenum == 3 and dyleasenum == 1 and staleasenum == 2 else False
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")

    @repeat_method(2)
    def test_09_verify_ping_between_lan_host_and_dhcplease(self):
        logger.info(f'ParamCases.TC01dhcplease is: {ParamCases.TC01dhcplease}')
        if ParamCases.TC01dhcplease:
            logger.info('need add static route on remote device to central subnet due to remote default route')
            res = add_route_on_pc(RMT_HOST, Parameter.X0_NET, Parameter.R_X0_IP, to_dut='central')
            logger.info(f'adding static route on remote device is :{res}')
            time.sleep(10)
            pingres1 = RMT_HOST.ping_from_eth(ip=Parameter.LAN_PC, eth='eth1')
            time.sleep(10)
            lanhostroute = LAN_HOST.send_command('ip -4 r')
            logger.info(f'lanhostroute is:{lanhostroute}')
            pingres2 = LAN_HOST.ping_from_eth(ip=ParamCases.TC01dhcplease, eth='eth1')
            time.sleep(10)
        else:
            logger.error("no dhcp lease,please check")
        logger.info(f'pingres1: {pingres1}, pingres2: {pingres2}')
        Assertion.assert_equal(pingres1 & pingres2, True, "ERR: Verify ping failed.")

    def test_10_verify_login_remote_gui_by_management_ip(self):
        res = r_login_mgmt_ip.api_logout()
        logger.info(res)
        ret = r_login_mgmt_ip.api_login()
        Assertion.assert_equal(ret, True, "ERR:login remote dut by management ip failed")


# Excepted: External dhcp server is used,client can release a lease.
class TestBaseFun_TC2(Test):
    uuid = "SOSAIOT-TC-54245"
    description = show_testcase_info(TESTPLAN, '2', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_release_lease_on_client_PC(self):
        ParamCases.TC02fw_time = lotimeapi.show_time()
        time.sleep(10)
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        Assertion.assert_equal(res, True, "ERR: Remote PC relase DHCP lease failed.")

    def test_03_check_central_system_log_event_about_release_through_dhcp_over_vpn(self):
        time.sleep(10)
        getlogres = logmonitorapi.get_log(id=224)
        res = check_log_by_time(ParamCases.TC02fw_time, getlogres, event_id=224)
        Assertion.assert_equal(res, True, "ERR: check log message failed.")

    def test_04_check_central_current_dhcp_over_vpn_leases(self):
        logger.info(f'ParamCases.TC01dhcplease is: {ParamCases.TC01dhcplease}')
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC01_TC02)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if leasenum == 2 and dyleasenum == 0 and staleasenum == 2 else False
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")


# Excepted: External server is used,client can renew a lease.
class TestBaseFun_TC3(Test):
    uuid = "SOSAIOT-TC-54245"
    description = show_testcase_info(TESTPLAN, '3', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '03')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_renew_lease_on_client_pc(self):
        flag = False
        ParamCases.TC03dhcplease = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'ParamCases.TC03dhcplease is :{ParamCases.TC03dhcplease}')

        LAN_HOST.send_command(
            f"sed -i 's/{Parameter.R_X0_SCOPE_START}/{Parameter.R_X0_SCOPE_START_RENEW}/g' {dhcpconfpath}")
        LAN_HOST.send_command('service dhcpd restart')
        LAN_HOST.send_command('cat /etc/dhcp/dhcpd.conf')
        ParamCases.TC03fw_time = lotimeapi.show_time()
        time.sleep(10)
        ParamCases.TC03dhcpleaserenew = renew_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'ParamCases.TC03dhcpleaserenew is :{ParamCases.TC03dhcpleaserenew}')
        if ParamCases.TC03dhcpleaserenew and (ParamCases.TC03dhcplease != ParamCases.TC03dhcpleaserenew):
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Remote PC relase DHCP lease failed.")

    def test_03_check_central_system_log_event_about_get_lease_through_dhcp_over_vpn(self):
        time.sleep(10)
        getlogres = logmonitorapi.get_log(id=225)
        res = check_log_by_time(ParamCases.TC03fw_time, getlogres, event_id=225)
        Assertion.assert_equal(res, True, "ERR: check log message failed.")

    def test_04_check_central_current_dhcp_over_vpn_leases(self):
        logger.info(f'ParamCases.TC03dhcplease is: {ParamCases.TC03dhcplease}')
        logger.info(f'ParamCases.TC03dhcpleaserenew is: {ParamCases.TC03dhcpleaserenew}')
        check_lease_dict_TC03['dhcpleaseip'] = [ParamCases.TC03dhcpleaserenew, ParamCases.TC03dhcplease]
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC03)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if (leasenum == 4 and dyleasenum == 2 and staleasenum == 2) or \
                       (leasenum == 3 and dyleasenum == 1 and staleasenum == 2) else False
        if ParamCases.TC03dhcplease in str(leasesinfo):
            ceres = dhcpovervpnapi.delete_dhcp_over_vpn_dynamic_lease(ParamCases.TC03dhcplease)
            reres = rdhcpovervpnapi.delete_dhcp_over_vpn_dynamic_lease(ParamCases.TC03dhcplease)
            logger.info(f'ceres is {ceres}, reres if {reres}')
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")

    @repeat_method(2)
    def test_05_verify_ping_between_lan_host_and_dhcplease(self):
        logger.info(f'ParamCases.TC03dhcpleaserenew is: {ParamCases.TC03dhcpleaserenew}')
        if ParamCases.TC03dhcpleaserenew:

            logger.info('need add static route on remote device to central subnet due to remote default route')
            res = add_route_on_pc(RMT_HOST, Parameter.X0_NET, Parameter.R_X0_IP, to_dut='central')
            logger.info(f'adding static route on remote device is :{res}')

            time.sleep(10)
            pingres1 = RMT_HOST.ping_from_eth(ip=Parameter.LAN_PC, eth='eth1')
            logger.info(f'pingres1 is {pingres1}')
            time.sleep(10)
            lanhostroute = LAN_HOST.send_command('ip -4 r')
            logger.info(f'lanhostroute is:{lanhostroute}')
            pingres2 = LAN_HOST.ping_from_eth(ip=ParamCases.TC03dhcpleaserenew, eth='eth1')
            logger.info(f'pingres2 is {pingres2}')
            time.sleep(10)
        else:
            logger.error("no dhcp lease,please check")
        logger.info(f'pingres1: {pingres1}, pingres2: {pingres2}')
        Assertion.assert_equal(pingres1 & pingres2, True, "ERR: Verify ping failed.")

    def test_06_verify_login_remote_gui_by_management_ip(self):
        res = r_login_mgmt_ip.api_logout()
        logger.info(res)
        ret = r_login_mgmt_ip.api_login()
        Assertion.assert_equal(ret, True, "ERR:login remote dut by management ip failed")

    def test_07_restore_dhcp_server_pool(self):
        cmds = [
            f"sed -i 's/{Parameter.R_X0_SCOPE_START_RENEW} {Parameter.R_X0_SCOPE_END}/{Parameter.R_X0_SCOPE_START} "
            f"{Parameter.R_X0_SCOPE_START}/g' {dhcpconfpath}",
            'service dhcpd restart',
            'cat /etc/dhcp/dhcpd.conf'
        ]
        LAN_HOST.send_commands(cmds)
        release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        ParamCases.TC03dhcplease_restore1 = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'restore1 ip is:{ParamCases.TC03dhcplease_restore1}')

        cmds1 = [
            f"sed -i 's/{Parameter.R_X0_SCOPE_START} {Parameter.R_X0_SCOPE_START}/{Parameter.R_X0_SCOPE_START} "
            f"{Parameter.R_X0_SCOPE_END}/g' {dhcpconfpath}",
            'service dhcpd restart',
            'cat /etc/dhcp/dhcpd.conf'
        ]
        LAN_HOST.send_commands(cmds1)
        release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        ParamCases.TC03dhcplease_restore2 = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'restore2 ip is:{ParamCases.TC03dhcplease_restore2}')

        Assertion.assert_equal(True, True, "ERR: restore dhcp server pool failed")


# Excepted: add static device on remote device,ping succeeds and lease table is showing correctly
class TestBaseFun_TC21(Test):
    uuid = "SOSAIOT-TC-54249"
    description = show_testcase_info(TESTPLAN, '21', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '21')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_get_remote_pc_lan_mac(self):
        flag = False
        # mark --- system
        # out = RMT_HOST.system('ifconfig eth1').decode()
        out = RMT_HOST.send_command('ifconfig eth1')
        rc = re.search(r'HWaddr\s+(\w+:\w+:\w+:\w+:\w+:\w+)', out, re.I | re.S)
        logger.info(rc)
        if rc:
            ParamCases.TC21rlanmac = rc.group(1)
            logger.info(f"Get remote PC MAC {ParamCases.TC21rlanmac}.")
            if len(ParamCases.TC21rlanmac) <= 17:
                flag = True
        Assertion.assert_equal(flag, True, "Error:Get MAC failed.")

    def test_03_add_static_device_on_remote_dhcp_over_vpn(self):
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        logger.info(f'release ip result is :{res}')
        ip_mac_list = {
            Parameter.STATIC_IP: ParamCases.TC21rlanmac,
        }
        rc = rdhcpovervpnapi.add_static_device_remotegw(**ip_mac_list)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    # after add static device on remote,then vpn becomes down,need disable and enable it
    def test_04_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_05_config_remote_pc_ip(self):
        RMT_HOST.send_command(f'ifconfig eth1 {Parameter.STATIC_IP}/24 up')
        time.sleep(3)
        Assertion.assert_equal(True, True, "ERR: Config remote PC static IP failed.")

    @repeat_method(2)
    def test_06_verify_ping_between_lan_host_and_dhcplease(self):
        logger.info('need add static route on remote device to central subnet due to remote default route')
        res = add_route_on_pc(RMT_HOST, Parameter.X0_NET, Parameter.R_X0_IP, to_dut='central')
        logger.info(f'adding static route on remote device is :{res}')

        pingres1 = RMT_HOST.ping_from_eth(ip=Parameter.LAN_PC, eth='eth1')
        time.sleep(10)
        lanhostroute = LAN_HOST.send_command('ip -4 r')
        logger.info(f'lanhostroute is:{lanhostroute}')
        pingres2 = LAN_HOST.ping_from_eth(ip=Parameter.STATIC_IP, eth='eth1')
        time.sleep(10)
        logger.info(f'pingres1: {pingres1}, pingres2: {pingres2}')
        Assertion.assert_equal(pingres1 & pingres2, True, "ERR: Verify ping failed.")

    def test_07_check_central_current_dhcp_over_vpn_leases(self):
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC21)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if leasenum == 3 and dyleasenum == 0 and staleasenum == 3 else False
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")


# Excepted: delete static device on remote device,vpn is down,client cannot get a lease
class TestBaseFun_TC23(Test):
    uuid = "SOSAIOT-TC-54250"
    description = show_testcase_info(TESTPLAN, '23', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '23')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_check_vpn_status_is_up(self):
        flag = False
        (vpnstatusres, info) = centralvpnapi.get_vpn_status('centralvpn')
        if info == 'up':
            ParamCases.TC23vpnstatusbefore = vpnstatusres
            logger.info(f'ParamCases.TC23vpnstatusbefore is : {ParamCases.TC23vpnstatusbefore}')
            flag = True
        Assertion.assert_equal(flag, True, "ERR: check lease table on central gateway failed.")

    def test_03_check_vpn_status_is_down_after_delete_static_device(self):
        flag = False
        logger.info(f'ParamCases.TC23vpnstatusbefore is : {ParamCases.TC23vpnstatusbefore}')
        if ParamCases.TC23vpnstatusbefore:
            ip_mac_list = {
                Parameter.STATIC_IP: ParamCases.TC21rlanmac,
            }
            rc = rdhcpovervpnapi.del_static_device_remotegw(**ip_mac_list)
            if rc:
                time.sleep(10)
                (vpnstatusafter, info) = centralvpnapi.get_vpn_status('centralvpn')
                if not vpnstatusafter and info == 'down':
                    flag = True
        else:
            logger.error('vpn is down,please make sure it is up before remove static device')
        Assertion.assert_equal(flag, True, "ERR: check vpn status after remove static device faild")

    def test_05_check_central_current_dhcp_over_vpn_leases(self):
        time.sleep(15)
        flag = False
        output = dhcpovervpnapi.show_dhcp_leases()
        if not output:
            flag = True
            logger.info('there is no entries in total on central gateway due to tunnel down')
        Assertion.assert_equal(flag, True, "ERR: check lease table on central gateway failed.")

    # after delete static device on remote,vpn becomes down,need disable and enable it
    def test_06_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")


# Excepted: add exculded device on remote device,client cannot get a lease through dhcp over vpn
class TestBaseFun_TC25(Test):
    uuid = "SOSAIOT-TC-54251"
    description = show_testcase_info(TESTPLAN, '25', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '25')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_add_excluded_lan_device_on_remote_dhcp_over_vpn(self):
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        logger.info(f'release ip result is :{res}')
        excluded_device_mac_list = [ParamCases.TC21rlanmac]
        rc = rdhcpovervpnapi.add_exclude_device_remotegw(*excluded_device_mac_list)
        Assertion.assert_equal(rc, True, "ERR: add excluded lan device on remote dut failed.")

    # after add exculded lan device on remote,vpn becomes down,need disable and enable to make it up
    def test_03_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_04_get_lease_on_client_pc(self):
        flag = False
        dhcplease = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'dhcplease is : {dhcplease}')
        if not dhcplease:
            flag = True
        else:
            logger.error("Remote eth1 got IP from central network, but it should not.")
        Assertion.assert_equal(flag, True, "ERR: Remote PC gets DHCP lease but it should not.")


# Excepted: after delete excluded device on remote device,client can get a lease through dhcp over vpn
class TestBaseFun_TC27(Test):
    uuid = "SOSAIOT-TC-54252"
    description = show_testcase_info(TESTPLAN, '27', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '27')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_remove_excluded_lan_device_on_remote_dhcp_over_vpn(self):
        excluded_device_mac_list = [ParamCases.TC21rlanmac]
        rc = rdhcpovervpnapi.del_exclude_device_remotegw(*excluded_device_mac_list)
        Assertion.assert_equal(rc, True, "ERR: delete excluded lan device on remote dut failed.")

    # after delete exculded lan device on remote,vpn becomes down,need disable and enable to make it up
    def test_03_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_04_get_lease_on_client_pc(self):
        flag = False
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        logger.info(f'release result is {res}')
        dhcplease = get_dhcp_lease(RMT_HOST, 'eth1')
        logger.info(f'get dhcp lease is : {dhcplease}')
        if dhcplease:
            logger.info("Remote PC get IP {} from central LAN PC.".format(dhcplease))
            flag = True
        Assertion.assert_equal(flag, True, "ERR: Remote PC gets DHCP lease failed.")

    def test_05_release_x0_ip_on_client_pc(self):
        res = release_dhcp_lease(RMT_HOST, 'eth1', Parameter.X0_NET, Parameter.R_X0_IP)
        logger.info(f'release ip result is :{res}')
        Assertion.assert_equal(True, True, "ERR: Remote PC gets DHCP lease failed.")


# Excepted: change dhcp lease bound to X2 with lan zone,client can get a lease through dhcp over vpn
class TestBaseFun_TC65(Test):
    uuid = "SOSAIOT-TC-54255"
    description = show_testcase_info(TESTPLAN, '65', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '65')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_remote_dhcp_over_vpn_bound_interface_from_x0_to_x2(self):
        remotegw_dict = {
            'bound_to': 'X2',
            'accept_bridged_wlan_request': True,
            'relay_ip': Parameter.RELAY_IP_X2,
            'management_ip': Parameter.MGMT_IP_X2,
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2',
            # 'static_device_ip_list': ['1.1.1.10','10.1.1.10'],
            # 'static_device_mac_list': ['a112412124da','acbda5115514'],
            # 'excluded_device_mac_list': ['b11231d521c5','ca123456d2f1'],
        }
        rc = rdhcpovervpnapi.config_dhcpvpn_remotegw(**remotegw_dict)
        Assertion.assert_equal(rc, True, "ERR: Config remote DHCP over VPN failed.")

    # change dhcp lease bound to X2,vpn is down,need disable and enable to make it up
    def test_03_disable_and_enable_central_and_remote_vpn_policy(self):
        res1 = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res2 = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        time.sleep(3)
        res3 = centralvpnapi.edit_vpn_policy(**s2svpn_main_central_vpn_disable)
        time.sleep(3)
        res4 = centralvpnapi.edit_vpn_policy(**s2svpn_main_central_vpn_enable)
        time.sleep(3)
        Assertion.assert_equal(res1 & res2 & res3 & res4, True, "ERR: Re-negociate VPN policy failed.")

    def test_04_get_lease_on_x2_client_pc(self):
        res = release_dhcp_lease(RMT_HOST, 'eth2', Parameter.X0_NET, Parameter.R_X2_IP)
        logger.info(f'release result is {res}')
        ParamCases.TC65fw_time = lotimeapi.show_time()
        time.sleep(10)
        # add_route_on_pc(LAN_HOST, Parameter.R_X2_NET, Parameter.X0_IP, to_dut='remote')
        ParamCases.TC65dhcplease = get_dhcp_lease(RMT_HOST, 'eth2')
        logger.info(f'Remote PC get IP {ParamCases.TC65dhcplease} from central LAN PC.')
        flag = True if ParamCases.TC65dhcplease else False
        Assertion.assert_equal(flag, True, "ERR: Remote PC gets DHCP lease failed.")

    def test_05_check_central_current_dhcp_over_vpn_leases(self):
        check_lease_dict_TC65['dhcpleaseip'] = ParamCases.TC65dhcplease
        logger.info(check_lease_dict_TC65['dhcpleaseip'])
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC65)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if leasenum == 3 and dyleasenum == 1 and staleasenum == 2 else False
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")

    @repeat_method(2)
    def test_08_verify_ping_between_lan_host_and_dhcplease(self):
        logger.info(f'ParamCases.TC65dhcplease is: {ParamCases.TC65dhcplease}')
        if ParamCases.TC65dhcplease:
            logger.info('need add static route on remote device to central subnet due to remote default route')
            res = add_route_on_pc(RMT_HOST, Parameter.X0_NET, Parameter.R_X2_IP, to_dut='central')
            logger.info(f'adding static route on remote device is :{res}')
            time.sleep(10)
            pingres1 = RMT_HOST.ping_from_eth(ip=Parameter.LAN_PC, eth='eth2')
            time.sleep(10)
            lanhostroute = LAN_HOST.send_command('ip -4 r')
            logger.info(f'lanhostroute is:{lanhostroute}')
            pingres2 = LAN_HOST.ping_from_eth(ip=ParamCases.TC65dhcplease, eth='eth1')
            time.sleep(10)
        else:
            logger.error("error:no dhcp lease,please check")
        logger.info(f'pingres1: {pingres1}, pingres2: {pingres2}')
        Assertion.assert_equal(pingres1 & pingres2, True, "ERR: Verify ping failed.")

    def test_09_verify_login_remote_gui_by_management_ip(self):
        res = r_login_mgmt_ip_x2.api_logout()
        logger.info(res)
        ret = r_login_mgmt_ip_x2.api_login()
        Assertion.assert_equal(ret, True, "ERR:login remote dut by management ip failed")


# Excepted:change dhcp lease bound to X2 with DMZ zone,client can get a lease through dhcp over vpn
class TestBaseFun_TC66(Test):
    uuid = "SOSAIOT-TC-54256"
    description = show_testcase_info(TESTPLAN, '66', description=True)['title']

    def test_01_show_testcase_info(self):
        show_testcase_info(TESTPLAN, '66')
        Assertion.assert_equal(True, True, "ERR: show test case info failed")

    def test_02_config_remote_x2_to_dmz_zone(self):
        logger.info("config remote x2 interface ... ")
        time.sleep(5)
        r_x2_static['zone'] = 'DMZ'
        rc = r_interface_api.config_interface(**r_x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config remote X2 to static failed")

    def test_03_disable_and_enable_remote_vpn_policy(self):
        res = remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_disable)
        time.sleep(3)
        res &= remotevpnapi.edit_vpn_policy(**s2svpn_main_remote_vpn_enable)
        Assertion.assert_equal(res, True, "ERR: Re-negociate remote VPN policy failed.")

    def test_04_get_lease_on_x2_client_pc(self):
        res = release_dhcp_lease(RMT_HOST, 'eth2', Parameter.X0_NET, Parameter.R_X2_IP)
        logger.info(f'release result is {res}')
        ParamCases.TC66fw_time = lotimeapi.show_time()
        time.sleep(10)
        ParamCases.TC66dhcplease = get_dhcp_lease(RMT_HOST, 'eth2')
        logger.info(f'Remote PC get IP {ParamCases.TC66dhcplease} from central LAN PC.')
        flag = True if ParamCases.TC66dhcplease else False
        Assertion.assert_equal(flag, True, "ERR: Remote PC gets DHCP lease failed.")

    def test_05_check_central_current_dhcp_over_vpn_leases(self):
        check_lease_dict_TC66['dhcpleaseip'] = ParamCases.TC66dhcplease
        logger.info(check_lease_dict_TC66['dhcpleaseip'])
        leasesinfo = dhcpovervpnapi.show_dhcp_leases()
        (leasenum, dyleasenum, staleasenum) = check_dhcp_over_vpn_lease_num(leasesinfo, check_lease_dict_TC66)
        logger.info(f'total lease num :{leasenum},dynamic lease num :{dyleasenum}, static lease num :{staleasenum}')
        flag = True if leasenum == 3 and dyleasenum == 1 and staleasenum == 2 else False
        Assertion.assert_equal(flag, True, "ERR: check lease table failed.")

    @repeat_method(2)
    def test_06_verify_ping_between_lan_host_and_dhcplease(self):
        logger.info(f'ParamCases.TC66dhcplease is: {ParamCases.TC66dhcplease}')
        if ParamCases.TC66dhcplease:
            logger.info('need add static route on remote device to central subnet due to remote default route')
            res = add_route_on_pc(RMT_HOST, Parameter.X0_NET, Parameter.R_X2_IP, to_dut='central')
            logger.info(f'adding static route on remote device is :{res}')
            time.sleep(10)
            pingres1 = RMT_HOST.ping_from_eth(ip=Parameter.LAN_PC, eth='eth2')
            time.sleep(10)
            lanhostroute = LAN_HOST.send_command('ip -4 r')
            logger.info(f'lanhostroute is:{lanhostroute}')
            pingres2 = LAN_HOST.ping_from_eth(ip=ParamCases.TC66dhcplease, eth='eth1')
            time.sleep(10)
        else:
            logger.error("no dhcp lease,please check")
        logger.info(f'pingres1: {pingres1}, pingres2: {pingres2}')
        Assertion.assert_equal(pingres1 & pingres2, True, "ERR: Verify ping failed.")

    def test_07_verify_login_remote_gui_by_management_ip(self):
        res = r_login_mgmt_ip_x2.api_logout()
        logger.info(res)
        ret = r_login_mgmt_ip_x2.api_login()
        Assertion.assert_equal(ret, True, "ERR:login remote dut by management ip failed")

    def test_08_release_x2_ip_on_client_pc(self):
        res = release_dhcp_lease(RMT_HOST, 'eth2', Parameter.X0_NET, Parameter.R_X2_IP)
        logger.info(f'release result is {res}')
        Assertion.assert_equal(True, True, "ERR: Remote PC gets DHCP lease failed.")
