import logging
import pprint
import os
import sys
from pathlib import Path

# define log file and result file
base_suite_file = os.path.basename(sys.argv[0]).split(".")
base_suite_file_name = base_suite_file[0]
root_dir = str(Path.home())
logs_dir_path = root_dir + r"/Python_Runner_Logs/"
if not os.path.exists(logs_dir_path):
    os.makedirs(logs_dir_path)
info_filename = logs_dir_path + str(base_suite_file_name)+ ".log"
result_csv = logs_dir_path + base_suite_file_name + ".csv"


def setup_logger(name, log_file, level=logging.INFO):

    root_logger = logging.getLogger(name)
    root_logger.setLevel(level)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)


def logger(msg, level="info"):

    log = logging.getLogger('all_logs')
    msg = pprint.pformat(msg)
    if level == "info":
        log.info(msg)
    if level == "error":
        log.error(msg)


try:
    if os.path.exists(info_filename):
        os.remove(info_filename)
except IOError as e:
    raise e


setup_logger('all_logs', info_filename, logging.INFO)
