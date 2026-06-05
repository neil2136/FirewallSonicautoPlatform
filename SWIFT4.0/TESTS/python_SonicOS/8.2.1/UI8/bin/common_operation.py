from bin.global_var import *


class PCRunner:

    def goto_test_page(self, url, refresh=0, login_type=None, headless=True, browser_type='firefox'):
        """go to test page steps, including start firefox, login, go to specific url and refresh if set
        :param browser_type: firefox/chrome
        :param headless: Ture/False
        :param login_type: after_resotre
        :param str url: go to url address, example 'https://192.168.168.168/sonicui/7/m/mgmt/policies/ngpe-dns-policies'
        :param int refresh: refresh times, defaults to 0
        """
        if browser_type =='firefox':
            PC1_LOGIN.send_command('pkill firefox')
        else:
            PC1_LOGIN.send_command('pkill chrome')
        # fw_page_ui.login_ui()
        fw_page_ui.login_ui_with_head(login_type=login_type, headless=headless, browser_type=browser_type)
        fw_page_ui.go_to_url(url)
        fw_page_ui.wait_for_page_data_to_be_rendered()
        for i in range(refresh):
            logger.info(f'Refresh for {i+1} time')
            fw_page_ui.refresh_browser()
            fw_page_ui.wait_for_page_data_to_be_rendered()


    def check_element_attribute(self, element, target, attribute='textContent', strict=False) -> bool:
        """find a element and get its attribute then compare with the target

        :param list or WebElement element: one element to check, list should be ['{selector}', '{path}'], example ['css', '.sw-status-flag--normal']
        :param str or list target: target to compare with the attribute of element
        :param str attribute: attribute of element to check, example 'textContent'/'class'/'tagName'/..., defaults to 'textContent'
        :param bool strict: compare result strictly or not(== or in), default to False
        :return bool: check result, True or False
        """
        try:
            if isinstance(element, list):
                text = fw_page_ui.get_attribute_value(*element, attrib_to_get_val=attribute)
            else:
                text = element.get_attribute(attribute)
            text = str(text).lstrip().rstrip()
            logger.info(f'> test\t: {text}')
            logger.info(f'> target\t: {target}')
            if not strict:
                res = text in target or target in text if text and target else False
            else:
                res = target == text if text and target else False
            logger.info(res)
            return res
        except Exception as err:
            logger.error(f"Exception \t:{err}")
            return False

    def check_elements_attribute(self, elements: list, target, attribute='textContent', strict=False) -> bool:
        """find element list and get their attribute then compare with the target list

        :param list element: a element path to find elements as a list, path should be ['{selector}', '{path}'], example ['css', '.sw-status-flag--normal']
        :param list or str target: target to compare with the attribute of element
        :param str attribute: attribute of element to check, example 'textContent'/'class'/'tagName'/..., defaults to 'textContent'
        :return bool: check result, True or False
        """
        try:
            ele_list = fw_page_ui.get_elements(*elements)
            if isinstance(target, list):
                attr_list = [ele.get_attribute(attribute) for ele in ele_list]
                logger.info(f'> test\t: {attr_list}')
                logger.info(f'> target\t: {target}')
                rc = all(item in target for item in attr_list) | all(item in attr_list for item in target)
                logger.info(rc)
                return rc
            rc = []
            for ele in ele_list:
                rc.append(self.check_element_attribute(ele, target=target, attribute=attribute, strict=strict))
            return all(rc)
        except Exception as err:
            logger.error(f"Exception \t:{err}")
            return False

    def check_dropdown_list_value(self, target_list) -> bool:
        """get dropdown list value then compare with the target list

        :param list target: target to compare with the value of the dropdown list
        :return bool: check result, True or False
        """
        try:
            logger.info(f'> target\t: {target_list}')
            test = fw_page_ui.get_drop_down_list_values()
            test_fmt = [str(x).lstrip().rstrip() for x in test]
            logger.info(f'> test\t: {test_fmt}')
            res = all(target in test_fmt for target in target_list)
            logger.info(res)
            return res
        except Exception as err:
            logger.error(f"Exception \t:{err}")
            return False
