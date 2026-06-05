import os
from pykeyboard import *
from pymouse import *
from modules.API.system import DiagnosticApi
from modules.UI7.common_require import *
sys.path.append(os.environ["PYTHON_COMMON_HOME"])

from utm import Firewall
fw = Firewall('192.168.168.168', user='admin', password='password', supported_config_mode='api')
TSR_obj = DiagnosticApi(fw)


''' Tech Support Report Page '''
''' IPv4 Network Settings Page '''
''' IPv6 Network Settings Page '''
''' DNS Name Lookup Page '''
''' Network Path Page '''
''' Ping Page '''
''' Trace Route Page  '''
''' Packet Replay Page '''
''' Real-Time Blacklist Page '''
''' Reverse Name Lookup Page '''
''' Geo and Botnet Page '''
''' MX and Banner Page '''
''' URL Rating Request Page '''
''' PMTU Discovery Page '''


class Diagnostics:

 ################################################### Ping Page ##################################################

    def verify_ping_result(self):
        element1 = self.browser.find_element(By.XPATH, "//div/input[@name='line1']")
        message1 = element1.get_attribute('value')
        element2 = self.browser.find_element(By.XPATH, "//div/input[@name='line2']")
        message2 = element2.get_attribute('value')
        time.sleep(2)
        result1 = "is alive"      
        # when IP is Normal IP format, and it can ping Successfully,the return is 'xxxx is alive'
        result2 = "Unable to resolve"   
        # when IP is Reserved IP, or Invalid IP listed below,  256.5.19.202  or 
        # "test#$%^" 10.-1.19.202 10/5.19.202 and it ping failed, the return is 'Unable to resolve xxxxx'
        if result1 in message1:
            logger.info("The result is:" + "\n" + ' '*35 + message1 + "\n" + ' '*35 + message2)
            return True
        elif result2 in message1:
            logger.info("The result is:" + "\n" + ' '*35 + message1 + "\n" + ' '*35 + message2)
            return False

    def ping(self):
        self.navigation.navigate_to_diagnostic_ping_section()
        if hasattr(self,'HostorIPforPing'):
            logger.debug("Input an host or ip address to ping\t:" + str(self.HostorIPforPing))
            time.sleep(2)
            self.ui_helper.configure_text_field('Ping host or IP address', self.HostorIPforPing)
        else:
            logger.info('Please input IP or Host to ping')
            return False
        if hasattr(self, 'Interface'):
            time.sleep(2)
            self.ui_helper.select_drop_down_value('Interface', self.Interface)
        if hasattr(self, 'PreferIPV6Networking'):
            time.sleep(2)
            self.ui_helper.configure_toggle_button("Prefer IPV6 Networking", self.PreferIPV6Networking)
            time.sleep(2)
            self.ui_helper.go_page()
            time.sleep(3)
        if self.verify_ping_result():
            logger.info('Ping {} Successfully' .format(self.HostorIPforPing))
            return True
        else:
            Assertion.fail("Ping {} failed, Please input IP or Host in the correct format" .format(self.HostorIPforPing))

################################################### Trace Route Page ##################################################

    def verify_trace_route_result(self):
        find_element = self.browser.find_element(By.CLASS_NAME, "fw-mgmt-ftr-diagnostics-trace-route__center_div_temp")
        trace_route_result = find_element.text        
        logger.info("Trace Route Result is:" + "\n" + ' '*35 + trace_route_result + "\n")
        result_invalid = 'is not responding'
        # when IP is Reserved IP, or Invalid IP listed below,  256.5.19.202  or 
        # "test#$%^" 10.-1.19.202 10/5.19.202 and it trace failed, the return is 'is not responding'
        if result_invalid in trace_route_result:
            return False
        else:
            return True

    def trace_route(self):
        self.navigation.navigate_to_diagnostic_trace_route_section()
        if hasattr(self,'HostorIPforTraceRoute'):
            logger.debug("Input an host or ip address to trace route\t:" + str(self.HostorIPforTraceRoute))
            time.sleep(2)
            self.ui_helper.configure_text_field('TraceRoute this host or IP address', self.HostorIPforTraceRoute)
        else:
            logger.info('Please input IP or Host to trace')
            return False
        if hasattr(self, 'Interface'):
            time.sleep(2)
            self.ui_helper.select_drop_down_value('Interface', self.Interface)
        if hasattr(self, 'PreferIPV6Networking'):
            time.sleep(2)
            self.ui_helper.configure_toggle_button( "Prefer IPV6 Networking", self.PreferIPV6Networking)
            time.sleep(2)
            self.ui_helper.go_page()
            time.sleep(100)
        if self.verify_trace_route_result():
            logger.info('Trace route {} Successfully' .format(self.HostorIPforTraceRoute))
            return True
        else:
            Assertion.fail("Trace route {} failed, Please input valid IP or Host in the correct format" .format(self.HostorIPforTraceRoute))

