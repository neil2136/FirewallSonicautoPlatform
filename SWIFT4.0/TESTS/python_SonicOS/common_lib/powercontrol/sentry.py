import telnetlib  
import time
import re
import sys

from runner.settings import logger

class CDU:
    def __init__(self, ip='', user='admin', password='password', controllername ='', time_reboot=15,file='/tmp/cdu.log'):
        self.ip = ip
        self.user = user
        self.password = password
        self.controllername = controllername
        self.telnet = telnetlib.Telnet()  
        self.file = file
        self.fileHandle = open(self.file, 'w+')
        self.module_name = sys._getframe().f_code.co_filename
        self.time_reboot=time_reboot

    def do_telnet(self):
        logger.info('Now start to login pdu: ' + self.ip)
        logger.info('Login user: ' + self.user)
        logger.info('Login password: ' + self.password)
        try:
            self.telnet.open(self.ip, port=23)
            rc1=self.telnet.read_until(b'Username: ', timeout=10)
            self.telnet.write(self.user.encode('ascii') + b'\r\n')
            rc2=self.telnet.read_until(b'Password: ', timeout=10)
            self.telnet.write(self.password.encode('ascii') + b'\r\n')            
        except Exception as e:
            logger.error("Login CDU failed: {}".format(e))
            self.telnet.close()
            return False

        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('ascii')
        logger.info('Login information: ' + command_result)

        if 'Switched CDU: ' in command_result:
            logger.info('login %s success'%self.ip)
            return True
        else:
            logger.error('Maybe the type, user or password is incorrect, pls check again')
            self.telnet.close(command_result)
            return False

    def execute(self, action, outlet):
        if re.search(r'^\w+$', outlet, re.I):
            outlet = "." + outlet
        if re.search(r'on', action, re.I):
            action = "ON" 
        elif re.search(r'off', action, re.I):
            action = "OFF"
        elif re.search(r'reset|reboot|cycle', action, re.I): 
            action = "REBOOT"
        if self.do_telnet():
            cmd = action + ' ' + str(outlet)

            if action == 'REBOOT':
                logger.info('OFF device first.')
                cmd_off= 'OFF' + ' ' + str(outlet)
                self.telnet.write(cmd_off.encode('ascii') + b'\n')
                time.sleep(20)
                logger.info('ON device.')
                command_result = self.telnet.read_very_eager().decode('ascii')
                cmd_on= 'ON' + ' ' + str(outlet)
                self.telnet.write(cmd_on.encode('ascii') + b'\n')

                command_result += self.telnet.read_very_eager().decode('ascii')
                logger.info(f'Sleep {self.time_reboot} seconds for REBOOT command')
                time.sleep(self.time_reboot)
            else:
                self.telnet.write(cmd.encode('ascii') + b'\n')
                time.sleep(2)
                command_result = self.telnet.read_very_eager().decode('ascii')
            self.telnet.close()

            if 'Command successful' in command_result:
                logger.info('Action %s executed successfully on outlet %s' %(action, outlet))
                return True
            else:
                logger.error('Action %s executed unsuccessfully on outlet %s' %(action, outlet))
                logger.error('Error message:\n%s' % command_result)
                return False
        else:
            return False



if __name__ == "__main__":
    from  powercontrol.sentry import CDU
    cdu_ip = '10.188.9.14'
    outlet = 'AA3'

    power = CDU(cdu_ip)
    power.execute('on', outlet)




