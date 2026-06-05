import sys
import os
import re
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Webproxy_813/lib')
sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/Network/Webproxy_813/testcases')
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from runner.unittest.setup import Test
from lib.modules.CLI import network
from lib.modules.CLI import system
from lib.modules.CLI import firewall
from utm import Firewall
from tools.trafficGen import MyHttpClinet
from settings import Parameter
from runner.utils.assertion import Assertion
from verification import capture_packet
from runner.settings import logger
from util.enhancedinfo import show_testcase_info

ip = Parameter.FIREWALL
fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
webproxy = network.WebproxyCli(fw)

class TestWebproxy_add_lan_route(Test):
    uuid = 'NonTC'
    description = 'Add route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL)

    def test_add_lan_route(self):
        logger.info('Add route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        rc = os.system('route add -host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        Assertion.assert_equal(rc, 0, "ERR: show testcae info failed")

class TestWebproxy_01(Test):
    uuid = "SOSAIOT-TC-57438"
    # description = 'Verify that the firewall will accept only valid port number in the Web Proxy configuration page'
    description= show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

    def test_01_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_01_01_port_to_an_invalid_number_a(self):
        webproxy_dict = { 
            'server': '1.1.1.1',
            'port': 'a',
        }
        output = webproxy.config_webproxy(tag=1, **webproxy_dict)[1]
        Assertion.assert_regular(output, 'Invalid input detected', "ERR: webproxy cannot be set to letter")

    def test_01_02_port_to_an_invalid_number_negtive(self):
        webproxy_dict = { 
            'server': '1.1.1.1',
            'port': '-1',
        }
        output = webproxy.config_webproxy(tag=1, **webproxy_dict)[1]
        Assertion.assert_regular(output, 'Invalid input detected', "ERR: webproxy cannot be set to -1")

    def test_01_03_port_to_an_invalid_number_65536(self):
        webproxy_dict = { 
            'server': '1.1.1.1',
            'port': '65536',
        }
        output = webproxy.config_webproxy(tag=1, **webproxy_dict)[1]
        Assertion.assert_regular(output, 'Out of bounds condition', "ERR: webproxy cannot be set to 65536")


class TestWebproxy_02(Test):
    uuid = "SOSAIOT-TC-57435"
    description= show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']
    dts = '221488' # or jira='SOSV-221448'
    
    def test_02_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_02_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.WAN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")

    def test_02_02_start_http_connection(self):
        url = 'http://' + Parameter.WEB_SERVER + '/wiki'
        http = MyHttpClinet(url)
        result = http.Http_get()
        Assertion.assert_equal(result, True, "ERR: Http connection to {} failed".format(url))


class TestWebproxy_03(Test):
    uuid = "SOSAIOT-TC-57436"
    description= show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']

    def test_03_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_03_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.WAN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")

    def test_03_02_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.WAN_PROXY_SERVER, proto_type='TCP')
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: http requests are not forwarded to web proxy server successfully")

    def test_03_03_config_a_down_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.DOWN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")

    def test_03_04_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.WAN_PROXY_SERVER, proto_type='TCP')
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: http requests are not forwarded to web proxy server successfully")        


class TestWebproxy_12(Test):
    uuid = "SOSAIOT-TC-57441"
    description= show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

    def test_12_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_12_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.WAN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': False,
            'forward-public-requests': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    

    def test_12_02_check_pref(self):
        output = fw.cgi_get('prefMeta.xml')
        foundit = 0
        if re.search(r''+ Parameter.WAN_PROXY_SERVER +'[\w\s<>\/]*<guitype>3[\w\s<>\/]*<minval>0[\w\s<>\/]*<maxval>39', output, re.I):
            logger.info('Found webproxy server in prefmeta.xml')
            foundit += 1
        if re.search(r''+ Parameter.WEBPROXY_PORT +'[\w\s<>\/]*<guitype>3[\w\s<>\/]*<minval>0[\w\s<>\/]*<maxval>65535', output, re.I):
            logger.info('Found webproxy port in prefmeta.xml')
            foundit += 1
        if re.search(r'0[\w\s<>\/]*<guitype>1[\w\s<>\/]*<minval>0[\w\s<>\/]*<maxval>0', output, re.I):
            logger.info('Found HTTP requests from LAN or WAN can be forwarded to web proxy server on DMZ in prefmeta.xml')
            foundit += 1
        if re.search(r'0[\w\s<>\/]*<guitype>1[\w\s<>\/]*<minval>0[\w\s<>\/]*<maxval>0', output, re.I):
            logger.info('Found HTTP requests are forwarded to the web proxy server in prefmeta.xml')
            foundit += 1
        Assertion.assert_equal(foundit, 4, "ERR: Check pref fail")    


