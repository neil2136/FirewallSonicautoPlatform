from definition.settings import *


def check_log_msg(fwlogs, partt):
    logger.info(f"log info: {fwlogs}")
    if fwlogs:
        fwlogs_str = json.dumps(fwlogs)
        hi = re.search(partt, fwlogs_str)
        if hi:
            return True
    return False


def check_user_status_info(status, expectedinfo):
    try:
        logger.info('user status:' + str(status))
        rc = False
        if status["data"]:
            userinfo = status["data"]
            for user in userinfo:
                if user['name'] == expectedinfo['name']:
                    for info in expectedinfo.keys():
                        if user[info] == expectedinfo[info]:
                            rc = True
    except Exception as e:
        logger.error("Exception \t: " + str(e))
        rc = False
    return rc


def check_traffic_to_server(interface_name):
    rc = False
    if interface_name == 'X2':
        rc = PC2_host.ping(Parameter.https_server_ip)
    elif interface_name == 'X3':
        rc = PC3_host.ping(Parameter.https_server_ip)
    elif interface_name == 'X4':
        rc = PC4_host.ping(Parameter.https_server_ip)
    return rc


class guestteststep():
    def __init__(self, zone, interface, username="guest", protocol="https", password="password", zone_obj=zone_api):
        self.zone = zone
        self.interface = interface
        self.protocol = protocol
        self.zone_obj = zone_obj
        self.username = username
        self.password=password

    def login_guest_user(self, expectedstep, pc_tag="pc4", protocol="https", user="guest", postauthstatus=0,
                         fail_info="Test Case Fail"):
        log_api.clear_log()
        url = Parameter.https_server if protocol == "https" else Parameter.http_server
        cmd = ('python3 ' + os.environ[
            "PYTHON_SONICOS_HOME"] + '/Network/Guest_Services_For_Non_Wireless_Zones_TP2379/definition/ui_guest.py '
               + '-url ' + url +
               f' -user {user} -pwd {self.password} -stepstop {expectedstep} -serverip {Parameter.https_server_ip} -postauth {postauthstatus}')
        if self.interface == 'X2':
            logger.info(f"works on PC2")
            out = PC2_host.send_command(cmd)
        elif self.interface == 'X3':
            logger.info(f"works on PC3")
            out = PC3_host.send_command(cmd)
        elif self.interface == 'X4':
            if pc_tag == "pc4":
                logger.info(f"works on PC4")
                out = PC4_host.send_command(cmd)
            elif pc_tag == "pc5":
                logger.info(f"works on PC4")
                out = PC5_host.send_command(cmd)
        logger.info("login with guest user\n" + out)
        if fail_info in out:
            return False
        return True

    def initial_disable_guest_service_for_zone(self):
        rs = self.zone_obj.show_zone_object(self.zone)
        status = rs["zones"][0]['guest_services']["enable"]
        rc = True
        if status:
            zoneedit_dict["zones"][0]["guest_services"]["enable"] = False
            zoneedit_dict["zones"][0]["name"] = self.zone
            rc = self.zone_obj.edit_zone_object(name=self.zone, **zoneedit_dict)
        Assertion.assert_equal(rc, True, "ERR: check icmp failed")

    def configure_interface(self):
        rc = False
        if self.interface == 'X2':
            logger.info(f"config x2 interface as {self.zone} zone... ")
            x2_dict['zone'] = self.zone
            rc = interface_api.config_interface(**x2_dict)
        elif self.interface == 'X3':
            logger.info(f"config x3 interface as {self.zone} zone... ")
            x3_dict['zone'] = self.zone
            rc = interface_api.config_interface(**x3_dict)
        elif self.interface == 'X4':
            logger.info(f"config x4 interface as {self.zone} zone... ")
            x4_dict['zone'] = self.zone
            rc = interface_api.config_interface(**x4_dict)
        Assertion.assert_equal(rc, True, "ERR: Config X2 IPv4 failed")

    def verify_pc_traffic_to_internet_passed(self, pc_tag="pc4", des=Parameter.https_server_ip):
        rc = False
        if self.interface == 'X2':
            rc = PC2_host.ping(des)
        elif self.interface == 'X3':
            rc = PC3_host.ping(des)
        elif self.interface == 'X4':
            if pc_tag == "pc4":
                rc = PC4_host.ping(des)
            elif pc_tag == "pc5":
                rc = PC5_host.ping(des)
        Assertion.assert_equal(rc, True, "ERR: check icmp failed")

    def enable_zone_with_guest_service(self):
        zoneedit_dict["zones"][0]["name"] = self.zone
        zoneedit_dict["zones"][0]["guest_services"]["enable"] = True
        rc = self.zone_obj.edit_zone_object(name=self.zone, **zoneedit_dict)
        Assertion.assert_equal(rc, True, "ERR: enable guest service for lan zone failed")

    def edit_zone_with_guest_service(self, payload):
        rc = self.zone_obj.edit_zone_object(name=self.zone, **payload)
        Assertion.assert_equal(rc, True, "ERR: edit guest service for zone failed")

    def verify_guest_service_enabled(self):
        rs = self.zone_obj.show_zone_object(name=self.zone)
        if rs:
            rc = rs["zones"][0]['guest_services']["enable"]
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Guest enable failed")

    def verify_pc_traffic_to_internet_failed(self, pc_tag="pc4", des=Parameter.https_server_ip):
        rc = True
        if self.interface == 'X2':
            rc = PC2_host.ping(des)
        elif self.interface == 'X3':
            rc = PC3_host.ping(des)
        elif self.interface == 'X4':
            if pc_tag == "pc4":
                rc = PC4_host.ping(des)
            elif pc_tag == "pc5":
                rc = PC5_host.ping(des)
        Assertion.assert_equal(rc, False, "ERR: check icmp failed")

    def login_guest_user_from_pc(self, expstep, pc_tag="pc4", postauth=0, fail_info="Test Case Fail"):
        rc = False
        for attempt in range(1, 5):
            result = self.login_guest_user(expstep, pc_tag, self.protocol, self.username, postauth, fail_info)
            if result is True:
                logger.info(f"Attempt to login {attempt} times: Success")
                rc = True
                break
            else:
                logger.info(f"Attempt to login{attempt} times: Failed, retrying in 20 seconds...")
                if attempt < 4:
                    time.sleep(20)
                rc = False
        Assertion.assert_equal(rc, True, "ERR: check icmp failed")

    def verify_guest_login_status(self):
        user_status = guest_api.get_guest_status()
        if self.interface == 'X2':
            compare_info = {'name': self.username, 'ip': PC2_ETH1_IP, 'iface': 'X2', 'zone': self.zone}
        elif self.interface == 'X3':
            compare_info = {'name': self.username, 'ip': PC3_ETH1_IP, 'iface': 'X3', 'zone': self.zone}
        elif self.interface == 'X4':
            compare_info = {'name': self.username, 'ip': Parameter.pc4eth1_ip, 'iface': 'X4', 'zone': self.zone}
        else:
            compare_info = {'name': self.username}
        rc = check_user_status_info(user_status, compare_info)
        Assertion.assert_equal(rc, True, "ERR: check icmp failed")

    def verify_guest_user_login_success_log(self, pattern):
        log = log_api.show_log()
        rc = check_log_msg(log, pattern)
        Assertion.assert_equal(rc, True, "ERR: check log failed")

    def logout_guest_user_via_logout_button(self):
        rc = guest_api.logout_all_guest_user()
        Assertion.assert_equal(rc, True, "ERR: logout guest user failed")

    def disable_guest_service(self):
        zoneedit_dict["zones"][0]["guest_services"]["enable"] = False
        zoneedit_dict["zones"][0]["name"] = self.zone
        rc = self.zone_obj.edit_zone_object(name=self.zone, **zoneedit_dict)
        Assertion.assert_equal(rc, True, "ERR: disable guest service for dmz zone failed")

    def verify_guest_service_disabled(self):
        rs = self.zone_obj.show_zone_object(name=self.zone)
        if rs:
            rcenable = rs["zones"][0]['guest_services']["enable"]
            rc = False if rcenable else True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: Guest disable failed")

    def login_guest_user_from_pc_expect_fail(self, expstep, pc_tag="pc4", postauth=0, fail_info="Test Case Fail"):
        rc = True
        for attempt in range(1, 5):
            result = self.login_guest_user(expstep, pc_tag, self.protocol, self.username, postauth, fail_info)
            if result is False:
                logger.info(f"Attempt to login{attempt} times: Failed")
                rc = False
                break
            else:
                logger.info(f"Attempt to login{attempt} times: Success, retrying in 20 seconds...")
                if attempt < 4:
                    time.sleep(20)
                rc = True
        Assertion.assert_equal(rc, False, "ERR: check icmp failed")

    def verify_user_not_in_status_page(self):
        user_status = guest_api.get_guest_status()
        rc = check_user_status_info(user_status, {'name': self.username})
        Assertion.assert_equal(rc, False, "ERR: User in status page")

    def verify_user_info_correct_status_page(self):
        user_status = guest_api.get_guest_status()
        compare_info = {
            'name': self.username,
            'ip': Parameter.pc4eth1_ip,
            'iface': self.interface,
            'zone': self.zone,
            'acct_exp': 'N/A',
            'sess_exp': 'strUnlimited',
            'receive_limit': 'strUnlimited',
            'transmit_limit': 'strUnlimited',
            'qouta_cycle': 'Non Cyclic'
        }
        rc = check_user_status_info(user_status, compare_info)
        Assertion.assert_equal(rc, True, "ERR: check icmp failed")

    def add_mac_ao(self, mac_address):
        mac_ao_dict = {
            "object_type": "mac",
            "name": "mac_ao_bypass",
            "zone": self.zone,
            "value": mac_address,
            "multi_homed": True
        }
        res = addressobjects_api.config_addressobject(**mac_ao_dict)
        Assertion.assert_equal(res, True, "ERR: add mac ao failed")

    def delete_mac_ao(self):
        res = addressobjects_api.del_ao_by_name(name='mac_ao_bypass', version='mac')
        Assertion.assert_equal(res, True, "ERR: delete mac ao failed")
