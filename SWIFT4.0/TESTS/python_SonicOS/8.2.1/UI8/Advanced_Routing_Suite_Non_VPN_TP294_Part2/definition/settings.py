# import form branch lib contents for test suite
from bin.global_var import *
from bin.common_path import *
from bin.common_operation import PCRunner

sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from lib.modules.API.network import InterfaceIPv4Api
from lib.modules.API.system import StatusApi, AdminApi, SettingApi
from lib.modules.CLI.network import AddressObjectCli
from lib.modules.CLI.system import LicenseCli, ScheduleCli


# import from test suite root path like definition
suite_path = os.environ["PYTHON_SONICOS_HOME"] + '/UI8/Advanced_Routing_Suite_Non_VPN_TP294_Part2/'
sys.path.append(suite_path)
sys.path.append(suite_path+'testcases')
TESTPLAN = suite_path + 'testplan/Advanced_Routing_Suite_Non_VPN_TP294.json'


# parameters on the test cases
class CParam:
    Name = "test"

# cases object instantiation
pc_runner = PCRunner()
admin_api = AdminApi(fw)
interface_api = InterfaceIPv4Api(fw)
schedule_cli = ScheduleCli(fw_cli)
ao_cli = AddressObjectCli(fw_cli)
status_api = StatusApi(fw)
license_cli = LicenseCli(fw_cli)
setting_api = SettingApi(fw)

result_dict = {}

# url
routing_page = base_url + 'network/routing'
# path
edit_ospfv2_window = get_xpath_by_text('Interface X0 (LAN) OSPFv2 Configuration')
ospfv2_arrow = get_dropdown_box_element_xpath('OSPFv2', 'arrow')
auth_arrow = get_dropdown_box_element_xpath('Authentication', 'arrow')

settings_icon = ['css', '.icon-settings']
settings_window = ['xpath', '//*[@class="sw-modal__title sw-flexbox__flex" and text()="Settings"]']
abr_arrow = get_dropdown_box_element_xpath('ABR Type', 'arrow')
default_metric_dropdown_box = ['xpath', '//input[@name="metricTypeOption"]/..']

asr_toggle = get_toggle_xpath('Redistribute Static Routes')
asr_metric = get_textbox_element_xpath(name='redistributeStaticRouteMetric')
asr_tag = get_textbox_element_xpath(name='redistributeStaticRouteTag')
asr_dropdown_box = ['xpath', '//input[@name="redistributeStaticRouteMetricType"]/..']

rcn_toggle = get_toggle_xpath('Redistribute Connected Networks')
rcn_metric = get_textbox_element_xpath(name='redistributeConnectedNetworksMetric')
rcn_tag = get_textbox_element_xpath(name='redistributeConnectedNetworkTag')
rcn_dropdown_box = ['xpath', '//input[@name="redistributeConnectedNetworkMetricType"]/..']

rrr_toggle = get_toggle_xpath('Redistribute RIP Routes')
rrr_metric = get_textbox_element_xpath(name='redistributeRipRouteMetric')
rrr_tag = get_textbox_element_xpath(name='redistributeRipRouteTag')
rrr_dropdown_box = ['xpath', '//input[@name="redistributeRipRouteMetricType"]/..']

rrvn_toggle = get_toggle_xpath('Redistribute Remote VPN Networks')
rrvn_metric = get_textbox_element_xpath(name='redistributeRemoteVpnMetric')
rrvn_tag = get_textbox_element_xpath(name='redistributeRemoteVpnTag')
rrvn_dropdown_box = ['xpath', '//input[@name="redistributeRemoteVpnMetricType"]/..']

edit_rip_window = get_xpath_by_text('Interface X0 (LAN) RIP Configuration')
rip_arrow = get_dropdown_box_element_xpath('RIP', 'arrow')

password_checkbox = ['xpath', '//*[@name="userPassword" and @type="checkbox"]/../..']
password_textbox = ['xpath', '//*[@name="userPassword" and @type="password"]/../..']
split_checkbox = ['xpath', '//*[@name="splitHorizon" and @type="checkbox"]/../..']
split_checkbox_edit = ['xpath', '//*[@name="splitHorizon" and @type="checkbox"]/../div[1]/div']
poison_checkbox = ['xpath', '//*[@name="poisonReverse" and @type="checkbox"]/../..']
send_dropdown = ['xpath', '//*[@name="send"]/..']
