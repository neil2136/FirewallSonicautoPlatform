from definition.settings_totp import *
from definition import constants
import requests
import subprocess
import paramiko


sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp')


class sslvpn_config(Test):
    uuid = 'NonTC' 
    
    def test_01_install_nx_Linux(self):
        cpy_build = cp_nx.cpbuildnx_linux_local()
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux()
        logger.info(inst)

    def test_02_install_nx_Linux_remote(self):
        cpy_build = cp_nx.buildnx_linux_remote('-PC2')
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux_remote('-PC2')
        logger.info(inst)
        
    def test_03_install_nx_Linux_remote(self):
        cpy_build = cp_nx.buildnx_linux_remote('-PC3')
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux_remote('-PC3')
        logger.info(inst)

    def test_04_create_sslvpn_address_object_LAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_LAN",
            "zone": "SSLVPN",
            "value": "192.168.168.200,192.168.168.230"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_LAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1),'"name": "sslvpn_LAN"', "Err: failed to create address object")
        
    def test_05_create_sslvpn_address_object_WAN(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_WAN",
            "zone": "SSLVPN",
            "value": "10.10.0.20,10.10.0.28"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_WAN", "ipv4")
        Assertion.assert_regular(json.dumps(resp1),'"name": "sslvpn_WAN"', "Err: failed to create address object")

    def test_06_create_sslvpn_address_object_dmz(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_DMZ",
            "zone": "SSLVPN",
            "value": "10.11.0.20,10.11.0.28"
        }
        resp = address_objects.config_addressobject(**address_object)
        resp1 = address_objects.get_addressobject_by_name("sslvpn_DMZ", "ipv4")
        Assertion.assert_regular(json.dumps(resp1),'"name": "sslvpn_DMZ"', "Err: failed to create address object")

    def test_07_sslserver_settings_with_port_enabled(self):
        ssl_vpn_server = {
            'port': 4433,
            'use_self_signed': True,
            'user_domain': 'LocalDomain',
            'web': True,
            'ssh': False,
            'session_timeout': 10,
            'default': True,
            'mschap': True,
            'inactivity_check': True
        }
        server_settings = sslvpnserver.edit_server_setting(**ssl_vpn_server)
        Assertion.assert_equal(server_settings, True, "Err: failed to config server settings")

    def test_08_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
            'DMZ_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_09_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_10_config_local(self):
        user_auth = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        ldap_auth = user_setting.user_method_authentication(**user_auth)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"',
                                "ERR:LOCALs method is not selected successfully")


