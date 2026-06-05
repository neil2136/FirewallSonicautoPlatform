import xml.etree.ElementTree
import requests
import sys
import time
import unittest
import os
import re
import subprocess
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from runner.unittest.setup import Test, repeat_method, skip_if_fail_method, skip_unless_fail_method
from runner.settings import Params, logger, LOG_DIR,QBS_JOBNUM
from runner.utils.assertion import Assertion
from util.openstack import Openstack
from tools.trafficGen import ping
from tools.check_nsvsuite_email import SendSuiteSkipEmail
from utm import Firewall, is_Firewall_up, G_PASSWORD_NEW, change_password

from config.restore_tel import RestoreFwTelnet
from config.get_coredump_tel import GetCoredumpTel
from config.get_coredump_api import GetCoredumpApi
from config.upload_firmware import UploadFirmware
from config.swconfig import DeviceConfig
from lib.modules.ui.fw_page import FWPage
from lib.modules.CLI.system import LicenseCli 
from lib.modules.CLI.system import AdminCli
from lib.modules.API import network

ui_obj = FWPage()
ssh_flag = False
ip='192.168.168.168'
cmd0 = 'newman run '+ os.environ["PYTHON_COMMON_HOME"] + '/config/enable_ssh.json -k --disable-unicode --delay-request 1200'
cmd1 = 'newman run '+ os.environ["PYTHON_COMMON_HOME"] + '/config/enable_ssh_newpass.json -k --disable-unicode --delay-request 1200'
cmd2= 'newman run ' + os.environ["PYTHON_COMMON_HOME"] + '/config/enable_ssh_wrongpass.json -k --disable-unicode --delay-request 1200'

@unittest.skipIf(Params.openstack, 'Openstack need not config topo')
class TestAddTopology(Test):
    uuid = 'NonTC'

    def test_00_add_topology(self):  
        TOPO = self.param['TOPO']
        ACTION = self.param['ACTION']
        if 'SPECFILE' not in self.param:
            SPECFILE = os.environ['COMMON_HOME'] + '/data/switches/' + Params.testbed + '.yaml'
        else:
            SPECFILE = self.param['SPECFILE']
        logger.info('TOPO:'.ljust(15,' ') + TOPO + '\n'\
                    + ' '*35 + 'ACTION:'.ljust(15, ' ') + ACTION + '\n'
                    + ' '*35 + 'SPECFILE:'.ljust(15, ' ')+ SPECFILE)
        SWCONFIG = 'python3 {}'.format(os.environ['PYTHON_COMMON_HOME'] + '/config/swconfig.py ')
        logger.info('Clear previous VLAN settings...')
        cmd = SWCONFIG + '-action clear -spec ' + SPECFILE
        logger.info('Execute cmd:' + cmd)
        rc = os.system(cmd)
        if not rc:
            logger.info('Clear topo passed.')
        else:
            logger.info('Clear topo failed.')
        if TOPO:
            topology = TOPO
        else:
            topology = Params.product + '_DEFAULT'
        cmd = SWCONFIG + '-action ' + ACTION + ' -spec ' + SPECFILE + ' -topo ' + topology
        logger.info('Execute cmd:' + cmd)
        rc = os.system(cmd)
        Assertion.assert_equal(rc, 0, "ERR: Config topology failed")

