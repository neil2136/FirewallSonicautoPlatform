from modules.UI7.common_require import *

class Navigation:

    def get_top_icon(self):
        logger.debug2("Getting page navigation icon")
        icons = self.ui_wrapper.get_element('class', 'fw-app-header__head__top-nav')
        return icons

    def get_left_panel(self):
        logger.debug2("Getting left navigation panel")
        icons = self.ui_wrapper.get_element('class', 'sw-app__nav')
        return icons

    def get_lower_top_icons(self):
        icons = self.ui_wrapper.get_element('class', "sw-tab-nav__cont__tabs-cont")
        return icons

    def navigate_to_page(self, page_identifier):
        icon = self.get_top_icon()
        self.ui_wrapper.click_relative_element(icon, 'class', page_identifier)

    def navigate_to_section(self, section_header, section_identifier, labelName=None):
        if self.ui_wrapper.does_element_exist_now('xpath', "//span[contains(@class, 'sw-breadcrumb__item__text') and text()='"+section_identifier+"']"):
            logger.debug2("Page :"+ section_identifier)
        else:
            if self.ui_wrapper.does_element_exist_now('xpath', "//span[contains(@class, '"+section_header +"')]/following::div/span[text()='" + section_identifier + "']"):
                logger.debug2("Section is already expanded")
            else:
                logger.debug2("Expanding section")
                icon = self.get_left_panel()
                if labelName is not None:
                    element_xpath = "//span[contains(@class, '"+section_header+"')]/following::span[text()='"+labelName+"'] "
                    self.ui_wrapper.click_relative_element(icon, 'xpath', element_xpath)
                else:
                    self.ui_wrapper.click_relative_element(icon, 'class', section_header)
                logger.debug2("Expanded section successfully")
            self.ui_wrapper.click_element('xpath', "//span[contains(@class, '"+section_header +"')]/following::div/span[text()='" + section_identifier + "']")
            self.ui_helper.wait_for_page_data_to_be_rendered()

    def navigate_to_tab(self, tab_identifier):
        tab_identifier_xpath1 = "//span[text()='" + tab_identifier + "']"
        tab_identifier_xpath2 = "//span[contains(text(),'" + tab_identifier + "')]"
        tab_level_identifier_xpath = "/ancestor::li[contains(@class, 'sw-tab--l1')]"
        class_value = self.ui_wrapper.get_attribute_value('xpath',
                                                          tab_identifier_xpath1 + tab_level_identifier_xpath + "|" +
                                                          tab_identifier_xpath2 + tab_level_identifier_xpath, 'class')
        if 'sw-tab--active' in class_value:
            logger.debug2("Tab : " + tab_identifier)
        else:
            self.ui_wrapper.click_element('xpath',
                                          tab_identifier_xpath1 + tab_level_identifier_xpath + "|" +
                                          tab_identifier_xpath2 + tab_level_identifier_xpath)
            self.ui_helper.wait_for_page_data_to_be_rendered()

    def navigate_to_level2_tab(self, tab_identifier):
        class_value = self.ui_wrapper.get_attribute_value('xpath',
                                                          "//span[text()='" + tab_identifier + "']/ancestor::li[contains(@class, 'sw-tab--l2')]",
                                                          'class')
        if 'sw-tab--active' in class_value:
            logger.debug2("Already is tab : " + tab_identifier)
        else:
            self.ui_wrapper.click_element('xpath', "//span[text()='"+tab_identifier+"']/ancestor::li[contains(@class, 'sw-tab--l2')]")
            self.ui_helper.wait_for_page_data_to_be_rendered()

    # Navigates to Home page
    def navigate_to_home_page(self):
        logger.debug2("Navigating to Home page")
        self.navigate_to_page("icon-dashboard")
        if self.ui_wrapper.does_element_exist_now('xpath', "//p[text()='No matching command found.']"):
            self.ui_helper.accept_alert()

    def navigate_to_overview_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Overview page")
        self.navigate_to_section("icon-tree", "Overview", labelName="Dashboard")

    def navigate_to_summary_tab_overview_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Overview -> Summary page")
        self.navigate_to_section("icon-tree", "Overview", labelName="Dashboard")
        self.navigate_to_tab("Summary")

    def navigate_to_network_tab_overview_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Overview -> Network page")
        self.navigate_to_section("icon-tree", "Overview", labelName="Dashboard")
        self.navigate_to_tab("Network")

    def navigate_to_threat_tab_overview_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Overview -> Threat page")
        self.navigate_to_section("icon-tree", "Overview", labelName="Dashboard")
        self.navigate_to_tab("Threat")

    def navigate_to_device_tab_overview_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Overview -> Device page")
        self.navigate_to_section("icon-tree", "Overview", labelName="Dashboard")
        self.navigate_to_tab("Device")

    def navigate_to_tools_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Tools page")
        self.navigate_to_section("icon-diagnostics", "Tools", labelName="Diagnostics")

    def navigate_to_tech_support_report_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Tech Support Report page")
        self.navigate_to_section("icon-diagnostics", "Tech Support Report", labelName="Diagnostics")

    def navigate_to_diagnostic_check_network_settings_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> IPv4 Network Settings page")
        self.navigate_to_section("icon-diagnostics", "IPv4 Network Settings", labelName="Diagnostics")

    def navigate_to_diagnostic_ipv6_check_network_settings_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> IPv6 Network Settings page")
        self.navigate_to_section("icon-diagnostics", "IPv6 Network Settings", labelName="Diagnostics")

    def navigate_to_diagnostic_dns_name_lookup_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> DNS Name Lookup page")
        self.navigate_to_section("icon-diagnostics", "DNS Name Lookup", labelName="Diagnostics")

    def navigate_to_diagnostic_network_path_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Network Path page")
        self.navigate_to_section("icon-diagnostics", "Network Path", labelName="Diagnostics")

    def navigate_to_diagnostic_ping_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Ping page")
        self.navigate_to_section("icon-diagnostics", "Ping", labelName="Diagnostics")

    def navigate_to_diagnostic_trace_route_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Trace Route page")
        self.navigate_to_section("icon-diagnostics", "Trace Route", labelName="Diagnostics")

    def navigate_to_packet_replay_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Packet Replay page")
        self.navigate_to_section("icon-diagnostics", "Packet Replay", labelName="Diagnostics")

    def navigate_to_diagnostic_real_time_blacklist_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Real-Time Blacklist page")
        self.navigate_to_section("icon-diagnostics", "Real-Time Blacklist", labelName="Diagnostics")

    def navigate_to_diagnostic_reverse_name_lookup_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Reverse Name Lookup page")
        self.navigate_to_section("icon-diagnostics", "Reverse Name Lookup", labelName="Diagnostics")

    def navigate_to_connection_topx_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Connection TopX page")
        self.navigate_to_section("icon-diagnostics", "Connection TopX", labelName="Diagnostics")

    def navigate_to_diagnostic_geo_and_botnet_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Geo and Botnet page")
        self.navigate_to_section("icon-diagnostics", "Geo and Botnet", labelName="Diagnostics")

    def navigate_to_diagnostic_mx_and_banner_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> MX and Banner page")
        self.navigate_to_section("icon-diagnostics", "MX and Banner", labelName="Diagnostics")

    def navigate_to_diagnostic_cfs_url_rating_request_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> URL Rating Request page")
        self.navigate_to_section("icon-diagnostics", "URL Rating Request", labelName="Diagnostics")

    def navigate_to_diagnostic_pmtu_discovery_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> PMTU Discovery page")
        self.navigate_to_section("icon-diagnostics", "PMTU Discovery", labelName="Diagnostics")

    def navigate_to_switch_diagnostics_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Switch Diagnostics page")
        self.navigate_to_section("icon-diagnostics", "Switch Diagnostics", labelName="Diagnostics")


    def navigate_to_network_monitor_section(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Diagnostics -> Network Monitor page")
        self.navigate_to_section("icon-diagnostics", "Network Monitor", labelName="Diagnostics")

    def navigate_to_legal_info_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Legal Information page")
        self.navigate_to_section("icon-register", "Legal Information")

    def navigate_to_api_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to API page")
        self.navigate_to_section("icon-diamond", "API")

    # Navigates to Analytics page
    def navigate_to_analytics_page(self):
        logger.debug2("Navigating to Analytics page")
        self.navigate_to_page("icon-stats-growth")

    def navigate_to_logs_events_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Logs -> Events page")
        self.navigate_to_section("icon-monitoring", "Events", labelName="Logs")

    def navigate_to_sdwan_activity_logs_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to SD-WAN Activity -> Logs page")
        self.navigate_to_section("icon-monitoring", "Logs", labelName="SD-WAN Activity")

    def navigate_to_aws_activity_logs_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to AWS Activity -> Logs page")
        self.navigate_to_section("icon-monitoring", "Logs", labelName="AWS Activity")

    def navigate_to_all_sessions_overview_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to All Sessions -> Overview page")
        self.navigate_to_section("icon-monitoring", "Overview", labelName="All Sessions")

    def navigate_to_threat_assessment_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Threat Assessment(CTA) page")
        self.navigate_to_section("icon-monitoring", "Threat Assessment(CTA)", labelName="Reports")

    def navigate_to_analytics_network_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Network page")
        self.navigate_to_section("icon-monitoring", "Network", labelName="Reports")

    def navigate_to_analytics_application_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Application")
        self.navigate_to_section("icon-monitoring", "Application", labelName="Reports")

    def navigate_to_web_url_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Web/URL page")
        self.navigate_to_section("icon-monitoring", "Web/URL", labelName="Reports")

    def navigate_to_ip_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> IP page")
        self.navigate_to_section("icon-monitoring", "IP", labelName="Reports")

    def navigate_to_analytics_user_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> User page")
        self.navigate_to_section("icon-monitoring", "User", labelName="Reports")

    def navigate_to_analytics_threats_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Threats page")
        self.navigate_to_section("icon-monitoring", "Threats", labelName="Reports")

    def navigate_to_analytics_regions_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Regions page")
        self.navigate_to_section("icon-monitoring", "Regions", labelName="Reports")

    def navigate_to_analytics_real_time_monitor_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> Real-Time Monitor page")
        self.navigate_to_section("icon-monitoring", "Real-Time Monitor", labelName="AppFlow")

    def navigate_to_analytics_appflow_monitor_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> AppFlow Monitor page")
        self.navigate_to_section("icon-monitoring", "AppFlow Monitor", labelName="AppFlow")

    def navigate_to_analytics_appflow_reports_page(self):
        self.navigate_to_analytics_page()
        logger.debug2("Navigating to Reports -> AppFlow Reports page")
        self.navigate_to_section("icon-monitoring", "AppFlow Reports", labelName="AppFlow")

    # Navigates to Device page
    def navigate_to_device_page(self):
        logger.debug2("Navigating to Device page")
        self.navigate_to_page("icon-monitor")

    def navigate_to_system_status_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Status page")
        self.navigate_to_section("icon-system", "Status", labelName="System")

    def navigate_to_system_licenses_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Licenses page")
        self.navigate_to_section("icon-system", "Licenses", labelName="System")

    def navigate_to_system_administration(self):
        logger.debug2("Navigating to System Administration page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-system", "Administration")
        logger.debug2("Administration Page loaded successfully")

    def navigate_to_system_time_settings_section(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Time page")
        self.navigate_to_section("icon-system", "Time", labelName="System")
        self.ui_wrapper.click_element('xpath', "//span/span[text()='Settings']")

    def navigate_to_system_ntp_servers_section(self):
        logger.debug2("Navigating to System Time page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-system", "Time")
        self.navigate_to_tab("NTP Servers")

    def navigate_to_network_dns_settings_section(self):
        logger.debug2("Navigating to Network DNS page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-system", "DNS", labelName="System")
        self.navigate_to_tab("Settings")

    def navigate_to_network_split_dns_section(self):
        logger.debug2("Navigating to Network DNS page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-system", "DNS", labelName="System")
        self.navigate_to_tab("Split DNS")

    # def navigate_to_dynamic_dns_section(self):
    #     logger.debug2("Navigating to Dynamic DNS Section Page")
    #     self.navigate_to_device_page()
    #     self.navigate_to_section("icon-device-hub", "Dynamic DNS")
    #     logger.debug2("Dynamic DNS Section Page loaded successfully")

    def navigate_to_system_dynamic_dns_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Dynamic DNS page")
        self.navigate_to_section("icon-system", "Dynamic DNS", labelName="System")

    def navigate_to_system_certificates_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Certificates page")
        self.navigate_to_section("icon-system", "Certificates", labelName="System")

    def navigate_to_system_snmp_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > SNMP page")
        self.navigate_to_section("icon-system", "SNMP", labelName="System")

    def navigate_to_system_wxa_firmware_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > WXA Firmware page")
        self.navigate_to_section("icon-system", "WXA Firmware", labelName="System")

    def navigate_to_system_firmware_settings_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Firmware and Settings page")
        self.navigate_to_section("icon-system", "Firmware and Settings", labelName="System")

    def navigate_to_system_settings_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to System - > Settings page")
        self.navigate_to_section("icon-system", "Settings", labelName="System")

    def navigate_to_device_restart(self):
        logger.debug2("Navigating to Device -> Restart page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-system", "Restart", labelName="System")
        logger.debug2("Restart Page loaded successfully")

    def navigate_to_configuration_audit_logs_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to Configuration - > Audit logs  page")
        self.navigate_to_section("icon-system", "Audit logs", labelName="Configuration")

    def navigate_to_configuration_config_logs_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to Configuration - > Config diffs page")
        self.navigate_to_section("icon-system", "Config diffs", labelName="Configuration")

    def navigate_to_configuration__page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to Configuration - >  page")
        self.navigate_to_section("icon-system", "", labelName="Configuration")

    def navigate_to_ha_status_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to High Availability - > Status page")
        self.navigate_to_section("icon-high-availability", "Status", labelName="High Availability")

    def navigate_to_ha_settings_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to High Availability - > Settings page")
        self.navigate_to_section("icon-high-availability", "Settings", labelName="High Availability")

    def navigate_to_ha_advanced_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to High Availability - > Advanced page")
        self.navigate_to_section("icon-high-availability", "Advanced", labelName="High Availability")

    def navigate_to_ha_monitoring_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to High Availability - > Monitoring page")
        self.navigate_to_section("icon-high-availability", "Monitoring", labelName="High Availability")

    def navigate_to_tenant_status_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to Tenant - > Status page")
        self.navigate_to_section("icon-high-availability", "Status", labelName="Tenant")

    def navigate_to_tenant_license_firmware_management_page(self):
        self.navigate_to_device_page()
        logger.debug2("Navigating to Tenant - > License and Firmware Management page")
        self.navigate_to_section("icon-high-availability", "License and Firmware Management", labelName="Tenant")

    def navigate_to_fw_settings_Advanced(self):
        logger.debug2("Navigating to Firewall Advanced Settings")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Advanced", labelName="Firewall Settings")
        logger.debug2("Firewall Advanced Settings Page loaded successfully")

    def navigate_to_fw_settings_Bandwidth_mgmt(self):
        logger.debug2("Navigating to Firewall Bandwidth Mgmt")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Bandwidth Mgmt", labelName="Firewall Settings")
        logger.debug2("Firewall Bandwidth Mgmt Page loaded successfully")

    def navigate_to_flood_protection_section(self):
        logger.debug2("Navigating to Flood Protection TCP Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Flood Protection", labelName="Firewall Settings")
        self.navigate_to_tab("TCP")
        logger.debug2("Flood Protection TCP Page loaded successfully")

    def navigate_to_flood_protection_udp_section(self):
        logger.debug2("Navigating to Flood Protection UDP Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Flood Protection", labelName="Firewall Settings")
        self.navigate_to_tab("UDP")
        logger.debug2("Flood Protection UDP Page loaded successfully")

    def navigate_to_flood_protection_icmp_section(self):
        logger.debug2("Navigating to Flood Protection ICMP Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Flood Protection", labelName="Firewall Settings")
        self.navigate_to_tab("ICMP")
        logger.debug2("Flood Protection ICMP Page loaded successfully")

    def navigate_to_multicast_section(self):
        logger.debug2("Navigating to Multicast Section Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Multicast", labelName="Firewall Settings")
        logger.debug2("Multicast Settings Page loaded successfully")

    def navigate_to_qos_mapping_section(self):
        logger.debug2("Navigating to Qos Mapping Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "QoS Mapping", labelName="Firewall Settings")
        logger.debug2("Qos Mapping Page loaded successfully")

    def navigate_to_ssl_control_section(self):
        logger.debug2("Navigating to SSL Control Section Page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "SSL Control", labelName="Firewall Settings")
        logger.debug2("SSL Control Page loaded successfully")

    def navigate_to_SSH_cipher_control_section(self):
        logger.debug2("Navigating to SSH Cipher Control section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Cipher Control", labelName="Firewall Settings")
        self.navigate_to_tab("SSH Ciphers")
        logger.debug2("SSH Cipher Control section loaded successfully")

    def navigate_to_TLS_cipher_control_section(self):
        logger.debug2("Navigating to TLS Cipher Control section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-firewall-settings", "Cipher Control", labelName="Firewall Settings")
        self.navigate_to_tab("TLS Ciphers")
        logger.debug2("TLS Cipher Control section loaded successfully")

    def navigate_to_users_status_section(self):
        logger.debug2("Navigating to User Status section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Status", labelName="Users")
        logger.debug2("User Status section loaded successfully")

    def navigate_to_users_settings_auth_section(self):
        logger.debug2("Navigating to User Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.navigate_to_tab("Authentication")
        logger.debug2("User Settings section loaded successfully")

    def navigate_to_users_settings_web_login_section(self):
        logger.debug2("Navigating to User Web login Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.navigate_to_tab("Web Login")
        logger.debug2("User Web login Settings section loaded successfully")

    def navigate_to_users_settings_auth_bypass_section(self):
        logger.debug2("Navigating to User Authentication Bypass Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.navigate_to_tab("Authentication Bypass")
        logger.debug2("User Authentication Bypass Settings section loaded successfully")

    def navigate_to_users_settings_user_sessions_section(self):
        logger.debug2("Navigating to User Session Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.navigate_to_tab("User Sessions")
        logger.debug2("User Sessions Settings section loaded successfully")

    def navigate_to_users_settings_accounting_section(self):
        logger.debug2("Navigating to User Accounting Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Settings", labelName="Users")
        self.navigate_to_tab("Accounting")
        logger.debug2("User Accounting Settings section loaded successfully")

    def navigate_to_users_partitions_section(self):
        logger.debug2("Navigating to User Partitions section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Partitions", labelName="Users")
        logger.debug2("User Partitions section loaded successfully")

    def navigate_to_local_users_section(self):
        logger.debug2("Navigating to Local Users & Groups section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Local Users & Groups", labelName="Users")
        self.navigate_to_tab("Local Users")
        logger.debug2("Local Users & Groups section loaded successfully")

    def navigate_to_local_groups_section(self):
        logger.debug2("Navigating to Local Groups section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Local Users & Groups", labelName="Users")
        self.navigate_to_tab("Local Groups")
        logger.debug2("Local Groups section loaded successfully")

    def navigate_to_local_users_group_settings_section(self):
        logger.debug2("Navigating to Local Users & Groups setting section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Local Users & Groups", labelName="Users")
        self.navigate_to_tab("Settings")
        logger.debug2("Local Users & Groups Settings section loaded successfully")

    def navigate_to_users_guest_services(self):
        logger.debug2("Navigating to Guest Services section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Guest Services", labelName="Users")
        logger.debug2("Guest Services section loaded successfully")

    def navigate_to_users_guest_accounts(self):
        logger.debug2("Navigating to Guest Accounts section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Guest Accounts", labelName="Users")
        logger.debug2("Guest Accounts section loaded successfully")

    def navigate_to_guest_status_section(self):
        logger.debug2("Navigating to Guest Status section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-user", "Guest Status", labelName="Users")
        logger.debug2("Guest Status section loaded successfully")

    def navigate_to_flow_reporting_section(self):
        logger.debug2("Navigating to Flow Reporting section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        logger.debug2("Flow Reporting section loaded successfully")

    def navigate_to_flow_reporting_statistics_section(self):
        logger.debug2("Navigating to Flow Reporting Statistics section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("Statistics")
        logger.debug2("Flow Reporting Statistics section loaded successfully")

    def navigate_to_flow_reporting_settings_section(self):
        logger.debug2("Navigating to Flow Reporting Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("Settings")
        logger.debug2("Flow Reporting Settings section loaded successfully")

    def navigate_to_flow_reporting_gmsflow_server_section(self):
        logger.debug2("Navigating to Flow Reporting GMSFlow Server section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("GMSFlow Server")
        logger.debug2("Flow Reporting GMSFlow Server section loaded successfully")

    def navigate_to_flow_reporting_appflow_server_section(self):
        logger.debug2("Navigating to Flow Reporting AppFlow Server section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("AppFlow Server")
        logger.debug2("Flow Reporting AppFlow Server section loaded successfully")

    def navigate_to_flow_reporting_external_collector_section(self):
        logger.debug2("Navigating to Flow Reporting External Collector section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("External Collector")
        logger.debug2("Flow Reporting External Collector section loaded successfully")

    def navigate_to_flow_reporting_sfr_mailling_section(self):
        logger.debug2("Navigating to Flow Reporting SFR mailling section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "Flow Reporting", labelName="AppFlow")
        self.navigate_to_tab("SFR mailling")
        logger.debug2("Flow Reporting SFR mailling section loaded successfully")

    def navigate_to_gms_flow_server_section(self):
        logger.debug2("Navigating to GMSFlow Server section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "GMSFlow Server", labelName="AppFlow")
        logger.debug2("GMSFlow Server section loaded successfully")

    def navigate_to_app_flow_server_section(self):
        logger.debug2("Navigating to AppFlow Server section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "AppFlow Server", labelName="AppFlow")
        self.navigate_to_tab("Discovered Servers")
        logger.debug2("AppFlow Server Discovered Servers section loaded successfully")

    def navigate_to_app_flow_server_settings_section(self):
        logger.debug2("Navigating to AppFlow Server section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-appflow-settings", "AppFlow Server", labelName="AppFlow")
        self.navigate_to_tab("Settings")
        logger.debug2("AppFlow Server Settings section loaded successfully")

    def navigate_to_device_log_settings_section(self):
        logger.debug2("Navigating to Log Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Settings", labelName="Log")
        logger.debug2("Log Settings loaded successfully")

    def navigate_to_log_management_syslog(self):
        logger.debug2("Navigating to Syslog page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-logger-settings", "Syslog")
        logger.debug2("Syslog Page loaded successfully")

    def navigate_to_device_log_syslog_settings_section(self):
        logger.debug2("Navigating to Log Syslog section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Syslog", labelName="Log")
        self.navigate_to_tab("Syslog Settings")
        logger.debug2("Log Syslog loaded successfully")

    def navigate_to_device_log_syslog_server_section(self):
        logger.debug2("Navigating to Log Syslog section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Syslog", labelName="Log")
        self.navigate_to_tab("Syslog Servers")
        logger.debug2("Log Syslog loaded successfully")

    def navigate_to_log_automation_section(self):
        logger.debug2("Navigating to Automation page")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Automation")
        logger.debug2("Log Automation loaded successfully")

    def navigate_to_device_log_automation_email_settings_section(self):
        logger.debug2("Navigating to Log Automation Email Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Automation", labelName="Log")
        self.navigate_to_tab("Email Settings")
        logger.debug2("Log Automation Email Settings loaded successfully")

    def navigate_to_device_ftp_log_automation_section(self):
        logger.debug2("Navigating to FTP log Automation section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Automation", labelName="Log")
        self.navigate_to_tab("FTP log Automation")
        logger.debug2("FTP log Automation loaded successfully")

    def navigate_to_device_log_solera_capture_stack_section(self):
        logger.debug2("Navigating to Solera Capture Stack section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Automation", labelName="Log")
        self.navigate_to_tab("Solera Capture Stack")
        logger.debug2("Solera Capture Stack loaded successfully")

    def navigate_to_name_resolution_section(self):
        logger.debug2("Navigating to Name Resolution section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Name Resolution", labelName="Log")
        logger.debug2("Name Resolution loaded successfully")

    def navigate_to_log_management_reports(self):
        logger.debug2("Navigating to Reports section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-log-settings", "Reports", labelName="Log")
        logger.debug2("Reports loaded successfully")

    def navigate_to_internal_wireless_status_section(self):
        logger.debug2("Navigating to Internal Wireless Access point Status section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Status", labelName="Internal Wireless")
        self.navigate_to_tab("Access Point Status")
        logger.debug2("Internal Wireless Access point status loaded successfully")

    def navigate_to_internal_wireless_station_status_section(self):
        logger.debug2("Navigating to Internal Wireless Station Status section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Status", labelName="Internal Wireless")
        logger.debug2("Internal Wireless Station status loaded successfully")

    def navigate_to_internal_wireless_settings_section(self):
        logger.debug2("Navigating to Internal Wireless Settings section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Settings", labelName="Internal Wireless")
        logger.debug2("Internal Wireless Settings loaded successfully")

    def navigate_to_internal_wireless_security_section(self):
        logger.debug2("Navigating to Internal Wireless Security section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Security", labelName="Internal Wireless")
        logger.debug2("Internal Wireless Security loaded successfully")

    def navigate_to_internal_wireless_advanced_section(self):
        logger.debug2("Navigating to Internal Wireless Advanced section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Advanced", labelName="Internal Wireless")
        logger.debug2("Internal Wireless Advanced loaded successfully")

    def navigate_to_internal_wireless_mac_filter_list_section(self):
        logger.debug2("Navigating to Internal Wireless MAC Filter List section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "MAC Filter List", labelName="Internal Wireless")
        logger.debug2("Internal Wireless MAC Filter List loaded successfully")

    def navigate_to_internal_wireless_ids_section(self):
        logger.debug2("Navigating to Internal Wireless IDS section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "IDS", labelName="Internal Wireless")
        logger.debug2("Internal Wireless IDS loaded successfully")

    def navigate_to_internal_wireless_virtual_access_point_section(self):
        logger.debug2("Navigating to Internal Wireless Virtual Access Point section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Virtual Access Point", labelName="Internal Wireless")
        self.navigate_to_tab("Virtual Access Point Groups")
        logger.debug2("Internal Wireless Virtual Access Point Groups loaded successfully")

    def navigate_to_internal_wireless_virtual_access_point_objects_section(self):
        logger.debug2("Navigating to Internal Wireless Virtual Access Point Objects section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Virtual Access Point", labelName="Internal Wireless")
        self.navigate_to_tab("Virtual Access Point Objects")
        logger.debug2("Internal Wireless Virtual Access Point Objects loaded successfully")

    def navigate_to_internal_wireless_virtual_access_point_profiles_section(self):
        logger.debug2("Navigating to Internal Wireless Virtual Access Point Profiles section")
        self.navigate_to_device_page()
        self.navigate_to_section("icon-service-wireless", "Virtual Access Point", labelName="Internal Wireless")
        self.navigate_to_tab("Virtual Access Point Profiles")
        logger.debug2("Internal Wireless Virtual Access Point Profiles loaded successfully")

    def navigate_to_switch_network_page(self):
        self.navigate_to_home_page()
        logger.debug2("Navigating to Switch Network page")
        self.navigate_to_section("icon-topo-toggle", "Switch Network")

    # Navigates to Network page
    def navigate_to_network_page(self):
        logger.debug2("Navigating to Network page")
        self.navigate_to_page("icon-topo")

    def navigate_to_interfaces_settings_section(self):
        logger.debug2("Navigating to Interfaces section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Interfaces", labelName="Firewall Network")
        self.navigate_to_tab("Interface Settings")
        logger.debug2("Interfaces loaded successfully")

    def navigate_to_interfaces_traffic_settings_section(self):
        logger.debug2("Navigating to Interfaces Traffic Settings section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Interfaces", labelName="Firewall Network")
        self.navigate_to_tab("Traffic Statistics")
        logger.debug2("Interfaces Traffic Settings loaded successfully")

    def navigate_to_portshield_groups_graphics_section(self):
        logger.debug2("Navigating to PortShield Groups section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "PortShield Groups", labelName="Firewall Network")
        self.navigate_to_tab("Port Graphics")
        logger.debug2("Interfaces PortShield Groups loaded successfully")

    def navigate_to_portshield_groups_configuration_section(self):
        logger.debug2("Navigating to PortShield Groups Configuration section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "PortShield Groups", labelName="Firewall Network")
        self.navigate_to_tab("Port Configuration")
        logger.debug2("Interfaces PortShield Groups Configuration loaded successfully")

    def navigate_to_portshield_groups_switch_configuration_section(self):
        logger.debug2("Navigating to PortShield Groups External Switch Configuration section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "PortShield Groups", labelName="Firewall Network")
        self.navigate_to_tab("External Switch Configuration")
        logger.debug2("Interfaces PortShield Groups External Switch Configuration loaded successfully")

    def navigate_to_portshield_groups_switch_diagnostics_section(self):
        logger.debug2("Navigating to PortShield Groups External Switch Diagnostics section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "PortShield Groups", labelName="Firewall Network")
        self.navigate_to_tab("External Switch Diagnostics")
        logger.debug2("Interfaces PortShield Groups External Switch Diagnostics loaded successfully")


    def navigate_to_failover_and_lb_settings_section(self):
        logger.debug2("Navigating to Failover & LB section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Failover & LB", labelName="Firewall Network")
        logger.debug2("Interfaces Failover & LB loaded successfully")

    def navigate_to_neighbor_discovery_section(self):
        logger.debug2("Navigating to Static NDP Entries section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Neighbor Discovery", labelName="Firewall Network")
        self.navigate_to_tab("Static NDP Entries")
        logger.debug2("Static NDP Entries loaded successfully")

    def navigate_to_ndp_settings_section(self):
        logger.debug2("Navigating to NDP Settings section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Neighbor Discovery", labelName="Firewall Network")
        self.navigate_to_tab("NDP Settings")
        logger.debug2("NDP Settings loaded successfully")

    def navigate_to_ndp_cache_section(self):
        logger.debug2("Navigating to NDP Cache section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Neighbor Discovery", labelName="Firewall Network")
        self.navigate_to_tab("NDP Cache")
        logger.debug2("NDP Cache loaded successfully")

    def navigate_to_static_arp(self):
        logger.debug2("Navigating to ARP section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "ARP", labelName="Firewall Network")
        self.navigate_to_tab("Static ARP Entries")
        logger.debug2("ARP loaded successfully")

    def navigate_to_arp_settings_section(self):
        logger.debug2("Navigating to ARP Settings section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "ARP", labelName="Firewall Network")
        self.navigate_to_tab("ARP Settings")
        logger.debug2("ARP Settings loaded successfully")

    def navigate_to_arp_cache_section(self):
        logger.debug2("Navigating to ARP Cache section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "ARP", labelName="Firewall Network")
        self.navigate_to_tab("ARP Cache")
        logger.debug2("ARP Cache loaded successfully")

    def navigate_to_mac_ip_anti_spoof_section(self):
        logger.debug2("Navigating to MAC IP Anti-Spoof section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "MAC IP Anti-Spoof", labelName="Firewall Network")
        self.navigate_to_tab("MAC IPv4 ANTI SPOOF SETTINGS")
        logger.debug2("MAC IP Anti-Spoof loaded successfully")

    def navigate_to_mac_ip_anti_spoof_cache_section(self):
        logger.debug2("Navigating to MAC IP ANTI-SPOOF CACHE section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "MAC IP Anti-Spoof", labelName="Firewall Network")
        self.navigate_to_tab("ANTI-SPOOF CACHE")
        logger.debug2("MAC IP ANTI-SPOOF CACHE loaded successfully")

    def navigate_to_mac_ip_anti_spoof_detected_list_section(self):
        logger.debug2("Navigating to MAC IP ANTI-SPOOF DETECTED LIST section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "MAC IP Anti-Spoof", labelName="Firewall Network")
        self.navigate_to_tab("SPOOF DETECTED LIST")
        logger.debug2("MAC IP ANTI-SPOOF DETECTED LIST loaded successfully")

    def navigate_to_web_proxy_section(self):
        logger.debug2("Navigating to Web Proxy section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Web Proxy", labelName="Firewall Network")
        logger.debug2("Web Proxy loaded successfully")

    # def navigate_to_dhcp_server_section(self):
    #     logger.debug2("Navigating to DHCP Server section")
    #     self.navigate_to_objects_page()
    #     self.navigate_to_section("icon-device-hub", "DHCP Server")
    #     self.navigate_to_tab("DHCP Server Settings")

    def navigate_to_dhcp_server_section(self):
        logger.debug2("Navigating to DHCP Server section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "DHCP Server", labelName="DHCP")
        self.navigate_to_tab("DHCP Server Settings")
        logger.debug2("DHCP Server loaded successfully")

    def navigate_to_dhcp_server_lease_scopes_section(self):
        logger.debug2("Navigating to DHCP Server Lease Scopes section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "DHCP Server", labelName="DHCP")
        self.navigate_to_tab("DHCP Server Lease Scopes")
        logger.debug2("DHCP Server Lease Scopes loaded successfully")

    def navigate_to_current_dhcp_leases_section(self):
        logger.debug2("Navigating to Current DHCP Leases section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "DHCP Server", labelName="DHCP")
        self.navigate_to_tab("Current DHCP Leases")
        logger.debug2("Current DHCP Leases loaded successfully")

    def navigate_to_ip_helper_section(self):
        logger.debug2("Navigating to IP Helper section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "IP Helper", labelName="DHCP")
        self.navigate_to_tab("Relay Protocols")
        logger.debug2("IP Helper loaded successfully")

    def navigate_to_ip_helper_policies_section(self):
        logger.debug2("Navigating to IP Helper Policies section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "IP Helper", labelName="DHCP")
        self.navigate_to_tab("Policies")
        logger.debug2("IP Helper Policies loaded successfully")

    def navigate_to_ip_helper_dhcp_relay_leases_section(self):
        logger.debug2("Navigating to IP Helper DHCP Relay leases section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "IP Helper", labelName="DHCP")
        self.navigate_to_tab("DHCP Relay leases")
        logger.debug2("IP Helper DHCP Relay leases loaded successfully")

    def navigate_to_ip_helper_dhcpv6_relay_leases_section(self):
        logger.debug2("Navigating to IP Helper DHCPv6 Relay leases section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-dhcp", "IP Helper", labelName="DHCP")
        self.navigate_to_tab("DHCPv6 Relay leases")
        logger.debug2("IP Helper DHCPv6 Relay leases loaded successfully")

    def navigate_to_dns_section(self):
        logger.debug2("Navigating to DNS Proxy Settings section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Proxy", labelName="DNS")
        self.navigate_to_tab("Settings")
        logger.debug2("DNS Proxy Settings loaded successfully")

    def navigate_to_static_dns_proxy_cache_section(self):
        logger.debug2("Navigating to Static DNS Proxy Cache Entries section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Proxy", labelName="DNS")
        self.navigate_to_tab("Static DNS Proxy Cache Entries")
        logger.debug2("Static DNS Proxy Cache Entries loaded successfully")

    def navigate_to_dns_proxy_cache_section(self):
        logger.debug2("Navigating to DNS Proxy Cache section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Proxy", labelName="DNS")
        self.navigate_to_tab("DNS Proxy Cache")
        logger.debug2("DNS Proxy Cache loaded successfully")

    def navigate_to_dns_security_section(self):
        logger.debug2("Navigating to DNS Security section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("DNS Sinkhole Service")
        logger.debug2("DNS Security loaded successfully")

    def navigate_to_dns_security_custom_malicious_domain_name_list_section(self):
        logger.debug2("Navigating to DNS Security Custom Malicious Domain Name List section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("Custom Malicious Domain Name List")
        logger.debug2("DNS Security Custom Malicious Domain Name List loaded successfully")

    def navigate_to_dns_security_whitelist_section(self):
        logger.debug2("Navigating to DNS Security White list section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("White list")
        logger.debug2("DNS Security White list loaded successfully")

    def navigate_to_dns_security_dns_tunnel_detection_section(self):
        logger.debug2("Navigating to DNS Tunnel Detection section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("DNS Tunnel Detection")
        logger.debug2("DNS Tunnel Detection loaded successfully")

    def navigate_to_dns_security_detected_suspicious_client_section(self):
        logger.debug2("Navigating to Detected Suspicious Client Info section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("Detected Suspicious Client Info")
        logger.debug2("Detected Suspicious Client Info loaded successfully")

    def navigate_to_dns_security_whitelist_dns_tunnel_section(self):
        logger.debug2("Navigating to White list for DNS tunnel Detection section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-web-activities", "DNS Security", labelName="DNS")
        self.navigate_to_tab("White list for DNS tunnel Detection")
        logger.debug2("White list for DNS tunnel Detection loaded successfully")

    def navigate_to_Voip_settings(self):
        logger.debug2("Navigating to Voip page")
        self.navigate_to_network_page()
        #self.navigate_to_policy_page()
        self.navigate_to_section("icon-voip", "Settings", labelName="VoIP")

    def navigate_to_Voip_call_status(self):
        logger.debug2("Navigating to Voip call status page")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-voip", "Call Status", labelName="VoIP")

    def navigate_to_dynamic_routing_section(self):
        logger.debug2("Navigating to Dynamic Routing section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("Route Advertisement")
        logger.debug2("Dynamic Routing loaded successfully")

    def navigate_to_dynamic_routing_ospfv2_section(self):
        logger.debug2("Navigating to Dynamic Routing OSPFv2 section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("OSPFv2")
        logger.debug2("Dynamic Routing OSPFv2 loaded successfully")

    def navigate_to_dynamic_routing_ospfv3_section(self):
        logger.debug2("Navigating to Dynamic Routing OSPFv3 section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("OSPFv3")
        logger.debug2("Dynamic Routing OSPFv3 loaded successfully")

    def navigate_to_dynamic_routing_rip_section(self):
        logger.debug2("Navigating to Dynamic Routing RIP section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("RIP")
        logger.debug2("Dynamic Routing RIP loaded successfully")

    def navigate_to_dynamic_routing_ripng_section(self):
        logger.debug2("Navigating to Dynamic Routing RIPng section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("RIPng")
        logger.debug2("Dynamic Routing RIPng loaded successfully")

    def navigate_to_dynamic_routing_settings_section(self):
        logger.debug2("Navigating to Dynamic Routing Settings section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Dynamic Routing", labelName="Routing")
        self.navigate_to_tab("Settings")
        logger.debug2("Dynamic Routing Settings loaded successfully")

    def navigate_to_policy_based_routing_section(self):
        logger.debug2("Navigating to Policy Based Routing section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-router", "Policy Based Routing", labelName="Routing")
        logger.debug2("Policy Based Routing loaded successfully")

    def navigate_to_sd_wan_groups_section(self):
        logger.debug2("Navigating to SD WAN GRoups section")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "SD-WAN Groups", labelName="SD-WAN")

    def navigate_to_sd_wan_sla_probes(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "SLA Probes", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > SLA Probes")


    def navigate_to_sd_wan_performance_class_object_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "SLA Class Objects", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > SLA Class Objects")

    def navigate_to_sd_wan_path_selection_profile(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "Path Selection Profiles", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > Path Selection Profiles")

    def navigate_to_sd_wan_policies(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "Policies", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > Policies")

    def navigate_to_sd_wan_monitor(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "Monitor", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > Monitor")

    def navigate_to_sd_wan_connection_logs(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-network-port-interface", "Connection Logs", labelName="SD-WAN")
        logger.debug("Navigated to Network > SD-WAN > Connection Logs")

    def navigate_to_ipsec_vpn_settings(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "Policies/Settings", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > Policies/Settings")

    def navigate_to_ipsec_vpn_advanced(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "Advanced", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > Advanced")

    def navigate_to_ipsec_vpn_dhcp_over_vpn(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "DHCP over VPN", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > DHCP over VPN")

    def navigate_to_ipsec_vpn_l2tp_server(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "L2TP Server", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > L2TP Server")

    def navigate_to_ipsec_vpn_aws_vpn(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "AWS VPN", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > AWS VPN")

    def navigate_to_ipsec_vpn_aws_object(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "AWS Objects", labelName="IPSec VPN")
        logger.debug("Navigated to Network > IPSec VPN > AWS Objects")

    def navigate_to_ssl_vpn_status_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Status", labelName="SSL VPN")
        logger.debug("Navigated to Policies > SSL VPN > Status")

    def navigate_to_ssl_vpn_status_bookmark_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Status", labelName="SSL VPN")
        self.navigate_to_tab("Bookmark")
        logger.debug("Navigated to Policies > SSL VPN > Status")

    def navigate_to_ssl_vpn_server_settings_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Server Settings", labelName="SSL VPN")
        logger.debug("Navigated to Policies > SSL VPN > server settings")

    def navigate_to_ssl_vpn_client_settings_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Client Settings", labelName="SSL VPN")
        logger.debug("Navigated to Policies > SSL VPN > Client Settings")

    def navigate_to_ssl_vpn_portal_settings_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Portal Settings", labelName="SSL VPN")
        logger.debug("Navigated to Policies > SSL VPN > portal settings")

    def navigate_to_ssl_vpn_virtual_bookmark_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-ssl-vpn", "Virtual Office", labelName="SSL VPN")
        logger.debug("Navigated to Policies > SSL VPN > Virtual office")

    # Navigates to Objects page
    def navigate_to_objects_page(self):
        logger.debug2("Navigating to objects page")
        self.navigate_to_page("icon-objects")

    def navigate_to_objects(self):
        logger.debug2("Navigating to objects panel")
        self.navigate_to_page("icon-objects")

    def navigate_to_match_object_section(self):
        logger.debug2("Navigating to Match Object section")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects","Custom Match")
        logger.debug2("Match Objects section loaded successfully")

    def navigate_to_zone_object(self):
        logger.debug2("Navigating to Zone Object page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Zones")
        logger.debug2("Zones section loaded successfully")

    def navigate_to_users_local_users_and_groups(self):
        logger.debug2("Navigating to Users > Local Users & Groups")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-user", "Local Users & Groups")

    def navigate_to_address_object_section(self):
        logger.debug2("Navigating to Address Object page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Addresses")
        self.navigate_to_tab("Address Objects")
        logger.debug2("Address Objects clicked ")

    def navigate_to_address_group_section(self):
        logger.debug2("Navigating to Address Group page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Addresses")
        self.navigate_to_tab("Address Groups")
        logger.debug2("Address Groups clicked ")

    def navigate_to_service_object_section(self):
        logger.debug2("Navigating to Service Object section")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects","Service Objects")
        self.navigate_to_tab("Service Objects")
        logger.debug2("Service Objects section loaded successfully")

    def navigate_to_dynamic_external_object_section(self):
        logger.debug2("Navigating to Dynamic External Object section")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Dynamic External Objects")
        logger.debug2(" Dynamic External Object section loaded successfully")

    def navigate_to_schedule_object_section(self):
        logger.debug2("Navigating to Schedule Object page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Schedules")
        logger.debug2("Schedule Objects clicked ")

    def navigate_to_email_address_object_section(self):
        logger.debug2("Navigating to Email Addresses page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Email Addresses", labelName="Match Objects")
        logger.debug2("Email Addresses clicked ")

    def navigate_to_custom_match_object_section(self):
        logger.debug2("Navigating to Custom Match page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Custom Match", labelName="Match Objects")
        logger.debug2("Custom Match clicked ")

    def navigate_to_content_filter_objects(self):
        logger.debug2("Navigating to Content Filter/URL page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Content Filter/URL", labelName="Match Objects")
        self.navigate_to_tab("URI List Objects")
        logger.debug2("Content Filter/URL clicked ")

    def navigate_to_content_filter_url_groups_section(self):
        logger.debug2("Navigating to Content Filter/URL URI List Groups page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Content Filter/URL", labelName="Match Objects")
        self.navigate_to_tab("URI List Groups")
        logger.debug2("Content Filter/URL URI List Groups clicked ")

    def navigate_to_cfs_action_url_section(self):
        logger.debug2("Navigating to Content Filter/URL CFS Action Objects page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Content Filter/URL", labelName="Match Objects")
        self.navigate_to_tab("CFS Action Objects")
        logger.debug2("Content Filter/URL CFS Action Objects clicked ")

    def navigate_to_cfs_profile_objects_section(self):
        logger.debug2("Navigating to Content Filter/URL CFS Profile Objects page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Content Filter/URL", labelName="Match Objects")
        self.navigate_to_tab("CFS Profile Objects")
        logger.debug2("Content Filter/URL CFS Profile Objects clicked ")

    def navigate_to_dhcp_options_section(self):
        logger.debug2("Navigating to DHCP Options page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "DHCP Options", labelName="Match Objects")
        self.navigate_to_tab("IPv4")
        logger.debug2("DHCP Options clicked ")

    def navigate_to_dhcp_options_ipv6_section(self):
        logger.debug2("Navigating to DHCP Options IPv6 page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "DHCP Options", labelName="Match Objects")
        self.navigate_to_tab("IPv6")
        logger.debug2("DHCP Options IPv6 clicked ")

    def navigate_to_security_services_summary_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Summary", labelName="Security Services")
        logger.debug2("Summary section loaded successfully")

    def navigate_to_security_services_content_filter(self):
        logger.debug2("Navigating to Content Filter Objects")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Content Filter", labelName="Security Services")
        logger.debug2("Content Filter Objects loaded successfully")

    def navigate_to_security_services_settings_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Settings", labelName="Security Services")
        logger.debug2("Settings section loaded successfully")

    def navigate_to_dpi_ssl_enforcement_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "DPI SSL Enforcement", labelName="Security Services")
        logger.debug2("DPI SSL Enforcement section loaded successfully")

    def navigate_to_client_av_enforcement_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Client AV Enforcement", labelName="Security Services")
        logger.debug2("Client AV Enforcement section loaded successfully")

    def navigate_to_client_anti_virus_enforcement_tab(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Client AV Enforcement", labelName="Security Services")
        self.navigate_to_tab("Client Anti-Virus Enforcement")
        logger.debug2("Client AV Enforcement tab loaded successfully")

    def navigate_to_client_cf_enforcement(self):
        logger.debug2("Navigating to Client CF Enforcement")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Client CF Enforcement", labelName="Security Services")
        logger.debug("Client CF Enforcement loaded successfully")

    def navigate_to_gav_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "GAV", labelName="Security Services")
        logger.debug2("GAV section loaded successfully")

    def navigate_to_ips_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "IPS", labelName="Security Services")
        self.navigate_to_tab("IPS Status / IPS Settings")
        logger.debug2("IPS section loaded successfully")

    def navigate_to_ips_policies_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "IPS", labelName="Security Services")
        self.navigate_to_tab("IPS Policies")
        logger.debug2("IPS Policies section loaded successfully")

    def navigate_to_content_filter(self):
        logger.debug2("Navigating to Objects -> Content Filter")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Content Filter")

    def navigate_to_anti_spyware_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Anti-Spyware", labelName="Security Services")
        self.navigate_to_tab("Anti-Spyware")
        logger.debug2("Anti-Spyware section loaded successfully")

    def navigate_to_anti_spyware_policies_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Anti-Spyware", labelName="Security Services")
        self.navigate_to_tab("Policies")
        logger.debug2("Anti-Spyware section loaded successfully")

    def navigate_to_rbl_filter_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "RBL Filter", labelName="Security Services")
        logger.debug2("RBL Filter section loaded successfully")

    def navigate_to_geo_ip_filter_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Geo-IP Filter", labelName="Security Services")
        self.navigate_to_tab("Countries")
        logger.debug2("Geo-IP Filter section loaded successfully")

    def navigate_to_geo_ip_filter_custom_list_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Geo-IP Filter", labelName="Security Services")
        self.navigate_to_tab("Custom List")
        logger.debug2("Geo-IP Filter section loaded successfully")

    def navigate_to_geo_ip_filter_web_block_page_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Geo-IP Filter", labelName="Security Services")
        self.navigate_to_tab("Web Block Page")
        logger.debug2("Geo-IP Filter section loaded successfully")

    def navigate_to_geo_ip_filter_diagnostics_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Geo-IP Filter", labelName="Security Services")
        self.navigate_to_tab("Diagnostics")
        logger.debug2("Geo-IP Filter section loaded successfully")

    def navigate_to_geo_ip_filter_settings_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Geo-IP Filter", labelName="Security Services")
        self.navigate_to_tab("Settings")
        logger.debug2("Geo-IP Filter section loaded successfully")

    def navigate_to_botnet_filter_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Custom Botnet List")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_dynamic_botnet_list_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Dynamic Botnet List")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_dynamic_botnet_list_server_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Dynamic Botnet List Server")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_botnet_web_block_page_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Web Block Page")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_botnet_diagnostics_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Diagnostics")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_botnet_settings_section(self):
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-security-services", "Botnet Filter", labelName="Security Services")
        self.navigate_to_tab("Settings")
        logger.debug2("Botnet Filter section loaded successfully")

    def navigate_to_action_object_section(self):
        logger.debug2("Navigating to Action Object page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Action Objects")
        self.navigate_to_tab("Action Objects")
        logger.debug2("Action Objects clicked")

    def navigate_to_bandwith_object_section(self):
        logger.debug2("Navigating to Bandwidth Objects page")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Bandwidth Objects", labelName="Action Objects")
        logger.debug2("Bandwidth Objects section loaded successfully")

    # Navigates to Policy page
    def navigate_to_policy_page(self):
        logger.debug2("Navigating to policy page")
        self.ui_wrapper.click_element('xpath', '//div/span/span[contains(@class, "icon-menu")]')
        self.navigate_to_page("icon-service-fwmanagement")

    def navigate_to_overview_monitor_page(self):
        logger.debug2("Navigating to Overview -> Monitor page", labelName="Overview")
        self.navigate_to_section("icon-tasks", "Monitor")

    def navigate_to_overview_diagnostics_page(self):
        logger.debug2("Navigating to Overview -> Diagnostics page", labelName="Overview")
        self.navigate_to_section("icon-tasks", "Diagnostics")

    def navigate_to_overview_shadow_rules_page(self):
        logger.debug2("Navigating to Overview -> Shadow Rules page", labelName="Overview")
        self.navigate_to_section("icon-tasks", "Shadow Rules")

    def navigate_to_dpissh_section(self):
        logger.debug2("Navigating to DPI-SSH -> Configure page", labelName="DPI-SSH")
        self.navigate_to_section("icon-dpi-ssh", "Configure")

    def navigate_to_dpissl_client_section(self):
        logger.debug2("Navigating to DPI-SSL -> Client SSL page", labelName="DPI-SSL")
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")

    def navigate_to_client_ssl_general_section(self):
        logger.debug2("Navigating to DPI-SSL client page general section")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")
        self.navigate_to_tab("General")

    def navigate_to_client_ssl_certificate_section(self):
        logger.debug2("Navigating to DPI-SSL client page certificate section")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")
        self.navigate_to_tab("Certificate")

    def navigate_to_client_ssl_objects_section(self):
        logger.debug2("Navigating to DPI-SSL client page objects section")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")
        self.ui_wrapper.click_element('xpath', "//span/span[text()='Objects']")

    def navigate_to_client_ssl_common_name_section(self):
        logger.debug2("Navigating to DPI-SSL client page common name section")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")
        self.navigate_to_tab("Common Name")
        if self.ui_wrapper.does_element_exist_now('xpath', '//p[text()="e.entries is undefined"]'):
            self.ui_helper.accept_alert()

    def navigate_to_client_ssl_cfs_category_section(self):
        logger.debug2("Navigating to DPI-SSL client page cfs category section")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Client SSL")
        self.navigate_to_tab("CFS Category-based Exclusion/Inclusion")
        if self.ui_wrapper.does_element_exist_now('xpath', '//p[text()="e.dpi_ssl.client.cfs_categories is undefined"]'):
            self.ui_helper.accept_alert()

    def navigate_to_server_ssl_section(self):
        logger.debug2("Navigating to DPI-SSL server page")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-dpi-ssl", "Server SSL")

    def navigate_to_policies_access_rules(self):
        logger.debug2("Navigating to Access Rules")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Access Rules", labelName="")
        logger.debug("Navigated to Policies > Rules and Policies > Access Rules")

    # def navigate_to_content_filter(self):
    #     logger.debug2("Navigating to Policies page")
    #     self.navigate_to_policy_page()
    #     self.navigate_to_section("icon-security-services", "Content Filter")

    def navigate_to_policies_application_rules(self):
        logger.debug2("Navigating to Application Rules")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Application Rules")
        logger.debug("Navigated to Policies > Rules and Policies > Application Rules")

    def navigate_to_policies_application_control(self):
        logger.debug2("Navigating to Application Control")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Application Control")
        self.navigate_to_tab("App Control Status")
        logger.debug("Navigated to Policies > Rules and Policies > Application Control")

    def navigate_to_policies_app_control_global_settings(self):
        logger.debug2("Navigating to App Control Global Settings")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Application Control")
        self.navigate_to_tab("App Control Global Settings")
        logger.debug("Navigated to Policies > Rules and Policies > Application Control")

    def navigate_to_policies_app_control_advanced(self):
        logger.debug2("Navigating to App Control Advanced")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Application Control")
        self.navigate_to_tab("App Control Advanced")
        logger.debug("Navigated to Policies > Rules and Policies > Application Control")

    def navigate_to_policies_nat(self):
        logger.debug2("Navigating to NAT")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "NAT")
        logger.debug("Navigated to Policies > Rules and Policies > NAT")

    def navigate_to_policy_based_routes(self):
        logger.debug2("Navigating to Policy Based Routes")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "Policy Based Routes")
        logger.debug("Navigated to Policies > Rules and Policies > Policy Based Routes")

    def navigate_to_policy_anti_spam_status(self):
        logger.debug2("Navigating to Status")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Status")
        logger.debug("Navigated to Policies > Rules and Policies > Status")

    def navigate_to_policy_anti_spam_settings(self):
        logger.debug2("Navigating to Settings")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Settings")
        self.navigate_to_tab("ANTI-SPAM GLOBAL SETTINGS")
        logger.debug("Navigated to Policies > Rules and Policies > Settings")

    def navigate_to_policy_anti_spam_user_defined_access_list(self):
        logger.debug2("Navigating to USER-DEFINED ACCESS LISTS")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Settings")
        self.navigate_to_tab("USER-DEFINED ACCESS LISTS")
        logger.debug("Navigated to Policies > Rules and Policies > Settings")

    def navigate_to_policy_anti_spam_user_advanced_settings(self):
        logger.debug2("Navigating to ANTI-SPAM ADVANCED SETTINGS")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Settings")
        self.navigate_to_tab("ANTI-SPAM ADVANCED SETTINGS")
        logger.debug("Navigated to Policies > Rules and Policies > Settings")

    def navigate_to_policy_anti_spam_statistics(self):
        logger.debug2("Navigating to Statistics")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Statistics")
        logger.debug("Navigated to Policies > Rules and Policies > Statistics")

    def navigate_to_policy_anti_spam_rbl_filter(self):
        logger.debug2("Navigating to RBL Filter")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "RBL Filter")
        logger.debug("Navigated to Policies > Rules and Policies > RBL Filter")

    def navigate_to_policy_anti_spam_relay_domains(self):
        logger.debug2("Navigating to Relay Domains")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Relay Domains")
        logger.debug("Navigated to Policies > Rules and Policies > Relay Domains")

    def navigate_to_policy_anti_spam_junk_box_view(self):
        logger.debug2("Navigating to Junk Box View")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Junk Box View")
        logger.debug("Navigated to Policies > Rules and Policies > Junk Box View")

    def navigate_to_policy_anti_spam_junk_box_summary(self):
        logger.debug2("Navigating to Junk Box Summary")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Junk Box Summary")
        logger.debug("Navigated to Policies > Rules and Policies > Junk Box Summary")

    def navigate_to_policy_anti_spam_user_view_setup(self):
        logger.debug2("Navigating to User View Setup")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "User View Setup")
        logger.debug("Navigated to Policies > Rules and Policies > User View Setup")

    def navigate_to_policy_anti_spam_address_books(self):
        logger.debug2("Navigating to Address Books")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Address Books")
        self.navigate_to_tab("Allowed")
        logger.debug("Navigated to Policies > Rules and Policies > Address Books")

    def navigate_to_policy_anti_spam_blocked_address_books(self):
        logger.debug2("Navigating to Address Books")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Address Books")
        self.navigate_to_tab("Blocked")
        logger.debug("Navigated to Policies > Rules and Policies > Address Books")

    def navigate_to_policy_anti_spam_manage_users(self):
        logger.debug2("Navigating to Manage Users")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Manage Users")
        logger.debug("Navigated to Policies > Rules and Policies > Manage Users")

    def navigate_to_policy_anti_spam_ldap_configuration(self):
        logger.debug2("Navigating to LDAP Configuration")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "LDAP Configuration")
        logger.debug("Navigated to Policies > Rules and Policies > LDAP Configuration")

    def navigate_to_policy_anti_spam_advanced(self):
        logger.debug2("Navigating to Advanced")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Advanced")
        logger.debug("Navigated to Policies > Rules and Policies > Advanced")

    def navigate_to_policy_anti_spam_downloads(self):
        logger.debug2("Navigating to Downloads")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-anti-spam", "Downloads")
        logger.debug("Navigated to Policies > Rules and Policies > Downloads")

    def navigate_to_advanced_vpn_settings_section(self):
        logger.debug2("Navigating to Advanced VPN Settings Section Page")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "Advanced")
        logger.debug2("Advanced VPN Settings Page loaded successfully")

    # def navigate_to_overview_monitor_page(self):
    #     logger.debug2("Navigating to Overview -> Monitor page")
    #     self.navigate_to_section("icon-tasks", "")

    def navigate_to_neighbour_discovery_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-device-hub", "Neighbor Discovery")
        logger.debug("Neighbor Discovery Section Page loaded successfully")

    def navigate_to_service_group_section(self):
        logger.debug2("Navigating to Service Group section")
        self.navigate_to_objects_page()
        self.navigate_to_section("icon-objects", "Services", labelName="Match Objects")
        self.navigate_to_tab("Service Groups")
        logger.debug2("Service Groups section loaded successfully")
        
    def navigate_to_ipsec_vpn_settings_ipv6(self):
        logger.debug2("Navigating to IPv6 VPN Settings Section Page")
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "Policies/Settings", labelName="IPSec VPN")
        self.navigate_to_tab("IPv6")
        logger.debug("Navigated to Network > IPSec VPN > Policies/Settings > IPv6")

    def navigate_to_nat_policy_section(self):
        logger.debug2("Navigating to Nat Policy")
        self.navigate_to_policy_page()
        self.navigate_to_section("icon-rules", "NAT")
        logger.debug("Nat Policy Page loaded successfully")

    def navigate_to_l2tp_server_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "L2TP Server")
        logger.debug("Click IPSec VPN---L2TP Server Page successfully") 

    def navigate_to_dhcp_over_vpn_section(self):
        self.navigate_to_network_page()
        self.navigate_to_section("icon-vpn", "DHCP over VPN")
        logger.debug("Click IPSec VPN---DHCP over VPN Page successfully")