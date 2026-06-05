from definition.settings import SCRIPTS_PATH
from concurrent.futures import ThreadPoolExecutor
import json
import re
import time
import os
from networkdevice import Host
from runner.settings import logger, Params
from runner.utils.assertion import Assertion


def ssh_connect_remote(
        openstack_PC,
        ip,
        username,
        password,
        action,
        enable=1,
        msg='Successfully login'):
    '''
    SSH connect over SSLVPN/VPN
    :param openstack_PC: -PC3
    :param ip: ip
    :param username: username
    :param password: password
    :param action: login or addao
    :param enable: 1:ssh should success 0:ssh should fail
    :param msg:
    :return: True or False
    '''
    ip_pc = Params.testbed + openstack_PC
    logger.info(ip_pc)
    PC_login = Host(ip_pc)
    logger.info(PC_login)
    time.sleep(160)
    command = f'python3 {SCRIPTS_PATH}LoginDUTFromInterface.py -i {ip} -a {action} -u {username} -p {password}'
    res = PC_login.send_command(command)
    if enable == 1:
        if action == 'login':
            rc = True if re.search(msg, res) else False
        elif action == 'check_login_failed':
            rc = True if not re.search(msg, res) else False
        else:
            rc = True if re.search(
                r'name test', res, re.I | re.S | re.M) and re.search(
                msg, res) else False
        Assertion.assert_equal(rc, True, "ERR: SSH to X0 via SSLVPN fail")
    else:
        if action == 'login':
            rc = True if re.search(msg, res) else False
        else:
            rc = True if re.search(
                r'name test', res, re.I | re.S | re.M) and re.search(
                msg, res) else False
        Assertion.assert_equal(
            rc, False, "ERR: SSH to X0 via SSLVPN success, but it should fail")


def run_io_tasks_in_parallel(tasks):
    with ThreadPoolExecutor() as executor:
        running_tasks = [executor.submit(task) for task in tasks]
        for running_task in running_tasks:
            running_task.result()


def check_SSH_processes(fw_console_login, enable=1):
    cmd = 'diag show processes'
    time.sleep(10)
    fw_console_login.cli_login()
    out = fw_console_login.do_cli_command(cmd)
    if enable == 1:
        rc = True if re.search('tSshC', out, re.I | re.S | re.M) else False
        Assertion.assert_equal(
            rc, True, "ERR: No X0 SSH connection, but it should exist.")
    else:
        rc = True if not re.search('tSshC', out, re.I | re.S | re.M) else False
        Assertion.assert_equal(
            rc, True, "ERR: X0 SSH connection has not been removed, it should be removed.")
