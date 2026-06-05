from definition.settings import *


class TestVLAN_Using_duplicate_VLAN_Tag(Test):
    uuid = "SOSAIOT-TC-57265"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 100,
            'if': 'x0',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='100')
        Assertion.assert_regular(json.dumps(response), 'vlan": 100', 'err: vlan tag not created')

    def test_02_add_sub_interface_with_same_vlan_tag_under_same_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 100,
            'if': 'x0',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(msg=True, **vlan)
        error_message = resp[1]['status']['info'][0]['message']
        expected_message = "'interface X0:V100 vlan 100' already exists."
        Assertion.assert_equal(expected_message, error_message, 'ERR: Duplicate sub interface created successfully')

    def test_03_add_sub_interface_with_same_vlan_tag_under_different_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 100,
            'if': 'x2',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '14.14.1.168',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='100')
        Assertion.assert_regular(json.dumps(response), 'vlan": 100', 'err: vlan tag not created')


class TestVLAN_Using_invalid_VLAN_Tag(Test):
    uuid = "SOSAIOT-TC-57266"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_invalid_VLAN_Tag_0(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 0,
            'if': 'x0',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        Assertion.assert_equal(False, resp, 'ERR: sub interface created successfully with Using invalid VLAN Tag')

    def test_02_add_sub_interface_with_invalid_VLAN_Tag_4095(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 0,
            'if': 'x0',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        Assertion.assert_equal(False, resp, 'ERR: sub interface created successfully Using invalid VLAN Tag')


class TestVLAN_Using_Overlap_networks(Test):
    uuid = "SOSAIOT-TC-57267"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_Overlap_networks(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 100,
            'if': 'x4',
            'zone': 'WAN',
            'mode': 'static',
            'ip': '10.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(msg=True, **vlan)
        error_message = resp[1]['status']['info'][0]['message']
        expected_message = 'Subnet on this interface overlaps with another interface'
        Assertion.assert_equal(expected_message, error_message,
                               'ERR: sub interface created successfully with Overlap networks')


class TestVLAN_Modifying_VLAN_Tag(Test):
    uuid = "SOSAIOT-TC-57270"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    @repeat_method(3)
    def test_01_verify_status_of_VLAN_Tag(self):
        static_client.send_command('pkill firefox')
        time.sleep(10)
        url = 'https://192.168.168.168'
        cmd = 'python3 ' + os.environ[
            'PYTHON_SONICOS_HOME'] + '/Network/VLAN_TP296_New/definition/ui_user.py -method firewall_login ' + '-url ' + url + ' -user admin -pwd S0nic@uto '
        out = static_client.send_command(cmd)
        logger.info('login with user\n' + out)
        words = out.split()
        res = ''.join(words[-1:])
        assert res == 'True', 'VLAN Tag is not grayed out'


class TestVLAN_Modifying_zone_assignment(Test):
    uuid = "SOSAIOT-TC-57271"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '19')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_DMZ_zone(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 110,
            'if': 'x0',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '12.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='110')
        Assertion.assert_regular(json.dumps(response), 'vlan": 110', 'err: vlan tag not created')

    def test_02_modify_sub_interface_with_LAN_zone(self):
        vlan = {'interfaces': [
            {'ipv4': {'mac': {'default': True}, 'multicast': False, 'exclude_route': False, 'routed_mode': {},
                      'asymmetric_route': False,
                      'flow_reporting': False, 'mtu': 1500, 'name': 'X0', 'ip_assignment': {'zone': 'LAN',
                                                                                            'mode': {'static': {
                                                                                                'ip': '12.5.193.11',
                                                                                                'netmask': '255.255.255.0',
                                                                                                'gateway': '0.0.0.0'}}},
                      'vlan': 110}}]}
        resp = (interfacev4api.edit_interface)(interface_name='X0', vlan_id='110', **vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='110')
        modified_zone = response['interfaces'][0]['ipv4']['ip_assignment']['zone']
        Assertion.assert_equal('LAN', modified_zone, 'ERR: modifying the zone of sub interface failed')


class TestVLAN_Different_parent_interface_and_same_zone(Test):
    uuid = "SOSAIOT-TC-57272"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_DMZ_zone(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 150,
            'if': 'x0',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '15.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='150')
        Assertion.assert_regular(json.dumps(response), 'vlan": 150', 'err: vlan tag not created')

    def test_02_add_sub_interface_with_DMZ_zone_under_different_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 150,
            'if': 'x2',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '16.5.193.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='150')
        Assertion.assert_regular(json.dumps(response), 'vlan": 150', 'err: vlan tag not created')


class TestVLAN_Modifying_parent_interface(Test):
    uuid = "SOSAIOT-TC-57273"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '20')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_DMZ_zone(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 120,
            'if': 'x0',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '17.5.163.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='120')
        Assertion.assert_regular(json.dumps(response), 'vlan": 120', 'err: vlan tag not created')

    def test_02_modify_parent_interface(self):
        vlan = {'interfaces': [
            {'ipv4': {'mac': {'default': True}, 'multicast': True, 'exclude_route': False, 'routed_mode': {},
                      'asymmetric_route': False,
                      'flow_reporting': False, 'mtu': 1500, 'name': 'X0', 'ip_assignment': {'zone': 'DMZ',
                                                                                            'mode': {'static': {
                                                                                                'ip': '17.5.163.11',
                                                                                                'netmask': '255.255.255.0',
                                                                                                'gateway': '0.0.0.0'}}},
                      'vlan': 120}}]}
        resp = (interfacev4api.edit_interface)(interface_name='X0', vlan_id='120', **vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='120')
        modified_value = response['interfaces'][0]['ipv4']['multicast']
        Assertion.assert_equal(True, modified_value, 'ERR: modifying parent interface failed')


class TestVLAN_Modifying_IP_Address_Subnet_Mask(Test):
    uuid = "SOSAIOT-TC-57274"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '21')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_static_ip_assignment(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 130,
            'if': 'x0',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '19.5.143.11',
            'netmask': '255.255.255.0'}
        resp = (interfacev4api.add_interface)(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='130')
        Assertion.assert_regular(json.dumps(response), 'vlan": 130', 'err: vlan tag not created')

    def test_02_modify_ip_and_subnet_mask_of_sub_interface(self):
        vlan = {'interfaces': [
            {'ipv4': {'mac': {'default': True}, 'multicast': False, 'exclude_route': False, 'routed_mode': {},
                      'asymmetric_route': False,
                      'flow_reporting': False, 'mtu': 1500, 'name': 'X0', 'ip_assignment': {'zone': 'DMZ',
                                                                                            'mode': {'static': {
                                                                                                'ip': '19.15.143.11',
                                                                                                'netmask': '255.255.0.0',
                                                                                                'gateway': '0.0.0.0'}}},
                      'vlan': 130}}]}
        resp = (interfacev4api.edit_interface)(interface_name='X0', vlan_id='130', **vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='130')
        modified_ip = response['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['ip']
        modified_subnet = response['interfaces'][0]['ipv4']['ip_assignment']['mode']['static']['netmask']
        Assertion.assert_equal('19.15.143.11', modified_ip, 'ERR: modifying ip failed')
        Assertion.assert_equal('255.255.0.0', modified_subnet, 'ERR: modifying subnetmask failed')


class TestVLAN_Modifying_management_rules(Test):
    uuid = "SOSAIOT-TC-57275"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_and_enable_HTTP_HTTPS_PING_SNMP_SSH(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 140,
            'if': 'x3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '19.5.143.11',
            'netmask': '255.255.255.0',
            'mgmt_ping': True,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='140')
        Assertion.assert_regular(json.dumps(response), 'vlan": 140', 'err: vlan tag not created')

    def test_02_modify_sub_interface_and_disable_HTTP_HTTPS_PING_SNMP_SSH(self):
        vlan = {'interfaces': [
            {'ipv4': {"management": {"https": False, "ping": False, "snmp": False, "ssh": False},
                      'mac': {'default': True}, 'multicast': False, 'exclude_route': False, 'routed_mode': {},
                      'asymmetric_route': False,
                      'flow_reporting': False, 'mtu': 1500, 'name': 'X3', 'ip_assignment': {'zone': 'DMZ',
                                                                                            'mode': {'static': {
                                                                                                'ip': '19.15.143.11',
                                                                                                'netmask': '255.255.255.0',
                                                                                                'gateway': '0.0.0.0'}}},
                      'vlan': 140}}]}
        resp = interfacev4api.edit_interface(interface_name='X3', vlan_id='140', **vlan)
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='140')
        mgmt_https = response['interfaces'][0]['ipv4']['management']['https']
        mgmt_ping = response['interfaces'][0]['ipv4']['management']['ping']
        mgmt_snmp = response['interfaces'][0]['ipv4']['management']['snmp']
        mgmt_ssh = response['interfaces'][0]['ipv4']['management']['ssh']

        Assertion.assert_equal(False, mgmt_https, 'ERR: modifying mgmt_https failed')
        Assertion.assert_equal(False, mgmt_ping, 'ERR: modifying mgmt_ping failed')
        Assertion.assert_equal(False, mgmt_snmp, 'ERR: modifying mgmt_snmp failed')
        Assertion.assert_equal(False, mgmt_ssh, 'ERR: modifying mgmt_ssh failed')

    def test_03_delete_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 140,
            'if': 'x3',
            'zone': 'DMZ',
            'mode': 'static',
            'ip': '19.5.143.11',
            'netmask': '255.255.255.0', }
        resp = interfacev4api.del_interface(**vlan)
        Assertion.assert_equal(resp, True, "ERR: Delete vlan interface for X3 failed")
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='140')
        resp_message = response['status']['info'][0]['message']
        Assertion.assert_equal(resp_message, "'140' not a reasonable value.",
                               "ERR: Delete vlan interface for X3 failed")


class TestVLAN_Modifying_user_login_rules(Test):
    uuid = "SOSAIOT-TC-57276"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '23')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_and_enable_user_HTTP_HTTPS(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 149,
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '29.5.143.11',
            'netmask': '255.255.255.0',
            'user_https': True,
            'user_http': True}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='149')
        Assertion.assert_regular(json.dumps(response), 'vlan": 149', 'err: vlan tag not created')

    def test_02_modify_sub_interface_and_disable_user_HTTP_HTTPS(self):
        vlan = {'interfaces': [
            {'ipv4': {"user_login": {"http": False, "https": False}, 'mac': {'default': True}, 'multicast': False,
                      'exclude_route': False, 'routed_mode': {},
                      'asymmetric_route': False,
                      'flow_reporting': False, 'mtu': 1500, 'name': 'X0', 'ip_assignment': {'zone': 'DMZ',
                                                                                            'mode': {'static': {
                                                                                                'ip': '29.5.143.11',
                                                                                                'netmask': '255.255.255.0',
                                                                                                'gateway': '0.0.0.0'}}},
                      'vlan': 149}}]}
        resp = interfacev4api.edit_interface(interface_name='X0', vlan_id='149', **vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='149')
        user_http = response['interfaces'][0]['ipv4']['user_login']['http']
        user_https = response['interfaces'][0]['ipv4']['user_login']['https']

        Assertion.assert_equal(False, user_http, 'ERR: modifying user_http failed')
        Assertion.assert_equal(False, user_https, 'ERR: modifying user_https failed')


