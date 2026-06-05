from definition.settings import fw, logger, Console_File_Location, fwcli, PC3_login, radius_server
from definition.settings import Parameter, user_ldap, ldap_server, usersetting, radius_api, sso_api, tacacs_api
import requests
import io
import zipfile
import os
from collections import OrderedDict

headers = OrderedDict([('Accept', 'application/json'),
                       ('Content-Type', 'application/json'),
                       ('Accept-Encoding', 'application/json'),
                       ('charset', 'UTF-8')])

cli_dict = {
    "enable_log_to_console": ['configure', 'dbg', 'general-settings', 'log-to console'],
    "enable_log_to_syslog": ['configure', 'dbg', 'general-settings', 'log-to syslog'],
    "enable_syslog_profile": ['configure', 'dbg', 'general-settings', 'log-to syslog server-profile 1'],
    "enable_syslog_anyserver": ['configure', 'dbg', 'general-settings', 'log-to syslog any-server'],
    "random_configure_user": ['configure', 'dbg', 'user', 'auth-level 2', 'ip-level 3', 'ha-level 4',
                              'connection-level 3'],
    "recover_user_level": ['configure', 'dbg', 'user', 'auth-level 0', 'ip-level 0', 'ha-level 0',
                           'connection-level 0'],
    "random_configure_auth": ['configure', 'dbg', 'auth', 'ldap relay', 'ldap trace'],
    "recover_auth_configure": ['configure', 'dbg', 'auth', 'no ldap relay', 'no ldap trace'],
    "set_conn_level_to_6": ['configure', 'dbg', 'user', 'connection-level 6'],
    "set_conn_level_to_0": ['configure', 'dbg', 'user', 'connection-level 0'],
    "set_ha_level_to_6": ['configure', 'dbg', 'user', 'ha-level 6'],
    "set_ha_level_to_0": ['configure', 'dbg', 'user', 'ha-level 0'],
    "set_ip_level_to_6": ['configure', 'dbg', 'user', 'ip-level 6'],
    "set_ip_level_to_0": ['configure', 'dbg', 'user', 'ip-level 0'],
    "set_cia_to_6": ['configure', 'dbg', 'auth', 'cia 9'],
    "set_cia_to_0": ['configure', 'dbg', 'auth', 'cia 0'],
    "open_ldap_all": ['configure', 'dbg', 'auth', 'ldap all'],
    "close_ldap_all": ['configure', 'dbg', 'auth', 'no ldap all'],
    "open_ldap_args": ['configure', 'dbg', 'auth', 'ldap args'],
    "close_ldap_args": ['configure', 'dbg', 'auth', 'no ldap args'],
    "open_ldap_ber": ['configure', 'dbg', 'auth', 'ldap ber'],
    "close_ldap_ber": ['configure', 'dbg', 'auth', 'no ldap ber'],
    "open_ldap_conns": ['configure', 'dbg', 'auth', 'ldap conns'],
    "close_ldap_conns": ['configure', 'dbg', 'auth', 'no ldap conns'],
    "open_ldap_clients": ['configure', 'dbg', 'auth', 'ldap client'],
    "close_ldap_clients": ['configure', 'dbg', 'auth', 'no ldap client'],
    "open_ldap_filter": ['configure', 'dbg', 'auth', 'ldap auth-filter'],
    "close_ldap_filter": ['configure', 'dbg', 'auth', 'no ldap auth-filter'],
    "open_ldap_daemon": ['configure', 'dbg', 'auth', 'ldap daemon'],
    "close_ldap_daemon": ['configure', 'dbg', 'auth', 'no ldap daemon'],
    "open_ldap_nameresolve": ['configure', 'dbg', 'auth', 'ldap name-resolve'],
    "close_ldap_nameresolve": ['configure', 'dbg', 'auth', 'no ldap name-resolve'],
    "open_ldap_packets": ['configure', 'dbg', 'auth', 'ldap packets'],
    "close_ldap_packets": ['configure', 'dbg', 'auth', 'no ldap packets'],
    "open_ldap_parse": ['configure', 'dbg', 'auth', 'ldap parse'],
    "close_ldap_parse": ['configure', 'dbg', 'auth', 'no ldap parse'],
    "open_ldap_pktdump": ['configure', 'dbg', 'auth', 'ldap pkt-dump'],
    "close_ldap_pktdump": ['configure', 'dbg', 'auth', 'no ldap pkt-dump'],
    "open_ldap_socketdump": ['configure', 'dbg', 'auth', 'ldap socket-dump'],
    "close_ldap_socketdump": ['configure', 'dbg', 'auth', 'no ldap socket-dump'],
    "open_ldap_relay": ['configure', 'dbg', 'auth', 'ldap relay'],
    "close_ldap_relay": ['configure', 'dbg', 'auth', 'no ldap relay'],
    "open_ldap_tool": ['configure', 'dbg', 'auth', 'ldap tool'],
    "close_ldap_tool": ['configure', 'dbg', 'auth', 'no ldap tool'],
    "open_ldap_toolverbose": ['configure', 'dbg', 'auth', 'ldap tool-verbose'],
    "close_ldap_toolverbose": ['configure', 'dbg', 'auth', 'no ldap tool-verbose'],
    "open_ldap_trace": ['configure', 'dbg', 'auth', 'ldap trace'],
    "close_ldap_trace": ['configure', 'dbg', 'auth', 'no ldap trace'],
    "open_rad_account": ['configure', 'dbg', 'auth', 'radius-account 10'],
    "close_rad_account": ['configure', 'dbg', 'auth', 'radius-account 0'],
    "open_sso_api": ['configure', 'dbg', 'auth', 'sso-api 10'],
    "close_sso_api": ['configure', 'dbg', 'auth', 'sso-api 0'],
    "open_radius": ['configure', 'dbg', 'auth', 'radius'],
    "close_radius": ['configure', 'dbg', 'auth', 'no radius'],
    "open_tsa": ['configure', 'dbg', 'auth', 'tsa 10'],
    "close_tsa": ['configure', 'dbg', 'auth', 'tsa 0'],
    "open_tacas": ['configure', 'dbg', 'auth', 'tacas'],
    "close_tacas": ['configure', 'dbg', 'auth', 'no tacas'],
    "show_user_command": ['configure', 'dbg', 'user', '?'],
    "show_dbg_user": ['show dbg user'],
    "show_auth_ldap_command": ['configure', 'dbg', 'auth', 'ldap ?'],
    "show_dbg_auth": ['show dbg auth'],
}


