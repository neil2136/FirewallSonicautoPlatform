import sys
import os
import json

sys.path.append(os.environ["PYTHON_SONICOS_HOME"] + '/User/CLDR-Feature/CLDR_Local_User')

from definition.settings import *


class sslvpn_config(Test):
    uuid = 'NonTC'

    def test_01_create_sslvpn_address_object(self):
        address_object = {
            "object_type": "range",
            "name": "sslvpn_range",
            "zone": "SSLVPN",
            "value": "192.168.168.10,192.168.168.20"
        }
        address_objects.config_addressobject(**address_object)
        resp = address_objects.get_addressobject_by_name("sslvpn_range", "ipv4")
        Assertion.assert_regular(json.dumps(resp), '"name": "sslvpn_range"', "Err: failed to create address object")

    def test_02_sslserver_settings_with_port_enabled(self):
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

    def test_03_enable_sslvpn_access(self):
        enable = {
            'WAN_enable': True
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_04_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_05_add_sslvpn_user(self):
        user_json = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL'
        }
        user_local.local_user(**user_json)
        resp = user_local.show_local_users()
        Assertion.assert_regular(json.dumps(resp), '"name": "testlocal"', 'err: sslvpnlocal not created')

    def test_06_add_user_client_access(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'vpn_client_access': ['LAN Subnets']
        }
        user_local.user_vpn_client_access(**member)
        resp = user_local.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp), '"group": "LAN Subnets"',
                                 'err: sslvpnlocal not added to SSLVPN Services')

    def test_07_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services']
        }
        user_local.user_member_of(**member)
        resp = user_local.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp), '"name": "SSLVPN Services"',
                                 'err: sslvpnlocal not added to SSLVPN Services')

    def test_08_install_nx_linux_remote(self):
        cpy_build = cp_nx.buildnx_linux_remote('-PC2')
        logger.info(cpy_build)
        inst = cp_nx.install_nx_linux_remote('-PC2')
        logger.info(inst)


def virtual_office_login(ip, user, password):
    obj = virtualoffice_page.VirtualPage(ip=ip, user=user, password=password)
    logger.info(obj)
    virtual_login = obj.login_ui()
    logger.info(virtual_login)

def run_io_tasks_in_parallel(tasks):
	results = []
	with ThreadPoolExecutor() as executor:
		running_tasks = [executor.submit(task) for task in tasks]
		for running_task in running_tasks:
			results.append(running_task.result())
	return results

# No restriction
class NonTC_1(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,
                    },
                    "block_local_user_update": False,
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,',
                                 "failed to enable toggle button")

    def test_Users_AdminPrivelage(self):
        add_localuser = {
            "action": "add",
            "username": "testlocal",
            "userpassword": "Passw0rdSWL",
            "member_of": ["SonicWALL Administrators"],
        }

        response = local_user.local_user(**add_localuser)
        response_get = local_user.show_local_users()
        Assertion.assert_regular(json.dumps(response_get), '"name": "testlocal"', 'err: Failed to create adminuser')

    def test_disable_password_restrictions(self):
        obj_json = {
            "administration": {
                "password": {
                    "aging": {},
                    "last_changed": {},
                    "uniqueness": {},
                    "enforce_character_difference": False,
                    "minimum_length": 8,
                    "complexity": {},
                }
            }
        }
        response = admin_setting.conf_admin_update(**obj_json)
        Assertion.assert_equal(response, True, "ERR: edit user setting failed")
        resp = admin_setting.show_admin_setting()
        # Assertion.assert_equal(resp['administration']['password']['complexity']['type'], 'alpha-and-numeric',
        #                        'err: edit admin setting failed ')
        Assertion.assert_regular(json.dumps(resp), '"complexity": {},', "ERR: Failed to edit password constraints")

# Block Remote Access is set
class NonTC_2(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
            "user": {
                "auth": {
                    "credential_auditor": {
                        "enable": True,
                    },
                    "block_local_user_update": False,
                    "periodic_detect_local_user_restriction":
                    {"block_remote_access": True},
                }
            }
        }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,',
                                 "failed to enable toggle button")

# Block Remote Access is set
class NonTC_3(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
                "user": {
                    "auth": {
                        "credential_auditor": {
                            "enable": True,
                        },
                        "block_local_user_update": False,
                        "periodic_detect_local_user_restriction":
                            {"block_all_access":True},
                    }
                }
            }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,',
                                     "failed to enable toggle button")