class TestVLAN_VLAN_sub_interface_deletion(Test):
    uuid = "SOSAIOT-TC-57277"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '24')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 159,
            'if': 'x1',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '39.5.143.11',
            'netmask': '255.255.255.0'}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X1', vlan_id='159')
        Assertion.assert_regular(json.dumps(response), 'vlan": 159', 'err: vlan tag not created')

    def test_02_delete_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 159,
            'if': 'x1',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '39.5.143.11',
            'netmask': '255.255.255.0'}
        resp = interfacev4api.del_interface(**vlan)
        Assertion.assert_equal(resp, True, "ERR: Delete vlan interface for X1 failed")
        response = interfacev4api.get_vlan_interface_status(name='X1', vlan_id='159')
        resp_message = response['status']['info'][0]['message']
        Assertion.assert_equal(resp_message, "Command 'show interface ipv4 X1 vlan 159' does not match",
                               "ERR: Delete vlan interface for X1 failed")


class TestVLAN_Different_parent_interface_and_different_zone(Test):
    uuid = "SOSAIOT-TC-57283"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface_with_DMZ_zone(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 179,
            'if': 'x0',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '46.15.5.143',
            'netmask': '255.255.255.0',
            'mgmt_https': True}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X0', vlan_id='179')
        Assertion.assert_regular(json.dumps(response), 'vlan": 179', 'err: vlan tag not created')

    def test_02_add_sub_interface_with_LAN_zone_under_different_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 189,
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '56.35.5.143',
            'netmask': '255.255.255.0',
            'mgmt_https': True}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='189')
        Assertion.assert_regular(json.dumps(response), 'vlan": 189', 'err: vlan tag not created')