class TestWebproxy_13(Test):
    uuid = "SOSAIOT-TC-57442"
    description= show_testcase_info(Parameter.TESTPLAN, '13', description=True)['title']

    def test_13_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '13')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_13_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.DOWN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': False,
            'forward-public-requests': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    

    def test_13_02_check_tsr(self):
        tsr_ojb = system.DiagnosticsCli(fw)
        tsr_content = tsr_ojb.export_tsr('192.168.168.169', 'scp', 'root', 'password')
        if not tsr_content:
            Assertion.assert_equal(tsr_content, True, "ERR: Fail to download tsr file.")    
        else:
            tsr_content = os.popen('cat /root/tsr.wri').read()
            tsr_content = get_tsr_part(tsr_content, 'Network', 'Web Proxy')
          
            Assertion.assert_regular(tsr_content, 'httpProxyName\s=\s' + '\'' + Parameter.DOWN_PROXY_SERVER + '\'', "ERR: Webproxy server settings are not correct in tsr.")
            Assertion.assert_regular(tsr_content, 'httpProxyPort\s=\s' + Parameter.WEBPROXY_PORT, "ERR: Webproxy server settings are not correct in tsr.")
            Assertion.assert_regular(tsr_content, 'Bypass Proxy server upon failure\s=\s' + 'FALSE', "ERR: Webproxy server settings are not correct in tsr.")
            Assertion.assert_regular(tsr_content, 'Forward public zones to Proxy Server\s=\s' + 'FALSE', "ERR: Webproxy server settings are not correct in tsr.")
            
class TestWebproxy_15(Test):
    uuid = "SOSAIOT-TC-57443"
    description= show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

    def test_15_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_15_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.DOWN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': False,
            'forward-public-requests': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")

    def test_15_02_start_http_connection(self):
        url = 'http://' + Parameter.WEB_SERVER + '/wiki'
        http = MyHttpClinet(url)
        result = http.Http_get()
        Assertion.assert_equal(result, False, "ERR: Http connection to {} passed, which should fail".format(url))


class TestWebproxy_11(Test):
    uuid = "SOSAIOT-TC-57440"
    description= show_testcase_info(Parameter.TESTPLAN, '11', description=True)['title']

    def test_11_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '11')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
 
    def test_11_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.MY_DMZ_PC_IP,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")  

    def test_11_02_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.MY_DMZ_PC_IP, proto_type='TCP')

        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from LAN can not be forwarded to web proxy server on DMZ successfully")        

    def test_11_03_start_http_connection_again(self):
        url = 'http://' + Parameter.WEB_SERVER + '/wiki'
        http = MyHttpClinet(url)
        result = http.Http_get()
        Assertion.assert_equal(result, True, "ERR: HTTP requests from LAN can NOT bypass when proxy server fails to work")        


