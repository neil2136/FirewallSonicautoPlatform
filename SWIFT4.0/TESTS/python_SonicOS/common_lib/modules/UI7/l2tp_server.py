import os
from modules.API.vpn import L2tpServerApi
from modules.UI7.common_require import *
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
l2tp_server_button_obj = L2tpServerApi(fw)


''' L2TP Server Page '''


class L2TPServer:
    
    def l2tp_server_json_compare(self, l2tp_server_base_page_json, l2tp_server_base_target_parameter, l2tp_server_base_target_value):
        try:
            flag = 0
            if l2tp_server_base_page_json[l2tp_server_base_target_parameter] == l2tp_server_base_target_value:
                logger.info("Check result is:\n" + ' '*35 + l2tp_server_base_target_parameter + " is right!")
            else:
                logger.info("Check result is:\n" + ' '*35 + l2tp_server_base_target_parameter + " is not right!")
                flag += 1
                Assertion.assert_regular(flag, 0, 'Firewall verification failed')  
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Some parameters of l2tp server part isn't defined,Firewall verification failed")

    
    def verify_l2tp_server_button_settings_on_firewall(self):
        try:
            logger.info("Verifying Button Settings of L2Tp Server in the firewall")
            data = l2tp_server_button_obj.show_ppp_settings()
            logger.info("From FW, get data of l2tp server switch:" + '\n' + data)
            l2tp_server_effective_json = data['vpn']['l2tp_server']
            if hasattr(self, 'Enable_L2TP_Server'):
                self.l2tp_server_json_compare(l2tp_server_effective_json, "enable", self.Enable_L2TP_Server)
                
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification on L2Tp Server button failed")    

    def enable_or_disable_l2tp_server(self):
        self.navigation.navigate_to_l2tp_server_section()
        try:
            if hasattr(self, 'Enable_L2TP_Server'):
                logger.debug("Configure - Enable L2TP Server button \t: " + str(self.Enable_L2TP_Server))
                self.ui_helper.configure_toggle_button('Enable L2TP Server', self.Enable_L2TP_Server)
                if self.Enable_L2TP_Server == True:
                    self.ui_helper.submit_page()
                else:
                    self.ui_helper.accept_alert()
                    self.ui_helper.submit_page()
            self.verify_l2tp_server_button_settings_on_firewall()

        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Please check necessary parameter of L2TP Server Part")

    
    def verify_l2tp_server_configurations_on_firewall(self):
        try:
            logger.info("Verifying Configurations Settings of L2Tp Server in the firewall")
            data = l2tp_server_button_obj.show_l2tpserver()
            logger.info("From FW, get data of l2tp server configurations:" + '\n' + data)
            l2tp_server_effective_json = data['vpn']['l2tp_server']
            if hasattr(self, 'keep_alive_time'):
                self.l2tp_server_json_compare(l2tp_server_effective_json, "keep_alive", self.keep_alive_time)
            if data['vpn']['l2tp_server']['dns']['primary'] == self.dns_server_1:
                log.info("Dns server 1 is right")
            else:
                log.info("Dns server 1 is not right")
                return False
            if data['vpn']['l2tp_server']['dns']['secondary'] == self.dns_server_2:
                log.info("Dns server 2 is right")
            else:
                log.info("Dns server 2 is not right")
                return False
            if data['vpn']['l2tp_server']['wins']['primary'] == self.wins_server_1:
                log.info("Wins server 1 is right")
            else:
                log.info("Wins server 1 is not right")
                return False
            if data['vpn']['l2tp_server']['wins']['secondary'] == self.wins_server_2:
                log.info("Wins server 2 is right")
            else:
                log.info("Wins server 2 is not right")
                return False
            if data['vpn']['l2tp_server']['ip_pool']['local']['begin'] == self.start_ip:
                log.info("Local protocol start IP is right")
            else:
                log.info("Local protocol start IP is not right")
                return False
            if data['vpn']['l2tp_server']['ip_pool']['local']['end'] == self.end_ip:
                log.info("Local protocol End IP is right")
            else:
                log.info("Local protocol End IP is not right")
                return False
            if data['vpn']['l2tp_server']['user_group'] == self.user_group_for_l2tp_users:
                log.info("Choose User group for l2tp users is right")
            else:
                log.info("Choose User group for l2tp users is not right")
                return False
            if self.user_type == 'radius_ldap':
                if data['vpn']['l2tp_server']['ip_pool']['provided']['provided'] == True:
                    log.info("Choose IP address provided by RADIUS/LDAP Server is right")
                else:
                    log.info("Choose IP address provided by RADIUS/LDAP Server is not right")
                    return False 
            return True

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification on L2Tp Server Configurations failed")


    def l2tp_server_configuration(self, user_type):
        self.navigation.navigate_to_l2tp_server_section()
        logger.info("Click configure button")
        element = self.browser.find_element('xpath', '//button[text()="Configure"]')
        element.click()
        try:
            if self.user_type == 'radius_ldap':
                logger.info("Go to L2TP Users Settings tab, click radius or ldap protocol")
                self.navigation.navigate_to_tab("L2TP Users Settings")
                logger.info("Choose IP address provided by RADIUS/LDAP Server")
                self.ui_helper.configure_radio_button("IP address provided by RADIUS/LDAP Server")
                logger.debug("RADIUS or LDAP authentication must be selected on the User Settings page to use this option")
                self.ui_helper.accept_alert()
            elif self.user_type == 'local_protocol':
                logger.info("Go to L2TP Users Settings tab, click local protocol")
                time.sleep(2)
                self.navigation.navigate_to_tab("L2TP Users Settings")
                logger.info("Choose Use the Local L2TP IP pool")
                time.sleep(2)
                self.ui_helper.configure_radio_button("Use the Local L2TP IP pool")
                if hasattr(self, 'start_ip'):
                    self.ui_helper.configure_text_field('Start IP', self.start_ip)
                else:
                    logger.info("Start IP must be entered")
                    return False
                if hasattr(self, 'end_ip'):
                    self.ui_helper.configure_text_field('End IP', self.end_ip)
                else:
                    logger.info("End IP must be entered")
                    return False
                if hasattr(self, 'user_group_for_l2tp_users'):
                    self.ui_helper.select_drop_down_value('User group for L2TP users', self.user_group_for_l2tp_users)
            else:
                logger.info("Please to choose: Use the Local L2TP IP pool or User IP address provided by RADIUS/LDAP Server")
                return False
            logger.info("Go to L2TP Server Settings tab")
            self.navigation.navigate_to_tab("L2TP Server Settings")
            if hasattr(self, 'keep_alive_time'):
                logger.debug("Configure - Keep alive time field \t: " + str(self.keep_alive_time))
                self.ui_helper.configure_text_field('Keep alive time (secs)', self.keep_alive_time)
            if hasattr(self, 'dns_server_1'):
                logger.debug("Configure - Dns Server 1 field \t: " + str(self.dns_server_1))
                self.ui_helper.configure_text_field('Dns Server 1', self.dns_server_1)
            if hasattr(self, 'dns_server_2'):
                logger.debug("Configure - Dns Server 2 field \t: " + str(self.dns_server_2))
                self.ui_helper.configure_text_field('Dns Server 2', self.dns_server_2)
            if hasattr(self, 'wins_server_1'):
                logger.debug("Configure - WINS Server 1 field \t: " + str(self.wins_server_1))
                self.ui_helper.configure_text_field('WINS Server 1', self.wins_server_1)
            if hasattr(self, 'wins_server_2'):
                logger.debug("Configure - WINS Server 2 field \t: " + str(self.wins_server_2))
                self.ui_helper.configure_text_field('WINS Server 2', self.wins_server_2)
            logger.info("Click Save button")
            self.ui_helper.submit_page()
            logger.info("Click Close button")
            self.ui_helper.close_page()
            logger.info("Verify L2TP Server configuration result on Firewall")
            self.verify_l2tp_server_configurations_on_firewall()           

        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Please check necessary parameter of L2TP Server Configuration Part")

    def verify_ppp_settings_configuration_on_firewall(self):
        try:
            logger.info("Verifying Configurations Settings of L2Tp Server in the firewall")
            data = l2tp_server_button_obj.show_ppp_settings()
            logger.info("From FW, get data of ppp settings configuration:" + '\n' + data)
            if self.from_available_to_selected in data:
                log.info("{} is choosed correctly" .format(self.from_available_to_selected))
            else:
                log.info("{} is choosed incorrectly" .format(self.from_available_to_selected))
                return False
            if self.from_selected_to_available in data:
                log.info("{} is choosed correctly" .format(self.from_selected_to_available))
            else:
                log.info("{} is choosed incorrectly" .format(self.from_selected_to_available))
                return False   
            return True

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification on PPP Settings Configurations failed")

    def ppp_settings_configuration(self):
        self.navigation.navigate_to_l2tp_server_section()
        logger.info("Click configure button")
        element = self.browser.find_element('xpath', '//button[text()="Configure"]')
        element.click()
        logger.info("Move to PPP Settings Part")
        self.navigation.navigate_to_tab("PPP Settings")
        self.ui_helper.unselect_tree_values(self.from_selected_to_available)
        try:
            if hasattr(self, 'from_available_to_selected'):
                logger.debug("Configure-choose {} protocol from available to selected field" .format(self.from_available_to_selected))
                self.ui_helper.select_tree_values(self.from_available_to_selected)
            if hasattr(self, 'from_selected_to_available'):
                logger.debug("Configure-choose {} protocol from selected to available field" .format(self.from_selected_to_available))
                self.ui_helper.unselect_tree_values(self.from_selected_to_available)
            logger.info("Click Save button")
            self.ui_helper.submit_page()
            logger.info("Click Close button")
            self.ui_helper.close_page()
            logger.info("Verify PPP Settings configuration result on Firewall")
            self.verify_ppp_settings_configuration_on_firewall()

        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Please check necessary parameter of PPP Settings Part")

    def verify_active_l2tp_server_exist_on_UI(self):
        find_l2tp_server = self.browser.find_element('xpath', '//div[contains(@class, "sw-table--light")]')
        bb = find_l2tp_server.text
        logger.info(bb)
        if self.l2tp_server_username in bb:
            logger.info("L2TP server: {} is on the UI correctly." . format(self.l2tp_server_username))
            return True
        else:
            logger.info("L2TP server: {} is not on the UI correctly." . format(self.l2tp_server_username))
            return False

    def verify_active_l2tp_server_on_firewall(self):
        try:
            logger.info("Verifying active l2tp servers section on the firewall")
            data = l2tp_server_button_obj.show_active_settings()
            logger.info("From FW, get data of active l2tp server:" + '\n' + data)
            if self.l2tp_server_username in data:
                return True
                log.info("{}: is in FW" .format(self.l2tp_server_username))
            else:
                log.info("{}: is not in FW" .format(self.from_available_to_selected))
                return False

        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification on PPP Settings Configurations failed")

    def disconnect_active_l2tp_server(self):
        self.navigation.navigate_to_l2tp_server_section()
        try:
            if self.verify_active_l2tp_server_exist_on_UI():                
                # self.ui_helper.search_string(self.l2tp_server_username)
                logger.info("testaddd")
                # if self.ui_helper.does_row_identifier_exist(self.l2tp_server_username):
                logger.info("Click 'disconnect' button")
                self.ui_helper.click_on_disconnect_element_after_hovering(self.l2tp_server_username)
                logger.info("Alert message:click 'OK' button")
                self.ui_helper.accept_alert()
                logger.info("Alert message:click 'OK' button again")
                self.ui_helper.accept_alert()
                if self.verify_active_l2tp_server_on_firewall():
                    logger.info("L2TP server {}: is still on the UI." . format(self.l2tp_server_username))
                    return False
                else:
                    logger.info("L2TP server {}: was disconnected successfully." . format(self.l2tp_server_username))
                    return True
            else:
               logger.info("L2TP server {} has been disconnected successfully." . format(self.l2tp_server_username))
               return True
            
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Please check necessary parameter of Active L2TP Server Part")
        

    