class TestVLAN_Maximum_numbers_of_VLAN_in_same_parent_interface(Test):
    uuid = "SOSAIOT-TC-57268"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_maximum_sub_interface(self):
        resp = status_api.show_status()
        model = resp['model'].upper()
        if model == 'TZ 270' or model == 'TZ 270W' or model == 'TZ 80' or model == 'TZ 280' or model == 'TZ 280W' or model == 'TZ 280P':
            max_vlan = 65
        elif model == 'TZ 370' or model == 'TZ 370W' or model == 'TZ 470' or model == 'TZ 470W' or model == 'TZ 380' or model == 'TZ 380W' or model == 'TZ 480':
            max_vlan = 129
        elif model == 'TZ 570' or model == 'TZ 570W' or model == 'TZ 570P' or model == 'NSA 2700' or model == 'NSA 3700' or model == 'NSA 3800' or model == 'NSA 2800' or model == 'TZ 680' or model == 'TZ 580':
            max_vlan = 257
        elif model == 'NSA 4700' or model == 'NSA 5700' or model == 'NSA 6700' or model == 'NSA 4800' or model == 'NSA 6800' or model == 'NSA 5800':
            max_vlan = 513
        elif model == 'NSSP 10700' or model == 'NSSP 11700' or model == 'NSSP 13700':
            max_vlan = 1025
        elif model == 'NSSP 15700':
            max_vlan = 705
        elif model == 'NSV 270' or model == 'NSV 470' or model == 'NSV 870':
            max_vlan = 129
        for vlan_value in range(1, max_vlan):
            vlan = {
                'type': 'vlan',
                'vlan_tag': vlan_value,
                'if': 'x3',
                'zone': 'LAN',
                'mode': 'static',
                'ip': '12.15.6.3',
                'netmask': '255.255.255.0'
            }
            resp = interfacev4api.add_interface(**vlan)
            Assertion.assert_equal(resp, True, "ERR: Creating sub interface for X3 failed")
            vlan = {
                "interfaces": [
                    {
                        "ipv4": {
                            "mac": {
                                "default": True
                            },
                            "flow_reporting": True,
                            "exclude_route": False,
                            "asymmetric_route": False,
                            "mtu": 1500,
                            "name": "X3",
                            "ip_assignment": {

                            },
                            "native_bridge": {

                            },
                            "vlan": vlan_value
                        }
                    }
                ]
            }
            resp = interfacev4api.edit_interface(interface_name='X3', vlan_id=str(vlan_value), **vlan)
            # resp1 = interfacev4api.unassign_vlan_interface(interface='X5',vlan_id=str(vlan_value))
            # print('unassign ref', resp1)

    def test_02_add_one_more_than_maximum_sub_interface(self):
        resp = status_api.show_status()
        model = resp['model'].upper()
        if model == 'TZ 270' or model == 'TZ 270W' or model == 'TZ 80' or model == 'TZ 280' or model == 'TZ 280W' or model == 'TZ 280P':
            max_vlan_value = 65
        elif model == 'TZ 370' or model == 'TZ 370W' or model == 'TZ 470' or model == 'TZ 470W' or model == 'TZ 380' or model == 'TZ 380W' or model == 'TZ 480':
            max_vlan_value = 129
        elif model == 'TZ 570' or model == 'TZ 570W' or model == 'TZ 570P' or model == 'NSA 2700' or model == 'NSA 3700' or model == 'NSA 3800' or model == 'NSA 2800' or model == 'TZ 680' or model == 'TZ 580':
            max_vlan_value = 257
        elif model == 'NSA 4700' or model == 'NSA 5700' or model == 'NSA 6700' or model == 'NSA 4800' or model == 'NSA 6800' or model == 'NSA 5800':
            max_vlan_value = 513
        elif model == 'NSSP 10700' or model == 'NSSP 11700' or model == 'NSSP 13700':
            max_vlan_value = 1025
        elif model == 'NSSP 15700':
            max_vlan_value = 705
        elif model == 'NSV 270' or model == 'NSV 470' or model == 'NSV 870':
            max_vlan_value = 129
        vlan = {
            'type': 'vlan',
            'vlan_tag': max_vlan_value,
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '12.15.6.3',
            'netmask': '255.255.255.0'
        }
        resp = interfacev4api.add_interface(msg=True, **vlan)
        error_message = resp[1]['status']['info'][0]['message']
        expected_message = 'Maximum number of VLAN interfaces configured already'
        Assertion.assert_equal(expected_message, error_message,
                               'ERR: sub interface created successfully')


