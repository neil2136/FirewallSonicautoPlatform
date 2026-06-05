from io import StringIO
import subprocess
import re
import os
import json
import yaml
from runner.settings import logger
import xml.etree.ElementTree as ET
import string 
import struct
from tempfile import TemporaryFile

class SSDH:
    def __init__(self, build):
        self.build = build
        
    def is_build_sig(self):
        if not os.path.exists(self.build):
            return False
        output = subprocess.Popen(f'ssdh -i {self.build}', shell=True,stdout = subprocess.PIPE).communicate()[0].decode('ASCII')
        if re.search(r'^Invalid header', output, re.I):
            logger.debug(f'Invalid header for the build {self.build}')
            return False
        try:
            data= subprocess.Popen(f'ssdh -x {self.build}', shell=True,stdout = subprocess.PIPE).communicate()[0].decode('ASCII')
            self.root= ET.fromstring(data)
            return True
        except Exception as e:
            logger.info(f'Can not load image header infomation:{e}')

    def get_product_suffix(self):
        try:
            return self.root.find('firmware_version').find('suffix').text
        except Exception as e:
            logger.info(f'Fail to get version suffix: {e}')

    def get_firmware_version(self):
        try:
            version = self.root.find('firmware_version').find('main').text
            pattern = r'(\d\.\d+\.\d+)\.\d+(.*)'
            match = re.search(pattern, version, re.I)
            if match:
                version = match.group(1)
                if match.group(2):
                    version += match.group(2)
                return version
            else:
                logger.error('Fail to get firmware version')
                logger.info(version)
        except Exception as e:
            logger.info(f'Fail to get version: {e}')     

    def get_product_name(self):
        try:
            return self.root.find('target').find('compatibility_list').find('li').find('prodcode').text
        except Exception as e:
            logger.info(f'Fail to get product name: {e}')

    def get_version_total_string(self):
        version = self.get_firmware_version()
        suffix = self.get_product_suffix()
        if version and suffix:
            return version+suffix
        else:
            logger.error('Fail to get firmware version or suffix')

if __name__ == '__main__':
    c = SSDH('/logs/downloads/sgao-1624420440799_sw_tz_370w_eng.7.0.2-R1598.bin.sig')
    print(c.is_build_sig())
    print(c.get_firmware_version())
    print(c.get_product_suffix())
    print(c.get_version_total_string())