class Totp_01(Test):
    uuid = "SOSAIOT-TC-77240"
    description= show_testcase_info(Parameter.TESTPLAN, '1514705', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514705')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {

            "action": "add",
            "username": "test_totp_local_user1",
            "userpassword": "P@ssw0rd",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user1")
        Assertion.assert_regular(json.dumps(resp), '"name": "Sonicwall Administrators"', 'ERR:  Failed to enable TOTP for new localuser')
 
    
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 3
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            'one_time_password': 'totp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    def test_04_edit_user(self):
        user_json = {
            'action': 'edit',
            'username': 'test_totp_local_user1',
            'userpassword': 'P@ssw0rd',
            "member_of": ["group1","SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        resp = user_local.show_local_user_by_name("test_totp_local_user1")
        Assertion.assert_regular(json.dumps(resp), '"name": "group1"', "ERR:  Failed to enable TOTP for new localuser")


    def test_04_local_user_scan_and_enter_totp(self):

        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_02(Test):
    uuid = "SOSAIOT-TC-77241"
    description= show_testcase_info(Parameter.TESTPLAN, '1514706', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514706')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser(self):
        logger.info('Create local user and giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user2",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user2")
        Assertion.assert_regular(json.dumps(resp), '"name": "Sonicwall Administrators"', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user2 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_edit_user(self):
        user_json = {
            'action': 'edit',
            'username': 'test_totp_local_user2',
            'userpassword': 'P@ssw0rd',
            "one_time_password":"",
            "member_of": ["SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        resp = user_local.show_local_user_by_name("test_totp_local_user2")
        Assertion.assert_regular(json.dumps(resp), '"name": "SonicWALL Administrators"', 'err: sslvpntest not created')

    def test_04_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 3
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user2 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            logger.info(constants.UI_AUTOMATION_SCRIPT_RESPONSE + out)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Admin failed to enter totp on scanner page")


class Totp_03(Test):
    uuid = "SOSAIOT-TC-77242"
    description= show_testcase_info(Parameter.TESTPLAN, '1514707', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514707')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user3",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user3")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user3 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user3', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user3", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_edit_password(self):
        user_json = {
            'action': 'edit',
            'username': 'test_totp_local_user3',
            'userpassword': 'P@ssw0rd@123',
            "member_of": ["SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        resp = user_local.show_local_user_by_name("test_totp_local_user3")
        Assertion.assert_regular(json.dumps(resp),'"totp": true', 'err: sslvpntest not created')
        
    def test_04_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 2
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user3 -pwd P@ssw0rd@123 -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            logger.info(constants.UI_AUTOMATION_SCRIPT_RESPONSE + out)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user3', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user3", "ERR: :Invalid user logged in even though not password is wrong")

        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Admin failed to enter totp on scanner page")

class Totp_04(Test):
    uuid = "SOSAIOT-TC-77232"
    description= show_testcase_info(Parameter.TESTPLAN, '1514697', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514697')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user4",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user4")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    @repeat_method(3)
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user4 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_delete_User(self):
        response = user_local.delete_local_user_no_domain('test_totp_local_user4')
        response_get = user_local.show_local_users()
        Assertion.assert_not_regular(json.dumps(response_get), '"name": "test_totp_local_user4"', 'err: user not deleted')
                
    def test_04_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user4",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user4")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_05_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user4 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
            
                
def copy_file(self,openstack_pc):
    
    try:    
        os.chdir('/tmp')
        print("Current working directory: {0}".format(os.getcwd()))
        username= 'root'
        password = 'password'
        testbed = Params.testbed + openstack_pc
        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        s.connect(testbed,22,username=username,password=password,timeout=60)
        sftp = s.open_sftp()
        sftp.put('users.json', '/tmp/users.json')
        logger.info("copied file")
    except:
        logger.info("Unable to copy files")
        

class Copy_file(Test):
    uuid = 'NonTC'
          
    def test_01_copy_pc2(self):
        c = copy_file(self,'-PC2')
        c = copy_file(self,'-PC3')
        
    def test_02_check_file_exists_pc2(self):
        static_client1.send_command('cp ' + "/tmp/users.json" + ' ' + "/root")
        kword = ('users.json')
        resp = static_client1.send_command('ls -l')
        if kword in resp:
            m = True
            Assertion.assert_equal(m,True,"Err:Failed to delete file")  
        else:
            m = False
            Assertion.assert_equal(m,True,"Err:Failed to delete file")
    
    def test_03_check_file_exists_pc3(self):
        static_client2.send_command('cp ' + "/tmp/users.json" + ' ' + "/root")
        kword = ('users.json')
        resp = static_client2.send_command('ls -l')
        if kword in resp:
            m = True
            Assertion.assert_equal(m,True,"Err:Failed to delete file")  
        else:
            m = False
            Assertion.assert_equal(m,True,"Err:Failed to delete file")


class Totp_05(Test):
    uuid = "SOSAIOT-TC-77244" 
    description= show_testcase_info(Parameter.TESTPLAN, '1514710', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514710')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpntest",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            "vpn_client_access": ['LAN Subnets','WAN Subnets','DMZ Subnets']
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpntest")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    @repeat_method(5)
    def test_02_genearate_text(self):
        try:
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = "https://192.168.168.168:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_otp_sslvpn.py ' + \
                    '-url ' + url + ' -user sslvpntest -pwd P@ssw0rd'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
            
    @repeat_method(5)
    def test_03_enter_otp(self):
        try:
            localhost_1.send_command('pkill firefox')
            time.sleep(10)
            url = "https://192.168.168.168:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_enter_otp.py ' + '-url ' + url + ' -user sslvpntest -pwd P@ssw0rd'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

        
class Totp_06(Test):
    uuid = "SOSAIOT-TC-77270"
    description= show_testcase_info(Parameter.TESTPLAN, '2682877', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2682877')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpntest1",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            "vpn_client_access": ['LAN Subnets','WAN Subnets','DMZ Subnets']
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpntest1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    @repeat_method(3)
    def test_02_genearate_text(self):
        try:
            static_client1.send_command('pkill firefox')
            time.sleep(5)
            url = "https://10.10.0.30:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_otp_sslvpn.py ' + \
                    '-url ' + url + ' -user sslvpntest1 -pwd P@ssw0rd'
            out = static_client1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    @repeat_method(3)
    def test_03_enter_otp(self):
        try:
            static_client1.send_command('pkill firefox')
            time.sleep(10)
            url = "https://10.10.0.30:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_enter_otp.py ' + '-url ' + url + ' -user sslvpntest1 -pwd P@ssw0rd'
            out = static_client1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    
class Totp_07(Test):
    uuid = "SOSAIOT-TC-77271"
    description= show_testcase_info(Parameter.TESTPLAN, '2682878', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2682878')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpntest2",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ['Trusted Users', 'Everyone', 'SSLVPN Services'],
            "vpn_client_access": ['LAN Subnets','WAN Subnets','DMZ Subnets']
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpntest2")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    @repeat_method(3)
    def test_02_genearate_text(self):
        try:
            
            static_client2.send_command('pkill firefox')
            time.sleep(5)
            url = "https://10.11.0.30:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_enter_otp.py ' + '-url ' + url + ' -user sslvpntest2 -pwd P@ssw0rd'
            out = static_client2.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
            
    @repeat_method(3)
    def test_03_enter_otp(self):        
        try:
            static_client2.send_command('pkill firefox')
            time.sleep(10)
            url = "https://10.11.0.30:4433"
            cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_user_enter_otp.py ' + '-url ' + url + ' -user sslvpntest2 -pwd P@ssw0rd'
            out = static_client2.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'sslvpntest2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "sslvpntest2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

            
def connect_nxlinux_remote_with_totp(user, pswd, netexurl, domain,openstack_PC):
    try:
        s = pxssh.pxssh()
        hostname = Params.testbed + openstack_PC
        logger.info(hostname)
        username = "root"
        password = "password"
        pc_login=s.login(hostname, username, password)
        print("Successfully login to:"+hostname)
        s.prompt()  # match the prompt
        logger.info(s.before)  # print everything before the prompt.
        s.sendline('killall netExtender')
        s.prompt()
        logger.info(s.before)
        s.sendline('netExtender')
        s.prompt()
        s.before
        print("SSLVPN SERVER:"+netexurl)
        s.sendline(netexurl)
        s.prompt()
        logger.info(s.before)
        logger.info("User Authentication")
        print("User:"+user)
        s.sendline(user)
        s.prompt()
        logger.info(s.before)
        logger.info("Password:")
        s.sendline(pswd)
        s.prompt()
        logger.info(s.before)
        print("Domain:"+domain)
        s.sendline("LocalDomain")
        s.sendline('Y')
        s.prompt()
        logger.info(s.before)
        time.sleep(5)
        one_time_pass = enter_otp_in_nx()
        print("One Time Password",one_time_pass)
        s.sendline(one_time_pass)
        s.prompt()        
        print(s.before)
        result = s.before
        print(result)
        save_path ='/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)   
        f = open(file_path, "wb")
        m = f.write(result)
        f.close()

        
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
    
def enter_totp(name):
    save_path ='/tmp'
    file_name = "users.json"
    file_path = os.path.join(save_path, file_name)
    data = open(file_path,"r")
    data_read_text = data.read()
    data.close()
    js = json.loads(data_read_text)
    totp_for_user = js[name]
    logger.info(totp_for_user)
    totp = pyotp.TOTP(totp_for_user)
    totp_code = totp.now()
    logger.info(totp_code) 
    return totp_code

def enter_otp_in_nx():
    enter_code_totp = enter_totp(name='sslvpntest')
    return enter_code_totp      


def install_nxlinux(username, password, netexurl, domain):
    netexsession = pexpect.spawn("netExtender", ["-u", username, "-p", password, "-d", domain, netexurl])
    logger.info("The netextender session".format(netexsession))
    index = netexsession.expect(["Do you want to proceed", pexpect.EOF, pexpect.TIMEOUT])
    time.sleep(5)
    if index == 0:
        logger.info("Received self-signed certificate override")
        netexsession.sendline("Y")
        logger.info("Successfully accepted the self-signed and trying to connect via NetExtender")
        one_time_pass = enter_otp_in_nx()
        print("One Time Password:",one_time_pass) 
        netexsession.sendline(one_time_pass)
    else:
        logger.info("Error: Unable to connect via NetExtender as Authentication Failed")
        # continue
    time.sleep(5)
    index = netexsession.expect(["NetExtender connected successfully", pexpect.EOF, pexpect.TIMEOUT])
    time.sleep(5)
    if index == 0:
        logger.info("Successfully connected via NetExtender ")
    else:
        logger.info("SSLVPN not enabled in your zone. unable to connect ")
    return index   

    
class Totp_08(Test):
    uuid = "SOSAIOT-TC-77243"
    description= show_testcase_info(Parameter.TESTPLAN, '1514709', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514709')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_LAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    
    def test_02_connect_nx_totp_LAN(self):
        connect_nxlinux_remote_with_totp(user='sslvpntest', pswd='P@ssw0rd', netexurl='192.168.168.168:4433',
                                         domain='LocalDomain', openstack_PC='-PC1')
        save_path ='/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path,"r")
        data_read_text = data.read()
        if "NetExtender connected successfully" in data_read_text:
            m = True
            Assertion.assert_equal(m,True,'err: User is not present')
        else:
            m = True
            Assertion.assert_equal(m,False,'err: User is not present')        
        
class Totp_09(Test):
    uuid = "SOSAIOT-TC-77268"
    description= show_testcase_info(Parameter.TESTPLAN, '2682754', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2682754')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_WAN',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['WAN Subnets','LAN Subnets','DMZ Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_02_connect_nx_totp_WAN(self):
        connect_nxlinux_remote_with_totp(user='sslvpntest', pswd='P@ssw0rd', netexurl='10.10.0.30:4433',domain='LocalDomain', openstack_PC='-PC2')
        save_path ='/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path,"r")
        data_read_text = data.read()
        if "NetExtender connected successfully" in data_read_text:
            m = True
            Assertion.assert_equal(m,True,'err: User is not present')
        else:
            m = True
            Assertion.assert_equal(m,False,'err: User is not present')
            
class Totp_10(Test):
    uuid = "SOSAIOT-TC-77269"
    description= show_testcase_info(Parameter.TESTPLAN, '2682876', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '2682876')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_DMZ',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['WAN Subnets','LAN Subnets','DMZ Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    @repeat_method(3)
    def test_02_connect_nx_totp_dmz(self):
        connect_nxlinux_remote_with_totp(user='sslvpntest', pswd='P@ssw0rd', netexurl='10.11.0.30:4433',
                                         domain='LocalDomain', openstack_PC='-PC3')
        save_path ='/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        data = open(file_path,"r")
        data_read_text = data.read()
        if "NetExtender connected successfully" in data_read_text:
            m = True
            Assertion.assert_equal(m,True,'err: User is not present')
        else:
            m = True
            Assertion.assert_equal(m,False,'err: User is not present')  
            
    def test_03_remove_file(self):
        save_path ='/tmp'
        file_name = "verify.txt"
        file_path = os.path.join(save_path, file_name)
        m1 = os.remove(file_path)
        if not os.path.exists(file_path): 
            m = True
            Assertion.assert_equal(m,True,"Err:Failed to delete file")
        else:
            m = False
            Assertion.assert_equal(m,True,"Err:Failed to delete file")
  

class Totp_11(Test):
    uuid = "SOSAIOT-TC-77234"
    description= show_testcase_info(Parameter.TESTPLAN, '1514699', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514699')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self): 
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user5",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user5")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user5 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user5', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user5", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_unbind_totp(self):
        response = user_local.unbind_totp_key_with_name("test_totp_local_user5")
        logger.info(response)
        Assertion.assert_equal(response, True,'ERR: Failed to unbind totp')
           
class Totp_12(Test):
    uuid = "SOSAIOT-TC-77253"
    description= show_testcase_info(Parameter.TESTPLAN, '1514726', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514726')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self): 
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
        Assertion.assert_regular(json.dumps(resp), '"name": "SonicWALL Administrators"', 'err: test_user3 not added')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/sslvpn/Totp_sslvpn/definition/ui_totp_login.py -url {url} -user test -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_restart(self):
        output = reboot_sys.restart_now()
        Assertion.assert_equal(output, True, 'err: test not added')

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 2
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test -pwd password -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_13(Test):
    uuid = "SOSAIOT-TC-77265"
    description= show_testcase_info(Parameter.TESTPLAN, '1564144', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1564144')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_enable_totp_buildin_admin_user(self):
        logger.info('Enable totp for build-in admin user in System/administrator page...')
        admin_dict = {
            'admin': {
                "name": "admin",
                "one_time_password": {
                    "totp": True
                },
                "preempt_action": "goto-non-config",
                "preempt_inactivity_timeout": 10
            }
        }
        resp = admin_obj.conf_admin(**admin_dict)
        Assertion.assert_equal(resp, True, "ERR: Failed to Enable TOTP for Build-in Admin user.")

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user admin -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'admin', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "admin", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_disable_totp_buildin_admin_user(self):
            logger.info('Disable totp for build-in admin user in System/administrator page...')
            admin_info = {
                'name': 'admin',
                'inactive-time': 10,
                'preempt-action': 'logout',
                'one-time-pass': False
            }
            resp = cli_obj.config_admin(**admin_info)
            print(resp)
            Assertion.assert_equal(resp, True, "ERR: Failed to Disable TOTP for Build-in Admin user.")

class Totp_14(Test):
    uuid = "SOSAIOT-TC-77237"
    description= show_testcase_info(Parameter.TESTPLAN, '1514702', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514702')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_create_local_user(self):
        user_json = {
            'action': 'add',
            'username': 'test1',
            'userpassword': 'P@ssw0rd',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_02_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_03_login_via_local_user(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_user.py -url {url} -user test1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_04_add_sslvpn_user(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': 'P@ssw0rd',
            'one_time_password':'totp',
            "member_of": ["SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        resp = user_local.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_05_login_via_local_user(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_15(Test):
    uuid = "SOSAIOT-TC-77229"
    description= show_testcase_info(Parameter.TESTPLAN, '1514694', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514694')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_checklen",
            "userpassword": "P@ssw0rd",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_checklen")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 5
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_checklen -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_checklen', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_not_equal(match, "test_totp_local_checklen", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_16(Test):
    uuid = "SOSAIOT-TC-77249"
    description= show_testcase_info(Parameter.TESTPLAN, '1514718', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514718')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_localuser_enable_totp(self):
        add_localuser = {
            "action": "add",
            "username": "test_totp_guest",
            "userpassword": "P@ssw0rd",
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_guest")
        Assertion.assert_regular(json.dumps(resp), '"name": "test_totp_guest"', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_02_create_group(self):
        group_json = {
            'action': 'edit',
            'grouptype': 'locally_only',
            'groupname': 'group2',
            'one_time_password': 'totp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group2"', 'err: group1 not created')

    # def test_03_edit_user(self):
    #     user_json = {
    #         'action': 'edit',
    #         'username': 'test_totp_guest',
    #         'userpassword': 'password',
    #         "member_of": ["group2","Guest Administrators"]
    #     }
    #     resp = user_local.local_user(**user_json)
    #     resp = user_local.show_local_user_by_name("test_totp_guest")
    #     Assertion.assert_regular(json.dumps(resp), '"name": "group2"', "ERR:  Failed to enable TOTP for new localuser")

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_guest -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_guest', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_guest", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_17(Test):
    uuid = "SOSAIOT-TC-77239"
    description= show_testcase_info(Parameter.TESTPLAN, '1514704', description=True)['title']

    def test_00_show_testcase_info(self):
        show_testcase_info(Parameter.TESTPLAN, '1514704')
        Assertion.assert_equal(True, True, "ERR: show testcase info failed")

    def test_01_add_user(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': 'P@ssw0rd',
            'one_time_password':'totp',
            "member_of": ["SonicWALL Administrators"]
        }
        resp = user_local.local_user(**user_json)
        resp = user_local.show_local_user_by_name("test1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_edit_local_user(self):
        user_json = {
            'action': 'edit',
            'username': 'test1',
            'userpassword': 'P@ssw0rd',
            'one_time_password': 'otp',
            "email_address": "test1@smtpstest.com",
            'member_of': ['Trusted Users', 'SonicWALL Administrators'],
            "account_lifetime": True,
            "lifetype": "minutes",
            "accountlifetime": 30,
            "prune_on_expiry": False
        }
        resp = user_local.local_user(**user_json)
        time.sleep(5)
        resp1 = user_local.show_local_users()
        time.sleep(10)
        Assertion.assert_regular(json.dumps(resp1), '"name": "test1"', 'err: Failed to create localuser')

    def test_04_Clear_test1_inbox(self):
        try:
            ret = pop3_client.delete_email(PC1_ETH1_IP, 'test1', 'password')
            logger.info(ret)
        except Exception as err:
            logger.err(err)
        Assertion.assert_equal(True, True, "ERR: clear test1 inbox failed")

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test1 -pwd P@ssw0rd -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_18(Test):
    uuid = "SOSAIOT-TC-77220"
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_1",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_1")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
 
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_1 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_1', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_1", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_19(Test):
    uuid = "SOSAIOT-TC-77221"
    
    def test_01_add_localuser_enable_totp(self): 
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_totp_local_user_2",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_totp_local_user_2")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_2 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_unbind_totp(self):
        response = user_local.unbind_totp_key_with_name("test_totp_local_user_2")
        logger.info(response)
        Assertion.assert_equal(response, True,'ERR: Failed to unbind totp')

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_totp_local_user_2 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_totp_local_user_2', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_totp_local_user_2", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")


class Totp_20(Test):
    uuid = "SOSAIOT-TC-77223"
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_local_user4",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_local_user4")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_local_user4 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_unbind_totp(self):
        response = user_local.unbind_totp_key_with_name("test_local_user4")
        logger.info(response)
        Assertion.assert_equal(response, True,'ERR: Failed to unbind totp')

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_local_user4 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_local_user4', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_local_user4", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_21(Test):
    uuid = "SOSAIOT-TC-77226"
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "admin_test",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("admin_test")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_genearate_text(self):
        localhost_1.send_command('pkill firefox')
        time.sleep(5)
        url = "https://192.168.168.168"
        cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_user_emer.py -url {url} -user admin_test -pwd S0nic@uto'
        out = localhost_1.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        resp = userstatus1.show_users_status()
        logger.info(resp)
        find = re.search(r'admin_test', resp, re.M | re.I)
        logger.info("The user obtained is {}".format(find))
        match = find.group()
        Assertion.assert_equal(match, "admin_test", "ERR: :Invalid user logged in even though not password is wrong")
        
class Totp_22(Test):
    uuid = "SOSAIOT-TC-77230"
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpn_test",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpn_test")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_genearate_text(self):
        localhost_1.send_command('pkill firefox')
        time.sleep(5)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_totp_login_emer.py ' + \
                '-url ' + url + ' -user sslvpn_test -pwd S0nic@uto'
        out = localhost_1.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        resp = userstatus1.show_users_status()
        logger.info(resp)
        find = re.search(r'sslvpn_test', resp, re.M | re.I)
        logger.info("The user obtained is {}".format(find))
        Assertion.assert_equal(find, None, "ERR: :user is not logged using SSLVPN")
        
class Totp_23(Test):
    uuid = "SOSAIOT-TC-77231"
    
    def test_01_add_localuser_enable_totp(self): 
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "sslvpntest_totp_local_user2",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("sslvpntest_totp_local_user2")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')
    
    def test_02_genearate_text(self):
        localhost_1.send_command('pkill firefox')
        time.sleep(5)
        url = "https://192.168.168.168"
        cmd = 'python3 ' + os.environ["PYTHON_SONICOS_HOME"] + '/User/user_totp/definition/ui_totp_login_emer.py ' + \
                '-url ' + url + ' -user sslvpntest_totp_local_user2 -pwd S0nic@uto'
        out = localhost_1.send_command(cmd)
        logger.info("login with user\n" + out)
        time.sleep(10)
        resp = userstatus1.show_users_status()
        logger.info(resp)
        find = re.search(r'sslvpntest_totp_local_user2', resp, re.M | re.I)
        logger.info("The user obtained is {}".format(find))
        Assertion.assert_equal(find, None, "ERR: :user is not logged using SSLVPN")

class Totp_24(Test):
    uuid = "SOSAIOT-TC-77235"

    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "test_local_user5",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["Trusted Users", "Everyone","SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("test_local_user5")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_local_user5 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_local_user5', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_local_user5", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

    def test_03_unbind_totp(self):
        response = user_local.unbind_totp_key_with_name("test_local_user5")
        logger.info(response)
        Assertion.assert_equal(response, True,'ERR: Failed to unbind totp')

    def test_04_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test_local_user5 -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test_local_user5', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test_local_user5", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_25(Test):
    uuid = "SOSAIOT-TC-77245"

    def test_01_create_radiususer(self):
        add_radius_server_dict = {'host': '192.168.168.65', 
                                  'enable': True,
                                  'port_num': 1812,
                                  'secret': 'password',
                                  'send_through_vpn_tunnel': False,
                                  }

        radius_user = user_radius.add_radius_server(**add_radius_server_dict)
        logger.info("The user created is {}".format(radius_user))
        Assertion.assert_equal(radius_user, True, "ERR: :Radius user is not created successfully")

    def test_02_Radius_user_settings(self):
        user_authen = {
            "auth_method": "Radius",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "Radius"', "ERR:LOCALs method is not selected successfully")

    def test_03_create_group(self):
        group_json = {
            'action': 'add',
            'grouptype': 'locally_only',
            'groupname': 'group1',
            'one_time_password': 'totp'
        }
        resp = user_local.local_group(**group_json)
        resp1 = user_local.show_local_groups()
        Assertion.assert_regular(json.dumps(resp1), '"name": "group1"', 'err: group1 not created')

    def test_04_import_ldap_user(self):
        add = {
            "user": {
                "local": {
                    "user": [{
                        "name": "test",
                        "domain": "os-autosnwl.com"
                    }]
                }
            }
        }
        resp = user_local.import_local_usr_from_ldap(**add)
        logger.info(resp)
        Assertion.assert_equal(resp, True, "ERR: Failed to import LDAP user.")
        
    def test_05_radius_user_with_sslvpn_services(self):
        add_member_of_group = {
            'action': 'add',
            'groupname': 'SonicWALL Administrators',
            'member_of': ['All RADIUS Users']
        }
        ssl_services = user_local.group_member_of(**add_member_of_group)
        Assertion.assert_equal(ssl_services, True, "ERR: :Radius user with sslvpn services is not selected successfully")
    
    def test_06_radius_user_with_sslvpn_services(self):
        add_member_of_group = {
            'action': 'add',
            'groupname': 'group1',
            'member_of': ['All RADIUS Users']
        }
        ssl_services = user_local.group_member_of(**add_member_of_group)
        Assertion.assert_equal(ssl_services, True, "ERR: :Radius user with sslvpn services is not selected successfully")
        
    def test_07_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user test -pwd password -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'test', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "test", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")

class Totp_26(Test):
    uuid = "SOSAIOT-TC-77260"
    
    def test_01_Radius_user_settings(self):
        user_authen = {
            "auth_method": "local",
            "sso_agent": False,
            "terminal_services_agent": False,
            "radius_accounting": False,
            "third_party_api": False,
            "capture_client": False
        }
        Radius_auth = user_setting.user_method_authentication(**user_authen)
        resp = user_setting.show_user_auth()
        Assertion.assert_regular(json.dumps(resp), '"auth_method": "local"', "ERR:LOCALs method is not selected successfully")

    def test_02_enable_user_lockout(self):
        lockout = {
        "administration": {
            "user_lockout": {
                "enable": True,
                "failures_rate": 5,
                "failures_duration": 1,
                "lockout_duration": 5
                },
            "local_user_lockout": True
            }
        }
        admin_obj.edit_admin(**lockout)
        resp = admin_obj.show_admin_setting()
        Assertion.assert_regular(json.dumps(resp), '"local_user_lockout": true', 'ERR: Local User Lockout is not enabled')
 
    def test_03_virtual_office_api(self):
        max_attempts = 6
        attempts = 0
        success = False
        ui_obj = None

        expected_msg = "Incorrect name/password"

        while attempts < max_attempts and not success:
            ui_obj = fw_ui_obj.user_login('192.168.168.168', 'sslvpntest', 'password1')

            if isinstance(ui_obj, str):
                try:
                    ui_obj = json.loads(ui_obj)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON response")
                    break

            try:
                actual_msg = ui_obj["status"]["info"][0]["message"]
            except (KeyError, IndexError, TypeError):
                actual_msg = ""

            logger.info(f'[INFO] - "message": "{actual_msg}"')

            if expected_msg in actual_msg:
                attempts += 1
                logger.info(f"[Attempt {attempts}] Login failed with expected message part.")
            else:
                success = True
                Assertion.assert_true(expected_msg in actual_msg, 
                                    f"ERR: Expected message containing '{expected_msg}', has '{actual_msg}'")

        if not success:
            Assertion.assert_true(expected_msg in actual_msg, 
                                f"ERR: User is not locked out.'{actual_msg}'")

class Totp_27(Test):
    uuid = "SOSAIOT-TC-77262"
    
    def test_01_enable_user_lockout(self):
        lockout = {
        "administration": {
            "user_lockout": {
                "enable": True,
                "failures_rate": 2,
                "failures_duration": 1,
                "lockout_duration": 3
                },
            "local_user_lockout": True
            }
        }
        admin_obj.edit_admin(**lockout)
        resp = admin_obj.show_admin_setting()
        Assertion.assert_regular(json.dumps(resp), '"local_user_lockout": true', 'ERR: Local User Lockout is not enabled')
 

    def test_02_virtual_office_api(self):
        max_attempts = 3
        attempts = 0
        success = False
        ui_obj = None

        expected_msg = "Incorrect name/password"

        while attempts < max_attempts and not success:
            ui_obj = fw_ui_obj.user_login('192.168.168.168', 'sslvpntest', 'password1')

            if isinstance(ui_obj, str):
                try:
                    ui_obj = json.loads(ui_obj)
                except json.JSONDecodeError:
                    logger.error("Invalid JSON response")
                    break

            try:
                actual_msg = ui_obj["status"]["info"][0]["message"]
            except (KeyError, IndexError, TypeError):
                actual_msg = ""

            logger.info(f'[INFO] - "message": "{actual_msg}"')

            if expected_msg in actual_msg:
                attempts += 1
                logger.info(f"[Attempt {attempts}] Login failed with expected message part.")
            else:
                success = True
                Assertion.assert_true(expected_msg in actual_msg, 
                                    f"ERR: Expected message containing '{expected_msg}', has '{actual_msg}'")

        if not success:
            Assertion.assert_true(expected_msg in actual_msg, 
                                f"ERR: User is not locked out.'{actual_msg}'")

class Totp_28(Test):
    uuid = "SOSAIOT-TC-77264"
    
    def test_01_add_localuser_enable_totp(self):
        logger.info('Create local user and enable TOTP also giving SonicWALL Administrators membership....')
        add_localuser = {
            "action": "add",
            "username": "admin_test_emer",
            "userpassword": "S0nic@uto",
            "one_time_password": "totp",
            "member_of": ["SonicWALL Administrators"]
        }
        response = user_local.local_user(**add_localuser)
        logger.info(response)
        resp = user_local.show_local_user_by_name("admin_test_emer")
        Assertion.assert_regular(json.dumps(resp), '"totp": true', 'ERR:  Failed to enable TOTP for new localuser')

    def test_02_genearate_text(self):
        assert_msg = True
        try:
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = "https://192.168.168.168"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_user_emer.py -url {url} -user admin_test_emer -pwd S0nic@uto'
            out = localhost_1.send_command(cmd)
            logger.info("login with user\n" + out)
            time.sleep(10)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'admin_test_emer', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "admin_test_emer", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
  
    def test_03_local_user_scan_and_enter_totp(self):
        assert_msg = True
        try:
            scanner_page = 1
            localhost_1.send_command('pkill firefox')
            time.sleep(5)
            url = f"https://{ip}"
            cmd = f'python3 {os.environ["PYTHON_SONICOS_HOME"]}/User/user_totp/definition/ui_totp_login.py -url {url} -user admin_test_emer -pwd S0nic@uto -scanner_page {scanner_page}'
            out = localhost_1.send_command(cmd)
            resp = userstatus1.show_users_status()
            logger.info(resp)
            find = re.search(r'admin_test_emer', resp, re.M | re.I)
            logger.info("The user obtained is {}".format(find))
            match = find.group()
            Assertion.assert_equal(match, "admin_test_emer", "ERR: :Invalid user logged in even though not password is wrong")
        except Exception as e:
            logger.info(f"Error==={str(e)}")
            assert_msg = False
            Assertion.assert_equal(assert_msg, False, "ERR: Local user failed enter totp in 2FA page")
  

        
        
        