class TestWebproxy_del_lan_route(Test):
    uuid = 'NonTC'
    description = 'Del route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL)

    def test_del_lan_route(self):
        logger.info('Del route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        rc = os.system('route del -host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        Assertion.assert_equal(rc, 0, "ERR: del route failed")


class TestWebproxy_add_dmz_route(Test):
    uuid = 'NonTC'
    description = 'Add route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP)

    def test_add_dmz_route(self):
        logger.info('Add route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        rc = os.system('route add -host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        Assertion.assert_equal(rc, 0, "ERR: show testcae info failed")


class TestWebproxy_10(Test):
    uuid = "SOSAIOT-TC-57439"
    description= show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

    def test_10_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")
    
    def test_10_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.MY_LAN_PC_IP,
            'port': Parameter.WEBPROXY_PORT,
            'bypass-upon-failure': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")     

    def test_10_02_add_access_rule_from_DMZ_to_LAN(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'deny',  # "allow,deny,discard"
            'action_new': 'allow',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed")     

    def test_10_03_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')

        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on LAN successfully")        

    def test_10_03_start_http_connection_again(self):
        url = 'http://' + Parameter.WEB_SERVER + '/wiki'
        http = MyHttpClinet(url)
        result = http.Http_get()
        Assertion.assert_equal(result, True, "ERR: HTTP requests from DMZ can NOT bypass when proxy server fails to work")            

    def test_10_04_reset_access_rule_from_DMZ_to_LAN(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'allow',  
            'action_new': 'deny',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed") 


class TestWebproxy_04(Test):
    uuid = "SOSAIOT-TC-57437"
    description= show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

    def test_04_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_04_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.WAN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'forward-public-requests': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")

    def test_04_02_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.WAN_PROXY_SERVER, proto_type='TCP')
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can NOT be forwarded to web proxy server successfully")           

    def test_04_03_Uncheck_Forward_Public_Zone_Client_Request_to_Proxy_Server(self):
        webproxy_dict = { 
            'forward-public-requests': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    
    
    def test_04_04_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.WAN_PROXY_SERVER, proto_type='TCP')
        Assertion.assert_equal(result, 0, "ERR: HTTP requests from LAN can be forwarded to web proxy server on DMZ successfully")  


class TestWebproxy_14(Test):
    uuid = "SOSAIOT-TC-57434"            
    description= show_testcase_info(Parameter.TESTPLAN, '14', description=True)['title']

    def test_14_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '14')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_14_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.WAN_PROXY_SERVER,
            'port': Parameter.WEBPROXY_PORT,
            'forward-public-requests': False,
            'bypass-upon-failure': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    

    def test_14_02_start_http_connection(self):
        result = capture_packet(dst_ip=Parameter.WAN_PROXY_SERVER, proto_type='TCP')
        if result == 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully")        

    def test_14_03_start_http_connection_again(self):
        url = 'http://' + Parameter.WEB_SERVER + '/wiki'
        http = MyHttpClinet(url)
        result = http.Http_get()
        Assertion.assert_equal(result, False, "ERR: HTTP requests from DMZ reach out")  

###del dmz route

class TestWebproxy_05(Test):
    uuid = "SOSAIOT-TC-57444"
    description= show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

    def test_05_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_05_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.MY_LAN_PC_IP,
            'port': Parameter.WEBPROXY_PORT,
            'forward-public-requests': False,
            'bypass-upon-failure': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")   

    def test_05_02_Start_a_Http_connection_from_LAN(self):
        logger.info('Add a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route add host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')
        logger.info('Del a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route del host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully") 

    def test_05_03_Reconfig_webproxy_server(self):
        webproxy_dict = { 
            'forward-public-requests': True,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed") 

    def test_05_04_Allow_DMZ_to_LAN_Rule(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'deny',
            'action_new': 'allow',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed")  

    def test_05_05_Start_a_Http_connection_from_LAN(self):
        logger.info('Add a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route add host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')
        logger.info('Del a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route del host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully") 

    def test_05_06_Restore_DMZ_to_LAN_Rule(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'allow',
            'action_new': 'deny',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed")  

class TestWebproxy_08(Test):
    uuid = "SOSAIOT-TC-57445"
    description= show_testcase_info(Parameter.TESTPLAN, '8', description=True)['title']

    def test_08_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '8')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_08_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.MY_LAN_PC_IP,
            'port': Parameter.WEBPROXY_PORT,
            'forward-public-requests': True,
            'bypass-upon-failure': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    

    def test_08_02_add_access_rule_from_DMZ_to_LAN(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'deny',
            'action_new': 'allow',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed")     

    def test_08_03_start_http_connection(self):
        logger.info('Add a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        os.system('route add host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')
        logger.info('Del a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        os.system('route del host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully") 

    def test_08_04_reset_access_rule_from_DMZ_to_LAN(self):
        rule_obj = firewall.AccessRuleCli(fw)
        rule_opt = {
            'from': 'DMZ',
            'to': 'LAN',
            'action': 'allow',
            'action_new': 'deny',
        }
        result = rule_obj.edit_access_rule(**rule_opt)
        Assertion.assert_equal(result, True, "ERR: Edit rule from DMZ to LAN failed")    


class TestWebproxy_09(Test):
    uuid = "SOSAIOT-TC-57446"
    description= show_testcase_info(Parameter.TESTPLAN, '9', description=True)['title']

    def test_09_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '9')
        Assertion.assert_equal(True, True, "ERR: show testcae info failed")

    def test_09_01_config_webproxy_server(self):
        webproxy_dict = { 
            'server': Parameter.MY_DMZ_PC_IP,
            'port': Parameter.WEBPROXY_PORT,
            'forward-public-requests': True,
            'bypass-upon-failure': False,
        }
        output = webproxy.config_webproxy(**webproxy_dict)
        Assertion.assert_equal(output, True, "ERR: Config webproxy failed")    

    def test_09_02_start_http_connection(self):
        logger.info('Add a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        os.system('route add host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')
        logger.info('Del a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        os.system('route del host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully") 

    def test_09_03_start_http_connection(self):
        logger.info('Add a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route add host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        result = capture_packet(dst_ip=Parameter.MY_LAN_PC_IP, proto_type='TCP')
        logger.info('Del a route to {} via {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        os.system('route del host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.FIREWALL))
        if result > 0:
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: HTTP requests from DMZ can not be forwarded to web proxy server on DMZ successfully") 


class TestWebproxy_del_dmz_route(Test):
    uuid = 'NonTC'
    description = 'Del route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP)

    def test_del_dmz_route(self):
        logger.info('Del route to {} via gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        rc = os.system('route del -host {} gw {}'.format(Parameter.WEB_SERVER, Parameter.X2_IP))
        Assertion.assert_equal(rc, 0, "ERR: show testcae info failed")


def get_tsr_part(tsr, feature, label1=None, label2=None):
    start = "#" + feature + " : " + label1 + "_START"
    end = "#" + feature + " : " + label1 + "_END"
    match1 = re.search(r''+ start +'\n(.*)'+ end +'', tsr, re.I|re.S)
    if match1:
        output1 = match1.group(1)
        if label2:
            match2 = re.serach(r'--'+ label2 +'--\n(.*)(\n+)--', output1, re.I|re.S)
            if match2:
                return match2.group(1)
            else:
                logger.error('Get part TSR failed.')
                return tsr
        else:
            return output1
    else:
        logger.error('Get part TSR failed.')
        return tsr
