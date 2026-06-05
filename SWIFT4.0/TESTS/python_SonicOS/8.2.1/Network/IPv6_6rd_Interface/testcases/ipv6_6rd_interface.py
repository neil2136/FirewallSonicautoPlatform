from settings import *


ip = Parameter.DUT_X0_IP
fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
interface = network.InterfaceIPv4Api(fw)
interface = network.InterfaceIPv4Api(fw)
inter_v6_obj = network.InterfaceIPv6Api(fw)
route_obj = network.RoutePolicyApi(fw)
ao_obj = network.AddressobjectsApi(fw)
ao_cli = AddressObjectCli(fw_cli)
pkg_api = system.PacketmonitorApi(fw)
x2_dhcp_ip = ''
x3_pppoe_ip = ''

def check_packet(src=None, proto=None):
    packets = pkg_api.export_captured_packets()
    # logger.info(packets)
    for packet in re.split('Packet number: \d+\*', packets):
        if re.search(r''+ f'Src=\[{src}\]' +'', packet, re.I) and re.search(r''+ f'IP Type: {proto}' +'', packet, re.I):
            logger.info(f'Got {proto} packet from {src} \n {packet}')
            return True
    logger.info(f'Not get {proto} packet from {src}')
    return False    

def check_packet2(src=None, proto=None,dst=None):
    packets = pkg_api.export_captured_packets()
    # logger.info(packets)
    for packet in re.split('Packet number: \d+\*', packets):
        if re.search(r''+ f'Src=\[{src}\]' +'', packet, re.I) and re.search(r''+ f'IP Type: {proto}' +'', packet, re.I) \
            and re.search(r''+ f'Dst=\[{dst}\]' +'', packet, re.I):
            logger.info(f'Got {proto} packet from {src} ')
            return True
    logger.info(f'Not get {proto} packet from {src}')
    return False    