################################################### Network Path Page ##################################################

    def verify_network_path(self):
        element1 = self.browser.find_element(By.XPATH, "//div/input[@name='line1']")
        message1 = element1.get_attribute('value')
        element2 = self.browser.find_element(By.XPATH, "//div/input[@name='line2']")
        message2 = element2.get_attribute('value')
        element3 = self.browser.find_element(By.XPATH, "//div/input[@name='line3']")
        message3 = element3.get_attribute('value')
        result = 'undefined'
        logger.info("Network Path Result is:" + "\n" + ' '*35 + message1 + "\n" + ' '*35 + message2 + '\n' + ' '*35 + message3)
        if result in message1 or result in message2 or result in message3:
            return False
        else:
            return True

    def network_path(self):
        self.navigation.navigate_to_diagnostic_network_path_section()
        if hasattr(self, 'IPforfindinglocation'):
            logger.debug("Input {} to find it's location" .format(str(self.IPforfindinglocation)))
            time.sleep(1)
            self.ui_helper.configure_text_field('Find location of this IP address', self.IPforfindinglocation)
            time.sleep(1)
            self.ui_helper.go_page()
            time.sleep(5)
        if self.verify_network_path():
            logger.info("Find network path Successfully")
            return True
        else:
            Assertion.fail('Find network path of {} failed' .format(self.IPforfindinglocation))            

################################################### PMTU Discovery Page ##################################################

    def verify_pmtu_discovery_path_result(self):
        find_element = self.browser.find_element(By.CLASS_NAME, "fw-mgmt-ftr-diagnostics-pmtu-discovery__center_div_temp")
        message = find_element.text       
        logger.info("PMTU Discovery Result is:" + "\n" + ' '*35 + message + "\n")
        result = 'is not responding'
        if result in message:
            return False
        else:
            return True

    def pmtu_discovery(self):
        self.navigation.navigate_to_diagnostic_pmtu_discovery_section()
        try:
            if hasattr(self, 'HostorIPforDiscovery'):
                logger.debug("Input an host or ip address to discovery\t:" + str(self.HostorIPforDiscovery))
                time.sleep(2)
                self.ui_helper.configure_text_field('Path MTU Discovery to this host or IP address', self.HostorIPforDiscovery)
            if hasattr(self, 'Interface'):
                time.sleep(2)
                self.ui_helper.select_drop_down_value('Interface', self.Interface)
                time.sleep(2)
                self.ui_helper.go_page()
            time.sleep(100)
            if self.verify_pmtu_discovery_path_result():
                return True
            else:
                return False
            
        except Exception as err:
            logger.info(str(err))
            Assertion.fail("Please check necessary parameter of pmtu discovery part")

################################################### Geo and Botnet Page ##################################################

    def verify_geo_and_botnet_result(self):
        element = self.browser.find_element(By.XPATH, "//div/input[@name='line1']")
        message = element.get_attribute('value')        
        time.sleep(2)
        logger.info("The Result is:" + "\n" + ' '*35 + message + "\n")
        result = "invalid IP"
       
        if result in message:            
            return False
        else:            
            return True

    def geo_and_botnet(self):
        self.navigation.navigate_to_diagnostic_geo_and_botnet_section()
        try:
            if hasattr(self, 'IPforLookup'):
                logger.debug("Input {} to Lookup" .format(str(self.IPforLookup)))
                time.sleep(1)
                self.ui_helper.configure_text_field('Lookup IP', self.IPforLookup)
                time.sleep(1)
            self.ui_helper.go_page()
            time.sleep(5)
            if self.verify_geo_and_botnet_result():
                logger.info('Lookup {} successfully' .format(self.IPforLookup))
                return True
            else:
                Assertion.fail('Lookup {} failed' .format(self.IPforLookup))

        except Exception as err:
            logger.info(str(err))
            Assertion.fail("Please check necessary parameter of geo and botnet part")

