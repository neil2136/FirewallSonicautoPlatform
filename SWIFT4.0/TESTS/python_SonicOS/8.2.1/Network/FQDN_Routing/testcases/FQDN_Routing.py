from definition.settings import *

class Test_01_TC8_TC13_Config_Stages(Test):
    uuid = 'NonTC'

    def test_01_Create_Address_Groups(self):
        logger.info('Add IPv4 address groups...')
        ipv4_ao_groups = {
            'address_groups': [
                {
                    'ipv6':{
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_ftp['name']}
                            ]
                        },
                        'name': test_01_fqdn_group_name
                    }
                },
                {
                    'ipv6':{
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_smb['name']}
                            ],
                            'ipv4': [
                                {'name': ipv4_host['name']},
                                {'name': ipv4_network['name']}
                            ]
                        },
                        'name': test_01_mixed_group_name
                    }
                },
            ]
        }
        rc = ao_group_api.add_addressgroup(**ipv4_ao_groups)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Groups")

    def test_02_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                { # # # Policy 1, for FQDN www.sonicwall-fqdn-test.com
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_01_ao_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                },
                { # # # Policy 2, for ipv4_fqdn_group including only FQDN AO
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "group": test_01_fqdn_group_name },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_01_group_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                },
                { # # # Policy 3, for ipv4_mixed_group including FQDN and IP AO
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "group": test_01_mixed_group_name },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_01_mixed_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }
        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_03_Ping_FQDN_AO_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc8_13_result['08'] = [True]
            tc8_13_result['10'] = [True]
        else:
            tc8_13_result['08'] = [False]
            tc8_13_result['10'] = [False]
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test 03")

    @repeat_method(3)
    def test_04_Ping_FQDN_GROUP_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF,
        }
        rc = verify(**opts)
        if rc == True:
            tc8_13_result['11'] = [True]
        else:
            tc8_13_result['11'] = [False]
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test 04")

    @repeat_method(3)
    def test_05_Ping_FQDN_AO_in_MIX_GROUP_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc8_13_result['12'].append(True)
        else:
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test 05")

    @repeat_method(3)
    def test_06_Ping_HOST_AO_in_MIX_GROUP_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_host['value'],
            'fqdn_ip': ipv4_host['value'],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc8_13_result['12'].append(True)
        else:
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test 06")

    @repeat_method(3)
    def test_07_Ping_NETWORK_AO_in_MIX_GROUP_on_LAN_PC_and_Capture_on_X3(self):
        out = re.search(r'(\d+\.\d+\.\d+)\.\d+,', ipv4_network['value'])
        test_ip = '201'
        if out:
            test_ip = out.group(1) + '.' + test_ip
        opts = {
            'fqdn': test_ip,
            'fqdn_ip': test_ip,
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc8_13_result['12'].append(True)
        else:
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test 07")

    def test_08_Clear_Environment(self):
        logger.info('Remove route policies...')
        route_rc = route_api.del_route_policy_by_name(test_01_ao_policy)
        route_rc &= route_api.del_route_policy_by_name(test_01_group_policy)
        route_rc &= route_api.del_route_policy_by_name(test_01_mixed_policy)
        if route_rc == True:
            tc8_13_result['13'] = [True]
        logger.info(f'TC8 to TC13 result:\n{tc8_13_result}')
        logger.info('Remove address groups...')
        ao_group_rc = ao_group_api.del_addressgroup(test_01_fqdn_group_name, version='v6')
        ao_group_rc &= ao_group_api.del_addressgroup(test_01_mixed_group_name, version='v6')
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'ipv4', 'name': ipv4_network['name'] }
        ao_rc = ao_api.del_addressobject(**ao_obj)
        ao_obj = { 'ip_type': 'ipv4', 'name': ipv4_host['name'] }
        ao_rc &= ao_api.del_addressobject(**ao_obj)

        rc = route_rc & ao_group_rc
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_02_TC08_Function_Test_of_IPv4_FQDN_PBR(Test):
    uuid = "SOSAIOT-TC-56067"
    description= show_testcase_info(Parameter.TESTPLAN, '08', description=True)['title']

    def test_01_Verify_Result_list_for_TC08(self):
        rc = False
        if False not in tc8_13_result['08'] and True in tc8_13_result['08']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC08 Failed.")


class Test_03_TC10_Function_Test_of_FQDN_PBR_Type_FQDN_AO(Test):
    uuid = "SOSAIOT-TC-56075"
    description= show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_01_Verify_Result_list_for_TC10(self):
        rc = False
        if False not in tc8_13_result['10'] and True in tc8_13_result['10']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC10 Failed.")


class Test_04_TC11_Function_Test_of_FQDN_PBR_Type_FQDN_AO_Group(Test):
    uuid = "SOSAIOT-TC-56076"
    description= show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_01_Verify_Result_list_for_TC11(self):
        rc = False
        if False not in tc8_13_result['11'] and True in tc8_13_result['11']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC11 Failed.")


class Test_05_TC12_Function_Test_of_FQDN_PBR_Type_Mixed_AO_Group(Test):
    uuid = "SOSAIOT-TC-56077"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_01_Verify_Result_list_for_TC12(self):
        rc = False
        if False not in tc8_13_result['12'] and len(tc8_13_result['12']) == 3:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC12 Failed.")


class Test_06_TC13_Delete_A_FQDN_PBR(Test):
    uuid = "SOSAIOT-TC-56068"
    description= show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_01_Verify_Result_list_for_TC12(self):
        rc = False
        if False not in tc8_13_result['13'] and True in tc8_13_result['13']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC13 Failed.")


