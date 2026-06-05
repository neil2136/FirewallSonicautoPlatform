import telnetlib
import time
import re
from runner.settings import logger


class Switchtelnet:
    def __init__(self, ip, proto, user='admin', password='password', file='/tmp/switch.log'):
        self.ip = ip
        self.user = user
        self.password = password
        self.proto = proto
        self.telnet = telnetlib.Telnet()  
        self.file = file
        self.fileHandle = open(file, 'w+')

        self.init_session()

    def init_session(self):
        print('init session')
        if re.search('force10', self.proto, re.I):
            result = self.do_force10_telnet()
        elif re.search('hp', self.proto, re.I):
            result = self.do_hp_telnet()    
        return result

    def do_force10_telnet(self):
        try:
            self.telnet.open(self.ip, port=23)
            self.telnet.read_until(b'Username:', timeout=10)
            self.telnet.write(self.user.encode('ascii') + b'\n')
            self.telnet.read_until(b'Password:', timeout=10)
            self.telnet.write(self.password.encode('ascii') + b'\n')            
        except:
            logger.warning("Login switch failed")
            self.telnet.close()
            return False

        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('ascii')
        if '#' in command_result:
            logger.debug('Login %s success'%self.ip)
            return self.telnet
        else:
            logger.warning('login %s fail, user or password incorrect'%self.ip)
            self.telnet.close()
            return False

    def do_hp_telnet(self):
        try:
            self.telnet.open(self.ip, port=23)
            self.telnet.read_until(b'Press any key to continue', timeout=10)
            self.telnet.write(b'\n')
            self.telnet.read_until(b'Username:', timeout=10)
            self.telnet.write(self.user.encode('ascii') + b'\n')
            self.telnet.read_until(b'Password:', timeout=10)
            self.telnet.write(self.password.encode('ascii') + b'\n')            
        except:
            logger.warning("Login switch failed")
            self.telnet.close()
            return False
        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('ascii')
        if '#' in command_result:
            logger.info('Login %s success'%self.ip)
            return self.telnet
        else:
            logger.warning('login %s fail, user or password incorrect'%self.ip)
            self.telnet.close()
            return False

    def capture(self, cmd):
        if self.telnet.eof:
            return None
        self.telnet.write(cmd.encode('ascii') + b'\n')
        time.sleep(1)
        line = b''
        while True:
            (index, match, text) = self.telnet.expect([b'--\s*(MORE|More)\s*--',b'#'], timeout=5)
            if index == 0:
                line = line + text
                self.telnet.write(' '.encode('ascii'))
            elif index == 1:
                line += text
                break
            else:
                line += text
                None
        lines = line.decode('utf-8').splitlines()
        self.fileHandle.write('\n'.join(lines))
        self.telnet.prompt = lines.pop()
        return '\n'.join(lines)
    
    def prompt(self):
        return self.telnet.prompt

    def close_session(self):
        if self.telnet:
            if re.search('hp', self.proto, re.I):
                self.telnet.write('logout'.encode('ascii')+ b'\n')
                self.telnet.read_until(b'Do you want to log out \[y/n\]?', timeout=5)
                self.telnet.write('y'.encode('ascii') + b'\n')
            else:
                self.telnet.write('exit'.encode('ascii')+ b'\n')
                self.telnet.close()
        return True


    # def get_session(self):
    #     if self.telnet:
    #         lines = self.telnet.write('show version'.encode('ascii'))
    #         if re.search('system image', lines, re.I):
    #             return self.telnet


