import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] +'/User/Guest_Admin')
from definition.settings import *
from lib.ui_group import *

#Check default group "Guest Administrors"
class Guest_admin_01(Test):
  uuid = "SOSAIOT-TC-76100"
  description = show_testcase_info(Parameter.TESTPLAN, '1', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  def test_get_groups(self):
    show_groups = guest_admin.show_local_groups()
    Assertion.assert_regular(json.dumps(show_groups), '"name": "Guest Administrators"','err: Failed to get Guest Admin')
    
#Add a group then include it in "Guest Administrators"
class Guest_admin_02(Test):
  uuid = "SOSAIOT-TC-76107"
  description = show_testcase_info(Parameter.TESTPLAN, '2', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_create_group(self):
    
    group_json = {
      
      'action': 'add',
      'grouptype': 'locally_only',
      'groupname': 'group3',
        
    }
    post_resp = guest_admin.local_group(**group_json)
    get_resp = guest_admin.show_local_groups()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "group3"', 'err: group2 not created')
 
  def test_add_group2(self):
    member = {
      'action': 'add',
      'groupname': 'Guest Administrators',
      'domain': 'any',
      'member_of': ['group3']
        
    }
    post_resp = guest_admin.group_member_of(**member)
    get_resp = guest_admin.show_local_group_by_name('Guest Administrators')
    Assertion.assert_regular(json.dumps(get_resp),'"name": "Guest Administrators"', 'err: group2 not added to Limited Administrators ')
    Assertion.assert_not_regular(json.dumps(get_resp), '"msg": "For Guest Administrators,only delete member is allowed."', 'err: user_test1 not created')
    
#Add a local user with "Guest Adminisrator", test functionality
class Guest_admin_03(Test):
  uuid = "SOSAIOT-TC-76109"
  description = show_testcase_info(Parameter.TESTPLAN, '3', description=True)['title']
  
  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '3')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_01_create_user(self):
    user_json = {
      'action': 'add',
      'username': 'test_user1',
      'userpassword': 'S0nic@uto',
      'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators']
        
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
    Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')
    
#Negative test: try to add a local user with " Guest Admin" and other admin priveledge (limit, read-only)  
class Guest_admin_04(Test):
  uuid = "SOSAIOT-TC-76110"
  description = show_testcase_info(Parameter.TESTPLAN, '4', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '4')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_01_create_user(self):
    
    user_json = {
      'action': 'add',
      'username': 'test_user2',
      'userpassword': 'S0nic@uto',
      'member_of': ['Limited Administrators','Guest Administrators','SonicWALL Read-Only Admins']
        
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_not_regular(json.dumps(get_resp), '"name": "test_user2"', 'err: user_test1 not created')
    
#Edit and delete "Guest Administrator" user(remove/add previledges) 
class Guest_admin_05(Test):
  uuid = "SOSAIOT-TC-76111"
  description = show_testcase_info(Parameter.TESTPLAN, '5', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '5')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  def test_01_create_user(self):
    
    user_json = {
      'action': 'edit',
      'username': 'test_user1',
      'userpassword': 'S0nic@uto',
      'member_of': ['Trusted Users', 'Everyone', 'Guest Administrators','Limited Administrators'] 
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_not_regular(json.dumps(get_resp), '"name": "Limited Administrators"', 'err: user_test1 not created')
    Assertion.assert_not_regular(json.dumps(get_resp), '"msg": "Note that it is not allowed that a user with guest administrator in any other group"', 'err: user_test1 not created')
    
  def test_02_create_user(self):
    user_json = {
      'action': 'edit',
      'username': 'test_user1',
      'userpassword': 'S0nic@uto',
      'member_of': ['Trusted Users', 'Everyone']   
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user1"', 'err: user_test1 not created')
    Assertion.assert_not_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: user_test1 not created')
    

#Function test on guest admin can login/manage FW via LAN interface    
class Guest_admin_06(Test):
  uuid = "SOSAIOT-TC-76112"
  description = show_testcase_info(Parameter.TESTPLAN, '6', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '6')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  #User with guest admin permission
  def test_01_create_user(self):
    
    user_json = {
      'action': 'add',
      'username': 'test1',
      'userpassword': 'S0nic@uto',
      'member_of': ['Guest Administrators']
        
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "test1"', 'err: test1 not created')
    Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: test1 not created')
    

  def test_02_login(self):
    dict1 = {
      'if': 'X0',
      'zone': 'LAN',
      'mgmt_https':True,
      'user_https': True,
      'ip': '192.168.168.168',
      "netmask": "255.255.255.0",
      "gateway": "0.0.0.0"            
    }
    
    post_resp = configure_user.config_interface(**dict1)
    resp_get = configure_user.get_interface_status('X0')
    Assertion.assert_regular(json.dumps(resp_get), '"https": true', "err:failed")
    
    
  def test_03_login(self):
    guest_user= users.UserLoginApi(headers, '192.168.168.168', 'test1', 'S0nic@uto')
    is_auth,guest_users= guest_user.local_user_login()
    Assertion.assert_equal(is_auth, True ,'err:Login failed')
    
    
    
#Check guest admin info inTSR 
class Guest_admin_07(Test):
  uuid = "SOSAIOT-TC-76101"
  description = show_testcase_info(Parameter.TESTPLAN, '10', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '10')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_add_user(self):
    member = {
      
      'action': 'add',
      'username': 'test_user2',
      'password': 'S0nic@uto',
      'member_of': ['Guest Administrators']
    }
    post_resp = guest_admin.local_user(**member)
    get_resp = guest_admin.show_local_user_by_name('test_user2')
    Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: test_user1 not added')

    output = diagnostic.download_tsr()
    with open('/tmp/techSupport', 'r') as tsr:
      doc = tsr.read()
      flag = True if re.search('Guest Administrators[\S\n ]+Members:.*test_user2', doc) else False
      Assertion.assert_equal(flag, True, "ERR: group1 config is incorrect")
      os.remove('/tmp/techSupport')
      
#Verify that related guest admin settings are intact after FW restart 
class Guest_admin_08(Test):
  uuid = "SOSAIOT-TC-76102"
  description = show_testcase_info(Parameter.TESTPLAN, '12', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '12')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_01_add_guest(self):
    
    member = {
      
      'action': 'add',
      'username': 'test_user3',
      'password': 'S0nic@uto',
      'member_of': ['Guest Administrators']
    }
    resp = guest_admin.local_user(**member)
    resp1 = guest_admin.show_local_user_by_name('test_user3')
    Assertion.assert_regular(json.dumps(resp1), '"name": "Guest Administrators"', 'err: test_user3 not added')
    Assertion.assert_regular(json.dumps(resp1), '"name": "test_user3"', 'err: test_user3 not added')
    
  def test_02_restart(self):
    
    member1 = {
      'action':'edit',
      'username':'test_user3',
      'password' :'S0nic@uto',
      'member_of':['Guest_Administrators','Trusted Users']
      
    }
    post_resp = guest_admin.local_user(**member1)
    get_resp = guest_admin.show_local_user_by_name('test_user3')
    Assertion.assert_regular(json.dumps(get_resp), '"name": "Trusted Users"', 'err: test_user3 not added')
    output = reboot_sys.restart_now()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user3"', 'err: test_user3 not added')
    
#Login guest admin via HTTP then manage FW 
class Guest_admin_09(Test):
  uuid = "SOSAIOT-TC-76103"
  description = show_testcase_info(Parameter.TESTPLAN, '15', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '15')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_01_user(self):
    
    user_json = {
      'action':'add',
      'username':'test_user4',
      'userpassword':'S0nic@uto',
      'member_of': ['Guest Administrators']
    }
    post_resp = guest_admin.local_user(**user_json)
    get_resp = guest_admin.show_local_users()
    Assertion.assert_regular(json.dumps(get_resp), '"name": "test_user4"', 'err: test1 not created')
    Assertion.assert_regular(json.dumps(get_resp), '"name": "Guest Administrators"', 'err: test1 not created')
    
  def test_02_http(self):
    dict1 = {
      'if': 'X0',
      'zone': 'LAN',
      'mgmt_https': True,
      'user_http': True,
      'user_https': False,
      'ip': '192.168.168.168',
      "netmask": "255.255.255.0",
      "gateway": "0.0.0.0"            
    }
    
    post_resp = configure_user.config_interface(**dict1)
    resp_get = configure_user.get_interface_status('X0')
    Assertion.assert_regular(json.dumps(resp_get), '"http": True', "err:failed")
    
  def test_03_login(self):
    guest_user= users.UserLoginApi(headers, '192.168.168.168', 'test1', 'S0nic@uto')
    is_auth,guest_users= guest_user.local_user_login()
    Assertion.assert_equal(guest_users, False ,'err:Login failed')
 
 
#Login guest admin via HTTPS then manage FW     
class Guest_admin_10(Test):
  uuid = "SOSAIOT-TC-76104"
  description = show_testcase_info(Parameter.TESTPLAN, '16', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '16')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_01_https(self):
    dict1 = {
      'if': 'X0',
      'zone': 'LAN',
      'mgmt_https': True,
      'user_http': False,
      'user_https': True,
      'ip': '192.168.168.168',
      "netmask": "255.255.255.0",
      "gateway": "0.0.0.0"            
    }
    
    resp = configure_user.config_interface(**dict1)
    resp_get = configure_user.get_interface_status('X0')
    Assertion.assert_regular(json.dumps(resp_get), '"https": True', "err:failed")
    
  def test_02_login(self):
    guest_user= users.UserLoginApi(headers, '192.168.168.168', 'test_user4', 'S0nic@uto')
    is_auth,guest_users= guest_user.local_user_login()
    Assertion.assert_equal(is_auth, True ,'err:Login failed')
    
    
#Login guest admin in non configured mode then try to configure/edit  
 
class Guest_admin_11(Test):
  uuid = "SOSAIOT-TC-76106"
  description = show_testcase_info(Parameter.TESTPLAN, '18', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '18')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
        
  @repeat_method(3)
  def test_01_login(self):
    static_client.send_command('pkill firefox')
    time.sleep(30)
    url = "https://13.0.0.10"
    cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/Guest_Admin/lib/ui_group.py ' + \
              '-url ' + url + ' -user admin -pwd S0nic@uto'
    out = static_client.send_command(cmd)
    time.sleep(30)
    logger.info("login with user\n" + out)
    
  def test_02_login(self):
    Guest_usr1= users.UserLoginApi(headers, '192.168.168.168', 'test_user4', 'S0nic@uto')
    is_auth,bearer_token = Guest_usr1.local_user_login()
    dict1 = {
      "name": "guest1",
      "password": "S0nic@uto",
      "bearer_token": bearer_token   
    }
    add_guest_acc = Guest_usr1.add_local_user_account(**dict1)
    Assertion.assert_equal(add_guest_acc, False ,'err:Login failed')    
    

#Login guest admin in configured mode then try to configure/edit 
class Guest_admin_12(Test):
  uuid = "SOSAIOT-TC-76105"
  description = show_testcase_info(Parameter.TESTPLAN, '17', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '17')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_login_guestadmin01(self):
    guest_user= users.UserLoginApi(headers, '192.168.168.168', 'test1', 'S0nic@uto')
    is_authenticated, bearer_token = guest_user.local_user_login()
    
    kwargs = {
      "name": "sup",
      "password": "S0nic@uto",
      "bearer_token": bearer_token
    }  
    add_guest_acc = guest_user.add_guest_user_account(**kwargs)
    Assertion.assert_equal(add_guest_acc, True ,'err:Failed to create guest account')
    

#Logout Guest Admin
class Guest_admin_13(Test):
  uuid = "SOSAIOT-TC-76108"
  description = show_testcase_info(Parameter.TESTPLAN, '22', description=True)['title']

  def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '22')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

  
  def test_logout_guestadmin(self):
    guest_user= users.UserLoginApi(headers, '192.168.168.168', 'test1', 'S0nic@uto')
    is_authenticated, bearer_token = guest_user.local_user_login()
    print(bearer_token)
    kwargs = {
      "bearer_token": bearer_token
    }
    add_guest_acc = guest_user.logout_guest_user(**kwargs)
    Assertion.assert_equal(add_guest_acc, True ,'err:Failed to create guest account')
    
    
    
    


    
    
  
  
    
    

    
    
  
    
    
  
  
  

  
  
    
    
   
    
    
    


    

    