################################################### Rea-Time Blacklist Page ##################################################

    def verify_real_time_blacklist_result(self):
        element = self.browser.find_element(By.XPATH, "//div/input[@name='rblResponse']")
        message = element.get_attribute('value')
        logger.info("Check whether it's in blacklist,the result is:" + '\n' + ' '*35 + 'RBL Response :' + message)
        result = "blacklist"
       
        if result in message:            
            return False
        else:            
            return True
    
    def real_time_blacklist(self):
        self.navigation.navigate_to_diagnostic_real_time_blacklist_section()
        try:
            if hasattr(self, 'IPforCheckBlackList'):
                logger.debug("Input {} to check whether it's in blacklist" .format(str(self.IPforCheckBlackList)))
                time.sleep(1)
                self.ui_helper.configure_text_field('IP address', self.IPforCheckBlackList)
            if hasattr(self, 'RBLDomain'):
                logger.debug("Input RBL Domain {}".format(str(self.RBLDomain)))
                time.sleep(1)
                self.ui_helper.configure_text_field('RBL Domain', self.RBLDomain)
            if hasattr(self, 'DNSServer'):
                logger.debug("Input DNS Server {}".format(str(self.DNSServer)))
                time.sleep(1)
                self.ui_helper.configure_text_field('DNS Server', self.DNSServer)
            time.sleep(2)
            self.ui_helper.go_page()
            time.sleep(5)
            if self.verify_real_time_blacklist_result():
                return True
                logger.info("{} is not in blacklist" .format(self.IPforCheckBlackList))
            else:
                logger.info("{} is in blacklist" .format(self.IPforCheckBlackList))
                False        

        except Exception as err:
            logger.info(str(err))
            Assertion.fail("Please check necessary parameter of real time blacklist part")

############################################### CFS URL Rating Page ##################################################

    def cfs_url_rating_request(self):
        self.navigation.navigate_to_diagnostic_cfs_url_rating_request_section()
        try:
            if hasattr(self, 'URLforLookuprating'):
                logger.debug("Specify URL for Lookup Rating \t:" + str(self.URLforLookuprating))
                time.sleep(2)
                self.ui_helper.configure_text_field('Lookup Rating for URL',self.URLforLookuprating)
                self.ui_helper.submit_page()
            time.sleep(20)
            result = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'sw-form-row__field')]/span")
            line1 = result[0].text
            line2 = result[1].text
            logger.info("The result of lookup Rating for {} is:" .format(self.URLforLookuprating))
            logger.info("URL: " + line1 + "\n" + ' '*35 + 'Rated as: ' + line2)

        except Exception as err:
            logger.info(str(err))

############################################### MX and Banner Page ##################################################

    def mx_and_banner(self):
        self.navigation.navigate_to_diagnostic_mx_and_banner_section()
        try:
            if hasattr(self, 'DNSServer1'):
                logger.debug("Specify DNS Server1 {}" .format(self.DNSServer1))
                time.sleep(2)
                self.ui_helper.configure_text_field('DNS Server 1',self.DNSServer1)
            if hasattr(self, 'DNSServer2'):
                logger.debug("Specify DNS Server2 {}" .format(self.DNSServer2))
                time.sleep(2)
                self.ui_helper.configure_text_field('DNS Server 2',self.DNSServer2)
            if hasattr(self, 'DNSServer3'):
                logger.debug("Specify DNS Server3 {}" .format(self.DNSServer3))
                time.sleep(2)
                self.ui_helper.configure_text_field('DNS Server 3',self.DNSServer3)
            if hasattr(self, 'HostorIPforLookup'):
                logger.debug("Specify host or IP {} for lookup" .format(self.HostorIPforLookup))
                time.sleep(2)
                self.ui_helper.configure_text_field('Lookup name or IP',self.HostorIPforLookup) 
            if hasattr(self, 'SMTPPort'):
                logger.debug("Input SMTP Port {}" .format(self.SMTPPort))
                time.sleep(2)
                self.ui_helper.configure_text_field('SMTP Port',self.SMTPPort) 
            time.sleep(2) 
            self.ui_helper.go_page()
            time.sleep(20)

        except Exception as err:
            logger.info(str(err))
            Assertion.fail('MX and Banner process failed, Please check you parameters')

############################################### Reverse name Lookup Page ##################################################
   
    def reverse_name_lookup(self):
        self.navigation.navigate_to_diagnostic_reverse_name_lookup_section()
        try:
            if hasattr(self, 'IPforReverseLookup'):
                logger.debug("Input {} to Lookup" .format(str(self.IPforReverseLookup)))
                time.sleep(1)
                self.ui_helper.configure_text_field('Reverse Lookup the IP Address', self.IPforReverseLookup)
                time.sleep(1)
            self.ui_helper.go_page()
            time.sleep(15)
            # result1 = self.browser.find_elements(By.XPATH, "//div[contains(@class, 'sw-flexbox--end-justify')]/span")
            # result2 = self.browser.find_elements(By.XPATH, "//div/input[@name='line2']")
            element1 = self.browser.find_element(By.XPATH, "//*/section/div/div/div[2]/div/div[5]")
            logger.info("The result of reverse lookup for {} is:" .format(self.IPforReverseLookup) + '\n' + element1.text)

        except Exception as err:
            logger.info(str(err))
            Assertion.fail('Reverse lookup {} failed' .format(self.IPforReverseLookup))