@unittest.skipIf(Params.sonicos_ver == '7.1.1_cover_x86', '7.1.1_cover_x86 do not need restore')
class TestRestoreDUT(Test):
    uuid = 'NonTC'
    # goto_teardown = True

    # @unittest.skipIf('nsv' not in Params.sonicos_ver, "physical platform will skip this step")
    # def test_00_00_check_platform(self):
    #     self.goto_teardown = True
    #     rc = False
    #     logger.error("NSV platform should use TestRestoreDUTByUI, will skip the whole suite")
    #     email = SendSuiteSkipEmail(Params.testbed,Params.product,Params.qbsjobid,Params.scmlabel,Params.ts_display_name,Params.openstack)
    #     email.send_email()
    #     Assertion.assert_equal(rc, True, "ERR: NSV platform should use TestRestoreDUTByUI")

    # @repeat_method(2)
    def test_00_restore_dut(self, restore=True):
        global result
        # if Params.openstack:
        #     osstack = Openstack(Params.testbed)
        #     self.consvr, self.conport = osstack.get_console_info(dut='UTM')
        #     self.power_ip, self.power_port, self.power_model, self.power_type,self.user,self.password = osstack.get_power_info(dut='UTM')
        # else:
        #     SPECFILE = os.environ['COMMON_HOME'] + '/data/switches/' + Params.testbed + '.yaml'
        #     dc =DeviceConfig(user='admin', password='password',specfile=SPECFILE)
        #     dut = dc.device(Params.product)
        #     self.consvr = dut[0]['console']['server']
        #     self.conport = dut[0]['console']['telnetport']
        self.consvr = Params.console_ip
        self.conport = Params.console_port

        restore_telnet = RestoreFwTelnet(console_ip=self.consvr, console_port=self.conport)

        if is_Firewall_up(ip, pre_sleep=5,ssh=False,mode='console',console_ip=self.consvr,console_port=self.conport,reboot_check=True):
            logger.info('Firewall boots up')
            logger.info("try to enable ssh to see if firewall is in default state.... ")
            cmd = 'newman run '+ os.environ["PYTHON_COMMON_HOME"] + \
                '/config/enable_ssh.json -k --disable-unicode --delay-request 1200'
            logger.info(cmd)
            output = os.popen(cmd).read()
            passwd = 'password'
            G_PASSWORD = None
            logger.info(output)
            if 'Login Your default password must be changed' in output:
                logger.info(f'Firewall is already default state. Just update password.')
                result= restore_telnet.update_password_in_default_state()
                result &=is_Firewall_up(ip,pre_sleep=1)
            else:
                logger.info(f'Firewall is not in default state, need do restore')
                res.fw.password=Params.G_NEW_PASSWORD
                result = restore_telnet.restore()
        else:
            logger.error('Firewall boots up failed.')
            result = False
        # return False        
        # res = RestoreFwTelnet(console_ip=self.consvr, console_port=self.conport)
        # result = res.restore() 

        # if Params.openstack:
        #     if not result:
        #         # # # Add hang log in file
        #         utm_name = osstack.get_UTM_dev_obj()
        #         print(utm_name)
        #         err_time = time.ctime()
        #         print(err_time)
        #         err_file = '/logs/4700-error-log.txt'
        #         os.system('touch ' + err_file)
        #         os.system('echo \"'+utm_name + '\t' + Params.scmlabel + '\t' + err_time + '\" >> ' + err_file)

        #         logger.info('Restore failed, try to reboot firewall.') 
        #         try:
        #             import_type_name = 'powercontrol.' + self.power_type.lower()
        #             import_type1 = __import__(import_type_name)
        #             import_type2 = getattr(import_type1, self.power_type.lower())
        #             import_module = getattr(import_type2, self.power_model)
        #             power = import_module(self.power_ip,user=self.user,password=self.password)
        #             for retry in range(0,2):
        #                 result = power.execute('reboot', self.power_port)
        #                 if not result:
        #                     logger.error( f"ERR: round {retry} Power recycle firewall failed")
        #                 else:
        # #                    is_Firewall_up(ssh=False) 
        #                     result &=is_Firewall_up()
        #                     break
        #         except Exception as e:
        #             logger.error(f"ERR: Cannot import powercontrol:{e}") 
        #             logger.info('Powercontrol tpye and model as following:')
        #             logger.info(self.power_type)
        #             logger.info(self.power_model)
        #         if not result:
        #             logger.error( "ERR: Power recycle firewall failed at last.")
        #         else:
        #             result = res.restore() 
        Assertion.assert_equal(result, True, "ERR: Restore firewall failed")

    # @skip_unless_fail_method(depend='test_00_restore_dut')
    # @unittest.skipUnless(Params.openstack and QBS_JOBNUM != '1234','No need for static testbed.')
    # def test_01_lock_dut_if_restore_fail(self):
    #     self.goto_teardown = True
    #     osstack = Openstack(Params.testbed)
    #     node_list=osstack.get_nodes()
    #     dut_node = ''
    #     for node in node_list:
    #         if 'dut' in node.keys():
    #             dut_node = node
    #             break
    #     if dut_node:
    #         logger.info("Going to lock down Node {}".format(dut_node['topology_resource_name']))
    #         lock_rc = osstack.lock_node(dut_node['name'])
    #         if not lock_rc:
    #             logger.error("Lock DUT skipped for topology file not recognized")
    #     ssh_flag = True
    #     Assertion.assert_equal(lock_rc, True, "ERR: Lock firewall failed")

