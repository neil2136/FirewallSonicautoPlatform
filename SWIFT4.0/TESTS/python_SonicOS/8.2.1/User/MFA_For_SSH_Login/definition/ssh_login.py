import json
import time
import pexpect
import poplib
import argparse
from definition.settings import *
from pexpect import pxssh
from email.parser import Parser
from email.header import decode_header, Header
from email.utils import parseaddr


def ssh_login(ip, username_fw, password_fw):
    try:
        cmd = f"ssh {username_fw}@{ip}"
        s = pexpect.spawn(cmd, timeout=30)
        i = s.expect(['yes/no', '[Pp]assword:'], timeout=15)
        logger.info(f"Initial prompt index: {i}")
        if i == 0:
            s.sendline('yes')
            logger.info("Sent yes to host key prompt")
            s.expect('[Pp]assword:', timeout=15)
        s.sendline(password_fw)
        s.expect('one-time password', timeout=20)
        received_mail = pop3_client.get_email('172.17.1.5', 'test1', 'password')
        login_otp = str(received_mail).strip()
        logger.info(f"OTP fetched: {login_otp}")
        s.sendline(login_otp)
        s.expect('>', timeout=20)
        output = s.before.decode()
        s.close()
        return output

    except Exception as e:
        logger.error(str(e))
        return None

def enable_cli_login(ip, username_fw, password_fw):
    time.sleep(20)
    output = ssh_login(ip, username_fw, password_fw)
    Assertion.assert_regular(output, "test1@", "ERR: CLI login failed")
    return output