############################################### DNS name Lookup Page ##################################################
    
    def dns_name_lookup(self):
        self.navigation.navigate_to_diagnostic_dns_name_lookup_section()
        try:
            if hasattr(self, 'SystemDNSServer'):
                if self.SystemDNSServer == "system":
                    logger.info("Choose System DNS Server")
                    self.ui_helper.configure_radio_button('System')
                    if hasattr(self, 'URLtofindLocation'):
                        self.ui_helper.configure_text_field('Find location of this URL', self.URLtofindLocation)
                        time.sleep(2)
                    if hasattr(self, 'Interface'):
                        self.ui_helper.select_drop_down_value('Find location of this URL', self.Interface)
                        time.sleep(2)
                else:
                    logger.info("Choose Customized DNS Server")
                    self.ui_wrapper.configure_radio_button('Customized')
                    if hasattr(self, 'IPV4DNSServer'):
                        self.ui_helper.configure_text_field('IPv4 DNS Server', self.IPV4DNSServer)
                    if hasattr(self, 'IPV6DNSServer'):
                        self.ui_helper.configure_text_field('IPv6 DNS Server', self.IPV6DNSServer)
                    if hasattr(self, 'URLtofindLocation'):
                        self.ui_helper.configure_text_field('Find location of this URL', self.URLtofindLocation)
                    if hasattr(self, 'Interface'):
                        self.ui_helper.select_drop_down_value('Find location of this URL', self.Interface)
            self.ui_helper.go_page()
            time.sleep(20)
            element = self.browser.find_element(By.XPATH, "//div/input[@name='domainName']")
            print(element.text)

        except Exception as err:
            logger.info(str(err))
            Assertion.fail("DNS name lookup for {} Failed".format(self.URLtofindLocation))

