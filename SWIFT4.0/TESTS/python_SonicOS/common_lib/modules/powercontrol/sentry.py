import telnetlib  
import time
import logging
import re

from runner.settings import logger

class CDU:
    def __init__(self, ip, user='admin', password='password'):
        self.cduip = ip
        self.user = user
        self.password = password
        self.telnet = telnetlib.Telnet()  

    def do_telnet(self):
        try:
            self.telnet.open(self.cduip, port=23)
            self.telnet.read_until(b'Username: ', timeout=10)
            self.telnet.write(self.user.encode('ascii') + b'\n')
            self.telnet.read_until(b'Password: ', timeout=10)
            self.telnet.write(self.password.encode('ascii') + b'\n')            
        except:
            logging.warning("Login CDU failed")
            self.telnet.close()
            return False

        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('ascii')
        if 'Switched CDU: ' in command_result:
            logging.info('login %s success'%self.cduip)
            return True
        else:
            logging.warning('login %s fail, user or password incorrect'%self.cduip)
            self.telnet.close()
            logging.warning('Error message：\n%s' % command_result)
            return False

    def execute(self, action, outlet):
        if re.match('^\w+$', outlet, re.I):
            outlet = "." + outlet
     
        if re.match('on', action, re.I):
            action = "ON" 
        elif re.match('off', action, re.I):
            action = "OFF"
        elif re.match('reset|reboot|cycle', action, re.I): 
            action = "REBOOT"
        if self.do_telnet():
            cmd = action + ' ' + str(outlet)
            self.telnet.write(cmd.encode('ascii')+b'\n')  
            time.sleep(2)
            command_result = self.telnet.read_very_eager().decode('ascii')
            self.telnet.close()
            if action == 'REBOOT':
                logging.info('Sleep 15 seconds for REBOOT command')
                time.sleep(15)
            if 'Command successful' in command_result:
                logging.info('Action %s executed successfully on outlet %s' %(action, outlet))
                return True
            else:
                logging.warning('Action %s executed unsuccessfully on outlet %s' %(action, outlet))
                logging.warning('Error message：\n%s' % command_result)
                return False
        else:
            return False

if __name__ == "__main__":
    from  modules.PowerControl.sentry import CDU
    cdu_ip = '10.188.9.14'
    outlet = 'AA3'

    power = CDU(cdu_ip)
    power.execute('off',outlet)       




