import sys
import os
import re
import argparse
from pprint import pprint
import platform
from runner.settings import Params, logger
sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append(os.environ["PYTHON_SONICOS_HOME"])
from util.openstack import Openstack
from utm import Firewall
from lib.modules.CLI.system import StatusCli
from lib.modules.CLI.system import SettingCli
from lib.modules.CLI.diag import DiagCli

class UploadFirmware():
    '''TestUploadFirmware Class'''
    def __init__(self, fw, version):
        self.fw = fw
        self.version = re.sub(r"(^7\.\d+\.\d+)\.\d+", r"\1", version) 
        self.system = StatusCli(self.fw)

    def compare_ver(self):
        status = self.system.show_version()
        model = self.system.show_status()
        pattern = re.compile(r'Firmware Version.*(\d+\.\d+\.\d+\S+)', re.I)
        ver = pattern.findall(status)
        if re.search('Model:[\t|\s]*NSv',model,re.I):
            ver[0]=re.sub('R','',ver[0])
        if ver and ver[0] == self.version or (len(ver[0])>= 33 and re.search(r'' + ver[0] + '', self.version, re.I)):
            logger.info('Firewall has the same version as uploaded. Omit uploading.')
            return True
        else:

            logger.info('Firewall has different build with uploaded. Prepare uploading.')
            return False

    def upload_firmware(self, build, boot_mode='4', testbed='', log_tag=False):
        if self.compare_ver():
            if boot_mode == '4':
                boot_mode = '2'
            elif boot_mode == '3':
                boot_mode = '1'
            if log_tag:
                return True, 'No need to upload firmware'
            return True
        # consvr = ''
        # conport = ''
        # # # # Get console information
        # if con_server and con_port:
        #     consvr = con_server
        #     conport = con_port
        # elif testbed:
        #     logger.info('------------ ' + testbed + '------------')
        #     ostack = Openstack(testbed)
        #     console_info = ostack.get_console_info()
        #     if console_info:
        #         consvr = console_info[0]
        #         conport = console_info[1]
        # else:
        #     out = os.popen('hostname').read()
        #     hostname = out.split('-')[0]
        #     if hostname:
        #         logger.info('------------ ' + hostname + '------------')
        #         ostack = Openstack(hostname)
        #         console_info = ostack.get_console_info()
        #         if console_info:
        #             consvr = console_info[0]
        #             conport = console_info[1]
        # logger.info('Console server: ' + consvr)
        # logger.info('Console port:   ' + conport)

        # if (not consvr or not conport) and (boot_mode == 4 or boot_mode == 2):
        #     logger.error('Please pass in UTM console info for enabling ssh managment.')
        #     return False

        setting = SettingCli(self.fw)
        pprint(setting)
        import_dict = {
            'protocol': 'scp',
            'passwd': Params.pc1_password,
            'server': '',
            'user': 'root',
            'file': build
        }
        if 'ubuntu' in platform.platform().lower():
            import_dict['passwd']='sonicauto'
        # # # Get IP connected to DUT X0
        ret = os.popen('ifconfig')
        output = ret.read()
        network_pattern = re.compile(r'\.\d+$')
        network = network_pattern.split(self.fw.ip)[0]
    
        ip_pattern = re.compile('[inet addr:|inet](' + network + '\.\d+)')
        ip = ip_pattern.findall(output)
        if ip:
            import_dict['server'] = ip[0]
    
        if not import_dict['server']:
            logger.error('Can\'t get LAN PC IP.')
            if log_tag:
                return False, 'Can\'t get LAN PC IP.'
            return False
        # print(import_dict)
    
        # # # make softlink under /root if build file is not in /root folder
        if '/' in build:
            path = '/' + build.split('/')[1]
            logger.info('=========== ' + path + '============')
            logger.info('ln -s ' + path + ' /root/')
            os.system('ln -s ' + path + ' /root/')

        pprint(import_dict)

        # # # skip ssh host key check
        diag = DiagCli(self.fw)
        diag.config_ssh_host_key_check()

        # # # import firmware
        if boot_mode == '3' or boot_mode == '4':
            rc_log = ''
            if log_tag:
                (rc, rc_log) = setting.import_firmware(log_tag=True, **import_dict)
            else:
                rc = setting.import_firmware(**import_dict)
            if not rc:
                logger.error('Import firmware failed.')
                if log_tag:
                    return False, rc_log
                return False
            elif rc != True:
                logger.info('Same firmware, skip upload')
                if log_tag:
                    return True, 'Same firmware, skip upload'
                return True
    
        # # # boot new firmware
        mode = {
            '1': ['current', ''],
            '2': ['current', 'factory-default'],
            '3': ['uploaded', ''],
            '4': ['uploaded', 'factory-default']
        }
        rc = setting.boot_firmware(mode[str(boot_mode)][0], mode[str(boot_mode)][1])
        # rc = setting.boot_firmware(mode[str(boot_mode)][0], mode[str(boot_mode)][1], str(consvr), str(conport))

        if not rc:
            logger.error('Boot firmware failed.')
            if log_tag:
                return False, 'Boot firmware failed.'
            return False

        logger.info('Upload firmware passed.')
        if log_tag:
            return True, 'Upload firmware passed.'
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='upload firmware.')
    parser.add_argument('-testbed', '--testbed', type=str, dest='testbed', required=True, help='testbed ID, like: VTB518')
    parser.add_argument('-build', type=str, dest='build', required=True, help='build name with absolute path')
    parser.add_argument('-ip', type=str, dest='ip', help='firewall ip')
    args = parser.parse_args()

    testbed = args.testbed
    ip = args.ip
    if not ip:
        ip = '192.168.168.168'
    build = args.build
    fw = Firewall(ip, user='admin', password='password', supported_config_mode='cli-ssh')
    version = '6.5.4.4-39n'

    upfw = UploadFirmware(fw, version)
    out = upfw.upload_firmware(
        build=build,
        testbed=testbed
        #log_tag=True
    )
    print(out)