############################################### IPv4 Network Setting Page ##################################################

    def vefify_check_default_dateway_result(self):
        checkresult = self.browser.find_elements('xpath', '//div[contains(@class, "sw-table-row__cell__wrapper")]')
        servername = checkresult[1].get_attribute('innerHTML')
        testresult = checkresult[3].get_attribute('innerHTML')
        need_info = 'Ping responded successfully'
        if need_info in testresult:
            logger.info('Test result of checking ' + servername + ' is: ' + testresult)
            return True
        else:
            return False

    def vefify_check_dns_server_result(self):
        checkresult = self.browser.find_elements('xpath', '//div[contains(@class, "sw-table-row__cell__wrapper")]')
        servername = checkresult[8].get_attribute('innerHTML')
        testresult = checkresult[10].get_attribute('innerHTML')
        need_info = 'DNS responded successfully'
        if need_info in testresult:
            logger.info('Test result of checking ' + servername + ' is: ' + testresult)
            return True
        else:
            return False

    def vefify_check_my_sonicwall_result(self):
        checkresult = self.browser.find_elements('xpath', '//div[contains(@class, "sw-table-row__cell__wrapper")]')
        servername = checkresult[15].get_attribute('innerHTML')
        testresult = checkresult[17].get_attribute('innerHTML')
        need_info = 'HTTPS responded successfully'
        if need_info in testresult:
            logger.info('Test result of checking ' + servername + ' is: ' + testresult)
            return True
        else:
            return False

    def vefify_check_license_manager_result(self):
        checkresult = self.browser.find_elements('xpath', '//div[contains(@class, "sw-table-row__cell__wrapper")]')
        servername = checkresult[22].get_attribute('innerHTML')
        testresult = checkresult[24].get_attribute('innerHTML')
        need_info = 'HTTPS responded successfully'
        if need_info in testresult:
            logger.info('Test result of checking ' + servername + ' is: ' + testresult)
            return True
        else:
            return False
            
    def vefify_check_Content_Filtering_result(self):
        checkresult = self.browser.find_elements('xpath', '//div[contains(@class, "sw-table-row__cell__wrapper")]')
        servername = checkresult[29].get_attribute('innerHTML')
        testresult = checkresult[31].get_attribute('innerHTML')
        need_info = 'Service responded successfully'
        if need_info in testresult:
            logger.info('Test result of checking ' + servername + ' is: ' + testresult)
            return True
        else:
            return False

    def check_IPv4_network_settings(self):
        self.navigation.navigate_to_diagnostic_check_network_settings_section()
        time.sleep(3)
        serverbutton = self.browser.find_elements(By.XPATH, "//span[@class='sw-icon__inner sw-font-icon icon-checkmark']")
        testbutton = self.browser.find_elements(By.XPATH, "//span[@class='sw-icon__inner sw-font-icon icon-cloud-app']")
        if self.CheckAll:
            if self.CheckAll == 'GeneralNetworkConnection':
                logger.debug("Select all servers to test on General Network Connection Part")
                serverbutton[0].click()
                time.sleep(2)
                testbutton[0].click()
                time.sleep(15)
                logger.debug("Check result of Default gateway.")
                if self.vefify_check_default_dateway_result():
                    logger.debug("Default gateway can ping Successfully.")
                else:
                    Assertion.fail('Ping default gateway failed, you can check it again.')
                logger.debug("Check result of dns server.")
                if self.vefify_check_dns_server_result():
                    logger.debug("DNS Server can ping Successfully.")
                else:
                    Assertion.fail('Ping DNS Server failed, you can check it again.')
            elif self.CheckAll == 'SecurityManagement':
                logger.debug("Select all servers to test on Security Management Part")
                serverbutton[5].click()
                time.sleep(2)
                testbutton[1].click()
                time.sleep(15)
                logger.debug("Check result of My sonicwall server.")
                if vefify_check_my_sonicwall_result():
                    logger.debug("My sonicwall server can ping Successfully.")
                else:
                    Assertion.fail('Ping My sonicwall server failed, you can check it again.')
                logger.debug("Check result of License manager.")
                if vefify_check_license_manager_result():
                    logger.debug("License manager can ping Successfully.")
                else:
                    Assertion.fail('Ping License manager failed, you can check it again.')
                logger.debug("Check result of Content Filtering server.")
                if vefify_check_Content_Filtering_result():
                    logger.debug("Content Filtering server can ping Successfully.")
                else:
                    Assertion.fail('Ping Content Filtering server failed, you can check it again.')
        if self.Check_Single_or_Several == True:
            if self.Default_gateway == True:
                logger.debug("To test default gataway.")
                serverbutton[1].click()
                time.sleep(2)
                testbutton[1].click()
                time.sleep(15)
                logger.debug("Check result of Default gateway.")
                if self.vefify_check_default_dateway_result():
                    logger.debug("Default gateway can ping Successfully.")
                else:
                    Assertion.fail('Ping default gateway failed, you can check it again.')
            if self.DNS_Server == True:
                logger.debug("To test DNS Server.")
                serverbutton[3].click()
                time.sleep(2)
                testbutton[2].click()
                time.sleep(15)
                logger.debug("Check result of DNS Server.")
                if self.vefify_check_dns_server_result():
                    logger.debug("DNS Server can ping Successfully.")
                else:
                    Assertion.fail('Ping DNS Server failed, you can check it again.')
            if self.my_sonicwall == True:
                logger.debug("To test my sonicwall Server.")
                serverbutton[6].click()
                time.sleep(2)
                testbutton[4].click()
                time.sleep(15)
                logger.debug("Check result of My sonicwall server.")
                if vefify_check_my_sonicwall_result():
                    logger.debug("My sonicwall server can ping Successfully.")
                else:
                    Assertion.fail('Ping My sonicwall server failed, you can check it again.')
            if self.license_manager == True:
                logger.debug("To test my sonicwall Server.")
                serverbutton[8].click()
                time.sleep(2)
                testbutton[5].click()
                time.sleep(15)
                logger.debug("Check result of License manager.")
                if vefify_check_license_manager_result():
                    logger.debug("License manager can ping Successfully.")
                else:
                    Assertion.fail('Ping License manager failed, you can check it again.')
            if self.Content_Filtering == True:
                logger.debug("To test Content Filtering Server.")
                serverbutton[10].click()
                time.sleep(2)
                testbutton[6].click()
                time.sleep(15)
                logger.debug("Check result of Content Filtering server.")
                if vefify_check_Content_Filtering_result():
                    logger.debug("Content Filtering server can ping Successfully.")
                else:
                    Assertion.fail('Ping Content Filtering server failed, you can check it again.')