class TestVLAN_Maximum_numbers_of_VLAN_in_different_parent_interface(Test):
    uuid = "SOSAIOT-TC-57269"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_one_more_than_maximum_sub_interface_in_different_parent_interface(self):
        resp = status_api.show_status()
        model = resp['model'].upper()
        if model == 'TZ 270' or model == 'TZ 270W' or model == 'TZ 80' or model == 'TZ 280' or model == 'TZ 280W' or model == 'TZ 280P':
            max_vlan_value = 65
        elif model == 'TZ 370' or model == 'TZ 370W' or model == 'TZ 470' or model == 'TZ 470W' or model == 'TZ 380' or model == 'TZ 380W' or model == 'TZ 480':
            max_vlan_value = 129
        elif model == 'TZ 570' or model == 'TZ 570W' or model == 'TZ 570P' or model == 'NSA 2700' or model == 'NSA 3700' or model == 'NSA 3800' or model == 'NSA 2800' or model == 'TZ 680' or model == 'TZ 580':
            max_vlan_value = 257
        elif model == 'NSA 4700' or model == 'NSA 5700' or model == 'NSA 6700' or model == 'NSA 4800' or model == 'NSA 6800' or model == 'NSA 5800':
            max_vlan_value = 513
        elif model == 'NSSP 10700' or model == 'NSSP 11700' or model == 'NSSP 13700':
            max_vlan_value = 1025
        elif model == 'NSSP 15700':
            max_vlan_value = 705
        elif model == 'NSV 270' or model == 'NSV 470' or model == 'NSV 870':
            max_vlan_value = 129
        vlan = {
            'type': 'vlan',
            'vlan_tag': max_vlan_value,
            'if': 'x4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '12.15.6.3',
            'netmask': '255.255.255.0'
        }
        resp = interfacev4api.add_interface(msg=True, **vlan)
        error_message = resp[1]['status']['info'][0]['message']
        expected_message = 'Maximum number of VLAN interfaces configured already'
        Assertion.assert_equal(expected_message, error_message,
                               'ERR: sub interface created successfully')


