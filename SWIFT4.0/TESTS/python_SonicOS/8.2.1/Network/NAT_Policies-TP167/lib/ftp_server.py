import argparse
import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers  import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp_server(server, user, pwd, dir):
    authorizer = DummyAuthorizer()
    authorizer.add_user(user, pwd, dir, perm='elradfmwMT')
    handler = FTPHandler
    handler.authorizer = authorizer
    server = FTPServer((server, 21), handler)
    server.serve_forever()


def stop_ftp_server():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start ftp server')
    parser.add_argument('-server', type=str, dest='server', required=True, help='ip to start ftp server on it')
    parser.add_argument('-user', type=str, dest='user', required=True, help='ftp user')
    parser.add_argument('-pwd', type=str, dest='pwd', required=True, help='ftp password')
    parser.add_argument('-dir', type=str, dest='dir', required=True, help='ftp dir')
    args = parser.parse_args()
    server = args.server
    user = args.user
    pwd = args.pwd
    dir = args.dir
    start_ftp_server(server, user, pwd, dir)