############################################### Tech Support Report Page ##################################################

    def download_TSR(self):
        self.navigation.navigate_to_tech_support_report_section()
        logger.info("Find 'Download report' Button.")
        element = self.browser.find_element('xpath', '//button[text()="Download Report"]')
        element.click()
        logger.info("Click the 'Confirm' Button.")
        self.ui_helper.accept_alert()
        pykey = PyKeyboard()
        pymou = PyMouse()
        if self.download_type == 'save_file':
            logger.info("Click the 'Save File' and 'OK' button to save report to your PC under /root/Downloads.")
            os.system('rm -rf /root/Downloads/export-tmp-file*')
            pykey.tap_key(pykey.enter_key)            
            output = os.system('ls -la /root/Downloads/')
            logger.info(output)
            Assertion.assert_regular(output, 'export-tmp-file', "ERR: Save TSR failed")
        elif self.download_type == 'open_file':
            logger.info("Click the 'Open File' button to open report to your PC under /tmp/mozilla_root0.")
            os.system('rm -rf /tmp/mozilla_root0/export-tmp-file*')
            time.sleep(2)
            pykey.tap_key(pykey.tab_key)
            time.sleep(5)
            pykey.tap_key(pykey.enter_key)
            time.sleep(2)
            pykey.press_key(pykey.tab_key)
            time.sleep(2)
            pykey.tap_key(pykey.enter_key)
            pykey.type_string("Firefox")
            time.sleep(2)
            pykey.press_key(pykey.tab_key)
            time.sleep(2)
            pykey.press_key(pykey.tab_key)
            time.sleep(2)
            pykey.press_key(pykey.tab_key)
            time.sleep(2)
            pykey.tap_key(pykey.enter_key)
            pymou.release(pymou.position()[0], pymou.position()[1], button=1)
            pykey.tap_key(pykey.enter_key) 
            time.sleep(10)
            output = os.system('ls -la /tmp/mozilla_root0/')
            logger.info(output)
            Assertion.assert_regular(output, 'export-tmp-file', "ERR: Open TSR failed")

    # FUNCTIONALITY     : Compare given paramters with settings in the firewall
    # INPUT             : tsr_page_json, tsr_target_parameter, tsr_target_value
    # RETURNS           : Returns true if settings match
    def tsr_json_compare(self, tsr_page_json, tsr_target_parameter, tsr_target_value):
        try:
            flag = 0
            if tsr_page_json[tsr_target_parameter] == tsr_target_value:
                logger.info("Check result is:\n" + ' '*35 + tsr_target_parameter + " is right!")
            else:
                logger.info("Check result is:\n" + ' '*35 + tsr_target_parameter + " is right!")
                flag += 1
                Assertion.assert_regular(flag, 0, 'Firewall verification failed')  
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Some parameters isn't defined,Firewall verification failed")

    def verify_TSR_button_settings_on_firewall(self):
        try:
            logger.info("Verifying TSR page Settings in the firewall")
            data = TSR_obj.show_tsr_conf()
            logger.info(data)
            if hasattr(self, 'Users_related'):
                tsr_effective_json = data['tech_support_report']['options']['users']
            elif hasattr(self, 'IPv6_related'):
                tsr_effective_json = data['tech_support_report']['options']['ipv6']
            elif hasattr(self, 'TimeInterval_related'):
                tsr_effective_json = data['tech_support_report']['options']['secure_backup']
            else:
                tsr_effective_json = data['tech_support_report']['options']
            if hasattr(self, 'Automaticsecurecrash'):
                self.tsr_json_compare(tsr_effective_json, "secured_crash_analysis", self.Automaticsecurecrash)
            if hasattr(self, 'TimeInterval'):
                TimeInterval = int(self.TimeInterval)
                self.tsr_json_compare(tsr_effective_json, "interval", self.TimeInterval)
            if hasattr(self, 'Includerawflow'):
                self.tsr_json_compare(tsr_effective_json, 'send_raw_flow_data', self.Includerawflow)
            if hasattr(self, 'SensitiveKeys'):
                self.tsr_json_compare(tsr_effective_json, "sensitive_keys", self.SensitiveKeys)
            if hasattr(self, 'Inactiveusers'):
                self.tsr_json_compare(tsr_effective_json, "inactive", self.Inactiveusers)
            if hasattr(self, 'ExtraRoutingInfo'):
                self.tsr_json_compare(tsr_effective_json, "extra_routing", self.ExtraRoutingInfo)
            if hasattr(self, 'ARPCache'):
                self.tsr_json_compare(tsr_effective_json, "arp_cache", self.ARPCache)
            if hasattr(self, 'Detailofusers'):
                self.tsr_json_compare(tsr_effective_json, "detail", self.Detailofusers)
            if hasattr(self, 'CaptureATPCache'):
                self.tsr_json_compare(tsr_effective_json, "atp_cache", self.CaptureATPCache)
            if hasattr(self, 'DHCPBindings'):
                self.tsr_json_compare(tsr_effective_json, "dhcp_bindings", self.DHCPBindings)
            if hasattr(self, 'IPStackInfo'):
                self.tsr_json_compare(tsr_effective_json, "ip_stack_info", self.IPStackInfo)
            if hasattr(self, 'VendorNameResolution'):
                self.tsr_json_compare(tsr_effective_json, "vendor_oui", self.VendorNameResolution)
            if hasattr(self, 'IKEInfo'):
                self.tsr_json_compare(tsr_effective_json, "ike_info", self.IKEInfo)
            if hasattr(self, 'IPv6NDP'):
                self.tsr_json_compare(tsr_effective_json, "ndp", self.IPv6NDP)
            if hasattr(self, 'Debuginfoinreport'):
                self.tsr_json_compare(tsr_effective_json, "debug_info", self.Debuginfoinreport)
            ################### On New UI7, Because there is no wireless zone, so the button doesn't work####################
            # if hasattr(self, 'WirelessDiagnostics'):
            #     self.tsr_json_compare(tsr_effective_json, "diagnostics", self.WirelessDiagnostics)              
            if hasattr(self, 'IPv6DHCP'):
                self.tsr_json_compare(tsr_effective_json, "dhcp", self.IPv6DHCP)
            if hasattr(self, 'IPReport'):
                self.tsr_json_compare(tsr_effective_json, "ip_report", self.IPReport)
            if hasattr(self, 'Listofcurrentusers'):
                self.tsr_json_compare(tsr_effective_json, "current", self.Listofcurrentusers)
            if hasattr(self, 'GeoIPBotnetCache'):
                self.tsr_json_compare(tsr_effective_json, "geo_ip_cache", self.GeoIPBotnetCache)
            if hasattr(self, 'ABREntries'):
                self.tsr_json_compare(tsr_effective_json, "abr_entries", self.ABREntries)
            if hasattr(self, 'DNSProxyCache'):
                self.tsr_json_compare(tsr_effective_json, "dns_proxy_cache", self.DNSProxyCache)
            if hasattr(self, 'UserName'):
                self.tsr_json_compare(tsr_effective_json, "user_name", self.UserName)            
            return True
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Firewall verification failed")        

    def config_TSR_settings(self):
        self.navigation.navigate_to_tech_support_report_section()
        try:
            logger.info("Configure - Buttons on TSR page")
            if hasattr(self, 'Automaticsecurecrash'):
                logger.debug("Configure - Automatic secure crash analysis reporting \t: " + str(self.Automaticsecurecrash))
                time.sleep(5)
                self.ui_helper.configure_toggle_button('Automatic secure crash analysis reporting', self.Automaticsecurecrash)
            if hasattr(self, 'Periodicsecure'):
                if self.Periodicsecure == True:
                    logger.debug("Configure - Periodic secure diagnostic reporting for support purposes \t: " + str(self.Periodicsecure))
                    self.ui_helper.configure_toggle_button("Periodic secure diagnostic reporting for support purposes", self.Periodicsecure)
                    if hasattr(self, 'TimeInterval'):
                        logger.debug("Configure - Time Interval (minutes) \t: " + str(self.TimeInterval))
                        self.ui_helper.configure_text_field('Time Interval (minutes)', self.TimeInterval)
                else:
                    logger.debug("Cannot configure - Time Interval (minutes) \t: " + str(self.TimeInterval))
            if hasattr(self, 'Includerawflow'):
                logger.debug("Configure - Include raw flow table data entries when sending diagnostic report \t: " + str(self.Includerawflow))
                self.ui_helper.configure_toggle_button('Include raw flow table data entries when sending diagnostic report', self.Includerawflow)
            if hasattr(self, 'SensitiveKeys'):
                logger.debug("Configure - Sensitive Keys \t: " + str(self.SensitiveKeys))
                self.ui_helper.configure_toggle_button('Sensitive Keys', self.SensitiveKeys)
            if hasattr(self, 'Inactiveusers'):
                logger.debug("Configure - Inactive users \t: " + str(self.Inactiveusers))
                self.ui_helper.configure_toggle_button('Inactive users', self.Inactiveusers)
            if hasattr(self, 'ExtraRoutingInfo'):
                logger.debug("Configure - Extra Routing Info \t: " + str(self.ExtraRoutingInfo))
                self.ui_helper.configure_toggle_button('Extra Routing Info', self.ExtraRoutingInfo)
            if hasattr(self, 'ARPCache'):
                logger.debug("Configure - ARP Cache \t: " + str(self.ARPCache))
                self.ui_helper.configure_toggle_button('ARP Cache', self.ARPCache)
            if hasattr(self, 'Detailofusers'):
                logger.debug("Configure - Detail of users \t: " + str(self.Detailofusers))
                self.ui_helper.configure_toggle_button('Detail of users', self.Detailofusers)
            if hasattr(self, 'CaptureATPCache'):
                logger.debug("Configure - Capture ATP Cache \t: " + str(self.CaptureATPCache))
                self.ui_helper.configure_toggle_button('Capture ATP Cache', self.CaptureATPCache)
            if hasattr(self, 'DHCPBindings'):
                logger.debug("Configure - DHCP Bindings \t: " + str(self.DHCPBindings))
                self.ui_helper.configure_toggle_button('DHCP Bindings', self.DHCPBindings)
            if hasattr(self, 'IPStackInfo'):
                logger.debug("Configure - IP Stack Info \t: " + str(self.IPStackInfo))
                self.ui_helper.configure_toggle_button('IP Stack Info', self.IPStackInfo)            
            if hasattr(self, 'VendorNameResolution'):
                logger.debug("Configure - Vendor Name Resolution \t: " + str(self.VendorNameResolution))
                self.ui_helper.configure_toggle_button('Vendor Name Resolution', self.VendorNameResolution)
            if hasattr(self, 'IKEInfo'):
                logger.debug("Configure - IKE Info \t: " + str(self.IKEInfo))
                self.ui_helper.configure_toggle_button('IKE Info', self.IKEInfo)
            if hasattr(self, 'IPv6NDP'):
                logger.debug("Configure - IPv6 NDP \t: " + str(self.IPv6NDP))
                self.ui_helper.configure_toggle_button('IPv6 NDP', self.IPv6NDP)
            if hasattr(self, 'Debuginfoinreport'):
                logger.debug("Configure - Debug info in report \t: " + str(self.Debuginfoinreport))
                self.ui_helper.configure_toggle_button('Debug info in report', self.Debuginfoinreport)
            ################### On New UI7, Because there is no wireless zone, so the button doesn't work####################
            # if hasattr(self, 'WirelessDiagnostics'):
            #     logger.debug("Configure - Wireless Diagnostics \t: " + str(self.WirelessDiagnostics))
            #     self.ui_helper.configure_toggle_button('Wireless Diagnostics', self.WirelessDiagnostics)
            if hasattr(self, 'IPv6DHCP'):
                logger.debug("Configure - IPv6 DHCP \t: " + str(self.IPv6DHCP))
                self.ui_helper.configure_toggle_button('IPv6 DHCP', self.IPv6DHCP)
            if hasattr(self, 'IPReport'):
                logger.debug("Configure - IP Report \t: " + str(self.IPReport))
                self.ui_helper.configure_toggle_button('IP Report', self.IPReport)
            if hasattr(self, 'Listofcurrentusers'):
                logger.debug("Configure - List of current users \t: " + str(self.Listofcurrentusers))
                self.ui_helper.configure_toggle_button('List of current users', self.Listofcurrentusers)
            if hasattr(self, 'GeoIPBotnetCache'):
                logger.debug("Configure - Geo-IP/Botnet Cache \t: " + str(self.GeoIPBotnetCache))
                self.ui_helper.configure_toggle_button('Geo-IP/Botnet Cache', self.GeoIPBotnetCache)
            if hasattr(self, 'ABREntries'):
                logger.debug("Configure - ABR Entries \t: " + str(self.ABREntries))
                self.ui_helper.configure_toggle_button('ABR Entries', self.ABREntries)
            if hasattr(self, 'DNSProxyCache'):
                logger.debug("Configure - DNS Proxy Cache \t: " + str(self.DNSProxyCache))
                self.ui_helper.configure_toggle_button('DNS Proxy Cache', self.DNSProxyCache)
            if hasattr(self, 'UserName'):
                logger.debug("Configure - User Name \t: " + str(self.UserName))
                self.ui_helper.configure_toggle_button('User Name', self.UserName)

            self.ui_helper.submit_page()
            self.ui_helper.accept_alert()
            self.verify_TSR_button_settings_on_firewall()
            
        except Exception as err:
            logger.error(str(err))
            Assertion.fail("Configuring TSR page Failed")