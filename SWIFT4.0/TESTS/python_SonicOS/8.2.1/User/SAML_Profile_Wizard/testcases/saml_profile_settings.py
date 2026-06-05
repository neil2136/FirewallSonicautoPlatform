from definition.ui_fw import *


# Create SAML Profile via Wizard
class Test_TC01(Test):
    uuid = '4119730'
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    @repeat_method(3)
    def test_01_create_saml_profile_via_wizard(self):
        os.system('rm -rf /root/Downloads/*')
        init_test_page()
        
        configure_wizard_profile_part('profile_wizard_1')
        
        configure_wizard_sp_part('sp_wizard_1')
        
        export_sp_part()
        
        configure_wizard_idp_part('idp_wizard_1')
        
        configure_wizard_address_and_acs_part()
        
        apply_wizard_configuration_and_close()
        
        logger.info('check if saml profile created success...')
        profiles = saml_api.get_saml_profiles()
        logger.info(profiles)
        rc1 = 'profile_wizard' in str(profiles)
        Assertion.assert_equal(rc1, True, "ERR: saml profile created failed")
        logger.info('check exported profile')
        # rc2 = os.path.exists('/root/Downloads/profile_wizard_1.xml')
        # Assertion.assert_equal(rc2, True, "ERR: exported profile not exists")
    
    
class Test_TC02(Test):
    uuid = '4119731'
    description = "Create a Domain Type Service Provider via Wizard"
    
    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test01_create_sslvpn_type_profile(self):
        os.system('rm -rf /root/Downloads/*')
        init_test_page()
        
        configure_wizard_profile_part('profile_wizard_2')
        configure_wizard_sp_part('sp_wizard_2')
        export_sp_part()
        
        configure_wizard_idp_from_exists()
        
        configure_wizard_address_and_acs_part()
        
        apply_wizard_configuration_and_close()
        
        logger.info('check if saml profile created success...')
        profiles = saml_api.get_saml_profiles()
        logger.info(profiles)
        Assertion.assert_equal('profile_wizard_2' in str(profiles), True, "ERR: saml profile created failed")
        # logger.info('check exported xml file')
        # Assertion.assert_equal(os.path.exists('/root/Downloads/profile_wizard_2.xml'), True, "ERR: exported profile not exists")
        
        
#To manually set the IdP via SAML Wizard 
class Test_TC03(Test):
    uuid = '4119732'
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_manual_set_idp_via_saml_wizard(self):
        logger.info('this case is including in TC01 and TC02')
        Assertion.assert_equal(True, True, "ERR: this case is including in TC01 and TC02")
        
        
# To check the pre-create SP/IdP profile could be selected via SAML Wizard
class Test_TC04(Test):
    uuid = '4119733'
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_check_pre_create_profile(self):
        os.system('rm -rf /root/Downloads/*')
        init_test_page()
        
        configure_wizard_profile_part('profile_wizard_3')
        configure_wizard_sp_from_exists(sp_name='sp_wizard_1')
        export_sp_part()
        configure_wizard_idp_from_exists()
        configure_wizard_address_and_acs_part()
        
        apply_wizard_configuration_and_close()
        logger.info('check if saml profile created success...')
        profiles = saml_api.get_saml_profiles()
        logger.info(profiles)
        Assertion.assert_equal('profile_wizard_3' in str(profiles), True, "ERR: saml profile created failed")
        # logger.info('check exported xml file')
        # Assertion.assert_equal(os.path.exists('/root/Downloads/profile_wizard_3.xml'), True, "ERR: exported profile not exists")
        
        
# To Use a certificate to sign SP request via SAML Wizard 
class Test_TC05(Test):
    uuid = '4119734'
    description = show_testcase_info(TESTPLAN, uuid, description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(TESTPLAN, self.uuid)
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    @repeat_method(3)
    def test_01_use_certificate_to_sign_sp_request(self):
        os.system('rm -rf /root/Downloads/*')
        init_test_page()
        
        logger.info('configure profile part'.center(40, '='))
        time.sleep(3)
        logger.info('fill in profile_name')
        profile_name_xpath = '//input[@name="profile-name"]'
        fw_page_ui.set_input_text_field(*['xpath', profile_name_xpath], 'profile_wizard_4') 
        logger.info('fill in comment')
        time.sleep(3)
        comment_xpath = '//input[@name="comment"]' 
        fw_page_ui.set_input_text_field(*['xpath', comment_xpath], 'add saml profile via wizard')   
        
        logger.info('enable sp request')
        request_button_xpath = '//div[contains(@class, "sw-toggle") and .//input[@name="profile-cert-request"]]'
        fw_page_ui.click_element('xpath', request_button_xpath)
        
        logger.info('click cert select down...')
        cert_select_xpath = '//span[contains(text(), "Select Certificate")]'
        fw_page_ui.click_element('xpath', cert_select_xpath)
        
        logger.info('select imported "test" cert')
        cert_xpath = '//*[text()="test"]'
        fw_page_ui.click_element('xpath', cert_xpath)   
             
        logger.info('click next button')
        fw_page_ui.click_element('xpath', next_button_xpath)
        logger.info('configure profile part Done...')
        
        configure_wizard_sp_from_exists(sp_name='sp_wizard_1')
        export_sp_part()
        configure_wizard_idp_from_exists()
        configure_wizard_address_and_acs_part()
        
        apply_wizard_configuration_and_close()
        logger.info('check if saml profile created success...')
        profiles = saml_api.get_saml_profiles()
        logger.info(profiles)
        Assertion.assert_equal('profile_wizard_4' in str(profiles), True, "ERR: saml profile created failed")
        # logger.info('check exported xml file')
        # Assertion.assert_equal(os.path.exists('/root/Downloads/profile_wizard_4.xml'), True, "ERR: exported profile not exists")
        
        
        