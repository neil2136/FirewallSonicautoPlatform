import os
import threading
import pexpect
import signal
import time
from runner.settings import logger

class RsyncTel:

    def __init__(self, testbed):
        self.testbed = testbed
        self.remote_user = "mlai"
        self.remote_host = "10.203.12.105"
        self.password = "S0nicw@ll"
        self.retry_times = 3
        self.retry_interval = 5
        self.timeout = 600

    def _get_sync_dir(self):
        if any(x in self.testbed for x in ['VTB5', 'VTB7', 'VTB8']):
            return "sync_from_SH"
        elif 'VTB6' in self.testbed:
            return "sync_from_SC"
        elif 'VTB9' in self.testbed:
            return "sync_from_BLR"
        return "others"

    def _run_cmd_with_password(self, cmd):
        logger.info(f"[Rsync] run: {cmd}")
        try:
            child = pexpect.spawn(cmd, encoding="utf-8", timeout=self.timeout)
            output = ""
            while True:
                i = child.expect(["yes/no", "password:", pexpect.EOF, pexpect.TIMEOUT])
                if i == 0:
                    logger.info("[Rsync] ssh first connect, send yes")
                    child.sendline("yes")
                elif i == 1:
                    logger.info("[Rsync] send password")
                    child.sendline(self.password)
                elif i == 2:
                    # EOF
                    output += child.before
                    break
                elif i == 3:
                    logger.error("[Rsync] command timeout, killing child process")
                    child.kill(signal.SIGKILL)
                    return False

            output += child.before
            output_lower = output.lower()
            if "permission denied" in output_lower or "rsync error" in output_lower:
                logger.error(f"[Rsync] command failed:\n{output}")
                return False

            logger.info(output)
            return True

        except Exception as e:
            logger.error(f"[Rsync] exception: {e}")
            return False

    def sync_to_analysis_server(self, local_folder, file_name):
        sync_dir = self._get_sync_dir()
        remote_base = f"/home/mlai/coredump_file/{sync_dir}/buildtestlogs"
        parent, last = os.path.split(local_folder)
        _, second_last = os.path.split(parent)
        remote_subfolder = f"{second_last}/{last}"
        remote_path = f"{remote_base}/{second_last}"

        logger.info(f"[Rsync] remote_subfolder={remote_subfolder}")

        mkdir_cmd = f"ssh {self.remote_user}@{self.remote_host} 'mkdir -p {remote_path}'"
        for attempt in range(1, self.retry_times + 1):
            if self._run_cmd_with_password(mkdir_cmd):
                break
            logger.warning(f"[Rsync] mkdir attempt {attempt} failed, retry in {self.retry_interval}s")
            time.sleep(self.retry_interval)
        else:
            logger.error("[Rsync] mkdir failed after retries")
            return False

        rsync_cmd = (
            f"rsync -az --progress "
            f"{local_folder}/ "
            f"{self.remote_user}@{self.remote_host}:{remote_base}/{remote_subfolder}/"
        )

        for attempt in range(1, self.retry_times + 1):
            if self._run_cmd_with_password(rsync_cmd):
                logger.info("[Rsync] rsync success")
                return True
            logger.warning(f"[Rsync] rsync attempt {attempt} failed, retry in {self.retry_interval}s")
            time.sleep(self.retry_interval)

        logger.error("[Rsync] rsync failed after retries")
        return False

    def sync_to_analysis_server_async(self, local_folder, file_name):
        def target():
            try:
                success = self.sync_to_analysis_server(local_folder, file_name)
                if not success:
                    logger.error(f"[Rsync] async rsync failed for {local_folder}")
            except Exception as e:
                logger.error(f"[Rsync] async thread exception: {e}")

        logger.info("[Rsync] start async rsync thread")
        t = threading.Thread(target=target)
        t.start()
        return t