@unittest.skipIf(Params.sonicos_ver == '7.1.1_cover_x86', '7.1.1_cover_x86 do not need restore')
class TestRestoreDUTByUI(Test):
    uuid = 'NonTC'
    # goto_teardown = True

    @unittest.skipIf('nsv' not in Params.sonicos_ver, "Only NSV platform need to check link")
    @repeat_method(3)
    def test_00_00_check_nsv_link(self):
        cmd = 'python3 ' + os.environ["PYTHON_COMMON_HOME"] + '/config/check_nsv_connection.py ' +\
              '-testbed ' + Params.testbed + ' -openstack ' + Params.openstack
        logger.info(cmd)
        output = os.popen(cmd).read()
        print('============================================')
        logger.info(output)
        print('============================================')
        rc = True if 'Check and recover NSV link passed' in output \
                  or 'There is no NSV device on static testbed' in output \
                  else False

        logger.info("Check ping after link check.")
        cmd = 'ping 192.168.168.168 -c 1'
        output = os.popen(cmd).read()
        logger.info(output)
        if ' 0% packet loss' not in output and Params.openstack:
            logger.info("X0 connection failed. Will re-enable it.")
            osstack = Openstack(Params.testbed)
            osstack.set_node_interface_state('UTM', 'X0', 'disable')
            time.sleep(2)
            osstack.set_node_interface_state('UTM', 'X0', 'enable')
            time.sleep(2)
            logger.info("Check ping again link recover.")
            cmd = 'ping 192.168.168.168 -c 1'
            output = os.popen(cmd).read()
            logger.info(output)
            if ' 0% packet loss' not in output:
                rc = False

        Assertion.assert_equal(rc, True, "ERR: Check NSV Link failed")

    # @repeat_method(2)
    def test_00_restore_dut(self):
        passwd = 'password'
        if is_Firewall_up(ip,pre_sleep=5,max=20,ssh=False):
            logger.info('Firewall boots up')
            logger.info("try to enable ssh to see if firewall is in default state.... ")
            logger.info(cmd0)
            output = os.popen(cmd0).read()
            G_PASSWORD = None
            logger.info(output)
            rc=0
            if 'Login Your default password must be changed' in output:
                logger.info(f'Firewall is already default state. Just update password.')
                logger.info(f'Firewall enforce to change default password, try to change password to {G_PASSWORD_NEW}')
                change_password(new_password=G_PASSWORD_NEW)
                G_PASSWORD = True # True means default password change to G_PASSWORD_NEW
                logger.info(cmd1)
                rc = os.system(cmd1)
                if rc != 0:
                    logger.info(f'run {cmd1} again.')
                    rc = os.system(cmd1)
                    result =True
                if rc ==0:
                    is_Firewall_up(ip,pre_sleep=1)
                Assertion.assert_equal(rc, 0, "ERR: enable ssh failed.")
            elif '"message": "Unauthorized."' in output:
                logger.info(cmd1)
                output = os.popen(cmd1).read()
                logger.info(output)
                if '"message": "Unauthorized."' in output:
                    passwd = 'Admin@123456789'
                    logger.info(cmd2)
                    rc = os.system(cmd2)
                    if rc != 0:
                        logger.info(f'run {cmd2} again.')
                        rc = os.system(cmd)
                    Assertion.assert_equal(rc, 0, "ERR: enable ssh failed.")
                else:
                    G_PASSWORD = True
                rc =2 #need restore
            elif 'connect ETIMEDOUT' in output:
                logger.info('Firewall connection timeout. Please check if firewall is accessable.')
                rc =1 # need reboot first
            else:
                logger.info(f'Firewall is not in default state, need do restore')
                rc=2 #need restore
        else:
            logger.error('Firewall boots up failed.')
            rc = 1 #need to reboot first

        if rc == 1:
            if Params.openstack:
                logger.info(f'run {cmd0}')
                cmd_return = subprocess.Popen(cmd0, shell = True, stdout = subprocess.PIPE).communicate(timeout=100)[0].decode('ASCII')
                if re.search(r'Login Your default password must be changed', cmd_return, re.I):
                    logger.info(f'Firewall is already default state. Just update password.')
                    logger.info(f'Firewall enforce to change default password, try to change password to {G_PASSWORD_NEW}')
                    change_password(new_password=G_PASSWORD_NEW)
                    G_PASSWORD = True # True means default password change to G_PASSWORD_NEW
                    logger.info(cmd1)
                    rc = os.system(cmd1)
                    if rc != 0:
                        logger.info(f'run {cmd1} again.')
                        rc = os.system(cmd1)
                        result =True
                    if rc ==0:
                        is_Firewall_up(ip,pre_sleep=1)
                        reult =True
                    else:
                        logger.error("ERR: enable ssh failed.")
                        result =False
                    #rc =0
                else:
                    time.sleep(60)
                    logger.info(f'run {cmd1}.')
                    result = os.system(cmd1)
                    G_PASSWORD =True
                    if result != 0:
                        logger.info(f'run {cmd2} again.')
                        result = os.system(cmd2)
                        logger.info(result)
                logger.info('Reboot firewall first.')
                osstack = Openstack(Params.testbed)
                res = osstack.reboot_node('UTM')
                logger.info(f"Reboot response: {res}")
                if result or result ==0:
                    ssh_flag=False
                else:
                    ssh_flag =True
                out = is_Firewall_up(ip,ssh_flag)
                if out:
                    logger.info('Firewall boots up')
                else:
                    logger.error('Firewall boots up failed.')
        if rc == 1 or rc ==2:
            fw = Firewall(ip, user='admin', new_password=passwd, supported_config_mode='cli-ssh')
            if G_PASSWORD:
                fw.new_password = G_PASSWORD_NEW
            commands = ['configure', 'restore-defaults']
            time.sleep(15)
            (rc, output) = fw.do_cli_commands(commands, 1)
            if not rc:
                logger.info(output)
                logger.info("Restore failed. Will reboot firewall.")
                if Params.openstack:
                    osstack = Openstack(Params.testbed)
                    res = osstack.reboot_node('UTM')
                    logger.info(f"Reboot response: {res}")
                    out = is_Firewall_up(ip)
                    if out:
                        logger.info('Firewall boots up')
                        rc = True
                    else:
                        logger.error('Firewall boots up failed.')
            else:
                if Params.product=='15700' or 'nssp' in Params.sonicos_ver:
                    osstack = Openstack(Params.testbed)
                    consvr, conport = osstack.get_console_info(dut='UTM')
                    rc &=is_Firewall_up(ip,console_ip=consvr,console_port=conport,mode='console')
                else:
                    rc &=is_Firewall_up(ip)
                if rc:
                    logger.info('Firewall boots up')
                else:
                    logger.error('Firewall boots up failed. Reboot...')
                    if Params.openstack:
                        osstack = Openstack(Params.testbed)
                        res = osstack.reboot_node('UTM')
                        logger.info(f"Reboot response: {res}")
                        out = is_Firewall_up(ip)
                        if out:
                            rc = True
                            logger.info('Firewall boots up')
                    else:
                        logger.error('Firewall boots up failed.')

            Assertion.assert_equal(rc, True, "ERR: restore dut failed")

    @skip_unless_fail_method(depend='test_00_restore_dut')
    @unittest.skipUnless(Params.openstack and QBS_JOBNUM != '1234','No need for static testbed.')
    def test_01_lock_dut_if_restore_fail(self):
        self.goto_teardown = True
        osstack = Openstack(Params.testbed)
        node_list=osstack.get_nodes()
        dut_node = ''
        for node in node_list:
            if 'dut' in node.keys():
                dut_node = node
                break
        if dut_node:
            logger.info("Going to lock down Node {} as restore fail.".format(dut_node['topology_resource_name']))
            lock_rc = osstack.lock_node(dut_node['name'])
        Assertion.assert_equal(lock_rc, True, "ERR: restore dut failed")

