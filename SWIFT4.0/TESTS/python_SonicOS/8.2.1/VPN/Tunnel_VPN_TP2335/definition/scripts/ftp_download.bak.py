from ftplib import FTP
import time
import argparse


def ftp_download(host, username, password, remote_file, local_file):
    remote_path = f'/var/www/https/{remote_file}'
    local_path = f'/tmp/{local_file}'
    print(f'host: {host}, \nusername: {username}, \npassword: {password}, \nremote_path: {remote_path}, \nlocal_path: {local_path}')
    try:
        print('start Connect to FTP server')
        ftp = FTP(host)
        ftp.login(username, password)

        print('start download file...')
        with open(local_path, 'wb') as file:
            ftp.retrbinary(f"RETR {remote_path}", file.write)
        print('quit ftp login...')
        ftp.quit()
        print("File download successful!")
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start ftp server')
    parser.add_argument('-host', type=str, dest='host', required=True, help='ip to start ftp server on it')
    parser.add_argument('-user', type=str, dest='user', required=False, help='ftp user', default='root')
    parser.add_argument('-pwd', type=str, dest='password', required=False, help='ftp password', default='password')
    parser.add_argument('-remote', type=str, dest='remote', required=False, help='remote file', default='Exploit.VBS.Agent.q.gz')
    parser.add_argument('-local', type=str, dest='local', required=False, help='local file', default='Exploit.VBS.Agent.q.gz')
    args = parser.parse_args()
    host = args.host
    user = args.user
    password = args.password
    remote = args.remote
    local = args.local

    ftp_login = ftp_download(host, user, password, remote, local)
    if ftp_login:
        print('File download successful!')
    else:
        print('File download failed!')