class Test_05_Config_for_6rdPrefix(Test):
    uuid = '1503473'
    description= show_testcase_info(Parameter.TESTPLAN, '05', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '05')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_05_01_add_6rd_tunnel_interface_to_dhcp(self):
        dhcp_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': True,
        }
        logger.info('Add 6rd tunnel interface with dhcp mode.')
        rc = inter_v6_obj.add_tunnel_interface(**dhcp_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp .")

    def test_05_02_add_6rd_tunnel_interface_to_manual(self):
        manual_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': False,
            '6rd_prefix': '3::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }
        rc = inter_v6_obj.edit_tunnel_interface(**manual_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp or manual failed.")

    def test_05_03_set_wrong_prefix(self):
        manual_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': False,
            '6rd_prefix': '1::1::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }   
        logger.info('set wrong 6rd prefix to 1::1::')     
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**manual_6rd, msg=True)
        Assertion.assert_regular(msg['status']['info'][0]['message'], "property 'prefix': invalid format", "ERR: set wrong prefix failed.")

    def test_05_04_set_link_local_or_multicast_prefix(self):
        manual_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': False,
            '6rd_prefix': 'fe80::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }   
        logger.info('set 6rd prefix to link_local address: fe80::')     
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**manual_6rd, msg=True)
        logger.info(msg)
        manual_6rd['6rd_prefix'] = 'ff02::'
        logger.info('set 6rd prefix to multicast address: ff02::')     
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**manual_6rd, msg=True)
        logger.info(msg)
        Assertion.assert_regular(msg['status']['info'][0]['message'], "IPv6 Interface number: Invalid 6rd Prefix, only non-link-local unicast address is allowed.", "ERR: set 6rd prefix to link local or multicast failed.")

    def test_05_05_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_08_Config_for_6rdBRIPv4(Test):
    uuid = '1503474'
    description= show_testcase_info(Parameter.TESTPLAN, '08', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '08')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_08_01_add_6rd_tunnel_interface_to_dhcp(self):
        logger.info('Add 6rd tunnel interface with dhcp mode.')
        rc = interface.config_interface(**x2_dhcp_dict)
        rc &= inter_v6_obj.add_tunnel_interface(**DHCP_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp .")

    def test_08_02_add_6rd_ti_to_manual_with_proper_ip(self):
        ref = copy.deepcopy(Manual_6rd)
        rc = inter_v6_obj.edit_tunnel_interface(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with  manual proper ip failed.")

    def test_08_03_set_wrong_bripv4(self):
        logger.info('set wrong 6rd border_relay_ipv4_address to 225.1.1.1')    
        ref = copy.deepcopy(Manual_6rd)
        ref['border_relay_ipv4_address'] = '225.1.1.1'
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**ref, msg=True)
        Assertion.assert_regular(msg['status']['info'][0]['message'], "Invalid BR IPv4 Address", "ERR: set wrong prefix failed.")

    def test_08_04_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_09_Config_for_6rdPrefix(Test):
    uuid = '1503475'
    description= show_testcase_info(Parameter.TESTPLAN, '09', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '09')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_09_01_add_6rd_ti_to_manual_with_proper_ip(self):
        ref = copy.deepcopy(Manual_6rd)
        ref['6rd_prefix'] = '2001::'
        ref['6rd_prefix_length'] = 64
        rc = inter_v6_obj.add_tunnel_interface(**ref)
        rc &= inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with  manual proper ip failed.")

    def test_09_02_add_6rd_ti_to_manual_with_proper_ip(self):
        ref = copy.deepcopy(Manual_6rd)
        ref['6rd_prefix'] = 'fec0::'
        ref['6rd_prefix_length'] = 64
        rc = inter_v6_obj.add_tunnel_interface(**ref)
        # rc &= inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with  manual proper ip failed.")

    def test_09_03_set_wrong_6rdPrefix(self):
        logger.info('set wrong 6rd 6rdPrefix ')    
        ref = copy.deepcopy(Manual_6rd)
        ref['6rd_prefix'] = 'ff00::'
        ref['6rd_prefix_length'] = 10
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**ref, msg=True)
        Assertion.assert_regular(msg['status']['info'][0]['message'], "Invalid 6rd Prefix, only non-link-local unicast address is allowed", "ERR: set wrong prefix failed.")

    def test_09_04_set_wrong_6rdPrefix(self):
        logger.info('set wrong 6rd 6rdPrefix ')    
        ref = copy.deepcopy(Manual_6rd)
        ref['6rd_prefix'] = 'fe80::'
        ref['6rd_prefix_length'] = 10
        (rc, msg) = inter_v6_obj.edit_tunnel_interface(**ref, msg=True)
        Assertion.assert_regular(msg['status']['info'][0]['message'], "Invalid 6rd Prefix, only non-link-local unicast address is allowed", "ERR: set wrong prefix failed.")

    def test_09_05_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_15_6rd_Elements_When_DHCP(Test):
    uuid = '1503476'
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_15_01_set_X2_dhcp(self):
        rc = interface.config_interface(**x2_dhcp_dict)
        Assertion.assert_equal(rc, True, "ERR: config X2 interface failed .")

    @repeat_method(5)
    def test_15_02_verify_X2_get_IP(self):
        time.sleep(10)
        x2_dict = interface.get_interface_address(name='X2')
        try:
            ip = x2_dict['ip_address']
        except:
            logger.error('Fail to get X2 ip.')
            logger.info(x2_dict)
            ip = ''
        Assertion.assert_equal(ip, Parameter.DUT_X2_IP, f"Error: X2 should obtain IP.")

    @repeat_method(3)
    def test_15_03_add_6rd_tunnel_interface_to_dhcp(self):
        logger.info('Add 6rd tunnel interface with dhcp mode.')
        rc = inter_v6_obj.add_tunnel_interface(**dhcp_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp .")

    ##should check  the 6rd Tunnel's Status is \"Interface Up\".\
    def test_15_04_get_6rd_interface_info(self):
        time.sleep(10)
        foundit = 0
        rc = inter_v6_obj.get_6rd_protocal()
        status = ""
        status_all = inter_v6_obj.get_interface_address()
        for i in status_all:
            if i['name'] == dhcp_6rd['name']:
                status = i
                break
        logger.info(f"--------------{status}")
        logger.info('-------------------')
        logger.info(status_all)
        try:
            prefix = rc['6rd Prefix']
            logger.info(f'Get tunnel prefix: {prefix}')
            prefix_length = rc['6rd Prefix Length']
            logger.info(f'Get tunnel prefix len: {prefix_length}')
            br_ipv4 = rc['Active BR']
            logger.info(f'Get tunnel border relay_ipv4_address: {br_ipv4}')
            mask_len = rc['IPv4 Mask Length']
            logger.info(f'Get tunnel mask len: {mask_len}')
            tc16_status = status['status']
            logger.info(f'Get 6rd_interface status: {tc16_status}')
            if prefix == '6868::':
                foundit += 1
            else:
                logger.error(f'tunnel prefix should be 6868::')
            if int(prefix_length) == 16:
                foundit += 1
            else:
                logger.error(f'tunnel prefix len should be 16')
            if br_ipv4 == '4.4.4.4':
                foundit += 1
            else:
                logger.error(f'tunnel border relay_ipv4_address should be 4.4.4.4')
            if int(mask_len) == 24:
                foundit += 1
            else:
                logger.error(f'tunnel ipv4 mask len should be 24')
            if tc16_status == 'Interface Up':
                foundit += 1
            else:
                logger.error(f'6rd_interface status should up')
        except Exception as e:
            logger.error(f'Error: {e}')
        Assertion.assert_equal(foundit, 5, "ERR: 6rd Tunnel General Information show right .")

    def test_15_05_delete_tunnel_interface(self):
       rc = inter_v6_obj.delete_tunnel_interface(name='tc16')
       Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_16_6rd_Elements_When_DHCP(Test):
    uuid = '1503477'
    description= show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

    def test_16_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_16_01_set_X2_dhcp(self):
        x2_dhcp_dict = {
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'dhcp',
        }
        rc = interface.config_interface(**x2_dhcp_dict)
        Assertion.assert_equal(rc, True, "ERR: config X2 interface failed .")

    @repeat_method(5)
    def test_16_02_verify_X2_get_IP(self):
        time.sleep(10)
        x2_dict = interface.get_interface_address(name='X2')
        try:
            ip = x2_dict['ip_address']
        except:
            logger.error('Fail to get X2 ip.')
            logger.info(x2_dict)
            ip = ''
        Assertion.assert_equal(ip, Parameter.DUT_X2_IP, f"Error: X2 should obtain IP.")

    def test_16_03_add_6rd_tunnel_interface_to_dhcp(self):
        dhcp_6rd = {
            'name': 'tc16',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X2'},
            'dynamic': True,
        }
        logger.info('Add 6rd tunnel interface with dhcp mode.')
        rc = inter_v6_obj.add_tunnel_interface(**dhcp_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp .")

    def test_16_04_get_6rd_interface_info(self):
        foundit = 0
        rc = inter_v6_obj.get_6rd_protocal()
        try:
            prefix = rc['6rd Prefix']
            logger.info(f'Get tunnel prefix: {prefix}')
            prefix_length = rc['6rd Prefix Length']
            logger.info(f'Get tunnel prefix len: {prefix_length}')
            br_ipv4 = rc['Active BR']
            logger.info(f'Get tunnel border relay_ipv4_address: {br_ipv4}')
            mask_len = rc['IPv4 Mask Length']
            logger.info(f'Get tunnel mask len: {mask_len}')
            if prefix == '6868::':
                foundit += 1
            else:
                logger.error(f'tunnel prefix should be 6868::')
            if int(prefix_length) == 16:
                foundit += 1
            else:
                logger.error(f'tunnel prefix len should be 16')
            if br_ipv4 == '4.4.4.4':
                foundit += 1
            else:
                logger.error(f'tunnel border relay_ipv4_address should be 4.4.4.4')
            if int(mask_len) == 24:
                foundit += 1
            else:
                logger.error(f'tunnel ipv4 mask len should be 24')
        except Exception as e:
            logger.error(f'Error: {e}')
        Assertion.assert_equal(foundit, 4, "ERR: 6rd Tunnel General Information show right .")

    def test_16_05_delete_tunnel_interface(self):
       rc = inter_v6_obj.delete_tunnel_interface(name='tc16')
       Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_20_Route_Policy_Check(Test):
    uuid = '1503478'
    description= show_testcase_info(Parameter.TESTPLAN, '20', description=True)['title']

    def test_20_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_20_01_add_6rd_tunnel_interface(self):
        manual_6rd = {
            'name': '6rd',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 64,
            'bound_to': {'interface': 'X1'},
            'dynamic': False,
            '6rd_prefix': '3::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }
        rc = inter_v6_obj.add_tunnel_interface(**manual_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp or manual failed.")

    def test_20_02_check_route_policy(self):
        routes = route_obj.show_route_policy(version='ipv6')
        foundit = 0
        try:
            for route in routes['route_policies']:
                try:
                    if route['ipv6']['destination']['name'] == '6rd ' + '6rd Tunnel Prefix':
                        logger.info('Found 6rd route in PBR table.')
                        foundit = 1
                        break
                except:
                    pass
        except Exception as e:
            logger.info(f'Error: {e}')
        Assertion.assert_equal(foundit, 1, "ERR: 6rd route not in PBR table.")
        
    def test_20_03_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='6rd')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_26_AO_Check(Test):
    uuid = '1503479'
    description= show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_26_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '26')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_26_01_Config_X2(self):
        x1_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP,
            'gateway': Parameter.DUT_X1_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_26_02_add_6rd_tunnel_interface(self):
        manual_6rd = {
            'name': 'tc26',
            'zone': 'WAN',
            'type': '6rd',
            'ip': Parameter.TUNNEL_IP,
            'prefix_length': 56,
            'bound_to': {'interface': 'X2'},
            'dynamic': False,
            '6rd_prefix': '6868::',
            '6rd_prefix_length': 64,
            'border_relay_ipv4_address': '1.2.3.4',
            'mask_length':24
        }
        rc = inter_v6_obj.add_tunnel_interface(**manual_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with manual failed.")

    def test_26_03_check_AO(self):
        ao = ao_obj.get_addressobject_by_name(name='tc26 6rd Tunnel Delegated Prefix',version='ipv6')
        rc = True
        try:
            ao_subnet= ao['address_objects'][0]['ipv6']['network']['subnet']
            logger.info(f"ao subnet is: {ao_subnet}")
            if ao_subnet == "6868::a800:0:0:0":
                logger.info('ao subnet is equal to 6868::a800:0:0:0')
            else:
                logger.info('ao subnet is not equal to 6868::a800:0:0:0')
                rc = False
        except:
            rc = False
        try:
            ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
            logger.info(f"ao subnet is: {ao_mask}")
            if ao_mask == "/72":
                logger.info('ao mask is equal to /72')
            else:
                logger.info('ao subnet is not equal to /72')
                rc = False
        except:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: ao subnet or mask is not right")

    def test_26_04_Change_X2_IP(self):
        x1_static = {
            'if': 'X2',
            'zone': 'WAN', 
            'mode': 'static',
            'ip': Parameter.DUT_X2_IP_NEW,
            'gateway': Parameter.DUT_X2_GW,
        }
        rc = interface.config_interface(**x1_static)
        Assertion.assert_equal(rc, True, "ERR: Config X1 to static failed")

    def test_26_05_check_AO(self):
        ao = ao_obj.get_addressobject_by_name(name='tc26 6rd Tunnel Delegated Prefix',version='ipv6')
        rc = True
        try:
            ao_subnet= ao['address_objects'][0]['ipv6']['network']['subnet']
            logger.info(f"ao subnet is: {ao_subnet}")
            if ao_subnet == "6868::6400:0:0:0":
                logger.info('ao subnet is equal to 6868::6400:0:0:0')
            else:
                logger.info('ao subnet is not equal to 6868::6400:0:0:0')
                rc = False
        except:
            rc = False
        try:
            ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
            logger.info(f"ao subnet is: {ao_mask}")
            if ao_mask == "/72":
                logger.info('ao mask is equal to /72')
            else:
                logger.info('ao subnet is not equal to /72')
                rc = False
        except:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: ao subnet or mask is not right")

    def test_26_06_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='tc26')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_29_Check_AO(Test):
    uuid = '1503480'
    description= show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_29_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '29')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_29_01_Config_X2(self):
        # rc = interface.config_interface(**x2_static)
        rc = interface.config_interface(**x2_dhcp_dict)
        interface.click_dhcp_renew(name = 'X2')
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_29_02_add_6rd_tunnel_interface(self):
        rc = inter_v6_obj.add_tunnel_interface(**tc29_6rd)
        ###for ao api cache update
        interface.config_interface(**Lx1)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with manual failed.")

    @repeat_method(3)
    def test_29_03_check_AO(self):
        time.sleep(30)
        ao = ao_obj.get_addressobject_by_name(name='tc29 6rd Tunnel Delegated Prefix',version='ipv6')
        rc = True
        try:
            ao_by_cli = ao_cli.show_address_object(name='tc29\ 6rd\ Tunnel\ Delegated\ Prefix',version='ipv6')
            logger.info(f'----{ao_by_cli}')
            if 'network 6868::a800:0:0:0 /72' in str(ao_by_cli):
                logger.info('ao mask is equal to /72')
            else:
                logger.info('ao subnet is not equal to /172')
                rc = False
        except:
            rc = False

        # ao = ao_obj.get_addressobject_by_name(name='tc29 6rd Tunnel Delegated Prefix',version='ipv6')
        # rc = True
        # try:
        #     ao_subnet= ao['address_objects'][0]['ipv6']['network']['subnet']
        #     logger.info(f"ao subnet is: {ao_subnet}")
        #     if ao_subnet == "6868::a800:0:0:0":
        #         logger.info('ao subnet is equal to 6868::a800:0:0:0')
        #     else:
        #         logger.info('ao subnet is not equal to 6868::a800:0:0:0')
        #         rc = False
        # except:
        #     rc = False
        # try:
        #     ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
        #     logger.info(f"ao subnet is: {ao_mask}")
        #     if ao_mask == "/72":
        #         logger.info('ao mask is equal to /72')
        #     else:
        #         logger.info('ao subnet is not equal to /72')
        #         rc = False
        # except:
        #     rc = False
        Assertion.assert_equal(rc, True, "ERR: ao subnet or mask is not right")

    def test_29_04_release_X2(self):
        rc = interface.click_dhcp_release(name = 'X2')
        
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(3)
    def test_29_05_check_AO_Update(self):
        time.sleep(30)
        ###for ao api cache update
        interface.config_interface(**Lx1)
        # ao = ao_obj.get_addressobject_by_name(name='tc29 6rd Tunnel Delegated Prefix',version='ipv6')
        ao_by_cli = ao_cli.show_address_object(name='tc29\ 6rd\ Tunnel\ Delegated\ Prefix',version='ipv6')
        logger.info(f'----{ao_by_cli}')
        rc = True
        try:
            ####ao_network is none,ui show /128
            # ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
            # ao_network= ao['address_objects'][0]['ipv6']['network']
            # logger.info(f"ao subnet is: {ao_network}")
            # if ao_network == "/128":
            if "network ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff /128" in str(ao_by_cli) or "no network" in str(ao_by_cli) or ":: /128" in str(ao_by_cli):
                logger.info('ao mask is equal to /128')
            else:
                logger.info('ao subnet is not equal to /128')
                rc = False
        except:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: ao  mask is not right")




    def test_29_06_Config_X2(self):
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(3)
    def test_29_07_check_AO(self):
        time.sleep(3)
        ao = ao_obj.get_addressobject_by_name(name='tc29 6rd Tunnel Delegated Prefix',version='ipv6')
        rc = True
        try:
            ao_subnet= ao['address_objects'][0]['ipv6']['network']['subnet']
            logger.info(f"ao subnet is: {ao_subnet}")
            if ao_subnet == "6868::a800:0:0:0":
                logger.info('ao subnet is equal to 6868::a800:0:0:0')
            else:
                logger.info('ao subnet is not equal to 6868::a800:0:0:0')
                rc = False
        except:
            rc = False
        try:
            ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
            logger.info(f"ao subnet is: {ao_mask}")
            if ao_mask == "/72":
                logger.info('ao mask is equal to /72')
            else:
                logger.info('ao subnet is not equal to /72')
                rc = False
        except:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: ao subnet or mask is not right")

    def test_29_08_disable_X2(self):
        rc = interface.disable_interface(name = 'X2')
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    @repeat_method(3)
    def test_29_09_check_AO_Update(self):
        time.sleep(10)
        ###for ao api cache update
        interface.config_interface(**Lx1)
        # ao = ao_obj.get_addressobject_by_name(name='tc29 6rd Tunnel Delegated Prefix',version='ipv6')
        ao_by_cli = ao_cli.show_address_object(name='tc29\ 6rd\ Tunnel\ Delegated\ Prefix',version='ipv6')
        logger.info(f'----{ao_by_cli}')
        rc = True
        try:
            ####ao_network is none,ui show /128
            # ao_mask= ao['address_objects'][0]['ipv6']['network']['mask']
            # ao_network= ao['address_objects'][0]['ipv6']['network']
            # logger.info(f"ao subnet is: {ao_network}")
            # if ao_network == "/128":
            if "network ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff /128" in str(ao_by_cli) or "no network" in str(ao_by_cli):
                logger.info('ao mask is equal to /128')
            else:
                logger.info('ao subnet is not equal to /128')
                rc = False
        except:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: ao  mask is not right")

    def test_29_10_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='tc29')
        rc &= interface.enable_interface(name = 'X2')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_31_Detect_AO(Test):
    uuid = '1503481'
    description= show_testcase_info(Parameter.TESTPLAN, '31', description=True)['title']

    def test_31_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '31')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_31_01_Config_X2(self):
        rc = interface.config_interface(**x2_static)
        Assertion.assert_equal(rc, True, "ERR: Config X2 to static failed")

    def test_31_02_add_6rd_tunnel_interface(self):
        ref = copy.deepcopy(tc29_6rd)
        ref['name'] = 'tc31'
        rc = inter_v6_obj.add_tunnel_interface(**ref)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with manual failed.")

    def test_31_03_check_AO(self):
        ao = ao_obj.get_all_addressobject_ipv6()
        dump_ao= json.dumps(ao)
        logger.info(f'The all ipv6 address objects are: {ao} ')
        if "tc31 6rd Tunnel Delegated Prefix" in dump_ao and 'tc31 6rd Tunnel Prefix' in dump_ao \
            and 'tc31 IPv6 Primary Static Address' in dump_ao and 'tc31 IPv6 Primary Static Address Subnet' in dump_ao:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: check four address objects are auto added fialed")

    def test_31_04_delete_tunnel_interface(self):
        rc = inter_v6_obj.delete_tunnel_interface(name='tc31')
        Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")

    def test_31_05_check_AO(self):
        ao = ao_obj.get_all_addressobject_ipv6()
        dump_ao= json.dumps(ao)
        logger.info(f'The all ipv6 address objects are: {ao} ')
        if "tc31 6rd Tunnel Delegated Prefix" in dump_ao or 'tc31 6rd Tunnel Prefix' in dump_ao \
            or 'tc31 IPv6 Primary Static Address' in dump_ao or 'tc31 IPv6 Primary Static Address Subnet' in dump_ao:
            rc = False
        else:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: check four address objects are auto deleted fialed")