class TestVLAN_Non_TC_delete_sub_interface(Test):
    uuid = 'NonTC'

    def test_00_delete_sub_interfaces(self):
        resp = status_api.show_status()
        model = resp['model'].upper()
        if model == 'TZ 270' or model == 'TZ 270W' or model == 'TZ 80' or model == 'TZ 280' or model == 'TZ 280W' or model == 'TZ 280P':
            max_vlan_value = 65
        elif model == 'TZ 370' or model == 'TZ 370W' or model == 'TZ 470' or model == 'TZ 470W' or model == 'TZ 380' or model == 'TZ 380W' or model == 'TZ 480':
            max_vlan_value = 129
        elif model == 'TZ 570' or model == 'TZ 570W' or model == 'TZ 570P' or model == 'NSA 2700' or model == 'NSA 3700' or model == 'NSA 3800' or model == 'NSA 2800' or model == 'TZ 680' or model == 'TZ 580':
            max_vlan_value = 257
        elif model == 'NSA 4700' or model == 'NSA 5700' or model == 'NSA 6700' or model == 'NSA 4800' or model == 'NSA 6800' or model == 'NSA 5800':
            max_vlan_value = 513
        elif model == 'NSSP 10700' or model == 'NSSP 11700' or model == 'NSSP 13700':
            max_vlan_value = 1025
        elif model == 'NSSP 15700':
            max_vlan_value = 705
        elif model == 'NSV 270' or model == 'NSV 470' or model == 'NSV 870':
            max_vlan_value = 129

        for i in range(1, max_vlan_value):
            vlan = {
                'type': 'vlan',
                'vlan_tag': i,
                'if': 'x3', }
            resp = interfacev4api.del_interface(**vlan)


