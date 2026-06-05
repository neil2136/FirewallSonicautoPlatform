import argparse
import os
import sys

sys.path.append(os.environ["PYTHON_COMMON_HOME"])
from tools.trafficGen import  MyFtp

parser = argparse.ArgumentParser(description='Process some parameter.')
parser.add_argument('--ip',  type=str)
parser.add_argument('--action',  type=int)

args = parser.parse_args()
suite_path = os.environ["PYTHON_SONICOS_HOME"]+'/7.1.1/VPN/VPN_nonLAN_116'

myftp = MyFtp(host=args.ip, user='root', password='password')
myftp.login()
output = myftp.download_file( "/tmp/ftpDataFile1.txt", f'{suite_path}/bin/ftp.py')
print(f'check {args.ip} to vpn ftp download result: {output}')
if args.action == 2:
    print('action is allow , Connection established and Server side verification  should pass')
    if output:
        rc = True
        print("verify FTP success")
    else:
        rc = False
        print("verify FTP failed")
elif args.action == 0:
    print('action is deny,ping should failed')
    if output:
        rc = False
        print("verify FTP success")
    else:
        rc = True
        print("verify FTP failed")