def get_console_log():
    url = "https://192.168.168.168/api/sonicos/export/console/log"
    logger.info('using api_get'.center(130, '='))
    fw.api_login()
    try:
        response = requests.get(url, headers=headers, timeout=60, verify=False)
    except Exception as e:
        logger.error("GET request is not successful {}".format(e))
        return False
    resp = response.content
    fw.api_logout()
    # logger.info(resp)
    return resp


def edit_ldap_hostname(json_input, msg=False):
    url = "api/sonicos/user/ldap/servers/name/" + Parameter.LDAP_SEVER
    ldap_server_resp = fw.api_put(url, msg, data=json_input)
    return ldap_server_resp


def save_console_log_to_file(file_name):
    os.makedirs(Console_File_Location, exist_ok=True)
    des_file = Console_File_Location + "/" + file_name
    if os.path.exists(des_file):
        os.remove(des_file)
    rs = get_console_log()
    logger.info(f"decode console log")
    with zipfile.ZipFile(io.BytesIO(rs), 'r') as zip_ref:
        all_files = zip_ref.namelist()
        logger.info(f"console file list is {all_files}")
        matched_files = ['scconsole', 'scconsole_1']
        for file in matched_files:
            if file in all_files:
                zip_ref.extract(file, Console_File_Location)
                # if file == 'scconsole_1' or file == 'scconsole':
                logger.info(f"change console log name to {file_name}")
                os.rename(Console_File_Location + "/" + file, des_file)
    if os.path.exists(des_file):
        return True
    else:
        return False