class TestVLAN_VLAN_items_in_TSR(Test):
    uuid = "SOSAIOT-TC-57316"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '63')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 113,
            'if': 'x4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '19.5.143.11',
            'netmask': '255.255.255.0'
        }
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X4', vlan_id='113')
        Assertion.assert_regular(json.dumps(response), 'vlan": 113', 'err: vlan tag not created')

    def test_02_download_tsr_and_verify(self):
        diag_api.download_tsr()
        file_path = '/tmp/techSupport'
        search_line = 'X4:V113'
        with open(file_path) as f:
            if search_line in f.read():
                res = True
            else:
                res = False
        assert res == True, "Configuration not found in TSR file"

    def test_03_delete_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 113,
            'if': 'x4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '19.5.143.11',
            'netmask': '255.255.255.0', }
        resp = interfacev4api.del_interface(**vlan)
        Assertion.assert_equal(resp, True, "ERR: Delete vlan interface for X4 failed")
        response = interfacev4api.get_vlan_interface_status(name='X4', vlan_id='113')
        resp_message = response['status']['info'][0]['message']
        Assertion.assert_equal(resp_message, "'113' not a reasonable value.",
                               "ERR: Delete vlan interface for X4 failed")


class TestVLAN_VLAN_Preference_support(Test):
    uuid = "SOSAIOT-TC-57317"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '64')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 123,
            'if': 'x2',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '45.5.143.11',
            'netmask': '255.255.255.0'}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='123')
        Assertion.assert_regular(json.dumps(response), 'vlan": 123', 'err: vlan tag not created')

    def test_02_export_setting(self):
        rc = system_settings.export_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(rc, True, "ERR: Export pref failed")

    def test_03_import_setting(self):
        rc = system_settings.import_setting_exp('/tmp/test.exp')
        Assertion.assert_equal(rc, True, "Error: Failed to import the settings...")

    def test_04_verify_config_after_import(self):
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='123')
        Assertion.assert_regular(json.dumps(response), 'vlan": 123', 'err: vlan tag not created')