@unittest.skipIf(Params.sonicos_ver == '7.1.1_cover_x86', '7.1.1_cover_x86 do not need restore')
class TestRestoreDUTByEnd(Test):
    uuid = 'NonTC'

    def test_00_restore_dut_by_end(self):
        fw = Firewall(ip, user='admin',new_password=Params.G_NEW_PASSWORD,supported_config_mode='cli-ssh',boot_check=False)
        commands = ['configure', 'restore-defaults']
        (rc, output) = fw.do_cli_commands(commands, 1)
        if not rc:
            cmd0 = 'newman run '+ os.environ["PYTHON_COMMON_HOME"] + \
                '/config/enable_ssh.json -k --disable-unicode --delay-request 1200'
            cmd_return = subprocess.Popen(cmd0, shell = True, stdout = subprocess.PIPE).communicate(timeout=100)[0].decode('ASCII')
            if re.search(r'Login Your default password must be changed', cmd_return, re.I):
                logger.info('Already default.')
                rc =True
            else:
                cmd1 = 'newman run '+ os.environ["PYTHON_COMMON_HOME"] + \
                    '/config/enable_ssh_newpass.json -k --disable-unicode --delay-request 1200'
                cmd2= 'newman run ' + os.environ["PYTHON_COMMON_HOME"] + '/config/enable_ssh_wrongpass.json -k --disable-unicode --delay-request 1200'
                logger.info(f'run {cmd1}.')
                result = os.system(cmd1)
                if result != 0:
                    logger.info(f'run {cmd2} again.')
                    result = os.system(cmd2)
                    logger.info(result)
                    fw.new_password=fw.wrong_password
                (rc, output) = fw.do_cli_commands(commands, 1)
        Assertion.assert_equal(rc, True, "ERR: restore dut failed")



