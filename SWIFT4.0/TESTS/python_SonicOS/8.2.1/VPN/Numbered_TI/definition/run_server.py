import os
import sys
import paramiko
import argparse

parser = argparse.ArgumentParser(description='Process args')
parser.add_argument('-ip', '--host', required=True, help='Host to run command')
parser.add_argument('-u', '--user', type=str, default='root', help='Host user name')
parser.add_argument('-p', '--password', type=str, default='password', help='Password to login jira')
parser.add_argument('-c', '--cmd', required=True, help='Command to run')
args = parser.parse_args()

print(args.cmd)
myssh = paramiko.SSHClient()
myssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
myssh.connect(args.host, username=args.user, password=args.password)
channel = myssh.get_transport().open_session()
channel.exec_command(args.cmd)
myssh.close()
