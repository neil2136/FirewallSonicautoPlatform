# from definition.settings import *
from ftplib import FTP
import socket
import os


def ftpconnect(host, username, password):
    ftp = FTP()
    ftp.set_debuglevel(2)          # debuglevel2 -> show detail info
    ftp.set_pasv(0)
    ftp.encoding = 'GB2312'        #
    ftp.connect(host, 21)          # connect to host
    ftp.login(username, password)  # login to host
    return ftp


def ftp_downloadfile(ftp, localpath, remotepath):
    bufsize = 1024                 # set buffer size
    fp = open(localpath, 'wb')
    ftp.retrbinary('RETR ' + remotepath, fp.write, bufsize)  # fetch remote file and write to local
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()


def ftp_uploadfile(ftp, localpath, remotepath):
    bufsize = 1024
    fp = open(localpath, 'rb')
    ftp.storbinary('STOR ' + remotepath, fp, bufsize)  # upload to remote path
    ftp.set_debuglevel(0)
    fp.close()
    ftp.quit()


# if __name__ == "__main__":
#     IP = '172.16.1.200'
#     user = 'root'
#     pwd = 'password'
#     remotefile = '/tmp/1.txt'
#     localfile = '/DEV_TESTS/python_SonicOS/7.0.1/VPN/Route_Based_VPN_2335/testcases/test.txt'
#     ftp = ftpconnect(IP, user, pwd)
#     ftp_downloadfile(ftp, localfile, remotefile)
    # ftp_uploadfile(ftp, localfile, remotefile)