# Block All But Console & GMS/NSM
class NonTC_4(Test):
    uuid = 'NonTC'

    def test_Enable_Credential_Auditor(self):
        json_obj = {
                "user": {
                    "auth": {
                        "credential_auditor": {
                            "enable": True,
                        },
                        "block_local_user_update": True,
                        "periodic_detect_local_user_restriction":
                            {"block_all_except_nsm":True},
                    }
                }
            }
        resp = user_settings.user_settings_base(**json_obj)
        Assertion.assert_equal(resp, True, "ERR: testcase failed")
        res = user_settings.show_user_setting()
        Assertion.assert_regular(json.dumps(res), '"credential_auditor": {"enable": True,',
                                     "failed to enable toggle button")


# No restriction
class TC001_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77654"
    def test_01_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_02_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_03_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','Guest Services']
        }
        resp = local_user.user_member_of(**member)
        resp1 = local_user.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')

    def test_04_login_FW(self):
        local_user_login = users.UserLoginApi(headers = None,ip = "192.168.168.168", username = "testlocal", password ="Passw0rdSWL")
        rc,user_d = local_user_login.local_user_login()
        Assertion.assert_equal(rc, False, "ERR: Admin login Not successful")
        logger.info("Admin login with API successful")

class TC002_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77653"

    def test_login_FW(self):
        rc = fw_cli.cli_login()
        Assertion.assert_equal(rc, True, "ERR: Admin user can not login failed")
        logger.info("Admin login with API successfull")

class TC003_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77657"

    def test_01_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    # @repeat_method(3)
    def test_03_login(self):
        static_client2.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('192.168.168.168:4433', 'testlocal', 'Passw0rdSWL')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "admin"', "failed to get user status")

    def test_04_login(self):
        static_client1.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('192.168.168.168:4433', 'testlocal', 'password')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_regular(json.dumps(status), '"name": "admin"', "failed to get user status")

class TC004_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77658"

    def test_02_verify_nx_from_DMZ(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='23.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC3'),
            lambda: nx.NX_disconnect_remote('-PC2')])

    def test_02_verify_nx_from_WAN(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='13.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC2'),
            lambda: nx.NX_disconnect_remote('-PC2')])

class TC005_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77652"
    def test_01_user_login(self):
        rc = fw_api.api_login()
        Assertion.assert_equal(rc, True, "ERR: login admin failed")

# Block Remote Access is set
class TC006_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77661"
    def test_01_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_02_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_03_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','Guest Services']
        }
        resp = local_user.user_member_of(**member)
        resp1 = local_user.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')

    def test_04_login_FW(self):
        local_user_login = users.UserLoginApi(headers = None,ip = "192.168.168.168", username = "testlocal", password ="Passw0rdSWL")
        rc,user_d = local_user_login.local_user_login()
        Assertion.assert_equal(rc, False, "ERR: Admin login Not successful")
        logger.info("Admin login with API successful Failed")

class TC007_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77662"

    def test_login_FW(self):
        rc = fw_cli.cli_login()
        Assertion.assert_equal(rc, True, "ERR: Admin user can not login failed")
        logger.info("Admin login with API successfull")

class TC008_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77663"
    def test_01_enable_server_access(self):
        enable = {
                'WAN_enable': True,
                'LAN_enable': True,
            }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    @repeat_method(3)
    def test_03_login(self):
        static_client2.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('13.0.0.100:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")
        logger.info("Login Failed")

    def test_04_login(self):
        static_client1.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('192.168.168.168:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")

class TC009_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77666"

    def test_02_verify_nx_from_DMZ(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='23.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC3'),
            lambda: nx.NX_disconnect_remote('-PC2')])

    def test_02_verify_nx_from_WAN(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='13.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC2'),
            lambda: nx.NX_disconnect_remote('-PC2')])

class TC010_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77667"
    def test_01_user_login(self):
        rc = fw_api.api_login()
        Assertion.assert_equal(rc, True, "ERR: login admin failed")

# Block All But Console Access is set

class TC011_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77679"
    def test_01_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_02_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_03_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','Guest Services']
        }
        resp = local_user.user_member_of(**member)
        resp1 = local_user.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')

    def test_04_login_FW(self):
        local_user_login = users.UserLoginApi(headers = None,ip = "192.168.168.168", username = "testlocal", password ="Passw0rdSWL")
        rc,user_d = local_user_login.local_user_login()
        Assertion.assert_equal(rc, False, "ERR: Admin login Not successful")
        logger.info("Admin login with API successfully failed")

