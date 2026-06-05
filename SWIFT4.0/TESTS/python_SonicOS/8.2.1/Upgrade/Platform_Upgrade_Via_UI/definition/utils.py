import re
from runner.settings import logger
from definition.settings import fwupgradeapi, hostconf

def upgrade_firmware_previous(path):
    resp = fwupgradeapi.upload_firmware_by_message(path)
    if resp:
        if re.search('Firmware uploaded successfully', resp, re.I):
            bootres = fwupgradeapi.boot_fw(mode=3)
            logger.info(bootres)
            return bootres
        elif re.search('same Firmware already exists', resp, re.I):
            logger.info(
                'error: the same Firmware already exists, do not need upgrade version')
            return True
    else:
        return False


def upgrade_firmware_current(path):
    resp = fwupgradeapi.upload_firmware_by_message(path)
    if resp:
        if re.search('Firmware uploaded successfully', resp, re.I):
            bootres = fwupgradeapi.boot_fw(mode=3)
            logger.info(bootres)
            return bootres
        elif re.search('same Firmware already exists', resp, re.I):
            logger.info(
                'error: previous version can not upgrade successful in the steps above.')
            return False
    else:
        return False
