import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPSec/dhcp_over_vpn/dhcp_smoke_cases')

from definition.settings import *


class dhcp_01(Test):
    uuid = "SOSAIOT-TC-47582"
    description = show_testcase_info(Parameter.TESTPLAN, '163', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '163')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcp_central_gateway(self):
       response = dhcp_settings.show_dhcpovervpn_central()
       flag = True if ('"internal_dhcp": "True"' in json.dumps(response)) else False
       if flag == False:
          edit_central= {
            'internal_dhcp': True,
            'global_vpn': False,
            'remote': True,
            'relay_ip': '0.0.0.0',
            'send_requests': False,
            
            }

          response = dhcp_settings.config_dhcpvpn_centralgw(**edit_central)
          response1 = dhcp_settings.show_dhcpovervpn_central()
          Assertion.assert_regular(json.dumps(response1), '"internal_dhcp": true', 'ERR:failed to enable internal dhcp for remote firewall')

          
class dhcp_02(Test):
    uuid = "SOSAIOT-TC-47583"
    description = show_testcase_info(Parameter.TESTPLAN, '366', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '366')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_edit_dhcp_remote_gateway(self):
       
          edit_remotegw= {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.1',
            'management_ip': '0.0.0.0',
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2'
           
            }

          response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
          response1 = dhcp_settings.show_dhcpovervpn_remote()
          Assertion.assert_regular(json.dumps(response1), '"relay_ip": "10.0.0.1"', 'ERR:failed to edit Relay IP Address in Remote Gateway')
                  

class dhcp_03(Test):
    uuid = "SOSAIOT-TC-47584"
    description = show_testcase_info(Parameter.TESTPLAN, '696', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '696')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
    def test_edit_dhcp_central_gateway(self):
       
          edit_central= {
            'internal_dhcp': True,
            'global_vpn': False,
            'remote': True,
            'relay_ip': '10.0.0.7',
            'send_requests': False,
            
            }

          response = dhcp_settings.config_dhcpvpn_centralgw(**edit_central)
          response1 = dhcp_settings.show_dhcpovervpn_central()
          Assertion.assert_regular(json.dumps(response1), '"relay_ip": "10.0.0.7"', 'ERR:failed to edit Relay IP Address in Central gateway')


class dhcp_04(Test):
    uuid = "SOSAIOT-TC-47585"
    description = show_testcase_info(Parameter.TESTPLAN, '748', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '748')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
              
    def test_edit_dhcp_remote_gateway(self):
       
          edit_remotegw= {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.1',
            'management_ip': '10.0.0.2',
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2',
         
            }

          response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
          response1 = dhcp_settings.show_dhcpovervpn_remote()
          Assertion.assert_regular(json.dumps(response1), '"management_ip": "10.0.0.2"', 'ERR:failed to create Management IP Address in Remote Gateway.')
             
             
class dhcp_05(Test):
    uuid = "SOSAIOT-TC-47586"
    description = show_testcase_info(Parameter.TESTPLAN, '755', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '755')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_edit_dhcp_central_gateway(self):
       
          edit_central= {
            'internal_dhcp': True,
            'global_vpn': False,
            'remote': True,
            'relay_ip': '0.0.0.0',
            'send_requests': True,
           
            }

          response = dhcp_settings.config_dhcpvpn_centralgw(**edit_central)
          response1 = dhcp_settings.show_dhcpovervpn_central()
          Assertion.assert_regular(json.dumps(response1), '"send_requests": true', 'ERR:failed to enable Send DHCP requests  in Central gateway')
          

class dhcp_06(Test):
    uuid = "SOSAIOT-TC-47588"
    description = show_testcase_info(Parameter.TESTPLAN, '764', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '764')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
              
    def test_edit_dhcp_remote_gateway(self):
       
          edit_remotegw= {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.1',
            'management_ip': '10.0.0.3',
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2',
         
            }

          response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
          response1 = dhcp_settings.show_dhcpovervpn_remote()
          Assertion.assert_regular(json.dumps(response1), '"management_ip": "10.0.0.3"', 'ERR:failed to edit Management IP Address in Remote Gateway')
          

class dhcp_07(Test):
    uuid = "SOSAIOT-TC-47587"
    description = show_testcase_info(Parameter.TESTPLAN, '758', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '758')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_edit_dhcp_remote_gateway(self):
       
          edit_remotegw= {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.1',
            'management_ip': '0.0.0.0',
            'block_spoof': True,
            'temp_lease': False,
            'lease_time': '2'
           
            }

          response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
          response1 = dhcp_settings.show_dhcpovervpn_remote()
          Assertion.assert_regular(json.dumps(response1), '"bound_to": "X0"', 'ERR:failed to Create DHCP with lease bound to interface X0 in Remote Gateway')
                            

class dhcp_08(Test):
    uuid = "SOSAIOT-TC-47589"
    description = show_testcase_info(Parameter.TESTPLAN, '768', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '768')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_edit_dhcp_remote_gateway(self):
       
          edit_remotegw= {
            'bound_to': 'X0',
            'relay_ip': '10.0.0.1',
            'management_ip': '0.0.0.0',
            'block_spoof': True,
            'temp_lease': True,
            'lease_time': '2'
           
            }

          response = dhcp_settings.config_dhcpvpn_remotegw(**edit_remotegw)
          response1 = dhcp_settings.show_dhcpovervpn_remote()
          Assertion.assert_regular(json.dumps(response1), '"block_spoof": true, "temp_lease": true, "lease_time": 2', 'ERR:failed to enable block_spoof and temp_lease in remote gateway')
            
        