class TestVLAN_Parent_interface_in_custom_zone(Test):
    uuid = "SOSAIOT-TC-57328"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_add_custom_zone(self):
        custom_zone = {
            "zones": [
                {
                    "name": "custom_zone",
                    "security_type": "public",
                }
            ]
        }
        rc = zone_obj.add_zone_object(**custom_zone)
        Assertion.assert_equal(rc, True, "ERR: add custom zone failed")

    def test_02_update_interface_with_custom_zone(self):
        edit_interface = {
            'if': 'X3',
            'zone': 'custom_zone',
            'mode': 'static',
            'ip': '45.63.2.5',
            'netmask': '255.255.255.0',
        }
        output = interfacev4api.config_interface(**edit_interface)

    def test_03_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 143,
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '89.5.143.11',
            'netmask': '255.255.255.0'}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='143')
        Assertion.assert_regular(json.dumps(response), 'vlan": 143', 'err: vlan tag not created')


class TestVLAN_Parent_interface_in_WLAN_zone(Test):
    uuid = "SOSAIOT-TC-57323"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '7')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_update_interface_with_WLAN_zone(self):
        edit_interface = {
            'if': 'X3',
            'zone': 'WLAN',
            'mode': 'static',
            'ip': '75.63.2.5',
            'netmask': '255.255.255.0',
        }
        output = interfacev4api.config_interface(**edit_interface)

    def test_02_add_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 144,
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '29.5.143.11',
            'netmask': '255.255.255.0',
            'mtu': 1300}
        resp = interfacev4api.add_interface(**vlan)
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='144')
        Assertion.assert_regular(json.dumps(response), 'vlan": 144', 'err: vlan tag not created')

    def test_03_delete_sub_interface(self):
        vlan = {
            'type': 'vlan',
            'vlan_tag': 144,
            'if': 'x3',
            'zone': 'LAN',
            'mode': 'static',
            'ip': '29.5.143.11',
            'netmask': '255.255.255.0',
            'mtu': 1300}
        resp = interfacev4api.del_interface(**vlan)
        Assertion.assert_equal(resp, True, "ERR: Delete vlan interface for X3 failed")
        response = interfacev4api.get_vlan_interface_status(name='X3', vlan_id='144')
        resp_message = response['status']['info'][0]['message']
        Assertion.assert_equal(resp_message, "'144' not a reasonable value.",
                               "ERR: Delete vlan interface for X3 failed")


