# This is a common library for FW configuration which internally calls different library based on authentication methods

from libs.fw_configuration import *


class CommonLib(FWConfiguration):

    # Selecting username and password based on auth methods
    def select_valid_unpw(self, auth):
        user_name = ""
        password = ""
        if auth == "Local":
            user_name = local_user_name
            password = local_user_password
        elif auth == "LDAP":
            user_name = ldap_user_name
            password = ldap_user_password
        elif auth == "RADIUS":
            user_name = radius_user_name
            password = radius_user_password
        elif auth == "TACACS":
            user_name = tacacs_user_name
            password = tacacs_user_password
        elif auth == "LDAP-Local":
            user_name = ldap_user_name
            password = ldap_user_password
        elif auth == "RADIUS-Local":
            user_name = radius_user_name
            password = radius_user_password
        elif auth == "TACACS-Local":
            user_name = tacacs_user_name
            password = tacacs_user_password
        return user_name, password

    # Checks whether process is running or not Windows/OSX/Linux
    def is_process_running(self, process_name):
        is_process_running = False
        is_process_running = not os.system('tasklist | findstr ' + process_name)
        logger.info('Is process "' + process_name + '" running - ' + str(is_process_running))
        return is_process_running

    # Wait for a process to stop
    def wait_for_process_to_stop(self, process_name, wait_time=10):
        i = 0
        try:
            while i <= wait_time and self.is_process_running(process_name):
                # Sleep while waiting for process to stop
                time.sleep(1)
                logger('Timeout: ' + str(i) + ' seconds elapsed waiting for "' + process_name + '" to stop.')
                i += 1
            assert i < wait_time, 'ERR: ' + str(
                wait_time) + ' seconds elapsed waiting for "' + process_name + '" to stop'
            return True
        except Exception as e:
            logger("ERR: Exception Occurred")
            logger(e)
            raise

    # Kill the running process
    def kill_process(self, process_name):
        try:
            # Checks whether process is running or not
            result = self.is_process_running(process_name)
            if result:
                os.popen(('taskkill /F /IM ' if client_platform == 'win' else 'killall ') + process_name).read()
                process_stopped = self.wait_for_process_to_stop(process_name)
                assert process_stopped, 'ERR: Process: ' + process_name + ' is not killed successfully'
                logger.info('Process: ' + process_name + ' is killed successfully')
                return True
        except Exception as e:
            logger.error("ERR: Exception Occurred")
            logger.error(e)
            return False

    # Execute windows command with admin privileges
    def execute_windows_command_as_admin(self, command, with_extreme_privileges=False, timeout=None):
        import ctypes
        if type(command) not in [list, str]:
            raise Exception('Err: Command can be either list or str')
        if timeout is not None and type(timeout) not in [int, float]:
            raise Exception('Err: timeout can be either int or float')

        # write command to a file, so that it will be read and executed by helper python program running as admin
        with open(mount_logs_cmdline + '.cmdline', 'w+') as cmdline:
            cmdline.write(str({'command': command, 'timeout': timeout}))

        # set exitcode in result file as None, program stops waiting when this value becomes Non None
        with open(mount_logs_cmdline + '.result', 'w+') as result:
            result.write(str({"exitcode": None}))

        logger.info('Executing command ' + ('with extreme privileges' if with_extreme_privileges else 'as admin')
                    + ': ' + command if type(command) == str else ' '.join(command))
        power_run = power_run_base_path + os.sep.join(['PowerRun.exe'])
        helper = os.path.join(root_dir, "User", "FireWall_Authentication", "libs", ".run_as_admin_helper.py")
        if with_extreme_privileges:
            # Run helper python program with highest privileges
            self.execute_windows_command([power_run, sys.executable, helper])
        elif ctypes.windll.shell32.IsUserAnAdmin():
            # Run as normal command if already running as admin
            return self.execute_windows_command(command, timeout=timeout)
        else:
            # Start the helper python program as admin which will then execute the Command.
            ctypes.windll.shell32.ShellExecuteW(None, 'runas', sys.executable, '"' + helper + '"', None, 1)

        # read the result file written by helper program
        result = eval(self.read_from_file(mount_logs_cmdline + '.result'))
        logger.info(result)

        # workaround for waiting until the command execution completes
        while result['exitcode'] is None:
            time.sleep(1)
            result = eval(self.read_from_file(mount_logs_cmdline + '.result'))

        # remove the temporary result file
        os.remove(mount_logs_cmdline + '.result')
        logger.info('exitcode: ' + str(result['exitcode']))
        return result['exitcode'], result['stdout'], result['stderr']

    # Execute windows command
    def execute_windows_command(self, command: str or list or tuple, timeout: int = None):
        logger.info('Executing command: ' + (command if type(command) is str else ' '.join(command)))
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, bufsize=-1)
        exitcode = process.wait(timeout=timeout)
        logger.info('exitcode: ' + str(exitcode))
        stdout = process.stdout.read().decode(encoding='utf-8').strip().replace('\r', '')
        stderr = process.stderr.read().decode(encoding='utf-8').strip().replace('\r', '')
        return exitcode, stdout, stderr

    # Read the file content located in the client
    def read_from_file(self, file_name):
        file = open(file_name, 'r')
        content = file.read()
        file.close()
        return content

    # Enable the network adapter.
    def enable_network_adapter(self, adapter_name):
        logger.info("Enabling the network adapter: " + adapter_name)
        enable_cmd = "PowerShell Enable-NetAdapter -Name " + adapter_name + " -Confirm:$false"
        logger.info(enable_cmd)
        result = self.execute_windows_command_as_admin(command=enable_cmd, with_extreme_privileges=False)
        if result[0] == 0:
            logger.info("Successfully enabled the network adapter: " + adapter_name)
        else:
            logger.info(result[2])
            logger.info("Unable to enable the network adapter: " + adapter_name)

    # Disable the network adapter.
    def disable_network_adapter(self, adapter_name):
        logger.info("Disabling the network adapter: " + adapter_name)
        disable_cmd = "net use X: {swift_path} /user:{user} {pwd} /persistent:yes || PowerShell Disable-NetAdapter " \
                      "-Name {adapter} -Confirm:$false".format(swift_path=mount_logs_path, user=mount_logs_username,
                                                               pwd=mount_logs_password, adapter=adapter_name)
        logger.info(disable_cmd)
        result = self.execute_windows_command_as_admin(command=disable_cmd, with_extreme_privileges=False)
        if result[0] == 0:
            logger.info("Successfully disabled the network adapter: " + adapter_name)
        else:
            logger.info(result[2])
            logger.info("Unable to disable the network adapter: " + adapter_name)


