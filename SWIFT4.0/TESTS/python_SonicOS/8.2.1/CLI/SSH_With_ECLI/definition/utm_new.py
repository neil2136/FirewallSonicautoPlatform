from definition.settings import *
from utm import *


class FirewallCLI_New(FirewallCLI):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)

    def ssh_connect_admin_user(self, errcode=0):
        os.system('sed -i ' + '\'' + '/' + self.ip + '/' + ' d' + '\'' + ' /root/.ssh/known_hosts')
        newSsh = "Are you sure you want to continue connecting"
        cmd = 'ssh -l ' + self.user + ' ' + self.ip
        logger.info(cmd)
        self.ssh = pexpect.spawn(cmd)
        enter_password = 0
        while True:
            try:
                index = self.ssh.expect([
                    pexpect.TIMEOUT,
                    '(yes\/no)',
                    '[pP]assword:\s?$',
                    'REMOTE HOST IDEN',
                    '--MORE--*',
                    '\[redisplay\]*|yes\/no\/redisplay*',
                    newSsh,
                    'Maximum login attempts exceeded',
                    self.prompt,
                    'Please enter old password',
                    'Please enter a new password',
                    'Please re-enter new password',
                ])
                logger.info(self.ssh.before.decode())
                logger.info(self.ssh.after.decode())
            except:
                logger.info('Could not start ssh to {}'.format(self.ip))
                if errcode:
                    return False, 'Could not start ssh'
                return False
            if index == 0:  # Timeout
                logger.error('Send command timeout')
                if errcode:
                    return False, 'Send command timeout'
                return False
            elif index == 1:  # SSH does not have the public key. Just accept it.
                self.ssh.sendline('yes')
                continue
            elif index == 2:  # password
                if enter_password == 0:
                    self.ssh.sendline(self.password)
                    self.flushbuffer()
                elif enter_password == 1:
                    self.ssh.sendline('')
                    self.flushbuffer()
                elif enter_password == 2:
                    self.ssh.sendline(self.password)
                    self.new_password = new_password
                elif enter_password == 3:
                    self.ssh.sendline(self.wrong_password)
                    self.new_password = self.wrong_password
                else:
                    if errcode:
                        return False, f'Try password,{self.new_password},{self.wrong_password} failed'
                    return False
                enter_password += 1
                time.sleep(2)
                continue
            elif index == 3:
                logger.info('FIX: .ssh/know_hosts')
                continue
            elif index == 4:
                self.ssh.send("q")
                continue
            elif index == 5 or index == 6:
                self.ssh.sendline('yes')
                continue
            elif index == 7:
                logger.info('Maximum login attempts exceeded: ' + 'ssh -l ' + self.user + ' ' + self.ip)
                if errcode:
                    return False, 'Maximum login attempts exceeded'
                return False
            elif index == 8:
                logger.info('Successfully login in ' + self.ip)
                if errcode:
                    return True, 'Successfully login in'
                return True
            elif index == 9:
                self.ssh.sendline(self.password)
                continue
            elif index == 10:
                time.sleep(65) #针对case使用
                self.ssh.sendline(self.new_password)
                continue
            elif index == 11:
                self.ssh.sendline(self.new_password)
                continue
        if errcode:
            return False, 'Final fail, no error code got'
        return False


class Firewall_new(FirewallCLI_New, FirewallAPI, FirewallCGI):
    def __init__(self, ip, **kwargs):
        super().__init__(ip, **kwargs)