class TestVLAN_Verify_traffic_statistics_of_vlan_interfaces(Test):
    uuid = "SOSAIOT-TC-57330"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '74')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_config_X4_LAN_zone(self):
        x4_static_dict = {
            'if': 'X4',
            'zone': 'LAN',
            'mode': 'static',
            'ip': Parameter.X4_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc = interfacev4api.config_interface(**x4_static_dict)
        Assertion.assert_equal(
            rc, True, "ERR: Config X4 to static LAN Zone failed")

    def test_02_add_VLAN_subinterface_to_X4(self):
        x4_dmz_vlan1_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN1_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN1_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        x4_lan_vlan2_dict = {
            'if': 'x4',
            'type': 'vlan',
            'vlan_tag': X4_VLAN2_ID,
            'zone': 'lan',
            'mode': 'static',
            'ip': Parameter.X4_VLAN2_IP,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_snmp': True,
            'mgmt_ping': True,
            'user_https': True,
        }
        rc1 = interfacev4api.add_interface(**x4_dmz_vlan1_dict)
        rc2 = interfacev4api.add_interface(**x4_lan_vlan2_dict)
        Assertion.assert_equal(
            rc1 & rc2, True, "ERR: Add Vlan interfaces to X4 failed")

    def test_03_access_sub_interfaces_on_different_PC(self):
        fw.api_logout()
        command = 'python3 ' + scripts_path + 'LoginDUTFromVLANInterface.py -i ' + \
                  Parameter.X4_VLAN1_IP + ' -a login'
        print('command', command)
        res = PC2_login.send_command(command)
        logger.info(f'run login dut script result: {res}')
        result = True if re.search('Successfully login', res) else False
        Assertion.assert_equal(
            result, True, "ERR: Login DUT from vlan subinterface failed")

        command = 'python3 ' + scripts_path + 'LoginDUTFromVLANInterface.py -i ' + \
                  Parameter.X4_VLAN2_IP + ' -a login'
        res = PC4_login.send_command(command)
        logger.info(f'run login dut script result: {res}')
        result = True if re.search('Successfully login', res) else False
        Assertion.assert_equal(
            result, True, "ERR: Login DUT from vlan subinterface failed")

    def test_04_verify_interface_statistic(self):
        flag1 = False
        flag2 = False
        resp = interfacev4api.get_interface_statistics()
        for i in resp:
            if i.get('interface_name') == f'X4:V{X4_VLAN1_ID}':
                if i['rx_unicast_packets'] > 0 and i['tx_unicast_packets'] > 0:
                    flag1 = True

            if i.get('interface_name') == f'X4:V{X4_VLAN2_ID}':
                if i['rx_unicast_packets'] > 0 and i['tx_unicast_packets'] > 0:
                    flag2 = True

        assert flag1 == True, f"verify traffic statistic failed for X4:V{X4_VLAN1_ID}"
        assert flag2 == True, f"verify traffic statistic failed for X4:V{X4_VLAN2_ID}"


class TestVLAN_Parent_interface_in_Transparent_mode(Test):
    uuid = "SOSAIOT-TC-57304"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_configure_x2_interface_in_transparent_mode_and_add_sub_interface(self):
        opt = {
            'if': 'x2',
            'comment': 'trans mode test',
            'zone': 'LAN',
            'mode': 'transparent',
            'transparent_range': {'group': ''},
            'gratuitous_arp_wan_forwarding': False,
            'gratuitous_arp_wan_generation': False,
            'mgmt_https': True,
            'mgmt_ping': True,
        }
        out1 = interfacev4api.config_interface(**opt)

        x2_vlan = {
            'if': 'x2',
            'type': 'vlan',
            'vlan_tag': 333,
            'zone': 'LAN',
            'mode': 'static',
            'ip': '68.45.5.89',
            'mgmt_ping': True,
        }
        resp = interfacev4api.add_interface(**x2_vlan)
        response = interfacev4api.get_vlan_interface_status(name='X2', vlan_id='333')
        Assertion.assert_regular(json.dumps(response), 'vlan": 333', 'err: vlan tag not created')

    def test_03_send_ping_traffic_from_PC1_to_PC2(self):
        command = f'ping {PC2_ETH0_IP} -c 5'
        res = PC1_login.send_command(command)
        logger.info(f'PC1 command result: {res}')
        result = True if '100% packet loss' not in res else False
        Assertion.assert_equal(
            result, True, "ERR: ping from PC1 to PC2 failed")

    def test_04_unassign_interface_X2(self):
        rc = interfacev4api.unassign_interface(interface='X2')


class TestVLAN_Management_traffic_PING(Test):
    uuid = "SOSAIOT-TC-57281"

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '28')
        Assertion.assert_equal(True, True, 'ERR: show testcase info failed')

    def test_01_ping_sub_interface_from_PC1(self):
        command = 'python3 ' + scripts_path + 'LoginDUTFromVLANInterface.py -i ' + \
                  Parameter.X4_VLAN1_IP + ' -a login'
        res = PC2_login.send_command(command)
        logger.info(f'run login dut script result: {res}')
        result = True if re.search('Successfully login', res) else False
        Assertion.assert_equal(
            result, True, "ERR: Login DUT from vlan subinterface failed")