# [Func] [DHCP] DUT MUST include a Parameter Request List Option [RFC2132] for the OPTION_6RD when sending DHCP requests
class Test_33_Check_OPTION_6RD_In_DHCP_Request(Test):
    uuid = '1503482'
    description= show_testcase_info(Parameter.TESTPLAN, '33', description=True)['title']

    def test_33_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '33')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_33_01_set_X2_dhcp(self):
        pkg_api.clear_packets()
        pkg_api.start_capture()
        rc = interface.config_interface(**x2_dhcp_dict)
        interface.click_dhcp_release(name = 'X2')
        interface.click_dhcp_renew(name = 'X2')
        Assertion.assert_equal(rc, True, "ERR: config X2 interface failed .")

    @repeat_method(5)
    def test_33_02_verify_X2_get_IP(self):
        time.sleep(10)
        x2_dict = interface.get_interface_address(name='X2')
        try:
            ip = x2_dict['ip_address']
        except:
            logger.error('Fail to get X2 ip.')
            logger.info(x2_dict)
            ip = ''
        Assertion.assert_equal(ip, Parameter.DUT_X2_IP, f"Error: X2 should obtain IP.")

    def test_33_03_add_6rd_tunnel_interface_to_dhcp(self):
        logger.info('Add 6rd tunnel interface with dhcp mode.')
        rc = inter_v6_obj.add_tunnel_interface(**dhcp_6rd)
        Assertion.assert_equal(rc, True, "ERR: Add 6rd tuennel interface with dhcp .")

    def test_33_04_get_6rd_interface_info(self):
        foundit = 0
        rc = inter_v6_obj.get_6rd_protocal()
        try:
            prefix = rc['6rd Prefix']
            logger.info(f'Get tunnel prefix: {prefix}')
            prefix_length = rc['6rd Prefix Length']
            logger.info(f'Get tunnel prefix len: {prefix_length}')
            br_ipv4 = rc['Active BR']
            logger.info(f'Get tunnel border relay_ipv4_address: {br_ipv4}')
            mask_len = rc['IPv4 Mask Length']
            logger.info(f'Get tunnel mask len: {mask_len}')
            if prefix == '6868::':
                foundit += 1
            else:
                logger.error(f'tunnel prefix should be 6868::')
            if int(prefix_length) == 16:
                foundit += 1
            else:
                logger.error(f'tunnel prefix len should be 16')
            if br_ipv4 == '4.4.4.4':
                foundit += 1
            else:
                logger.error(f'tunnel border relay_ipv4_address should be 4.4.4.4')
            if int(mask_len) == 24:
                foundit += 1
            else:
                logger.error(f'tunnel ipv4 mask len should be 24')
        except Exception as e:
            logger.error(f'Error: {e}')
        Assertion.assert_equal(foundit, 4, "ERR: 6rd Tunnel General Information show right .")


    #####.DHCP request from X2 contains OPTION_6RD(212) in the option field
    def test_33_05_check_DHCP_request(self):
        packets = pkg_api.export_captured_packets_pcapng()
        logger.info(packets)
        cmd = "tshark -r /tmp/packet-c.pcapng -R 'bootp.option.dhcp == 3' -V -w /tmp/filter.pcapng"
        packets_info = os.popen(cmd).read()
        rc = False
        for packet in re.split('Packet comments', packets_info):
            if "Parameter Request List Item: (212) 6RD" in  packet :
                logger.info(f'Got OPTION_6RD(212) from  packet   ')
                rc = True
                break
        Assertion.assert_equal(rc, True, "ERR: 6rd dhcp request Information show right in packet .")

    # def test_33_06_delete_tunnel_interface(self):
    #    rc = inter_v6_obj.delete_tunnel_interface(name='tc16')
    #    Assertion.assert_equal(rc, True, "ERR: delete tunnel interface failed.")


