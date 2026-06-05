from ftplib import FTP
from time import sleep
import argparse
import os
import sys


def ftp_to_server(host, user, password):
    ftp = FTP(host)
    sleep(1)
    out = ftp.login(user, password)
    print(out)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start ftp server')
    parser.add_argument('-host', type=str, dest='host', required=True, help='ip to start ftp server on it')
    parser.add_argument('-user', type=str, dest='user', required=False, help='ftp user', default='root')
    parser.add_argument('-pwd', type=str, dest='password', required=False, help='ftp password', default='password')
    args = parser.parse_args()
    host = args.host
    user = args.user
    password = args.password
    ftp_to_server(host, user, password)