def compare_console_info(file_before="command_before", file_after="command_after", verify_file="console"):
    '''
    compare the console before command and console after command,
    return the more console info in command after with string
    '''
    before_file_path = Console_File_Location + "/" + file_before
    after_file_path = Console_File_Location + "/" + file_after
    with open(before_file_path, 'r', encoding='utf-8', errors='ignore') as f1, open(
            after_file_path, 'r', encoding='utf-8', errors='ignore') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    len_after = len(lines2)
    len_before = len(lines1)
    logger.info(f"The length for command_before is {len_before}. The length for command_after is {len_after}")
    overlap_index = 0
    line_last = ''
    if len_after > len_before:
        if verify_file == "console":
            for i in range(1, len_before + 1):
                # logger.info(f"the last {i} line content is {lines1[-i]}")
                if ']:' in lines1[-i]:
                    if ']:' in lines1[-i - 1]:
                        line_last = lines1[-i - 1]
                    else:
                        line_last = lines1[-i - 2]
                    logger.info(f'The last line is: {line_last}')
                    break
                else:
                    continue
        else:
            for i in range(1, len_before + 1):
                # logger.info(f"the last {i} line content is {lines1[-i]}")
                if lines1[-i] != '':
                    line_last = lines1[-i]
                    logger.info(f'The last line is: {line_last}')
                    break
                else:
                    continue
        for i in range(1, len_after + 1):
            if lines2[-i] == line_last:
                overlap_index = i
                break
        logger.info(f'The overlap index is: {overlap_index}')
        extra1 = lines2[-overlap_index + 1:] if overlap_index > 0 else []
        more_str = ','.join(extra1) if extra1 != [] else ""
        logger.info(f'The more string after command is: {more_str}')
    else:
        more_str = ''
    return more_str


def send_cli_command(commands):
    exit_commands = ['commit', 'end', 'exit']
    new_commands = commands + exit_commands
    logger.info(f"commands list is: {new_commands}")
    result = fwcli.do_cli_commands(new_commands)
    return result


def check_str_in_command(content, command_back):
    rs = []
    if content:
        for i in content:
            if i in command_back:
                rs.append(True)
            else:
                rs.append(False)
    else:
        rs.append(False)
    return all(rs)


def check_str_not_in_command(content, command_back):
    rs = []
    if content:
        for i in content:
            if i not in command_back:
                rs.append(True)
            else:
                rs.append(False)
    else:
        rs.append(False)
    return all(rs)


def set_auth_level(level):
    commands = ['configure', 'dbg', ' user', f'auth-level {level}']
    for command in ['commit', 'end', 'exit']:
        commands.append(command)
    result = fwcli.do_cli_commands(commands)
    return result


def show_via_cli_command(commands):
    output = fwcli.do_cli_commands(commands, tag=1)[1]
    return output


