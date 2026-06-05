import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Radius_Users_api')
from definition.settings import *

# 	PUT User radius settings
class TC001_Radius_users(Test):
    uuid = "SOSAIOT-TC-47875"
    Stage_description = 'Put User-Radius settings'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      add_radiususer = {
        'local_users_only': False,
        'default_user_group': "",
        'timeout': 6,
        'retries': 10,
        'user_group_mechanism': {
        'radius_attribute': 'vendor-specific'
      }
      }
      response = Radius_user.user_radius_settings(**add_radiususer)
      response_get = Radius_user.show_user_radius_settings() 
      Assertion.assert_regular(json.dumps(response_get), '"local_users_only": false', 'err: Failed to create Radius user')

#GET User radius settings
class TC002_Radius_users(Test):
  uuid = "SOSAIOT-TC-47876"
  def test_get_users(self):
    Stage_description = 'Get Radius users'
    logger.info(Stage_description)
    response_get = Radius_user.show_user_radius_settings() 
    Assertion.assert_regular(json.dumps(response_get), '"local_users_only": false', 'err: Failed to get Radius user')


class TC003_Radius_users(Test):
    uuid = "SOSAIOT-TC-47877"
    Stage_description = 'POST User-Radius server'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      add_radiususer = {
        "host": "10.10.10.12",
        "enable": True,
        "port_num": 40,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      response = Radius_user.add_radius_server(**add_radiususer)
      logger.info(response) 
      response_get = Radius_user.show_radius_server() 
      Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.12"', 'err: Failed to create radius server')

class TC004_Radius_users(Test):
    uuid = "SOSAIOT-TC-47878"
    Stage_description = 'Get User-Radius'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      response_get = Radius_user.show_radius_server() 
      Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.12"', 'err: Failed to get radius server with name')


class TC005_Radius_users(Test):
    uuid = "SOSAIOT-TC-47879"
    Stage_description = 'Put Radius server using name'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      add_radiususer = {
        "host": "10.10.10.12",
        "enable": False,
        "port_num": 10,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"   
      }
      response = Radius_user.edit_radius_server(**add_radiususer)
      logger.info(response) 
      response_get = Radius_user.show_radius_server() 
      Assertion.assert_regular(json.dumps(response_get), '"port": 10', 'err: Failed to edit radius server')


class TC006_Radius_users(Test):
  uuid = "SOSAIOT-TC-47883"
  Stage_description = 'Delete Radius server by name'
  logger.info(Stage_description)
  
  def test_del_user(self):
    response = Radius_user.del_radius_server("10.10.10.12")
    response1 = Radius_user.show_radius_server()
    Assertion.assert_not_regular(json.dumps(response1), '"host": "10.10.10.12"', 'err: Failed to delete radius server with name')

class TC007_Radius_users(Test):
    uuid = "SOSAIOT-TC-47880"
    Stage_description = 'POST multiple Radius Servers'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      add_radiususer1 = {
        "host": "10.10.10.14",
        "enable": True,
        "port_num": 40,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      add_radiususer2= {
        "host": "10.10.10.15",
        "enable": True,
        "port_num": 40,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      response1 = Radius_user.add_radius_server(**add_radiususer1)
      response2 = Radius_user.add_radius_server(**add_radiususer2)
      #logger.info(response1)
      #logger.info(response2) 
      response_get = Radius_user.show_radius_server()
      Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.14"', 'err: Failed to create Radius server')
      Assertion.assert_regular(json.dumps(response_get), '"host": "10.10.10.15"', 'err: Failed to create Radius server')


class TC008_Radius_users(Test):
  uuid = "SOSAIOT-TC-47881"
  Stage_description = ''
  logger.info(Stage_description)

  def test_get_user(self):
    response1 = Radius_user.show_radius_server()
    Assertion.assert_regular(json.dumps(response1), '"host": "10.10.10.14"', "err: Failed to get radius server")

class TC009_Radius_users(Test):
  uuid = "SOSAIOT-TC-47882"
  Stage_description = 'PUT multiple radius server'
  logger.info(Stage_description)

  def test_add_radiususer(self):
      radiususer1 = {
        "host": "10.10.10.14",
        "enable": True,
        "port_num": 10,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      radiususer2= {
        "host": "10.10.10.15",
        "enable": True,
        "port_num": 20,
        "secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      response1 = Radius_user.edit_radius_server(**radiususer1)
      response_get = Radius_user.show_radius_server()
      Assertion.assert_regular(json.dumps(response_get), '"port": 10', 'err: Failed to create Radius server')
      response2 = Radius_user.edit_radius_server(**radiususer2) 
      response_get = Radius_user.show_radius_server()
      Assertion.assert_regular(json.dumps(response_get), '"port": 20', 'err: Failed to create Radius server')


class TC010_Radius_users(Test):
  uuid = "SOSAIOT-TC-47886"
  Stage_description = 'Delete Radius server by name'
  logger.info(Stage_description)
  
  def test_del_user(self):
    response = Radius_user.del_radius_server('10.10.10.14')
    response1 = Radius_user.show_radius_server()
    Assertion.assert_not_regular(json.dumps(response1), '"host": "10.10.10.14"', 'err: Failed to delete radius server with name')


class TC011_Radius_users(Test):
  uuid = "SOSAIOT-TC-47884"
  Stage_description =  'GET reporting radius statistics'
  logger.info(Stage_description)

  def test_add_radiususer(self):
      add_radiususer1 = {
        "host": "10.10.10.10",
        "enable": True,
        "port": 40,
        "shared_secret": "1234abcd",
        "send_through_vpn_tunnel": True,
        "user_name_format": "name_dot_domain"
      }
      response = Radius_user.add_radius_account(**add_radiususer1)
      Assertion.assert_equal(response, True, 'err: Failed to get radius account')

class TC012_Radius_users(Test):
  uuid = "SOSAIOT-TC-47885"
  Stage_description = 'DELETE reporting radius statistic'
  logger.info(Stage_description)

  def test_del_user(self):
    response = Radius_user.del_radius_account('10.10.10.10')
    response1 = Radius_user.show_radius_account()
    Assertion.assert_not_regular(json.dumps(response1), '"host": "10.10.10.10"', 'err: Failed to delete radius accounting')


class TC013_Radius_users(Test):
    uuid = "SOSAIOT-TC-47887"
    Stage_description = 'Attmpt to get non-existant radius server using name'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      response_get = Radius_user.show_radius_server() 
      Assertion.assert_not_regular(json.dumps(response_get), '"host": "10.10.10.20"', 'err: Failed to get radius server')


class TC014_Radius_users(Test):
    uuid = "SOSAIOT-TC-47888"
    Stage_description = 'Attempt to DELETE non-existant radius server by name'
    logger.info(Stage_description)

    def test_add_radiususer(self):
      del_serv= Radius_user.del_radius_server('10.10.10.20')
      response_get = Radius_user.show_radius_server()  
      Assertion.assert_not_regular(json.dumps(response_get), '"host": "10.10.10.20"', 'err: Failed to delete radius')