class Test_07_TC14_PBR_not_Work_When_Delete_One_AO_From_Dst_Group(Test):
    uuid = "SOSAIOT-TC-56078"
    description= show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_01_Create_Address_Groups(self):
        logger.info('Add IPv4 address groups...')
        ipv4_ao_groups = {
            'address_groups': [
                {
                    'ipv6':{
                        'name': fqdn_group_name,
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_www['name']},
                                {'name': ipv4_fqdn_smb['name']}
                            ]
                        }
                    }
                }
            ]
        }
        rc = ao_group_api.add_addressgroup(**ipv4_ao_groups)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Groups")

    def test_02_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "group": fqdn_group_name },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_03_Ping_AO1_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO1 first time")

    def test_04_Ping_AO2_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO2 first time")

    def test_05_Remove_One_AO_from_FQDN_Group(Test):
        logger.info('Remove one AO from IPv4 address group...')
        ipv4_ao_groups = {
            'address_groups': [
                {
                    'ipv6':{
                        'name': fqdn_group_name,
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_www['name']}
                            ]
                        }
                    }
                },
            ]
        }
        rc = ao_group_api.edit_addressgroup_by_name(version='v6', name=fqdn_group_name, msg=False, **ipv4_ao_groups)
        Assertion.assert_equal(rc, True, "ERR: Failed To Edit Address Groups")

    def test_06_Ping_AO1_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO1 second time")

    def test_07_Ping_AO2_Not_in_Group_on_LAN_PC_and_Capture_on_X1(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, False, "ERR: Failed To Verify traffic - test AO2 second time")

    def test_08_Clear_Environment(self):
        logger.info('Remove route policies...')
        route_rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address groups...')
        ao_group_rc = ao_group_api.del_addressgroup(fqdn_group_name, version='v6')

        rc = route_rc & ao_group_rc
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_08_TC15_PBR_Works_When_Add_One_AO_to_Dst_Group(Test):
    uuid = "SOSAIOT-TC-56079"
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_01_Create_Address_Groups(self):
        logger.info('Add IPv4 address groups...')
        ipv4_ao_groups = {
            'address_groups': [
                {
                    'ipv6':{
                        'name': fqdn_group_name,
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_www['name']}
                            ]
                        }
                    }
                }
            ]
        }
        rc = ao_group_api.add_addressgroup(**ipv4_ao_groups)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Groups")

    def test_02_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "group": fqdn_group_name },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_03_Ping_AO1_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO1 first time")

    def test_04_Ping_AO2_Not_in_Group_on_LAN_PC_and_Capture_on_X1(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, False, "ERR: Failed To Verify traffic - test AO2 first time")

    def test_05_Add_One_AO_to_FQDN_Group(Test):
        logger.info('Add one AO to IPv4 address group...')
        ipv4_ao_groups = {
            'address_groups': [
                {
                    'ipv6':{
                        'name': fqdn_group_name,
                        'address_object': {
                            'fqdn': [
                                {'name': ipv4_fqdn_www['name']},
                                {'name': ipv4_fqdn_smb['name']}
                            ]
                        }
                    }
                }
            ]
        }
        rc = ao_group_api.edit_addressgroup_by_name(version='v6', name=fqdn_group_name, msg=False, **ipv4_ao_groups)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Edit Address Groups")

    def test_06_Ping_AO1_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO1 second time")

    def test_07_Ping_AO2_in_Group_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO2 second time")

    def test_08_Clear_Environment(self):
        logger.info('Remove route policies...')
        route_rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address groups...')
        ao_group_rc = ao_group_api.del_addressgroup(fqdn_group_name, version='v6')

        rc = route_rc & ao_group_rc
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_09_TC17_Function_Test_FQDN_PBR_when_FQDN_AO_Include_Wildcard(Test):
    uuid = "SOSAIOT-TC-56069"
    description= show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

    def test_01_Create_Address_Object(self):
        logger.info('Add IPv4 FQDN address object 1...')
        rc = ao_api.config_addressobject(**ipv4_fqdn_wildcard)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Groups")

    def test_02_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_wildcard['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_03_Ping_AO1_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO1")

    @repeat_method(3)
    def test_04_Ping_AO2_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test AO2")

    def test_05_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_wildcard['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_10_TC18_TC19_TC26_Config_Stages(Test):
    uuid = 'NonTC'

    def test_01_Create_Address_Object(self):
        logger.info('Add IPv4 FQDN address object 1...')
        rc = ao_api.config_addressobject(**ipv4_fqdn_wildcard)
        rc &= ao_api.config_addressobject(**ipv4_fqdn_test)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Address Groups")

    def test_02_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_test['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_03_Verify_FQDN_PBR_Not_Active(self):
        commands = ['show tech-support-report routes']
        (rc, output) = fw_cli.do_cli_commands(commands, 1)
        logger.info(output)
        match = re.compile(r'No\s+Any\s+'+ipv4_fqdn_test['name'])
        out = match.search(output, re.I)
        if out:
            logger.info(out.group())
            tc18_19_26_result['18'].append(True)
            tc18_19_26_result['26'].append(True)
        else:
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    @repeat_method(3)
    def test_04_Verify_Traffic_Outgoing_Interface_is_X1(self):
        dn = ipv4_fqdn_test['value']
        dn_ip = domain_list[ipv4_fqdn_test['value']]
        os.popen(f"echo '{dn_ip}    {dn}' >> /etc/hosts")

        out = os.popen(f"cat /etc/hosts | grep {dn}")
        logger.info(dn)
        logger.info(dn_ip)
        logger.info(out)

        opts = {
            'fqdn': dn,
            'fqdn_ip': dn_ip,
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X1_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc18_19_26_result['18'].append(True)
        else:
            time.sleep(5)
        os.popen(f"sed -i '/{dn_ip}/ d' /etc/hosts")
        Assertion.assert_equal(rc, True, "ERR: Verify traffic outgoing interface failed.")

    def test_05_Modify_DNS_Server_on_ROUTER_and_Restart_Service(self):
        ipaddr = domain_list[ipv4_fqdn_test['value']]
        router.send_command(f"chmod +w {dn_file}")

        cmd = f"echo 'test    A       {ipaddr}' >> {dn_file}"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        output = router.send_command(f"cat {dn_file}")
        output += router.send_command(f"netstat -ant|grep ':53 '")

        match = re.compile('test\s+A\s+'+ipaddr)
        out = match.search(output)

        rc = False
        if out and re.search(r':53', output):
            rc = True
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To modify DNS server on router")

    @repeat_method(3)
    def test_06_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_test['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_test['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        if rc == True:
            tc18_19_26_result['19'] = [True]
            tc18_19_26_result['26'].append(True)
        else:
            tc18_19_26_result['19'] = [False]
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_wildcard['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_test['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_08_Restore_DNS_Server_on_ROUTER(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)

        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        router.send_command("service named restart")

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        rc = False
        if re.search(r'TTL 1D', new_config) and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to reset DNS server")


class Test_11_TC18_FQDN_PBR_Should_Be_Gray_Out_when_No_Host_Can_Be_Resolved(Test):
    uuid = "SOSAIOT-TC-56070"
    description= show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

    def test_01_Verify_Result_list_for_TC18(self):
        rc = False
        if False not in tc18_19_26_result['18'] and len(tc18_19_26_result['18']) == 2:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC18 Failed.")


class Test_12_TC19_Gray_FQDN_PBR_Should_Change_Active_Once_AO_Get_Resolved(Test):
    uuid = "SOSAIOT-TC-56080"
    description= show_testcase_info(Parameter.TESTPLAN, '19', description=True)['title']

    def test_01_Verify_Result_list_for_TC19(self):
        rc = False
        if False not in tc18_19_26_result['19'] and True in tc18_19_26_result['19']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC19 Failed.")


class Test_13_TC26_FQDN_PBR_Should_Work_when_New_FQDN_Get_Resolved(Test):
    uuid = "SOSAIOT-TC-56084"
    description= show_testcase_info(Parameter.TESTPLAN, '26', description=True)['title']

    def test_01_Verify_Result_list_for_TC26(self):
        rc = False
        if False not in tc18_19_26_result['26'] and len(tc18_19_26_result['26']) == 2:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC26 Failed.")


class Test_14_TC23_Modify_FQDN_AO_When_It_Is_Used_in_PBR(Test):
    uuid = "SOSAIOT-TC-56081"
    description= show_testcase_info(Parameter.TESTPLAN, '23', description=True)['title']

    def test_01_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_smb['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_02_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_03_Edit_FQDN_Name(self):
        ao_dict = {
            "address_objects": [
                {
                    "fqdn": {
                        "name": test_13_new_name,
                        "domain": ipv4_fqdn_smb['value'],
                        "zone": ipv4_fqdn_smb['zone']
                    }
                }
            ]
        }
        rc = ao_api.edit_addressobject(
            object_type="fqdn", object_path="name", obj_name_uuid=ipv4_fqdn_smb['name'],
            ip_type="ipv4", json_put=ao_dict
        )
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To edit AO")

    def test_04_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_05_Edit_FQDN_Zone(self):
        ao_dict = {
            "address_objects": [
                {
                    "fqdn": {
                        "name": test_13_new_name,
                        "domain": ipv4_fqdn_smb['value'],
                        "zone": test_13_new_zone
                    }
                }
            ]
        }
        rc = ao_api.edit_addressobject(
            object_type="fqdn", object_path="name", obj_name_uuid=test_13_new_name,
            ip_type="ipv4", json_put=ao_dict
        )
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To edit AO")

    def test_06_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Edit_FQDN_Host(self):
        ao_dict = {
            "address_objects": [
                {
                    "fqdn": {
                        "name": test_13_new_name,
                        "domain": test_13_new_host,
                        "zone": test_13_new_zone
                    }
                }
            ]
        }
        rc = ao_api.edit_addressobject(
            object_type="fqdn", object_path="name", obj_name_uuid=test_13_new_name,
            ip_type="ipv4", json_put=ao_dict
        )
        time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed To edit AO")
        
    def test_08_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': test_13_new_host,
            'fqdn_ip': domain_list[test_13_new_host],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_09_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': test_13_new_name }
        rc &= ao_api.del_addressobject(**ao_obj)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_15_TC24_FQDN_PBR_Will_Not_Be_Interrupted_after_Its_Host_IP_Getting_Expired(Test):
    uuid = "SOSAIOT-TC-56082"
    description= show_testcase_info(Parameter.TESTPLAN, '24', description=True)['title']

    def test_00_Disable_DNS_Proxy(self):
        dns_proxy = {
            'enable': False,
            'enforce_all_dns_requests': False,
            'dns_cache': False
        }
        rc = dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to disable DNS proxy")

    def test_01_Modify_DNS_Server(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)
        router.send_command(f"chmod +w {dn_file}")
        cmd = f"sed -i 's/TTL.*/TTL 60S/' {dn_file}"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        dn = ipv4_fqdn_smb['value']
        dn_ip = domain_list[dn]
        os.popen(f"echo '{dn_ip}    {dn}' >> /etc/hosts")

        rc = False

        if re.search(r'TTL 60s', new_config, re.I) and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_02_Add_FQDN_AO(self):
        logger.info('Add IPv4 FQDN address object...')

        rc = ao_api.config_addressobject(**ipv4_fqdn_smb)
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_start_time = int(tmp_time)
        logger.info(f'AO start time {ao_start_time}')
        Assertion.assert_equal(rc, True, "ERR: Failed To Add FQDN AO")

    def test_03_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_smb['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_04_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_05_Stop_DNS_Server_on_ROUTER(self):
        router.send_command("service named stop")
        out = router.send_command("netstat -ant|grep ':53 '")

        rc = False
        if re.search(r':53\s+\S+\s+LISTEN', out, re.I) == None:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed To stop DNS server")

    @repeat_method(3)
    def test_06_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Ping_FQDN_Test_Expired_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        global ao_cur_time
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_cur_time = int(tmp_time)
        logger.info(f"AO start time {ao_start_time}")
        logger.info(f"AO end time {ao_cur_time}")
        run_time = ao_cur_time - ao_start_time
        logger.info(f"AO lasts {run_time}s.")
        if run_time <= 60 and run_time >= 0:
            sleep_time = 60 - run_time
            time.sleep(sleep_time)
        elif run_time < 0:
            time.sleep(60)
        
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_08_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X1(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X1_IF
        }

        global ao_cur_time
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_cur_time = int(tmp_time)
        logger.info(f"AO start time {ao_start_time}")
        logger.info(f"AO end time {ao_cur_time}")
        run_time = ao_cur_time - ao_start_time
        logger.info(f"AO lasts {run_time}s.")
        if run_time <= 120 and run_time >= 0:
            sleep_time = 120 - run_time
            time.sleep(sleep_time)
        elif run_time < 0:
            time.sleep(120)

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_09_Restore_DNS_Server_on_ROUTER(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)

        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        dn_ip = domain_list[ipv4_fqdn_smb['value']]
        os.popen(f"sed -i '/{dn_ip}/ d' /etc/hosts")

        rc = False
        if re.search(r'TTL 1D', new_config, re.I) and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")        

    def test_09_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_smb['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_16_TC25_Previous_Connection_Cache_for_Expired_IP_Should_Be_Flushed(Test):
    uuid = "SOSAIOT-TC-56083"
    description= show_testcase_info(Parameter.TESTPLAN, '25', description=True)['title']

    def test_00_Disable_DNS_Proxy(self):
        dns_proxy = {
            'enable': False,
            'enforce_all_dns_requests': False,
            'dns_cache': False
        }
        rc = dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to disable DNS proxy")

    def test_01_Modify_DNS_Server(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)
        router.send_command(f"chmod +w {dn_file}")
        cmd = f"sed -i 's/TTL.*/TTL 60S/' {dn_file}"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        cmd = "service named restart"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        dn = ipv4_fqdn_smb['value']
        dn_ip = domain_list[dn]
        os.popen(f"echo '{dn_ip}    {dn}' >> /etc/hosts")

        rc = False
        if re.search(r'TTL 60s', new_config, re.I) and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_02_Add_FQDN_AO(self):
        logger.info('Add IPv4 FQDN address object...')
        rc = ao_api.config_addressobject(**ipv4_fqdn_smb)
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_start_time = int(tmp_time)
        logger.info(f'AO start time {ao_start_time}')
        Assertion.assert_equal(rc, True, "ERR: Failed To Add FQDN AO")

    def test_03_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_smb['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_04_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_05_Remove_the_FQDN_from_DNS_Server_on_ROUTER(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)

        router.send_command(f"chmod +w {dn_file}")
        cmd = f"sed -i '/smb/d' {dn_file}"
        logger.info(cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f"cat {dn_file}")
        out += router.send_command("netstat -ant|grep ':53 '")
        rc = False

        if re.search(r'smb\s+A\s+\d+\.\d+\.\d+\.\d+', out, re.I) == None and re.search(r':53', out):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed To modify DNS server")

    @repeat_method(3)
    def test_06_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }
        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Ping_FQDN_Test_Expired_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        global ao_cur_time
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_cur_time = int(tmp_time)
        logger.info(f"AO start time {ao_start_time}")
        logger.info(f"AO end time {ao_cur_time}")
        run_time = ao_cur_time - ao_start_time
        logger.info(f"AO lasts {run_time}s.")
        
        if run_time <= 60 and run_time >= 0:
            sleep_time = 60 - run_time
            time.sleep(sleep_time)
        elif run_time < 0:
            time.sleep(60)

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_08_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X1(self):
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X1_IF
        }

        global ao_cur_time
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_cur_time = int(tmp_time)
        logger.info(f"AO start time {ao_start_time}")
        logger.info(f"AO end time {ao_cur_time}")
        run_time = ao_cur_time - ao_start_time
        logger.info(f"AO lasts {run_time}s.")

        if run_time <= 120 and run_time >= 0:
            sleep_time = 120 - run_time
            time.sleep(sleep_time)
        elif run_time < 0:
            time.sleep(120)

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_09_Restore_DNS_Server_on_ROUTER(self):
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)

        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        dn_ip = domain_list[ipv4_fqdn_smb['value']]
        os.popen(f"sed -i '/{dn_ip}/ d' /etc/hosts")

        rc = False
        if re.search(r'TTL 1D', new_config) and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_10_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_smb['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_17_TC27_Advertise_FQDN_Based_Policy_Route_to_Dynamic_Routing_Disabled(Test):
    uuid = "SOSAIOT-TC-56085"
    description= show_testcase_info(Parameter.TESTPLAN, '27', description=True)['title']

    def test_01_Switch_the_Route_Mode_to_Advanced(self):
        rc = dynamic_route_api.set_advanced_routing_mode(**{'advanced': 'on'})
        Assertion.assert_equal(rc, True, "ERR: Failed To Set Dynamic Routing.")

    def test_02_Disable_FQDN_Advertise(self):
        rc = diag_cli.conf_diag_adv(func='network', sub_para={'advertise-fqdn-route': False})
        Assertion.assert_equal(rc, True, "ERR: Failed To Config Diag Page.")

    def test_03_Enable_OSPF_on_X2_and_Check_Redistribute_Static_Routes(self):
        ospf_config = {
            'static_route': 'on',
            'static_metric': '',
            'static_tag': '',
            'static_metric_type': '2',
            'router_id': '10.0.0.1',
        }
        rc = dynamic_route_api.ospf2_config(**ospf_config)
        ospf_setting = {
            'interface': 'X2',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20'
        }
        rc &= dynamic_route_api.set_ospf2(**ospf_setting)
        Assertion.assert_equal(rc, True, "ERR: Failed To Set OSPF on X2.")

    def test_04_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        time.sleep(15)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_05_Check_the_Router_NSM_via_CLI3(self):
        rc = False
        output = show_nsm_db()
        logger.info(output)
        test_ip = domain_list[ipv4_fqdn_www['value']]
        match = re.compile('Error|' + str(test_ip))
        out = match.search(output, re.I)
        if not out:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to check router NSM via CLI3")

    def test_06_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_18_TC28_TC29_Config_Stages(Test):
    uuid = 'NonTC'

    def test_01_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_02_Switch_the_Route_Mode_to_Advanced(self):
        rc = dynamic_route_api.set_advanced_routing_mode(**{'advanced': 'on'})
        Assertion.assert_equal(rc, True, "ERR: Failed To Set Dynamic Routing.")

    def test_03_Enable_FQDN_Advertise(self):
        rc = diag_cli.conf_diag_adv(func='network', sub_para={'advertise-fqdn-route': ''})
        Assertion.assert_equal(rc, True, "ERR: Failed To Config Diag Page.")

    def test_04_Enable_OSPF_on_X2_and_Check_Redistribute_Static_Routes(self):
        ospf_config = {
            'static_route': 'on',
            'static_metric': '',
            'static_tag': '',
            'static_metric_type': '2',
            'router_id': '10.0.0.1',
            'abr_type': 'standard',
        }
        rc = dynamic_route_api.ospf2_config(**ospf_config)
        ospf_setting = {
            'interface': 'X2',
            'mode': 'enable',
            'hello_interval': '5',
            'dead_interval': '20',
            'area': '0',
            'area_type': 'normal',
        }
        rc &= dynamic_route_api.set_ospf2(**ospf_setting)
        Assertion.assert_equal(rc, True, "ERR: Failed To Set OSPF on X2.")

    @repeat_method(3)
    def test_05_Check_the_Router_NSM_via_CLI3(self):
        output = show_nsm_db()
        logger.info(output)

        rc = False
        if re.search(r'Error', output, re.I):
            logger.info("CLI command error.")
            time.sleep(5)
        elif test_17_ipaddr1 in output:
            rc = True
            tc28_29_result['28'].append(True)
        else:
            time.sleep(10)
        Assertion.assert_equal(rc, True, "ERR: Failed to check router NSM via CLI3")

    def test_06_Modify_DNS_Server_on_ROUTER_and_Restart_Service(self):
        router.send_command(f"chmod +w {dn_file}")

        cmd = f"echo 'www     A       {test_17_ipaddr2}' >> {dn_file}"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        output = router.send_command(f"cat {dn_file}")
        logger.info(output)
        output += router.send_command(f"netstat -ant|grep ':53 '")

        match = re.compile('www\s+A\s+' + test_17_ipaddr2)
        out = match.search(output)

        rc = False
        if out and re.search(r':53', output):
            rc = True

        rc &= ao_api.resolve_all()
        time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed To modify DNS server on router")

    @repeat_method(3)
    def test_07_Check_the_Router_NSM_via_CLI3(self):
        os.system(f"ping {ipv4_fqdn_www['value']} -c 10")
        os.system(f"ping {test_17_ipaddr2} -c 10")
        time.sleep(5)

        output = show_nsm_db()
        logger.info(output)

        rc = False
        if re.search(r'Error', output, re.I):
            logger.info("CLI command error.")
            time.sleep(5)
        elif test_17_ipaddr1 in output and test_17_ipaddr2 in output:
            rc = True
            tc28_29_result['28'].append(True)
        else:
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed to check router NSM via CLI3")

    def test_08_Disable_Advertise_FQDN_Based_Policy_Route_to_Dynamic_Routing_Protocol(self):
        rc = diag_cli.conf_diag_adv(func='network', sub_para={'advertise-fqdn-route': False})
        time.sleep(15)
        Assertion.assert_equal(rc, True, "ERR: Failed To Config Diag Page.")

    @repeat_method(3)
    def test_09_Check_the_Router_NSM_via_CLI3(self):
        output = show_nsm_db()
        logger.info(output)

        rc = False
        if re.search(r'Error', output, re.I):
            tc28_29_result['29'] = [False]
            logger.info("CLI command error.")
            time.sleep(5)
        elif test_17_ipaddr1 not in output and test_17_ipaddr2 not in output:
            rc = True
            tc28_29_result['29'] = [True]
        else:
            tc28_29_result['29'] = [False]
            time.sleep(5)
        Assertion.assert_equal(rc, True, "ERR: Failed to check router NSM via CLI3")

    def test_10_Restore_DNS_Server_on_ROUTER(self):
        router.send_command(f"ifconfig {Parameter.X2_IF}:0 down")
        old_config = router.send_command(f"cat {dn_file}")
        logger.info(old_config)

        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        new_config = router.send_command(f"cat {dn_file}")
        new_config += router.send_command("netstat -ant|grep ':53 '")
        logger.info(new_config)

        rc = False
        if test_17_ipaddr2 not in new_config and re.search(r':53', new_config):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_11_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_19_TC28_Advertise_FQDN_Route_to_Dynamic_Routing_Enabled(Test):
    uuid = "SOSAIOT-TC-56071"
    description= show_testcase_info(Parameter.TESTPLAN, '28', description=True)['title']

    def test_01_Verify_Result_list_for_TC28(self):
        rc = False
        if False not in tc28_29_result['28'] and len(tc28_29_result['28']) == 2:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC28 Failed.")


class Test_20_TC29_Advertise_FQDN_Route_to_Dynamic_Routing_Enable_then_Disable(Test):
    uuid = "SOSAIOT-TC-56086"
    description= show_testcase_info(Parameter.TESTPLAN, '29', description=True)['title']

    def test_01_Verify_Result_list_for_TC29(self):
        rc = False
        if False not in tc28_29_result['29'] and True in tc28_29_result['29']:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: TC29 Failed.")


class Test_21_TC30_Add_FQDN_PBR_in_CLI(Test):
    uuid = "SOSAIOT-TC-56087"
    description= show_testcase_info(Parameter.TESTPLAN, '30', description=True)['title']

    def test_01_Ping_FQDN_Test_on_LAN_PC_and_Capture_on_X1(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X1_IP,
            'dst_if': Parameter.X1_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_02_Add_Route_Policies_out_X3_via_CLI(self):
        route_policies = {
            'if': 'X3',
            'metric': 1,
            'source': 'any',
            'destination': f"name {ipv4_fqdn_www['name']}",
            'name': fqdn_policy,
            'gateway': 'name "X3 Default Gateway"'
        }

        rc = route_cli.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    def test_03_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X3(self):
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_04_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_22_TC32_FQDN_PBR_Works_when_FQDN_AO_Matched_DNS_Proxy_Split_DNS_Entry(Test):
    uuid = '1059520'
    description= show_testcase_info(Parameter.TESTPLAN, '32', description=True)['title']

    def test_01_Modify_DNS_Server(self):
        out = router.send_command(f'cat {named_conf}')
        logger.info(f"Old file:\n{out}")
        cmd = "sed -i 's/listen-on.*/listen-on port 53 { " + Parameter.ROUTER_E1_X2 + "; " \
            + Parameter.ROUTER_E2_X3 + "; };/' " + named_conf
        logger.info(cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f'cat {named_conf}')
        logger.info(f"New file:\n{out}")
        out += router.send_command("netstat -ant|grep ':53 '")

        rc = False
        if f"{Parameter.ROUTER_E0_X1}:53" not in out and f"{Parameter.ROUTER_E1_X2}:53" in out and \
           f"{Parameter.ROUTER_E2_X3}:53" in out:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to modify DNS server")

    def test_02_Add_A_Split_DNS(self):
        split_dns = {
            'domain': ipv4_fqdn_smb['value'],
            'local_interface': "X3",
            'ipv4': {
                'primary': Parameter.ROUTER_E1_X2,
                'secondary': Parameter.ROUTER_E2_X3,
            }
        }
        rc = dns_setting_api.add_split_dns(**split_dns)
        Assertion.assert_equal(rc, True, "ERR: Failed to add split DNS")

    def test_03_Enable_DNS_Proxy_and_Force_Proxy(self):
        dns_proxy = {
            'enable': True,
            'enforce_all_dns_requests': True,
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to config DNS proxy")

    def test_04_Add_FQDN_Object(self):
        logger.info('Add IPv4 FQDN address object...')

        rc = ao_api.config_addressobject(**ipv4_fqdn_smb)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add FQDN AO")

    def test_05_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_smb['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_06_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Restore_DNS_Server_on_ROUTER(self):
        old_config = router.send_command(f"cat {named_conf}")
        logger.info(old_config)

        cmd = "cp -f " + CONFPATH + "/named.conf /var/named/chroot/etc/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f"cat {named_conf}")
        out += router.send_command("netstat -ant|grep ':53 '")
        logger.info(out)

        rc = False
        if f"{Parameter.ROUTER_E0_X1}:53" in out and f"{Parameter.ROUTER_E1_X2}:53" in out and \
           f"{Parameter.ROUTER_E2_X3}:53" in out:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_08_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove all splitDNS...')
        rc &= dns_setting_api.delete_split_dns(domain=ipv4_fqdn_smb['value'])
        logger.info('Disable DNS proxy...')
        dns_proxy = {
            'enable': False,
            'enforce_all_dns_requests': False,
            'dns_cache': False
        }
        rc &= dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_23_TC34_FQDN_PBR_Be_Updated_after_Change_Split_DNS_Entry(Test):
    uuid = '1059522'
    description= show_testcase_info(Parameter.TESTPLAN, '34', description=True)['title']

    def test_01_Modify_DNS_Server(self):
        out = router.send_command(f'cat {named_conf}')
        out += router.send_command(f'cat {dn_file}')
        logger.info(f"Old file:\n{out}")

        cmd = "sed -i 's/listen-on.*/listen-on port 53 { " + Parameter.ROUTER_E1_X2 + "; " \
            + Parameter.ROUTER_E2_X3 + "; };/' " + named_conf
        logger.info(cmd)
        router.send_command(cmd)
        cmd = f"sed -i 's/TTL.*/TTL 60S/' {dn_file}"
        logger.info(cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f'cat {named_conf}')
        out += router.send_command(f'cat {dn_file}')
        logger.info(f"New file:\n{out}")
        out += router.send_command("netstat -ant|grep ':53 '")

        rc = False
        if f"{Parameter.ROUTER_E0_X1}:53" not in out and f"{Parameter.ROUTER_E1_X2}:53" in out and \
           f"{Parameter.ROUTER_E2_X3}:53" in out and 'TTL 60S' in out:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to modify DNS server")

    def test_02_Add_A_Split_DNS(self):
        split_dns = {
            'domain': ipv4_fqdn_smb['value'],
            'local_interface': "X3",
            'ipv4': {
                'primary': Parameter.ROUTER_E1_X2,
            }
        }
        rc = dns_setting_api.add_split_dns(**split_dns)
        Assertion.assert_equal(rc, True, "ERR: Failed to add split DNS")

    def test_03_Enable_DNS_Proxy_and_Force_Proxy(self):
        dns_proxy = {
            'enable': True,
            'enforce_all_dns_requests': True,
            'dns_cache': True
        }
        rc = dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to config DNS proxy")

    def test_04_Add_FQDN_AO(self):
        logger.info('Add IPv4 FQDN address object...')

        rc = ao_api.config_addressobject(**ipv4_fqdn_smb)
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_start_time = int(tmp_time)
        logger.info(f'AO start time {ao_start_time}')
        Assertion.assert_equal(rc, True, "ERR: Failed To Add FQDN AO")

    def test_05_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_smb['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_06_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_smb['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Modify_the_FQDN_IP_Address_from_DNS_Server(self):
        out = router.send_command(f'cat {dn_file}')
        logger.info(f"Old file:\n{out}")
        router.send_command(f'chmod +w {dn_file}')

        cmd = f"sed -i 's/smb.*/smb     A       {test_22_newip}/' {dn_file}"
        logger.info(cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f'cat {dn_file}')
        logger.info(f"New file:\n{out}")
        out += router.send_command("netstat -ant|grep ':53 '")

        rc = False
        match = re.compile(f"smb\s+A\s+{test_22_newip}")
        if ":53" in out and match.search(out):
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to modify DNS server")

    def test_08_Modify_Split_DNS(self):
        split_dns = {
            'domain': ipv4_fqdn_smb['value'],
            'local_interface': "X3",
            'ipv4': {
                'primary': Parameter.ROUTER_E2_X3,
            }
        }
        rc = dns_setting_api.edit_split_dns(**split_dns)
        Assertion.assert_equal(rc, True, "ERR: Failed to add split DNS")

    @repeat_method(3)
    def test_09_Ping_FQDN_Test_Expired_and_the_Offset_Time_Elapsed_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_smb['value'],
            'fqdn_ip': test_22_newip,
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        global ao_cur_time
        global ao_start_time
        tmp_time = local_host.send_command("date +%s")[-5:]
        if tmp_time.startswith('0'):
            tmp_time = '1' + tmp_time
        ao_cur_time = int(tmp_time)
        run_time = int(ao_cur_time) - int(ao_start_time)
        if run_time <= 120 and run_time >= 0:
            sleep_time = 120 - run_time
            time.sleep(sleep_time)
        elif run_time < 0:
            time.sleep(120)

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_10_Restore_DNS_Server_on_ROUTER(self):
        out = router.send_command(f"cat {named_conf}")
        out += router.send_command(f'cat {dn_file}')
        logger.info(out)

        cmd = "cp -f " + CONFPATH + "/named.conf /var/named/chroot/etc/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        cmd = "cp -f " + CONFPATH + "/sonicwall-fqdn-test.com.zone /var/named/chroot/var/named/"
        logger.info("cmd: " + cmd)
        router.send_command(cmd)
        router.send_command("service named restart")

        out = router.send_command(f"cat {dn_file}")
        out += router.send_command(f"cat {named_conf}")
        out += router.send_command("netstat -ant|grep ':53 '")
        logger.info(out)

        rc = False
        if f"{Parameter.ROUTER_E0_X1}:53" in out and f"{Parameter.ROUTER_E1_X2}:53" in out and \
           f"{Parameter.ROUTER_E2_X3}:53" in out and 'TTL 1D' in out:
            rc = True
        Assertion.assert_equal(rc, True, "ERR: Failed to Modify DNS server")

    def test_11_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        logger.info('Remove address objects...')
        ao_obj = { 'ip_type': 'fqdn', 'name': ipv4_fqdn_smb['name'] }
        rc &= ao_api.del_addressobject(**ao_obj)
        logger.info('Remove all splitDNS...')
        rc &= dns_setting_api.delete_split_dns(domain=ipv4_fqdn_smb['value'])
        logger.info('Disable DNS proxy...')
        dns_proxy = {
            'enable': False,
            'enforce_all_dns_requests': False,
            'dns_cache': False
        }
        rc &= dns_proxy_api.config_dnsproxy(**dns_proxy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_24_TC38_Prefs_Export_and_Import_Test(Test):
    uuid = "SOSAIOT-TC-56072"
    description= show_testcase_info(Parameter.TESTPLAN, '38', description=True)['title']

    def test_01_Add_Route_Policies_out_X2_and_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                { # # # Policy 1, for FQDN www.sonicwall-fqdn-test.com
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X2 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_23_policy1,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                },
                { # # # Policy 2, for FQDN ftp.sonicwall-fqdn-test.com
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_ftp['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_23_policy2,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }
        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_02_Ping_FQDN_on_LAN_PC_and_Capture_on_X2(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X2_IP,
            'dst_if': Parameter.X2_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    @repeat_method(3)
    def test_03_Ping_FQDN_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_04_Download_Preference_File_to_Local(self):
        local_host.send_command(f'rm -rf {test_23_pref_file}')
        rc = setting_api.export_setting_exp(filepath=test_23_pref_file)
        rc &= os.path.exists(test_23_pref_file)
        Assertion.assert_equal(rc, True, "ERR: Download setting file failed")

    def test_05_00_Restore_Firewall_to_Factory_Default(self):
        rc = setting_api.boot_fw(2)
        Assertion.assert_equal(rc, True, "ERR: Failed To restore FW")

    def test_05_01_Config_X1_and_Sync_License_On_Line(self):
        rc = if_api.config_interface(**x1_static)
        rc &= license_cli.register('online')
        Assertion.assert_equal(rc, True, "ERR: Config X1 and Sync license on line failed")

    def test_06_Upload_Preference_File(self):
        rc = setting_api.import_setting_exp(test_23_pref_file)
        time.sleep(10)
        rc &= ao_api.resolve_all()
        Assertion.assert_equal(rc, True, "ERR: Import setting file failed")
        
    @repeat_method(3)
    def test_07_Ping_FQDN_on_LAN_PC_and_Capture_on_X2(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X2_IP,
            'dst_if': Parameter.X2_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    @repeat_method(3)
    def test_08_Ping_FQDN_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_09_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(test_23_policy1)
        rc &= route_api.del_route_policy_by_name(test_23_policy2)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_25_TC39_Restart_Test(Test):
    uuid = "SOSAIOT-TC-56073"
    description= show_testcase_info(Parameter.TESTPLAN, '39', description=True)['title']

    def test_01_Add_Route_Policies_out_X2_and_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                { # # # Policy 1, for FQDN www.sonicwall-fqdn-test.com
                    "ipv4": {
                        "interface": "X2",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X2 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_24_policy1,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                },
                { # # # Policy 2, for FQDN ftp.sonicwall-fqdn-test.com
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_ftp['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": test_24_policy2,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }
        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_02_Ping_FQDN_on_LAN_PC_and_Capture_on_X2(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X2_IP,
            'dst_if': Parameter.X2_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    @repeat_method(3)
    def test_03_Ping_FQDN_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_04_Restart_Firewall(self):
        rc = setting_api.boot_fw(1)
        time.sleep(10)
        rc &= ao_api.resolve_all()
        Assertion.assert_equal(rc, True, "ERR: Failed To restart FW")

    @repeat_method(3)
    def test_05_Ping_FQDN_on_LAN_PC_and_Capture_on_X2(self):
        time.sleep(10)
        
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X2_IP,
            'dst_if': Parameter.X2_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    @repeat_method(3)
    def test_06_Ping_FQDN_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_ftp['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_ftp['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_07_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(test_24_policy1)
        rc &= route_api.del_route_policy_by_name(test_24_policy2)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")


class Test_26_TC40_Test_TSR(Test):
    uuid = "SOSAIOT-TC-56074"
    description= show_testcase_info(Parameter.TESTPLAN, '40', description=True)['title']

    def test_01_Add_Route_Policies_out_X3(self):
        logger.info('Add IPv4 route policies...')
        route_policies = {
            "route_policies": [
                {
                    "ipv4": {
                        "interface": "X3",
                        "metric": 1,
                        "source": { "any": True },
                        "destination": { "name": ipv4_fqdn_www['name'] },
                        "service": { "any": True },
                        "gateway": { "name": 'X3 Default Gateway' },
                        "tos": "0x00",
                        "mask": "0x00",
                        "distance": { "auto": True },
                        "name": fqdn_policy,
                        "type": "standard",
                        "priority": 1,
                        "comment": "",
                        "disable_on_interface_down": True,
                        "vpn_precedence": False,
                        "probe": "",
                        "ticket": { "tag1": "", "tag2": "", "tag3": "" }
                    }
                }
            ]
        }

        rc = route_api.add_route_policy(**route_policies)
        Assertion.assert_equal(rc, True, "ERR: Failed To Add Route Policies")

    @repeat_method(3)
    def test_02_Ping_FQDN_on_LAN_PC_and_Capture_on_X3(self):
        time.sleep(10)
        opts = {
            'fqdn': ipv4_fqdn_www['value'],
            'fqdn_ip': domain_list[ipv4_fqdn_www['value']],
            'src_ip': Parameter.X3_IP,
            'dst_if': Parameter.X3_IF
        }

        rc = verify(**opts)
        Assertion.assert_equal(rc, True, "ERR: Failed To Verify traffic - test FQDN test")

    def test_03_Download_and_Check_TSR_and_Check_Corresponding(self):
        local_host.send_command(f'rm -rf {test_25_tsr_file}')
        diagnostic_api.download_tsr(filepath=test_25_tsr_file)
        rc = os.path.exists(test_25_tsr_file)

        tsr_str = local_host.send_command(f'cat {test_25_tsr_file}')
        out = re.search(r'(Network : Routing_START.*Network : Routing_END)', tsr_str, re.I|re.S)
        rc = False
        if out:
            check_str = out.group(1)
            pattern = '\d+\s+Yes\s+Any\s+' + ipv4_fqdn_www['name'] \
                    + '\s+Any.*?Any\W+' + Parameter.X3_GW + '\s+X3'
            logger.info(pattern)
            match = re.compile(pattern)
            if match.search(check_str, re.I):
                rc = True
            else:
                logger.info(check_str)
        if os.path.exists('/etc/resolv.conf_cp'):
            os.system("\cp -rf /etc/resolv.conf_cp /etc/resolv.conf")
        Assertion.assert_equal(rc, True, "ERR: Failed To check TSR")

    def test_04_Clear_Environment(self):
        logger.info('Remove route policies...')
        rc = route_api.del_route_policy_by_name(fqdn_policy)
        Assertion.assert_equal(rc, True, "ERR: Failed to Clear Environment")
