import pexpect       
import pyotp         
import time 
from definition.settings import *

def ssh_totp_first_time(ip, username_fw, password_fw):
    try:
        time.sleep(20)
        cmd = f"ssh {username_fw}@{ip}"
        s = pexpect.spawn(cmd, timeout=30)
        i = s.expect(['yes/no', '[Pp]assword:'], timeout=15)
        logger.info(f"Initial prompt index: {i}")
        if i == 0:
            s.sendline('yes')
            logger.info("Sent yes to host key prompt")
            s.expect('[Pp]assword:', timeout=15)
        s.sendline(password_fw)
        logger.info("Sent password")
        s.expect('TOTP key is:\s*(\S+)', timeout=20)
        full_line = s.after.decode()
        logger.info(f"Full secret line from console: {repr(full_line)}")
        raw = s.after.decode()
        totp_secret = raw.strip().split()[-1]
        logger.info(f"TOTP secret extracted: {totp_secret}")
        s.expect('[Pp]lease enter 2FA [Cc]ode', timeout=10)
        logger.info("2FA prompt received")
        totp_code = pyotp.TOTP(totp_secret).now()
        t=time.time()
        logger.info(time.ctime(t))
        logger.info(f"Generated TOTP: {totp_code}")
        s.sendline(totp_code)
        s.expect('>', timeout=20)
        output = s.before.decode()
        logger.info(output)
        logger.info("SSH TOTP login successful")
        s.close()
        return True, output

    except pexpect.TIMEOUT:
        logger.error(f"Timeout exceeded.\n{s}")
        return False, "Timeout exceeded"
    except Exception as e:
        logger.error(str(e))
        return False, str(e)

def ssh_login(ip, username_fw, password_fw):
    try:
        time.sleep(20)
        cmd = f"ssh {username_fw}@{ip}"
        s = pexpect.spawn(cmd, timeout=30)
        i = s.expect(['yes/no', '[Pp]assword:'], timeout=15)
        logger.info(f"Initial prompt index: {i}")
        if i == 0:
            s.sendline('yes')
            logger.info("Sent yes to host key prompt")
            s.expect('[Pp]assword:', timeout=15)
        s.sendline(password_fw)
        logger.info("Sent password")
        s.expect('>', timeout=20)
        output = s.before.decode()
        logger.info(output)
        s.close()
        return True, output
    except Exception as e:
        logger.error(str(e))
        return False, str(e)