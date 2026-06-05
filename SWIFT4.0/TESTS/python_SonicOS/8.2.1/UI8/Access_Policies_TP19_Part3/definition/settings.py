# import form branch lib contents for test suite
from bin.global_var import *
from bin.common_path import *
from bin.common_operation import PCRunner

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.firewall import AccessRuleApi


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/UI8/Access_Policies_TP19_Part3/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/Access_Policies_TP19_Part3.json'


# cases object instantiation
pc_runner = PCRunner()
acl_api = AccessRuleApi(fw)

class CParam:
    Name = ""
    ACL_UUID = ""
    Hits = ''
    custom_acl_1 = 'Custom_1'

class PathData:
    acl_page = base_url + 'policies/ngpe-access-rules'
    acl_table = ['css', '.fw-ftr-ngpe-access-rules__table']
    edit_rule_window = get_xpath_by_text('Editing Rule ')
    add_rule_window = get_xpath_by_text('Adding Rule ')
    grid_icon = ['css', '.icon-grid']
    settings_icon = ['css', '.icon-item-list']
    add_icon = ['css', '.icon-add']
    
    tcp_urgent_toggle = get_toggle_xpath('Allow TCP Urgent Packets')
    hit_num = get_table_entry_element_xpath(CParam.Name, 'hit')
    expend_hit = ['css', '.expanded-rule-details__source-hits']
    expend_diag = ['css', '.expanded-rule-details__action-diagram']
    # expend_conn = ['css', '.expanded-rule-details__destn-hits']
    expend_conn = ['xpath', '//*[contains(@class, "expanded-rule-details__source-hits ")][2]']
    hits_count = ['xpath', '//*[text()="Hits count"]/../following-sibling::div/span']
    hits_usage = ['xpath', '//*[text()="Hits usage"]/../following-sibling::div/span']

    T_Name = '//*[@class="sw-tooltip__inner"]/descendant::*[text()="Name"]/../following-sibling::div/span'
    diagram_window = ['xpath', '//div[contains(@class,"expanded-action-diagram")]/ancestor::div[contains(@class,"sw-modal__content")][1]']
    sticked_diagram = ['xpath', '//div[contains(@class,"expanded-action-diagram")]/ancestor::div[@class="add-access-rule-modal__basic-details"]']
    search_icon = ['xpath', '//div[@name="searchText"]']
    search_text = ['xpath', '//*[@name="searchText" and @type="text"]']


# parameters on the test cases
result_dict = {}

custom_acl_dict = {"access_rules": [{
    "ipv4": {
        "name": CParam.custom_acl_1,
        "from": "LAN",
        "to": "WAN",
        "service": {
            "group": "Ping"
        }
    }
}]}