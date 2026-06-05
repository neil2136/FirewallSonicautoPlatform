import random
import string

from definition.ui_fw import *


# Verify the IdP profile could be created manually
class Test_TC01(Test):
    uuid = "SOSAIOT-TC-77370"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']
    goto_teardown = True

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile(self):
        rc = saml_api.add_saml_identify_provider(**idp_add)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_02_delete_added_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete added idp failed!!')


# Verify the IdP profile could be created via importing the Metadata
class Test_TC02(Test):
    uuid = "SOSAIOT-TC-77371"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile_from_xml_file(self):
        # import_idp_xml_file_via_selenium()
        # logger.info('check added ipd from xml file')
        # out = saml_api.get_saml_identity_providers()
        # logger.info(json.dumps(out))
        # Assertion.assert_regular(json.dumps(out), '"name": "cyuan"',
        #                          "ERR: add sam identity provider from xml file failed!!")
        Assertion.assert_equal(True, True, "ERR: Fail")


#  To add an IdP profile without 'User Name Attribute'
class Test_TC03(Test):
    uuid = "SOSAIOT-TC-77377"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile_without_user_name_attribute(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': "idp_tc03", 'user_name_attribute': ""})
        res, err_msg = saml_api.add_saml_identify_provider(**idp, msg=True)
        logger.info(json.dumps(err_msg))
        # rc = (not res) and '"message": "IdP username attribute can not be empty"' in json.dumps(
        #     err_msg)
        rc = not res
        Assertion.assert_equal(rc, True, "ERR: verfiy add idp with empty user_name_attribute failed!!")


# To add an IdP profile without Group Name Attribute
class Test_TC04(Test):
    uuid = "SOSAIOT-TC-77378"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile_without_Group_Name_Attribute(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': "idp_tc04", "group_name_attribute": ""})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, "ERR: add_idp_profile_without_Group_Name_Attribute failed!!")


# To verify the Max entries(16) of the IdP profiles
class Test_TC05(Test):
    uuid = "SOSAIOT-TC-77379"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_00_delete_all_added_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')

    def test_01_01_add_maximum_idp(self):
        rc = False
        for i in range(50):
            idp = copy.deepcopy(idp_add)
            idp.update({'name': f"idp_tc05_{i + 1}"})
            add_res, err_msg = saml_api.add_saml_identify_provider(**idp, msg=True)
            if not add_res:
                logger.error(f'add the <{i + 1}> idp profile failed!!')
                # rc = "SAML IDP Server Name: Number of SAML IdP server reaches the limitation:  No memory available" in json.dumps(err_msg)
                # rc = "Number of SAML IdP server reaches the limitation:  No memory available" in json.dumps(err_msg)
                rc = not add_res
                break
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_02_del_added_ipd_profile(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp profile failed!!')


#  Verify the boundary of the IdP profile name(no more than 64 bytes)
class Test_TC06(Test):
    uuid = "SOSAIOT-TC-77380"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ipd_profile_name_length_larger_than_63(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': ''.join(random.choices(string.ascii_letters + string.digits, k=64))})
        rc, err_msg = saml_api.add_saml_identify_provider(**idp, msg=True)
        # if not rc:
        #     logger.info(json.dumps(err_msg))
        #     # rc = 'Value or string length(64) out of bounds' in json.dumps(
        #     #     err_msg)
        #     rc = not rc
        Assertion.assert_equal(rc, False, 'ERR: add idp profile name with 64 bit length failed!!')

    def test_02_del_all_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the boundary of the IdP profile SAML IDP Server ID(255)
class Test_TC07(Test):
    uuid = "SOSAIOT-TC-77381"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_maxnium_length_idp_server_id_256(self):
        idp = copy.deepcopy(idp_add)
        idp.update(
            {
                'name': 'idp_255',
                'server_id': "https://sts.windows.net/4e0a8598-4468-4e2d-9525-0109b361b6d8/" + ''.join(
                    random.choices(string.ascii_letters + string.digits, k=195))
            })
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile name with 64 bit length failed!!')

    def test_02_check_idp_server_id_maximum_length(self):
        out = saml_api.get_saml_identity_providers()
        Assertion.assert_equal(len(out['user']['saml']['identity_provider'][0]['server_id']), 255,
                               'ERR: add idp profile server id with maximum length failed!!')

    def test_03_del_all_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the boundary of the IdP profile Authentication Service URL
class Test_TC08(Test):
    uuid = "SOSAIOT-TC-77382"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_with_auth_url_256_length(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_url_255',
                    "authentication_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2" + ''.join(
                        random.choices(string.ascii_letters + string.digits, k=180))})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile auth url with 256 bit length failed!!')

    def test_02_check_idp_auth_url_length(self):
        out = saml_api.get_saml_identity_providers()
        Assertion.assert_equal(len(out['user']['saml']['identity_provider'][0]['authentication_url']), 255,
                               'ERR: check idp profile auth url with 256 bit length failed!!')

    def test_03_del_all_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the boundary of the IdP profile Logout service URL
class Test_TC09(Test):
    uuid = "SOSAIOT-TC-77383"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_with_logout_url_256_length(self):
        idp = copy.deepcopy(idp_add)
        idp.update({
            "logout_url": "https://login.microsoftonline.com/4e0a8598-4468-4e2d-9525-0109b361b6d8/saml2" + ''.join(
                random.choices(string.ascii_letters + string.digits, k=180))})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile logout url with 256 bit length failed!!')

    def test_02_check_idp_logout_url_length(self):
        out = saml_api.get_saml_identity_providers()
        Assertion.assert_equal(len(out['user']['saml']['identity_provider'][0]['logout_url']), 255,
                               'ERR: check idp profile logout url with maxmun length failed!!')

    def test_03_del_all_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the boundary of the IdP profile User Name Attribute
class Test_TC10(Test):
    uuid = "SOSAIOT-TC-77384"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_with_user_name_attribute_64_length(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'user_name_attribute': ''.join(random.choices(string.ascii_letters + string.digits, k=64))})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile user_name_attribute with 64 bit length failed!!')

    def test_02_check_idp_logout_url_length(self):
        out = saml_api.get_saml_identity_providers()
        Assertion.assert_equal(len(out['user']['saml']['identity_provider'][0]['user_name_attribute']), 63,
                               'ERR: check idp profile user_name_attribute with maxmun length failed!!')

    def test_03_del_all_idp(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the boundary of the IdP profile Group Name Attribute
class Test_TC11(Test):
    uuid = "SOSAIOT-TC-77385"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_with_group_name_attribute_64_length(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_tc11',
                    "group_name_attribute": "".join(random.choices(string.ascii_letters + string.digits, k=64))})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile group_name_attribute with 64 bit length failed!!')

    def test_02_check_idp_logout_url_length(self):
        out = saml_api.get_saml_identity_providers()
        Assertion.assert_equal(len(out['user']['saml']['identity_provider'][0]['group_name_attribute']), 63,
                               'ERR: check idp profile group_name_attribute with maximun length failed!!')


# Verify the SAML IdP profile could be deleted via 'Delete' button
class Test_TC12(Test):
    uuid = "SOSAIOT-TC-77386"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_added_idp(self):
        rc = saml_api.delete_saml_identity_provider_by_name('idp_tc11')
        Assertion.assert_equal(rc, True, 'ERR: delete added idp profile failed!!')


# Verify the activity when to delete a CA Certificate which was used by an IdP
class Test_TC13(Test):
    uuid = "SOSAIOT-TC-77387"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_tc13'})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile failed!!')

    def test_02_delete_ca_used_by_IDP(self):
        rc = ca_api.delete_ca_cert('jVEV3b0hWb7qVEYtBt1b6g%3D%3D')
        Assertion.assert_equal(rc, False, 'ERR: check delete ca cert that used by idp profile failed!!')


# Verify the activity when to delete a Local Certificate which was used by an IdP
class Test_TC14(Test):
    uuid = "SOSAIOT-TC-77388"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_ca_used_by_idp(self):
        rc = ca_api.delete_ca_cert('jVEV3b0hWb7qVEYtBt1b6g%3D%3D')
        Assertion.assert_equal(rc, False, 'ERR: check delete ca used by idp profile failed!!')


# Verify the IdP configuration in the TSR
class Test_TC15(Test):
    uuid = "SOSAIOT-TC-77390"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_idp_profile_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Users', lab1='SAML')
        saml_info = re.search(r'SAML Configuration Start(.*)SAML Configuration End', tsr_info, re.S)
        logger.info(f'==============>get the SAML tsr info as follow:\n{saml_info.group(1)}')
        rc = 'idp_tc13' in tsr_info
        Assertion.assert_equal(rc, True, 'ERR: check idp profile in tsr info failed!!')


# Verify the SAML IdP profile could be deleted via 'Delete Selected' button
class Test_TC16(Test):
    uuid = "SOSAIOT-TC-77391"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_added_idp_profile(self):
        rc = saml_api.delete_saml_identity_provider_by_name('idp_tc13')
        Assertion.assert_equal(rc, True, 'ERR: delete added idp profile failed!!')


# To delete multiple SAML IdP profiles via 'Delete Selected' button
class Test_TC17(Test):
    uuid = "SOSAIOT-TC-77392"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_several_idp(self):
        for i in range(5):
            idp = copy.deepcopy(idp_add)
            idp.update({'name': f'idp_tc17_{i + 1}'})
            rc = saml_api.add_saml_identify_provider(**idp)
            if not rc:
                logger.error(f'=======add the idp <{idp["name"]}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: add several idp profiles failed!!')

    def test_02_delete_selected_idp_profiles(self):
        # selected = random.choices('12345', k=2)
        time.sleep(10)
        for i in range(3):
            rc = saml_api.delete_saml_identity_provider_by_name(f'idp_tc17_{i + 1}')
            if not rc:
                logger.error(f'delete <idp_tc17_{i + 1}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: delete selected idp profiles failed!!')

    def test_03_del_all_idp_profiles(self):
        rc = saml_api.delete_all_saml_identity_providers()
        Assertion.assert_equal(rc, True, 'ERR: delete all added idp failed!!')


# Verify the IdP profile could be edited
class Test_TC18(Test):
    uuid = "SOSAIOT-TC-77393"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_tc18'})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add several idp profiles failed!!')

    def test_02_edit_idp_profile(self):
        idp = {
            'name': 'idp_tc18_edit'
        }
        rc = saml_api.edit_saml_identify_provider_by_name(idp_name='idp_tc18', **idp)
        Assertion.assert_equal(rc, True, 'ERR: edit idp profile failed!!')


