import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke')

from definition.settings import *


class tunnelvpn_68(Test):
    uuid = "SOSAIOT-TC-47618"
    description = show_testcase_info(Parameter.TESTPLAN, '68', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '68')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn1(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_1"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_1",
            "enable": True,
            "pri_gate": "10.10.155.39",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "email_address",
            "local_ike_id": "auto_user1@gmail.com",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "0.0.0.0"
          }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"ike_id": {"local": {"email_address": "auto_user1@gmail.com"}', "err:failed Create a Tunnel Interface with Local IKE ID - E-mail Address")
          
    def test_create_tunnelvpn2(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_2"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_2",
            "enable": True,
            "pri_gate": "10.10.155.29",
            "auth_mode": "shared_secret",
            "secret": "test123",
            "local_ike_type": "firewall_id",
            "local_ike_id": "123",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.1.1.1"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), ' "ike_id": {"local": {"firewall_id": "123"}', "err:failed Create a Tunnel Interface with Local IKE ID- Firewall Identifier")
          
class tunnelvpn_70(Test):
    uuid = "SOSAIOT-TC-47619"
    description = show_testcase_info(Parameter.TESTPLAN, '70', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '70')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn3(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_3"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_3",
            "enable": True,
            "pri_gate": "10.10.155.19",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "123",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.0.0.0"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"ike_id": {"local": {"key_id": "123"}', "err:failed Create a Tunnel Interface with Local IKE ID - Key Identifier")  
          
class tunnelvpn_71(Test):
    uuid = "SOSAIOT-TC-47620"
    description = show_testcase_info(Parameter.TESTPLAN, '71', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '71')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn4(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_4"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_4",
            "enable": True,
            "pri_gate": "10.10.155.49",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "1234",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.1.0.0"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"peer": {"ipv4": "1.1.0.0"}}}}', "err:failed Create a Tunnel Interface with Peer IKE ID - IPV4 Address")               
                       
    def test_create_tunnelvpn5(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_5"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_5",
            "enable": True,
            "pri_gate": "10.10.155.59",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "121",
            "peer_ike_type": "domain_name",
            "peer_ike_id": "gmail.com"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"peer": {"domain_name": "gmail.com"}}}}', "err:failedCreate a Tunnel Interface with Peer IKE ID - domain name")
          
          
class tunnelvpn_83(Test):
    uuid = "SOSAIOT-TC-47622"
    description = show_testcase_info(Parameter.TESTPLAN, '83', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '83')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn6(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_6"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_6",
            "enable": True,
            "pri_gate": "10.10.155.9",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "12345",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.1.1.0",
            "ipsec_encryption": "des"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"encryption": {"des": true}', "err:failed Create a Tunnel Interface with the Encryption - DES in the Ipsec (Phase 2) Proposal")               
                                      
    def test_create_tunnelvpn7(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_7"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_7",
            "enable": True,
            "pri_gate": "10.10.155.69",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "112",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.1.0.1",
            "ipsec_encryption": "triple_des"
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"encryption": {"triple_des": true}', "err:failed Create a Tunnel Interface with the Encryption - 3DES in the Ipsec")               
                                                         
class tunnelvpn_93(Test):
    uuid = "SOSAIOT-TC-47623"
    description = show_testcase_info(Parameter.TESTPLAN, '93', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '93')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn8(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_8"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_8",
            "enable": True,
            "pri_gate": "10.10.155.79",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "1212",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.0.1.0",
            "ipsec_encryption": "aes_gmac_256",
            "ipsec_auth": ""
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"encryption": {"aes_gmac_256": true}', "err:failed Create a Tunnel Interface with the Encryption - AESGMAC-256")               
                                                   
class tunnelvpn_94(Test):
    uuid = "SOSAIOT-TC-47616"
    description = show_testcase_info(Parameter.TESTPLAN, '94', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '94')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")


    def test_create_tunnelvpn9(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_9"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_9",
            "enable": True,
            "pri_gate": "10.10.155.89",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "12121",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.0.1.1",
            "ipsec_auth": "md5"       
          }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"authentication": {"md5": true}', "err:failed Create a Tunnel Interface with the Authentication - MD5")            

    def test_create_tunnelvpn10(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_10"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_10",
            "enable": True,
            "pri_gate": "10.10.155.99",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "12112",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.0.0.1",
            "ipsec_auth": "sha_1"       
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"authentication": {"sha_1": true}', "err:failed Create a Tunnel Interface with the Authentication - sha1")               
                                           
class tunnelvpn_101(Test):
    uuid = "SOSAIOT-TC-47617"
    description = show_testcase_info(Parameter.TESTPLAN, '101', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '101')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_create_tunnelvpn11(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_11"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_11",
            "enable": True,
            "pri_gate": "10.10.155.109",
            "auth_mode": "shared_secret",
            "secret": "sonicwall",
            "local_ike_type": "key_id",
            "local_ike_id": "121212",
            "peer_ike_type": "ipv4",
            "peer_ike_id": "1.0.2.0",
            "bound_to": ["interface", "X0"]      
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"bound_to": {"interface": "X0"}', "err:failed Create a Tunnel Interface with VPN Policy bound to: Interface X0") 
                    
class tunnelvpn_78(Test):
    uuid = "SOSAIOT-TC-47621"
    description = show_testcase_info(Parameter.TESTPLAN, '78', description=True)['title']
    jira = 'GEN8-10188'


    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '78')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test1_create_local_cert(self):
      confPath = os.environ["PYTHON_SONICOS_HOME"] + '/VPN/IPSec/IPSec_Tunnel_Interface/Tunnel_Interface_Smoke/cert/'
      certPath = confPath + 'cert_local.pfx'
      cert_file = certificate.import_cert_local(cert_path="@" + certPath, name='local_cert_tunnel_interface', password='password')
      logger.info(cert_file)

    def test_create_tunnelvpn12(self):
       response = tunnelvpn_settings.show_tunnelvpnpolicy()
       flag = True if ('"name": "tunnel_12"' in json.dumps(response)) else False
       if flag == False:
          tunnelvpn_put= {
            "ipversion": "ipv4",
            "type": "tunnel_interface",
            "name": "tunnel_12",
            "enable": True,
            "pri_gate": "10.10.155.119",
            "auth_mode": "certificate",
            "local_cert": "local_cert_tunnel_interface",
            "local_ike_type": "default-id",
            #"local_ike_id": "1212121",
            "peer_ike_type": "distinguished_name",
            "peer_ike_id": "ou=gmail.com" 
                
      }
          response = tunnelvpn_settings.add_vpn_policy(**tunnelvpn_put)
          logger.info(response)
          response1 = tunnelvpn_settings.show_tunnelvpnpolicy()
          Assertion.assert_regular(json.dumps(response1), '"peer": {"distinguished_name": "ou=gmail.com"}}}}', "err:failed Create a Tunnel Interface Peer IKE ID - Distinguished Name(DN)")
