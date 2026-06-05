import telnetlib  
import time
import re
import sys

from runner.settings import logger


class PDU():
    def __init__(self, ip='', user='admin', password='password', controllername ='', time_reboot=15,file='/tmp/pdu.log'):
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
        logger.info('Mediatek login: ' + self.user)
        logger.info('Password: ' + self.password)

        try:
            self.telnet.open(self.ip, port=23)
            self.telnet.read_until(b'Mediatek login: ', timeout=10)
            self.telnet.write(self.user.encode('ascii') + b'\r\n')
            self.telnet.read_until(b'Password: ', timeout=10)
            self.telnet.write(self.password.encode('ascii') + b'\r\n')
        except:
            logger.error("Login PDU failed")
            self.telnet.close()
            return False

        time.sleep(2)
        command_result = self.telnet.read_very_eager().decode('ascii')
        logger.info('Login information: ' + command_result)

        if '~#' in command_result:
            logger.info('login %s success'%self.ip)
            return True
        else:
            logger.error('Maybe the type, user or password is incorrect, pls check again')
            logger.error(command_result)
            self.telnet.close()
            return False

    def execute(self, action, outlet):
        if re.search(r'on', action, re.I):
            action = "control on 0" 
        elif re.search(r'off', action, re.I):
            action = "control off 0"
        elif re.search(r'reset|reboot|cycle', action, re.I): 
            action = "control reboot 0"
        if self.do_telnet():
            cmd = action + ' ' + str(outlet)
            if action == 'control reboot 0':
                logger.info('OFF device first.')
                cmd_off= 'control off 0' + ' ' + str(outlet)
                self.telnet.write(cmd_off.encode('ascii') + b'\n')
                time.sleep(20)
                logger.info('ON device.')
                command_result = self.telnet.read_very_eager().decode('ascii')
                cmd_on= 'control on 0' + ' ' + str(outlet)
                self.telnet.write(cmd_on.encode('ascii') + b'\n')

                command_result += self.telnet.read_very_eager().decode('ascii')
                logger.info(f'Sleep {self.time_reboot} seconds for REBOOT command')
                time.sleep(self.time_reboot)

            else:
                self.telnet.write(cmd.encode('ascii') + b'\r\n')  
                time.sleep(2)
                command_result = self.telnet.read_very_eager().decode('ascii')
            if 'Success:' in command_result:
                logger.info('Action %s executed successfully on outlet %s' %(action, outlet))
                return True
            else:
                logger.error('Action %s executed unsuccessfully on outlet %s' %(action, outlet))
                logger.error('Error message:\n%s' % command_result)
                return False
        else:
            return False

if __name__ == "__main__":
    #from  powercontrol.sentry import PDU
    pdu_ip = '10.188.9.15'
    outlet = '17'

    power = PDU(pdu_ip,password='admin123')
    power.execute('reboot', outlet)