def ldap_operation(operation):
    if operation == "disable_enable_ldap_server":
        edit_ldap_servers = {
            'role': 'primary',
            'host': Parameter.LDAP_SEVER,
            'enable': False,
            'port_num': 388,
            'use_tls': False,
            'timeout': False,
            'servertimeout': 14,
            'overalloperationtimeout': 6,
        }
        rs1 = user_ldap.edit_ldap_server(**edit_ldap_servers)
        edit_ldap_servers = {
            'role': 'primary',
            'host': Parameter.LDAP_SEVER,
            'enable': True,
            'port_num': 389,
            'use_tls': False,
            'timeout': True,
            'servertimeout': 15,
            'overalloperationtimeout': 7,
        }
        rs2 = user_ldap.edit_ldap_server(**edit_ldap_servers)
        rs = rs1 & rs2
    elif operation == "schema_read_server":
        command = ["configure", "user ldap", "server 192.168.168.85", "schema microsoft-active-directory",
                   "read-from-server display"]
        rs = send_cli_command(command)
    elif operation == "import_user":
        command = ["configure", "user ldap", "import type user-list from server " + Parameter.LDAP_SEVER]
        rs = send_cli_command(command)
    elif operation == "test_user":
        command = ["configure", "user ldap",
                   'test ' + Parameter.LDAP_SEVER + ' type user-authentication ldap_auto_1 S0nic@uto']
        rs = send_cli_command(command)
    elif operation == "test_connection":
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "192.168.168.85",
                        "type": {
                            "ldap_search": {
                                "return_attribute": "DC=os-autosnwl",
                                "basic": {
                                    "searchContent": "ldap_auto_1",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        rs = user_ldap.test_ldap_server_basic_search(**ldap_test)
    elif operation == "delete_add_ldap_server":
        try:
            resp = user_ldap.del_ldap_server(Parameter.LDAP_SEVER)
        except:
            pass
        rs = user_ldap.add_ldap_server_new(**ldap_server)
    elif operation == "test_connection_with_domain":
        ldap_test = {
            "user": {
                "ldap": {
                    "test": {
                        "name": "ForestDnsZones.ldapqa.com",
                        "type": {
                            "ldap_search": {
                                "basic": {
                                    "searchContent": "ldap_auto_1",
                                    "use": {
                                        "user": "login-name"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        rs = user_ldap.test_ldap_server_basic_search(**ldap_test)
    elif operation == "enable_relay":
        edit_ldap_servers_relay = {
            "user": {
                "ldap": {
                    'relay': {
                        "enable": True,
                    }
                }}}
        rs1 = user_ldap.config_ldap_setting(**edit_ldap_servers_relay)
        edit_ldap_servers_relay = {
            "user": {
                "ldap": {
                    'relay': {
                        "enable": False,
                    }
                }}}
        rs2 = user_ldap.config_ldap_setting(**edit_ldap_servers_relay)
        rs = rs1 & rs2
    elif operation == "enable_disable_radius_account":
        edit_user_method1 = {
            "radius_accounting": True
        }
        edit_user_method2 = {
            "radius_accounting": False
        }
        rs = usersetting.user_method_authentication(**edit_user_method1)
        rs &= usersetting.user_method_authentication(**edit_user_method2)
    elif operation == "add_radius_server_and_test":
        try:
            radius_api.add_radius_server(**radius_server)
            test_payload = {
                "user": {
                    "radius": {
                        "test": {
                            "name": "10.8.141.162"
                        }
                    }
                }
            }
            radius_api.test_radius_server(payload=test_payload)
            rs = True
        except Exception as e:
            logger.error("add_radius_server_and_test failed {}".format(e))
            rs = True
    elif operation == "enable_3rdParty_API":
        try:
            edit_user_method1 = {
                "third_party_api": True
            }
            rs = usersetting.user_method_authentication(**edit_user_method1)
            thirdparyhost = {
                "host": "10.8.153.163",
                "enable": True,
                "authentication_type": "shared-secret",
                "shared_secret": "12345678",
                "security_level": {
                    "high": "allow-all"
                },
                "replay_prevention": False,
                "origin_restriction": {},
                "persistent_connections": False
            }
            sso_api.create_sso_third_party_client(**thirdparyhost)
            sso_api.delete_sso_third_party_client("10.8.153.163")
        except Exception as e:
            logger.error("add 3td Party host failed {}".format(e))
            rs = True
    elif operation == "add_tacacs_server_and_delete":
        try:
            tacacs_server = {
                "enable": True,
                "host": "10.8.156.153",
                "secret": "12345678",
                "port_num": 49
            }
            tacacs_api.add_tacacs_server(**tacacs_server)
            tacacs_api.del_tacacs_server("10.8.156.153")
            rs = True
        except Exception as e:
            logger.error("add_tacacs_server failed {}".format(e))
            rs = True
    elif operation == "enable_terminal_service":
        try:
            edit_user_method1 = {
                "terminal_services_agent": True
            }
            rs = usersetting.user_method_authentication(**edit_user_method1)
            thirdparyhost = {
                "action": "add",
                "host": "10.8.153.163",
                "enable": True,
                "port": 2259,
                "shared_key": "12345678",
            }
            sso_api.terminal_services_agent(**thirdparyhost)
            sso_api.del_terminal_services_agent_by_host(host="10.8.153.163", port="2259")
        except Exception as e:
            logger.error("add_terminal_server failed {}".format(e))
            rs = True
    else:
        rs = False
    return rs


def get_syslog_pc1(file_name):
    des_file = Console_File_Location + "/" + file_name
    if os.path.exists(des_file):
        logger.info(f"delete the file: {des_file}")
        os.remove(des_file)
    with open('/var/log/messages', 'r', encoding='gb2312', errors='ignore') as file:
        syslog = file.read()
    # logger.info(f"syslog is {syslog}")
    with open(des_file, 'w', encoding='utf-8') as file:
        file.write(syslog)
    if os.path.exists(des_file):
        return True
    else:
        return False


def get_syslog_pc3(file_name):
    des_file = Console_File_Location + "/" + file_name
    if os.path.exists(des_file):
        logger.info(f"delete the file: {des_file}")
        os.remove(des_file)
    file_content = PC3_login.send_command('cat /var/log/messages')
    # logger.info(f"syslog is {syslog}")
    with open(des_file, 'w', encoding='utf-8') as file:
        file.write(file_content)
    if os.path.exists(des_file):
        return True
    else:
        return False
