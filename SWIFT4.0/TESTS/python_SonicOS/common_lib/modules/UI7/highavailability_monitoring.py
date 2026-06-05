from modules.UI7.common_require import *

class HighAvailabilityMonitoring:
    ''' HighAvailabilityMonitoring '''

    def __init__(self):
        x0_mon = {
            'port': 'X0',
            'phy_mon': True,
            'pri_ip': '192.168.168.169',
            'sec_ip': '192.168.168.170',
            'allow_manage': False,
            'log_probe_ip': '192.168.168.161',
        }
        x1_mon = {
            'port': 'X1',
            'phy_mon': True,
            'pri_ip': '192.168.168.169',
            'sec_ip': '192.168.168.170',
            'allow_manage': False,
            'log_probe_ip': '192.168.168.161',
        }

    def get_row_element(self, port: str, version=4):
        self.navigation.navigate_to_ha_monitoring_section()
        version_tab = 'Monitoring Ipv4 Settings'
        if version == 6:
            version_tab = 'Monitoring IPv6 Settings'
        self.navigation.navigate_to_tab(version_tab)
        rows = self.ui_wrapper.get_table_rows('class', 'sw-table-body__cont__table')
        for item in rows:
            info = item.text.lower()
            if port.lower() in info:
                logger.info('Find ' + port + ' element.')
                return item
        logger.error("Didn't find " + port + ' element.')
        return False

    def get_all_toggles(self):
        objs = self.ui_wrapper.get_elements('class', 'sw-toggle')
        return objs

    def get_monitoring_info(self, port: str, version=4):
        row = self.get_row_element(port, version)
        if not row:
            return {}
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 8:
            logger.error('Not enough columns found.')
            return {}
        mon_dict = {
            'port': port
        }
        mon_dict.update({'pri_ip': cols[2].text})
        mon_dict.update({'sec_ip': cols[3].text})
        mon_dict.update({'probe_ip': cols[4].text})
        if 'background-color: rgb(153, 204, 0)' in cols[5].get_attribute('innerHTML'):
            mon_dict.update({'phy_mon': True})
        else:
            mon_dict.update({'phy_mon': False})
        if 'background-color: rgb(153, 204, 0)' in cols[6].get_attribute('innerHTML'):
            mon_dict.update({'log_mon': True})
        else:
            mon_dict.update({'log_mon': False})
        if 'background-color: rgb(153, 204, 0)' in cols[7].get_attribute('innerHTML'):
            mon_dict.update({'manage': True})
        else:
            mon_dict.update({'manage': False})
        pprint.pprint(mon_dict)
        return mon_dict

    def config_monitoring(self, **kwargs):
        pprint.pprint(kwargs)
        self.navigation.navigate_to_ha_monitoring_section()
        if 'port' not in kwargs.keys() or 'version' not in kwargs.keys():
            Assertion.fail('Please pass in port information and version information.')
        row_obj = self.get_row_element(kwargs['port'], kwargs['version'])
        if not row_obj:
            Assertion.fail("Didn't find " + str(kwargs['port']) + " row.")

        self.ui_helper.click_on_edit_element_after_hovering(kwargs['port'])
        toggles = self.get_all_toggles()
        pprint.pprint(toggles)
        if not toggles:
            Assertion.fail("Can't locate toggles.")
        for item in toggles:
            source = item.get_attribute('innerHTML')
            if 'physical' in source.lower():
                ele_stat = True
                if 'value="0"' in source:
                    ele_stat = False
                if 'phy_mon' in kwargs.keys() and kwargs['phy_mon'] != ele_stat:
                    item.click()
            elif 'logical' in source.lower():
                ele_stat = True
                if 'value="0"' in source:
                    ele_stat = False
                if 'log_mon' in kwargs.keys() and kwargs['log_mon'] != ele_stat:
                    item.click()
            elif 'management' in source.lower():
                ele_stat = True
                if 'value="0"' in source:
                    ele_stat = False
                if 'manage' in kwargs.keys() and kwargs['manage'] != ele_stat:
                    item.click()

        if 'pri_ip' in kwargs.keys():
            ele_name = 'primary-ipv' + str(kwargs['version']) + '-addres'
            self.ui_wrapper.clear_text_field('name', ele_name)
            self.ui_wrapper.set_text_field('name', ele_name, kwargs['pri_ip'])
        if 'sec_ip' in kwargs.keys():
            ele_name = 'secondary-ipv' + str(kwargs['version']) + '-address'
            self.ui_wrapper.clear_text_field('name', ele_name)
            self.ui_wrapper.set_text_field('name', ele_name, kwargs['sec_ip'])
        if 'log_mon' in kwargs.keys() and kwargs['manage']:
            if 'probe_ip' in kwargs.keys():
                ele_name = 'logical-probe-ipv' + str(kwargs['version']) + '-address'
                self.ui_wrapper.clear_text_field('name', ele_name)
                self.ui_wrapper.set_text_field('name', ele_name, kwargs['probe_ip'])
        try:
            self.ui_helper.submit_page()
            self.ui_wrapper.wait_for_text('Success')
            self.ui_helper.close_page()
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            Assertion.fail("Config monitoring failed.")