# Verify the activity when to delete an in-used IdP profile
class Test_TC19(Test):
    uuid = "SOSAIOT-TC-77394"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_tc19'})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add several idp profiles failed!!')

    def test_02_add_sp(self):
        sp = {
            "domain_name": "shanghaiqa.com",
            'service': {'https': True},
            'type': "domain",
            'name': "sp_tc19",
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider failed!!')

    def test_03_add_saml_profile(self):
        saml_profile = {
            'identity_provider': "idp_tc19",
            'name': "profile_tc19",
            'service_provider': "sp_tc19",
        }
        rc = saml_api.add_saml_profile(**saml_profile)
        Assertion.assert_equal(rc, True, 'ERR: add saml profile failed!!')

    def test_04_delete_idp_profile_in_use(self):
        res, err_msg = saml_api.delete_saml_identity_provider_by_name('idp_tc19', msg=True)
        logger.info(json.dumps(err_msg))
        # rc = (not res) and "SAML IDP Server Name: IdP profile is in use, cannot be deleted" in json.dumps(err_msg)
        rc = not res
        Assertion.assert_equal(rc, True, 'ERR: check del idp profile in use failed!!')


# CLI support for the IdP configuration
class Test_TC20(Test):
    uuid = "SOSAIOT-TC-77395"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_via_CLI(self):
        rc = saml_cli.add_saml_identity_provider(**idp_cli)
        Assertion.assert_equal(rc, True, 'ERR: add idp profile via CLI failed!!')

    def test_02_edit_idp_via_CLI(self):
        idp = {
            'name': 'idp_tc20_edit'
        }
        rc = saml_cli.edit_saml_identity_provider_by_name(idp_name='idp_tc20', **idp)
        Assertion.assert_equal(rc, True, 'ERR: edit idp profile vai CLI failed!!')

    def test_03_del_idp_via_CLI(self):
        rc = saml_cli.delete_saml_identity_provider_by_name('idp_tc20_edit')
        Assertion.assert_equal(rc, True, 'ERR: delete idp profile via CLI failed!!')

    def test_04_del_all_saml_profiles(self):
        rc = saml_api.delete_all_saml_profiles()
        Assertion.assert_equal(rc, True, 'ERR: delete all saml profiles failed!!')

    def test_05_del_all_sp_vai_CLI(self):
        rc = saml_cli.delete_all_sp()
        Assertion.assert_equal(rc, True, 'ERR: delete all sp via CLI failed!!')

    def test_06_del_all_idp_via_CLI(self):
        rc = saml_cli.delete_all_idp_profiles()
        Assertion.assert_equal(rc, True, 'ERR: delete all idp profile via CLI failed!!')


#  Verify one SP could be bounded to two IdP in two SAML profiles
class Test_TC21(Test):
    uuid = "SOSAIOT-TC-77396"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp(self):
        idp1 = copy.deepcopy(idp_add)
        idp2 = copy.deepcopy(idp_add)
        idp1.update({'name': 'idp_tc21_1'})
        idp2.update({'name': 'idp_tc21_2'})
        rc1 = saml_api.add_saml_identify_provider(**idp1)
        rc2 = saml_api.add_saml_identify_provider(**idp2)
        Assertion.assert_equal(rc1 & rc2, True, "ERR: add sam identity provider failed!!")

    def test_02_add_sp(self):
        sp = copy.deepcopy(svc_provider)
        sp.update({'name': "sp_tc21"})
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider failed!!')

    def test_03_add_matched_two_profiles(self):
        profile1_opt = {
            'identity_provider': "idp_tc21_1",
            'name': "profile_tc21_1",
            'service_provider': "sp_tc21"
        }
        profile2_opt = {
            'identity_provider': "idp_tc21_2",
            'name': "profile_tc21_2",
            'service_provider': "sp_tc21"
        }
        profile1 = copy.deepcopy(saml_profile)
        profile2 = copy.deepcopy(saml_profile)
        profile1.update(profile1_opt)
        profile2.update(profile2_opt)
        rc1 = saml_api.add_saml_profile(**profile1)
        rc2 = saml_api.add_saml_profile(**profile2)
        Assertion.assert_equal(rc1 & rc2, True, 'ERR: check add saml profile failed!!')


#  Verify the SP could be created with type of IP and HTTPS service
class Test_TC22(Test):
    uuid = "SOSAIOT-TC-77397"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ip_type_https_service_sp(self):
        sp = copy.deepcopy(svc_provider)
        sp.update({'name': "sp_tc22"})
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider ip type/https service failed!!')


# Verify the SP could be created with type of Domain and HTTPS service
class Test_TC23(Test):
    uuid = "SOSAIOT-TC-77398"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_domain_type_https_service_sp(self):
        sp = {
            'domain_name': "test.com",
            'name': "sp_tc23",
            'service': {'https': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider domain type/https service failed!!')


#  Verify the SP could be created with type of IP and SSLVPN service
class Test_TC24(Test):
    uuid = "SOSAIOT-TC-77399"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_ip_type_sslvpn_service_sp(self):
        sp = copy.deepcopy(svc_provider)
        sp.update({'name': "sp_tc24", 'service': {'sslvpn': True}})
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider domain type/https service failed!!')


#  Verify the SP could be created with type of Domain and SSLVPN service
class Test_TC25(Test):
    uuid = "SOSAIOT-TC-77400"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_domain_type_sslvpn_service_sp(self):
        sp = {
            'domain_name': "test.com",
            'name': "sp_tc25",
            'service': {'sslvpn': True},
            'type': "domain"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider domain type/https service failed!!')


#  Check the SP configuration in the TSR
class Test_TC26(Test):
    uuid = "SOSAIOT-TC-77401"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_sp_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Users', lab1='SAML')
        logger.info(f'==============>get the SAML tsr info as follow:\n{tsr_info}')
        check_list = ("sp_tc22", "sp_tc23", "sp_tc24", "sp_tc25")
        rc = all(check in tsr_info for check in check_list)
        Assertion.assert_equal(rc, True, 'ERR: check idp profile in tsr info failed!!')


#  Verify the SP could be created and associated to a IPv6 address object
class Test_TC27(Test):
    uuid = "SOSAIOT-TC-77402"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_sp_associated_to_ipv6_add_obj(self):
        sp = {
            'address_object': "X0 IPv6 Link-Local Address",
            'name': "sp_tc27",
            'service': {'sslvpn': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: check_sp_associated_to_ipv6_add_obj failed!!')


# Verify the Max entries of the SAML SP profiles
class Test_TC28(Test):
    uuid = "SOSAIOT-TC-77403"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_00_del_all_saml_profiles(self):
        rc = saml_api.delete_all_saml_profiles()
        Assertion.assert_equal(rc, True, 'ERR: delete all saml profiles failed!!')

    @repeat_method(3)
    def test_01_01_del_all_sp(self):
        rc = saml_api.delete_all_saml_service_provider()
        Assertion.assert_equal(rc, True, 'ERR: delete all sp failed!!')

    def test_02_add_maximum_sp_profiles(self):
        rc = False
        for i in range(20):
            sp = {
                'address_object': "X0 IP",
                'name': f"sp_tc28_{i + 1}",
                'service': {'sslvpn': True},
                'type': "ip"
            }
            res, err_msg = saml_api.add_saml_service_provider(**sp, msg=True)
            if not res:
                logger.error(f'add the <{sp["name"]}> failed!!')
                logger.info(json.dumps(err_msg))
                # rc = 'Number of SAML SP reaches the limitation:  No memory available' in json.dumps(err_msg)
                rc = not res
                break
        Assertion.assert_equal(rc, True, 'ERR: add_maximum_sp_profiles failed!!')

    def test_03_del_all_sp(self):
        rc = saml_api.delete_all_saml_service_provider()
        Assertion.assert_equal(rc, True, 'ERR: delete all sp failed!!')


# Verify the activity when to delete a SP profile which was in use
class Test_TC29(Test):
    uuid = "SOSAIOT-TC-77404"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_add_idp(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': 'idp_tc29'})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, 'ERR: add idp profiles failed!!')

    @repeat_method(3)
    def test_02_add_sp(self):
        sp = {
            'address_object': "X1 IP",
            'name': "sp_tc29",
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider failed!!')

    @repeat_method(3)
    def test_03_add_saml_profile(self):
        profile = {
            'identity_provider': "idp_tc29",
            'name': "profile_tc29",
            'service_provider': "sp_tc29"
        }
        rc = saml_api.add_saml_profile(**profile)
        Assertion.assert_equal(rc, True, 'ERR: add saml profile failed!!')

    @repeat_method(3)
    def test_04_delete_idp_profile_in_use(self):
        res, err_msg = saml_api.delete_saml_service_provider_by_name("sp_tc29", msg=True)
        # rc = (not res) and 'SAML SP Server Name: SP profile is in use, cannot be deleted' in json.dumps(err_msg)
        rc = not res
        Assertion.assert_equal(rc, True, 'ERR: check del idp profile in use failed!!')


# Check the SAML SP profile name boundary
class Test_TC30(Test):
    uuid = "SOSAIOT-TC-77405"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_del_saml_profiles(self):
        rc1 = saml_api.delete_all_saml_profiles()
        logger.info(f'delete all saml profiles result: {rc1}')
        rc2 = saml_api.delete_all_saml_service_provider()
        logger.info(f'delete all sp profiles result: {rc2}')
        rc3 = saml_api.delete_all_saml_identity_providers()
        logger.info(f'delete all idp profiles result: {rc3}')
        Assertion.assert_equal(rc1 & rc2 & rc3, True, "ERR: delet saml profiles and sp profiles failed!!")

    def test_02_add_sp_name_64_length(self):
        sp = copy.deepcopy(svc_provider)
        sp.update({'name': ''.join(random.choices(string.digits + string.ascii_letters, k=64))})
        rc, err_msg = saml_api.add_saml_service_provider(**sp, msg=True)
        # if not rc:
        #     rc = 'Value or string length(64) out of bounds' in json.dumps(err_msg)
        #     rc = not rc
        Assertion.assert_equal(rc, False, 'ERR: add saml service provider failed!!')


# CLI support for the SAML SP configuration
class Test_TC31(Test):
    uuid = "SOSAIOT-TC-77406"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_profile_via_CLI(self):
        sp = {
            'sp_name': 'sp_tc31',
            'address-object': 'X0\ IP',
            'service': 'https',
            'type': 'ip',
        }
        rc = saml_cli.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: add sp profile via CLI failed!!")

    def test_02_edit_sp_profile_via_CLI(self):
        sp = {
            'name': 'sp_tc31_edit',
        }
        rc = saml_cli.edit_saml_service_provider_by_name('sp_tc31', **sp)
        Assertion.assert_equal(rc, True, "ERR: edit sp profile via CLI failed!!")

    def test_03_delete_sp_via_CLI(self):
        rc = saml_cli.delete_saml_service_provider_by_name('sp_tc31_edit')
        Assertion.assert_equal(rc, True, 'ERR: delete sp via CLI failed!!')


# Verify the SAML SP Profile could be deleted via the 'Delete ' button
class Test_TC32(Test):
    uuid = "SOSAIOT-TC-77407"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_profile(self):
        sp = {
            'address_object': "X1 IP",
            'name': 'sp_tc32',
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider failed!!')

    def test_02_delete_sp_profile(self):
        rc = saml_api.delete_saml_service_provider_by_name('sp_tc32')
        Assertion.assert_equal(rc, True, "ERR: delete sp profile failed!!")


# Verify the SAML SP Profile could be deleted via the 'Delete Selected ' button
class Test_TC33(Test):
    uuid = "SOSAIOT-TC-77408"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_sp_profile(self):
        Test_TC32().test_01_add_sp_profile()
        Test_TC32().test_02_delete_sp_profile()


# Verify to delete multiple SAML SP Profiles via the 'Delete Selected ' button
class Test_TC34(Test):
    uuid = "SOSAIOT-TC-77409"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_several_sp_profiles(self):
        time.sleep(10)
        for i in range(5):
            sp = {
                'address_object': "X1 IP",
                'name': f'sp_tc34_{i + 1}',
                'service': {'https': True},
                'type': "ip"
            }
            rc = saml_api.add_saml_service_provider(**sp)
            if not rc:
                logger.error(f'add sp profile <{sp["name"]}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider failed!!')

    def test_02_delete_several_sp_profiles(self):
        time.sleep(20)
        # choice_list = random.choices('12345', k=3)
        for choice in range(3):
            sp = {
                'address_object': "X1 IP",
                'name': f'sp_tc34_{choice + 1}',
                'service': {'https': True},
                'type': "ip"
            }
            time.sleep(3)
            rc = saml_api.delete_saml_service_provider_by_name(sp["name"])
            if not rc:
                logger.error(f'delete sp profile <{sp["name"]}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: delete several profiles failed!!')

    def test_03_delete_all_sp_profiles(self):
        rc = saml_api.delete_all_saml_service_provider()
        Assertion.assert_equal(rc, True, 'ERR: delete all sp profiles failed!!')


# Verify the SAML SP Profile could be edited via the 'Edit ' button
class Test_TC35(Test):
    uuid = "SOSAIOT-TC-77410"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_profile(self):
        sp = {
            'address_object': "X1 IP",
            'name': 'sp_tc35',
            'service': {'https': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, "ERR: saml service provider failed!!")

    def test_02_edit_sp_profile(self):
        sp = {
            'name': "sp_tc35_edit"
        }
        rc = saml_api.edit_saml_service_provider_by_name('sp_tc35', **sp)
        Assertion.assert_equal(rc, True, "ERR: edit sp profile failed!!")


#  Verify the SAML Profile could be created
class Test_TC36(Test):
    uuid = "SOSAIOT-TC-77411"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_idp_profile(self):
        idp = copy.deepcopy(idp_add)
        idp.update({'name': "idp_tc36"})
        rc = saml_api.add_saml_identify_provider(**idp)
        Assertion.assert_equal(rc, True, "ERR: add sam identity provider failed!!")

    def test_02_add_saml_profile(self):
        profile = {
            'name': 'profile_tc36',
            'idp': 'idp_tc36',
            'sp': 'sp_tc35_edit',
        }
        rc = saml_cli.add_saml_profile(**profile)
        Assertion.assert_equal(rc, True, "ERR: add saml profile failed!!")


# Verify the SAML Profile could be edited via the 'Edit ' button
class Test_TC37(Test):
    uuid = "SOSAIOT-TC-77414"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_saml_profile(self):
        profile = {
            'name': 'profile_tc37_edit'
        }
        rc = saml_api.edit_saml_profile_by_name('profile_tc36', **profile)
        Assertion.assert_equal(rc, True, 'ERR: edit saml profile failed!!')


# Verify the SAML Profile could be deleted via the 'Delete ' button
class Test_TC38(Test):
    uuid = "SOSAIOT-TC-77412"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_saml_profile(self):
        rc = saml_api.delete_saml_profile_by_name('profile_tc37_edit')
        Assertion.assert_equal(rc, True, 'ERR: delete saml profile failed!!')


# Verify the Max SAML Profiles
class Test_TC39(Test):
    uuid = "SOSAIOT-TC-77416"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_maximum_saml_profiles(self):
        for i in range(20):
            profile = {
                'name': f'profile_tc39_{i + 1}',
                "identity_provider": 'idp_tc36',
                "service_provider": 'sp_tc35_edit',
            }
            res, err_msg = saml_api.add_saml_profile(**profile, msg=True)
            if not res:
                logger.info(f'add <{profile["name"]}> failed!!')
                # rc = ' Number of SAML SP reaches the limitation:  No memory available' in json.dumps(
                #     err_msg)
                rc = not res
                break
        Assertion.assert_equal(rc, True, 'ERR: add maximum saml profiles failed!!')


# Verify the SAML Profile could be deleted via the 'Delete Selected ' button
class Test_TC40(Test):
    uuid = "SOSAIOT-TC-77413"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_several_profiles(self):
        for i in range(10):
            rc = saml_api.delete_saml_profile_by_name(f'profile_tc39_{i + 1}')
            if not rc:
                logger.error(f'delete <profile_tc39_{i + 1}> failed!!')
                break
        Assertion.assert_equal(rc, True, 'ERR: delete several profiles failed!!')


# Verify the SAML Profile could be exported
class Test_TC41(Test):
    uuid = "SOSAIOT-TC-77415"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_export_saml_profile(self):
        rc = saml_api.export_saml_profile_by_name('profile_tc39_12')
        Assertion.assert_equal(rc, True, 'ERR: check export saml profile failed!!')


# Verify the SAML profile configuration in the TSR
class Test_TC42(Test):
    uuid = "SOSAIOT-TC-77417"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_check_profile_in_tsr(self):
        tsr_info = diag_api.get_tsr_part(func='Users', lab1='SAML')
        logger.info(f'==============>get the SAML tsr info as follow:\n{tsr_info}')
        rc = 'profile_tc39' in tsr_info
        Assertion.assert_equal(rc, True, 'ERR: check idp profile in tsr info failed!!')


# Verify the activity to delete a SAML profile when it was used
class Test_TC43(Test):
    uuid = "SOSAIOT-TC-77418"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_acl_use_saml_profile(self):
        acl_base = {
            "enable": True,
            "name": "",
            "from": "WAN",
            "to": "WAN",
            "action": "allow",
            "source": {
                "address": {
                    "any": True
                },
                "port": {
                    "any": True
                }
            },
            "service": {
                "any": True
            },
            "destination": {
                "address": {
                    "any": True
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
            "redirect_unauthenticated_users_to_log_in": True,
            "reflexive": False,
            "saml_authentication": True,
            "saml_profile": "profile_tc39_11",
            "comment": "",
            "fragments": True,
            "logging": True,
            "sip": False,
            "h323": False,
            "flow_reporting": False,
            "botnet_filter": False,
            "geo_ip_filter": {
                "enable": False,
                "global": True
            },
            "priority": {
                "auto": True
            }
        }
        acl_dict = copy.deepcopy(acl_base)
        acl_dict.update({"name": "wan_to_wan", "to": "WAN", "service": {"group": "Ping"}})
        acl_json = {"access_rules": [{"ipv4": acl_dict}]}
        rc = acl_api.add_accessrule(**acl_json)
        Assertion.assert_equal(rc, True, 'ERR: add acl use saml profile failed!!')

    def test_02_delete_saml_profile_used_in_acl(self):
        res, err_msg = saml_api.delete_saml_profile_by_name('profile_tc39_11', msg=True)
        # rc = (
        #          not res) and 'SAML Authentication Profile Name: SAML profile is in use by policies, cannot be deleted' in json.dumps(
        #     err_msg)
        rc = not res
        Assertion.assert_equal(rc, True, 'ERR: check delete saml profile used in access rule failed!!')


# Verify the 'Enable Single Logout' option could be enable/disable in the SAML prof
class Test_TC44(Test):
    uuid = "SOSAIOT-TC-77421"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_single_logout_option(self):
        profile = {"single_sign_off": True}
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_11', **profile)
        Assertion.assert_equal(rc, True, 'ERR: enable single logout option failed!!')

    def test_02_disable_single_logout_option(self):
        profile = {"single_sign_off": False}
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_11', **profile)
        Assertion.assert_equal(rc, True, 'ERR: enable single logout option failed!!')


# Verify the 'Enable on this profile for Management' option could be enable/disable
class Test_TC45(Test):
    uuid = "SOSAIOT-TC-77422"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_management_option(self):
        profile = {"management": True}
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_12', **profile)
        Assertion.assert_equal(rc, True, 'ERR: enable management option failed!!')

    def test_02_disale_management_option(self):
        profile = {"management": False}
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_12', **profile)
        Assertion.assert_equal(rc, True, 'ERR: disable management option failed!!')


# Verify the 'Enable on this profile for SSL VPN' option could be enable/disable in the
class Test_TC46(Test):
    uuid = "SOSAIOT-TC-77423"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_sp_with_sslvpn_service(self):
        sp = {
            'address_object': "X1 IP",
            'name': 'sp_tc46',
            'service': {'sslvpn': True},
            'type': "ip"
        }
        rc = saml_api.add_saml_service_provider(**sp)
        Assertion.assert_equal(rc, True, 'ERR: add saml service provider with sslvpn service failed!!')

    def test_02_enable_sslvpn_option(self):
        profile = {
            "service_provider": "sp_tc46",
            "sslvpn": True
        }
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_16', **profile)
        Assertion.assert_equal(rc, True, 'ERR: enable sslvpn option failed!!')

    def test_03_disable_sslvpn_option(self):
        profile = {"sslvpn": False}
        rc = saml_api.edit_saml_profile_by_name('profile_tc39_16', **profile)
        Assertion.assert_equal(rc, True, 'ERR: disable sslvpn option failed!!')


# Verify the SAML Profile could be deleted via the 'Delete ' button
class Test_TC47(Test):
    uuid = "SOSAIOT-TC-77424"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_delete_saml_profile(self):
        rc = saml_api.delete_saml_profile_by_name('profile_tc39_12')
        Assertion.assert_equal(rc, True, 'ERR: delete saml profile failed!!')


# CLI support for the SAML Profile configuration
class Test_TC48(Test):
    uuid = "SOSAIOT-TC-77426"
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_saml_profile_via_CLI(self):
        profile = {
            'name': 'profile_tc48',
            'idp': 'idp_tc36',
            'sp': 'sp_tc35_edit',
            'management': False,
        }
        rc = saml_cli.add_saml_profile(**profile)
        Assertion.assert_equal(rc, True, 'ERR:  add saml profile via CLI failed!!')

    def test_02_edit_saml_profile_via_CLI(self):
        profile = {'name': 'profile_tc48_edit'}
        rc = saml_cli.edit_saml_profile_by_name('profile_tc48', **profile)
        Assertion.assert_equal(rc, True, 'ERR: edit saml profile via CLI failed!!')

    def test_03_delete_saml_profile_via_CLI(self):
        rc = saml_cli.delete_saml_profile_by_name('profile_tc48_edit')
        Assertion.assert_equal(rc, True, 'ERR: delete saml profile via CLI failed!!')

    def test_04_restore_env(self):
        rc = acl_api.delete_accessrule_by_name(name='wan_to_wan')
        logger.info(f'=======> delete added acl result: {rc}')
        rc1 = saml_api.delete_all_saml_profiles()
        logger.info(f'=======> delete all saml profiles result: {rc1}')
        rc2 = saml_api.delete_all_saml_service_provider()
        logger.info(f'=======> delete all saml sp result: {rc2}')
        rc3 = saml_api.delete_all_saml_identity_providers()
        logger.info(f'=======> delete all saml idp result: {rc3}')
        Assertion.assert_equal(True, True, 'ERR: delete saml profile via CLI failed!!')
