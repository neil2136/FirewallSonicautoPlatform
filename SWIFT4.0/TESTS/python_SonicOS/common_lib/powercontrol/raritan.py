import telnetlib  
import time
import re
import sys

from runner.settings import logger

class PDU:
    def __init__(self, ip='', user='admin', password='password', controllername ='', file='/tmp/cdu.log'):
        self.ip = ip
        self.user = user
        self.password = password
        self.controllername = controllername
        self.telnet = telnetlib.Telnet()  
        self.file = file
        self.fileHandle = open(self.file, 'w+')
        self.module_name = sys._getframe().f_code.co_filename

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

        time.sleep(5)
        command_result = self.telnet.read_very_eager().decode('ascii')
        logger.info('Login information: ' + command_result)

        if '[My PDU] # ' in command_result:
            logger.info('login %s success'%self.ip)
            return True
        else:
            logger.error('Maybe the type, user or password is incorrect, pls check again')
            self.telnet.close()
            return False

    def execute(self, action, outlet):
       # if re.search(r'^\w+$', outlet, re.I):
        #    outlet = "." + outlet
        if re.search(r'on', action, re.I):
            action = "on" 
        elif re.search(r'off', action, re.I):
            action = "off "
        elif re.search(r'reset|reboot|cycle', action, re.I): 
            action = "cycle"
        if self.do_telnet():
            cmd = 'power outlets ' + str(outlet) +' ' + action 
            self.telnet.write(cmd.encode('ascii') + b'\n')  
            rc2=self.telnet.read_until(b'Do you wish to turn outlet ', timeout=10)
            self.telnet.write(b'y' + b'\n')  
            time.sleep(2)
            command_result = self.telnet.read_very_eager().decode('ascii')
            self.telnet.close()
            if action == 'cycle':
                logger.info('Sleep 15 seconds for REBOOT command')
                time.sleep(15)
            if '[My PDU]' in command_result:
                logger.info('Action %s executed successfully on outlet %s' %(action, outlet))
                return True
            else:
                logger.error('Action %s executed unsuccessfully on outlet %s' %(action, outlet))
                logger.error('Error message:\n%s' % command_result)
                return False
        else:
            return False


if __name__ == "__main__":
    import sys
    sys.path.append('/DEV_TESTS/python_SonicOS/common_lib')
    from  powercontrol.raritan import PDU
    cdu_ip = '10.5.64.164'
    outlet = '24'

    power = PDU(cdu_ip,password='sonicwall')
    power.execute('on', outlet)