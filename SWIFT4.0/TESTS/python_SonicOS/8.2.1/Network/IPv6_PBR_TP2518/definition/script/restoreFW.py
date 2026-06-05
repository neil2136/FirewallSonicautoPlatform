import os
import sys
import argparse

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from config.restore_tel import RestoreFwTelnet

parser = argparse.ArgumentParser(description='Process args')
parser.add_argument('-ip', '--ip', required=True, help='Host to run command')
parser.add_argument('-p', '--port', type=str, default='root', help='Host user name')

args = parser.parse_args()
res = RestoreFwTelnet(console_ip=args.ip, console_port=args.port, boot_check=False)
rc = res.restore()