class Test_40_Check_6over4_packets(Test):
    uuid = '1503483'
    description= show_testcase_info(Parameter.TESTPLAN, '40', description=True)['title']

    def test_40_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '40')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_40_01_config_X0_IPv6(self):
        opt = {
            'name': 'X0',
            'mode': 'static',
            'zone': 'LAN',
            'ip': '2010:0:a8::168',
            'prefix_length': 64,
            'mgmt_ping': True,
            'mgmt_https': True
        }
        rc= inter_v6_obj.config_interface_ipv6(**opt)
        Assertion.assert_equal(rc, True, "ERR: Config X0 IPv6 failed")
    
    def test_40_02_config_v6_route_on_pc1(self):
        cmd = 'ip -6 route add 1::/24 via 2010:0:a8::168'
        os.system(cmd)
        Assertion.assert_equal(True, True, 'ERR: config route failed!!')

    def test_40_03_configure_capture(self):
        rc = False
        pkt_setting= {   
            'display_filter': {
                'bidirectional': True,
                'destination_ips': '',
                'destination_ports': '',
                'ip_types': '6OVER4',
            }
        }
        rc = pkg_api.conf_packmon(**pkt_setting)
        Assertion.assert_equal(rc, True, "ERR: configure packet monitor failed.")
    
    @repeat_method(3)
    def test_40_04_check_packets(self):
        pkg_api.clear_packets()
        pkg_api.start_capture()
        os.system(f'ping6 1::1 -c 10')
        time.sleep(3)
        pkg_api.stop_capture()
        rc = check_packet(src=Parameter.DUT_X2_IP, proto='6over4')
        Assertion.assert_equal(rc, True, f"ERR: Got 6over4 packet from {Parameter.DUT_X2_IP}.")



class Test_44_Check_dest_addr(Test):
    uuid = '1503485'
    description= show_testcase_info(Parameter.TESTPLAN, '44', description=True)['title']

    def test_44_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '44')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_44_01_check_packets(self):
        pkg_api.conf_packmon(**pkt_setting)
        pkg_api.clear_packets()
        pkg_api.start_capture()
        for i in range(5):
            os.system(f'ping6 1::1 -c 3')
            time.sleep(3)
            pkg_api.stop_capture()
            rc = check_packet2(src=Parameter.DUT_X2_IP, proto='6over4', dst=Parameter.BORDER_RELAY)
            if rc:
                break
        Assertion.assert_equal(rc, True, f"ERR: Got 6over4 packet from {Parameter.DUT_X2_IP}.")
        