class TC012_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77680"

    def test_login_FW(self):
        rc = fw_cli.cli_login()
        Assertion.assert_equal(rc, True, "ERR: Admin user can not login failed")
        logger.info("Admin login with API successfull")

class TC013_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77681"

    def test_01_enable_server_access(self):
            enable = {
                'WAN_enable': True,
                'LAN_enable': True,
            }
            server_access = sslvpnserver.edit_server_access_setting(**enable)
            Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    @repeat_method(3)
    def test_03_login(self):
        static_client2.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('13.0.0.100:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")
        logger.info("Login Failed")

    def test_04_login(self):
        static_client1.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('192.168.168.168:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")

class TC014_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77684"

    def test_02_verify_nx_from_DMZ(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='23.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC3'),
            lambda: nx.NX_disconnect_remote('-PC2')])

    def test_02_verify_nx_from_WAN(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='13.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC2'),
            lambda: nx.NX_disconnect_remote('-PC2')])

class TC015_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77685"
    def test_01_user_login(self):
        rc = fw_api.api_login()
        Assertion.assert_equal(rc, True, "ERR: login admin failed")

# Block All But Console & GMS/NSM
class TC016_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77688"
    def test_01_enable_server_access(self):
        enable = {
            'WAN_enable': True,
            'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    def test_02_edit_client_settings(self):
        ssl_vpn_client = {
            'ipv4_network_address_name': 'sslvpn_range',
            'ipv4_network_address_zone': 'SSLVPN',
            'route_type': ' ',
            'route_ipv4': ['LAN Subnets']
        }
        client_settings = clientsetobj.edit_default_device_profile(**ssl_vpn_client)
        Assertion.assert_equal(client_settings, True, "Err: Client settings page is not configured successfully")

    def test_03_add_user_sslvpn_services(self):
        member = {
            'action': 'add',
            'username': 'testlocal',
            'userpassword': 'Passw0rdSWL',
            'member_of': ['Trusted Users', 'Everyone', 'SSLVPN Services','Guest Services']
        }
        resp = local_user.user_member_of(**member)
        resp1 = local_user.show_local_user_by_name('testlocal')
        Assertion.assert_regular(json.dumps(resp1), '"name": "SSLVPN Services"',
                                 'err: sslvpntest not added to SSLVPN Services')

    def test_04_login_FW(self):
        local_user_login = users.UserLoginApi(headers = None,ip = "192.168.168.168", username = "testlocal", password ="Passw0rdSWL")
        rc,user_d = local_user_login.local_user_login()
        Assertion.assert_equal(rc, False, "ERR: Admin login Not successful")
        logger.info("Admin login with API successfuly failed")

class TC017_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77689"

    def test_login_FW(self):
        rc = fw_cli.cli_login()
        Assertion.assert_equal(rc, True, "ERR: Admin user can not login failed")
        logger.info("Admin login with API successfull")

class TC018_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77690"
    def test_01_enable_server_access(self):
        enable = {
                'WAN_enable': True,
                'LAN_enable': True,
        }
        server_access = sslvpnserver.edit_server_access_setting(**enable)
        Assertion.assert_equal(server_access, True, "Err: failed to config server access")

    @repeat_method(3)
    def test_02_login(self):
        static_client2.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('13.0.0.100:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")
        logger.info("Login Failed")

    def test_04_login(self):
        static_client1.send_command('pkill firefox')
        time.sleep(10)
        virtual_office_login('192.168.168.168:4433', 'testlocal1', 'Passw0rd')
        # check user status
        status = user_status.show_user_status()
        Assertion.assert_not_regular(json.dumps(status), '"name": "testlocal1"', "failed to get user status")

class TC019_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77693"

    def test_02_verify_nx_from_DMZ(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='23.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC3'),
            lambda: nx.NX_disconnect_remote('-PC2')])

    def test_02_verify_nx_from_WAN(self):
        run_io_tasks_in_parallel([
            lambda: nx.connect_nxlinux_remote(user='testlocal', pswd='Passw0rdSWL', netexurl='13.0.0.100:4433',
                                           domain='LocalDomain', openstack_PC='-PC2'),
            lambda: nx.NX_disconnect_remote('-PC2')])

class TC020_LocalUsers(Test):

    uuid = "SOSAIOT-TC-77694"
    def test_01_user_login(self):
        rc = fw_api.api_login()
        Assertion.assert_equal(rc, True, "ERR: login admin failed")
                