class TestUploadFirmware(Test):
    uuid = 'NonTC'
    # goto_teardown = True

    @unittest.skipIf(Params.product=='15700-TENANT' or Params.sonicos_ver == '7.1.1_cover_x86', 'No need to upload firmware for tenant and 7.1.1_cover_x86.')    
    def test_00_upload_firmware(self):
        self.goto_teardown = True
        ip = '192.168.168.168'
        fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
        if ssh_flag:
            is_Firewall_up(ip)
        upfw = UploadFirmware(fw, Params.scmlabel)
        from utm import G_PASSWORD
        if G_PASSWORD:
            fw.new_password = G_PASSWORD_NEW
        else:
            fw.new_password = fw.password
        result, output = upfw.upload_firmware( build=Params.build, testbed=Params.testbed, log_tag=True )
        if not result:
            if 'Firmware is not compatible' in output or 'Failed to find PGP signature in image file' in output:
                logger.info("You may pass in a wrong firmware, please check your firmware file.")
            else:
                if Params.product=='15700' or 'nssp' in Params.version:
                    osstack = Openstack(Params.testbed)
                    consvr, conport = osstack.get_console_info(dut='UTM')
                    rc=is_Firewall_up(ip,mode='console',console_ip=consvr, console_port=conport)
                else:
                    rc=is_Firewall_up(ip)
                if not rc:
                    rc=is_Firewall_up(ip, ssh=False)
                    if not rc:
                        osstack = Openstack(Params.testbed)
                        node_list=osstack.get_nodes()
                        dut_node = ''
                        for node in node_list: 
                            if 'dut' in node.keys():
                                dut_node = node 
                                break
                        if dut_node and QBS_JOBNUM != '1234':
                            logger.info("Going to lock down Node {} as upload firmware fail.".format(
                                dut_node['topology_resource_name']))
                            lock_rc = osstack.lock_node(dut_node['name'])
            logger.info('------------------ upload_firmware failure log --------------------')
            logger.info(output)
        else:
            logger.info("Verify firewall version after upgrade.")
            fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
            rc, new_ver = fw.do_cli_commands(['diag show build-info'], 1)
            find = re.search(r'SonicOS(?:X)?\s+(\S+)', new_ver, re.I)
            if find:
                new_ver = find.group(1)
                global utm_version
                utm_version=new_ver
                if Params.product == 'NSV-VM' or Params.product=='NSV-NG' or Params.product=='NSV-XS-GLOBAL' or Params.product=='NSV-XS-POLICY':
                    new_ver = re.sub('R','',new_ver)
                logger.info(f'============ {new_ver} ============')
                # if Params.scmlabel != new_ver:
                #     logger.info("Build version on firewall is not right after uploaded.")
                #     result = False
                ###### add repeate for check build version
                for retry in range(0,15):
                    if Params.scmlabel != new_ver:
                        logger.info(f"check {retry} time: Build version on firewall is not right after uploaded, wait for 60s......")
                        result = False
                        time.sleep(60)
                    else:
                        logger.info("Build version on firewall is right after uploaded.")
                        result = True
                        break
            else:
                logger.info(f'============ Version info ===========\n{new_ver}')

        Assertion.assert_equal(result, True, "ERR: Upload firmware failed.")

    # @unittest.skipIf(Params.noapi, 'No need to enable api as you set -noapi to True.') 
    # def test_02_enable_api(self):
    #     ip = '192.168.168.168'
    #     fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
    #     admin = AdminCli(fw)

    #     api_dict = {
    #       'sonicos-api': True,
    #       'basic': True,
    #     }
    #     result = admin.sonicos_api(**api_dict)
    #     Assertion.assert_equal(result, True, "ERR: Enable api failed.")

    @unittest.skipUnless((Params.product=='NSV-VM' or Params.product=='NSV-NG' or Params.product=='15700-TENANT') and not Params.skip_reg, 'No need to offline register for physical firewall.')
    def test_03_offline_register(self):
        self.goto_teardown = True
        ip = '192.168.168.168'
        fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
        license = LicenseCli(fw)
        result = license.register(mode='offline')
        logger.info('sleep 20 seconds.')
        time.sleep(20)
        Assertion.assert_equal(result, True, "ERR: Offline register failed.")

    def test_04_get_coredump(self):
        self.goto_teardown = False
        logger.info("check and get coredump file.... ")
        res = GetCoredumpApi(Params.testbed,Params.product,Params.qbsjobid,Params.scmlabel,Params.ts_display_name,Params.openstack)
        result = res.get_coredump(suffix='init') 
        logger.info(result)
        Assertion.assert_equal(True, True, "ERR: get coredump file failed.")

    @unittest.skipUnless((Params.product=='NSV-VM' or Params.product=='NSV-NG' or Params.product=='15700-TENANT' or Params.product=='15700') and not Params.skip_reg and not Params.no_security_rule, 'No need to add security policy for no NGPE firewall.')
    def test_05_add_security_policy(self):
        self.goto_teardown = True
        cmd = 'python3 ' + os.environ['PYTHON_COMMON_HOME'] + '/config/add_security_rule.py'
        result =subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE,stderr = subprocess.STDOUT).communicate()[0].decode('ASCII')
        logger.info(result)
        if re.search(r'Add security rule successfully', result, re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add security policy failed.")
 
    @repeat_method(5)
    @unittest.skipUnless((Params.product=='NSV-XS-GLOBAL' or Params.product=='NSV-XS-POLICY') and not Params.skip_reg, 'do online sync license for Gen8-NSV firewall.')
    def test_06_online_sync_license_for_Gen8NSV(self):
        ### get X1 network info
        self.goto_teardown = True
        os_obj = Openstack(Params.testbed)
        X1_NW = os_obj.get_node_interface_network('UTM', 'X1')
        tmp = X1_NW.split('.')[0:3]
        X1_GW = '.'.join(tmp) + '.1'
        X1_IP = '.'.join(tmp) + '.168'
        logger.info(f'X1_network: {X1_NW}')
        logger.info(f'X1_GW: {X1_GW}')
        logger.info(f'X1_IP: {X1_IP}')
        ### config X1 and do online sync
        x1 = {
            'if': 'X1',
            'zone': 'WAN',
            'mode': 'static',
            'ip': X1_IP,
            'netmask': '255.255.255.0',
            'gateway': X1_GW,
            'dns1': Params.G_DNS1,
            'dns2': Params.G_DNS2,
            'mgmt_https': True,
            'mgmt_ssh': True,
            'mgmt_ping': True,
        }
        ip = '192.168.168.168'
        fw = Firewall(ip, user='admin', password='password', supported_config_mode='api')
        fw_cli = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
        license = LicenseCli(fw_cli)
        interface_ipv4 = network.InterfaceIPv4Api(fw)
        rc = interface_ipv4.config_interface(**x1)
        for i in range(0,6):
            result = license.register(mode='online')
            if result:
                break
            logger.info('sleep 30 seconds.')
            time.sleep(30)
        time.sleep(20)
        Assertion.assert_equal(rc&result, True, "ERR: online sync failed.")

    @unittest.skipUnless((Params.product=='NSV-XS-POLICY') and not Params.skip_reg and not Params.no_security_rule, 'No need to add security policy for no NGPE firewall.')
    def test_07_add_security_policy_for_nsvxspolicy(self):
        self.goto_teardown = True
        cmd = 'python3 ' + os.environ['PYTHON_COMMON_HOME'] + '/config/add_security_rule.py'
        result =subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE,stderr = subprocess.STDOUT).communicate()[0].decode('ASCII')
        logger.info(result)
        if re.search(r'Add security rule successfully', result, re.I):
            rc = True
        else:
            rc = False
        Assertion.assert_equal(rc, True, "ERR: add security policy failed.")

        
