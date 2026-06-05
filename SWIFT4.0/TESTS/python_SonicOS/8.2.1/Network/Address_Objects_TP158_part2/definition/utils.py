import re
import time
from runner.settings import logger
from definition.settings import *


def get_interface_default_generated_ao_list(addressobjects_api, inter_face, detail=False):
    ipv4searchlist = []
    ipv6searchlist = []
    outputv4 = addressobjects_api.get_all_addressobject_ipv4()
    logger.info(f'outputv4 is:{outputv4}')
    outputv6 = addressobjects_api.get_all_addressobject_ipv6()
    logger.info(f'outputv6 is:{outputv6}')
    ipv4aolist = outputv4["address_objects"]
    ipv6aolist = outputv6["address_objects"]
    logger.info(f'ipv6aolist is:{ipv6aolist}')

    if len(inter_face) == 2:
        for ipv4ao in ipv4aolist:
            if f"{inter_face} " in ipv4ao["ipv4"]["name"]:
                if detail:
                    ipv4searchlist.append(ipv4ao["ipv4"])
                else:
                    ipv4searchlist.append(ipv4ao["ipv4"]["name"])
    if len(inter_face) == 3:
        for ipv4ao in ipv4aolist:
            if f"{inter_face}" in ipv4ao["ipv4"]["name"]:
                if detail:
                    ipv4searchlist.append(ipv4ao["ipv4"])
                else:
                    ipv4searchlist.append(ipv4ao["ipv4"]["name"])

    for ipv6ao in ipv6aolist:
        if f"{inter_face} IPv6" in ipv6ao["ipv6"]["name"]:
            if detail:
                ipv6searchlist.append(ipv6ao["ipv6"])
            else:
                ipv6searchlist.append(ipv6ao["ipv6"]["name"])
    logger.info(f'ipv4searchlist is:{ipv4searchlist}')
    logger.info(f'ipv6searchlist is:{ipv6searchlist}')
    searchlist = ipv4searchlist + ipv6searchlist
    logger.info(f'searchlist is:{searchlist}')
    return searchlist

def initial_login_ui():
    for i in range(4):
        logger.info(f'open browser for {i+1} time')
        PC1_Login.send_command('pkill firefox')
        result = fwpageui.login_ui_with_head(headless=True, browser_type='chrome')
        logger.info(f'login gui is :{result}')
        if result:
            fwpageui.go_to_url(f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/objects/address-objects/address-object')
            time.sleep(15)
            res = fwpageui.does_element_exist_now('xpath',"//span[text()='Add']")
            if res:
                break
            else:
                res1 = fwpageui.does_element_exist_now('xpath', "//div[@class = 'sw-spinning-progress']")
                if res1:
                    logger.info('quit browser')
                    fwpageui.quit()
        else:
            fwpageui.quit()

def select_ao_or_ao_group_view_item(viewitem = ''):
    if viewitem:
        view_arrow_xpath = "//div[contains(@class,'sw-content-toolbar__inner')]/div[contains(@class,'select-view-filter')]/div[contains(@class,'sw-select__icon')]"
        logger.info('click View arrow')
        fwpageui.click_element('xpath', view_arrow_xpath)
        fwpageui.wait_for_element_to_be_visible('xpath', "//div[@class='sw-dropdown sw-typo-default']")
        fwpageui.move_to_the_element('xpath',
                                     f"//div[contains(@class,'sw-dropdown__inner')]//span[text()='{viewitem}']").click()
        logger.info('wait drop-down list disappears')
        fwpageui.wait_for_element_to_be_invisible('xpath', "//*[contains(@class, 'sw-dropdown-unit')]")
        return True
    else:
        logger.info('viewitem is none,please check...')
        return False