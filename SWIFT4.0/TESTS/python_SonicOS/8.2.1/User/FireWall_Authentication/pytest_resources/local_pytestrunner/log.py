#!/usr/local/bin/python3.4
__author__ = 'Syed Maaz'

import os.path
import sys
import logging
import datetime

# get the base suite file name
list_argv = sys.argv
for args in range(len(list_argv)):
    if ".py" in list_argv[args]:
        index = args
base_suite_file = os.path.basename(sys.argv[index]).split(".")
base_suite_file_name = base_suite_file[0]

current_path = os.path.dirname(os.path.abspath(__file__)).split("/")
root_dir = os.sep.join(str(__file__).split(os.sep)[0:-5]) + os.sep

print("Parent project folder is: " + root_dir)

# currently log_level is set to Debug
log_level = "DEBUG"
DEBUG2 = 9
logging.addLevelName(DEBUG2, "DEBUG2")


def setup_logger(name, log_file, level=logging.INFO):
    """Function setup as many loggers as you want"""
    file_handler = logging.FileHandler(log_file, mode='w+')
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)6s] [%(filename)15s:%(lineno)3s] [%(funcName)30s] - %(message)s')
    if level == 9:
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)6s] [%(filename)15s:%(lineno)3s] [%(funcName)30s] - %(message)s')
    file_handler.setFormatter(formatter)
    root_logger = logging.getLogger(name)
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)


def debug2(self, message, *args, **kws):
    if self.isEnabledFor(DEBUG2):
        self._log(DEBUG2, message, args, **kws)
logging.Logger.debug2 = debug2
TIMESTAMP = str(datetime.datetime.now().replace(microsecond=0)).replace(" ", "_").replace(":", "_")
results_dir_path = os.path.join(root_dir, "User", "FireWall_Authentication", "results")
logs_dir_path = os.path.join(results_dir_path, "logs")
csv_dir_path = os.path.join(results_dir_path, "csv")
print("logs_dir", logs_dir_path)
destination_log_path = os.path.join(logs_dir_path, base_suite_file_name + "_" + TIMESTAMP)
os.path.exists(logs_dir_path) or os.makedirs(logs_dir_path)
info_filename = os.path.join(logs_dir_path, str(base_suite_file_name) + ".log")
os.path.exists(csv_dir_path) or os.makedirs(csv_dir_path)
pytest_result_csv = os.path.join(csv_dir_path, str(base_suite_file_name) + ".csv")

if log_level == "debug":
    log_level= logging.DEBUG
elif log_level == "debug2":
    log_level = DEBUG2
else:
    log_level = logging.INFO

setup_logger('all_logs', info_filename, log_level)