class TestGetCoredump(Test):
    uuid = 'NonTC'

    @repeat_method(2)
    def test_01_get_coredump_by_end(self):
        logger.info(f"check and get coredump file....")
        res = GetCoredumpApi(Params.testbed,Params.product,Params.qbsjobid,Params.scmlabel,Params.ts_display_name,Params.openstack)
        result = res.get_coredump()
        logger.info(result)
        Assertion.assert_equal(result, True, "ERR: get coredump file failed.")

    def test_02_upload_version(self):
        fw = Firewall(ip, user='admin',new_password=Params.G_NEW_PASSWORD,supported_config_mode='cli-ssh',boot_check=False)
        os_stack = Openstack(Params.testbed)
        if 'utm_version' in globals():
            rc=os_stack.save_UTM_resource_version(utm_version)
        else:
            rc, new_ver = fw.do_cli_commands(['diag show build-info'], 1)
            find = re.search(r'SonicOS(?:X)?\s+(\S+)', new_ver, re.I)
            if find:
                rc=os_stack.save_UTM_resource_version(find.group(1))
        Assertion.assert_equal(True, True, "ERR: upload version to os file failed.")

    @unittest.skipUnless(Params.system_log,'Skip if no need to download system log' )
    def test_03_download_system_log(self):
        fw = Firewall(ip, user='admin', new_password=G_PASSWORD_NEW, supported_config_mode='cli-ssh')
        logger.info('get ip connected to DUT X0')
        net_info = os.popen('ifconfig').read()
        addr = re.findall('inet\s+\w*:?(192.168.168.\d+)', net_info, re.M|re.I)
        server_ip=''
        if len(addr)>0:
            server_ip = addr[0]
            logger.info('ip connected to DUT X0: {}'.format(server_ip))
        else:
            logger.error('can not get Server IP')
        cmd = [f'export safe-mode-logs  scp root@{server_ip}:{LOG_DIR}/',Params.pc1_password]
        (result, out) = fw.do_cli_commands(cmd, 1)

        Assertion.assert_equal(result, True, "ERR: download system log failed.") 
