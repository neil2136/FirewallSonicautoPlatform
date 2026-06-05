# This is not for general usage

import ctypes
import os
import subprocess

from pytest_resources.common_require import *

# run only if main program (not imported module) an has admin privileges
if __name__ == '__main__' and ctypes.windll.shell32.IsUserAnAdmin():
    os.path.exists(mount_logs_cmdline) or exit(-1)

    # read command and timeout from file
    with open(mount_logs_cmdline + '.cmdline', 'r') as cmdline:
        command_info = eval(cmdline.read())
    os.remove(mount_logs_cmdline + '.cmdline')
    timeout = command_info['timeout']
    command = command_info['command']
    try:
        # start command execution as admin
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=-1)
        # wait until the process completes and obtain exitcode
        exitcode = process.wait(timeout=timeout)

        stdout = process.stdout.read().decode(encoding='utf-8').strip().replace('\r', '')
        stderr = process.stderr.read().decode(encoding='utf-8').strip().replace('\r', '')

    except Exception as ex:
        exitcode = -1
        stdout = ''
        stderr = str(type(ex)) + ' ' + str(ex)

    with open(mount_logs_cmdline + '.result', 'w') as result:
        # write exitcode, stdout and stderr to a file
        result.write(str({'exitcode': exitcode, 'stdout': stdout, 'stderr': stderr}))
    exit(0)

