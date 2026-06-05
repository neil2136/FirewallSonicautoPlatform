__author__ = 'sgao'
from global_var import *

class Local_HA_Lib():
    def __init__(self):
        self.result = True

    def upload_firmware_HA(self, fw_cli, fw_console):
        max_retries = 3          # Maximum number of retry attempts
        retry_interval = 30      # Delay (in seconds) between retries
        target_version = Params.scmlabel  # Target firmware version to match (improves readability)

        # Initial check prompt (centered display)
        logger.info(' Check current FW version matches expected build '.center(40, '-'))

        # Loop through retry attempts (1-based index for user-friendly messaging)
        for attempt in range(1, max_retries + 1):
            # Attempt-specific prompt
            logger.info(f' Firmware check attempt {attempt}/{max_retries} '.center(40, '-'))
            
            # Execute CLI command to fetch version info (timeout after 1 second)
            ret, output = fw_console.do_cli_commands(['diag show build'], 1)
            
            # Log detailed CLI output (optional, useful for debugging)
            logger.debug(f'CLI command output: {output}')  # Remove if debug logs are unnecessary
            # Log version comparison (user-facing info)
            logger.info(f'Expected version: {target_version}, Actual version: {output}')

            # Check if current version matches the target
            if target_version in output:
                logger.info(f'Success: Current FW version matches expected ({target_version}). No upload needed.')
                return True  # Exit early as version is already correct
        
            # Handle retry logic (skip final retry message)
            if attempt < max_retries:
                logger.warning(f'Version mismatch (attempt {attempt}). Retrying in {retry_interval}s...')
                time.sleep(retry_interval)  # Pause before next attempt
        
        logger.info(' Start to upload new firmware '.center(40,'-'))
        upfw = UploadFirmware(fw_cli, Params.scmlabel)
        result = upfw.upload_firmware(boot_mode='4',build=Params.build, testbed=Params.testbed)

        time.sleep(5)
        logger.info(' Enable Api '.center(40,'-'))

        cmds = ['config', 'administration', 'sonicos-api','basic', 'commit', 'end','exit']
        (ret,output) = fw_console.do_cli_commands(cmds, 1)
        logger.info(ret)
        result &= ret

        time.sleep(5)
        logger.info(' Enable SSH '.center(40, '-'))
        cmds = ['config', 'interface x0', 'management ssh', 'commit', 'end', 'exit']
        (ret, output) = fw_console.do_cli_commands(cmds, 1)
        logger.info(ret)
        result &= ret

        logger.info(" Check and get coredump file ".center(40,'-'))
        res = GetCoredumpTel(Params.testbed)
        result &= res.get_coredump()

        return result
