from base64 import decode
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from io import StringIO
import os
import sys
import smtplib
import imaplib
import poplib
import getpass, email, sys
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from typing import IO
import base64
# from pandas.core.strings import str_decode
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.utils import parseaddr, formataddr
from email import encoders
from runner.settings import logger
import time
import signal

'''
This file is used to send and receive mail.
1).as you see,send_mail_smtps_or_starttls function used to send mail by smtps or starttls protocol,
    smtps protocol by default, support attachment, no attachments by default;
2).get_mail function used to receive email by pop3s protocol, You can use recv_email_by_imaps function
 to receive emails using the imaps protocol. 
3).also,you can clear your user mail box by using clear_remote_mailbox.

'''


def get_file_content(filename):
    logger.info('get file content...')
    with open(filename, 'rb') as f:
        content = f.readlines

    return content


def send_mail_smtps_or_starttls(
        server,
        mail_from,
        mail_to,
        mail_subject,
        mail_content='mail body',
        mail_attach=None,
        starttls=False
):
    logger.info('send mail...')
    port1 = 25
    mail_postfix = 'sonicauto.com'
    # me="hello"+"<"+mail_from+"@"+mail_postfix+">"
    message = MIMEText(mail_content, 'plain', )
    message['From'] = "{}@{}".format(mail_from, mail_postfix)
    message['To'] = "{}@{}".format(mail_to, mail_postfix)
    message['Subject'] = Header(mail_subject)
    print(message)

    if mail_attach is not None:
        message_1 = MIMEText(mail_content, 'plain', )
        msg = MIMEMultipart('mixed')
        msg.attach(message_1)
        msg['From'] = "{}@{}".format(mail_from, mail_postfix)
        msg['To'] = "{}@{}".format(mail_to, mail_postfix)
        msg['Subject'] = Header(mail_subject)
        for item in mail_attach:
            Apart = MIMEBase('application', 'octet-stream')
            Apart.set_payload(open(item, 'rb').read())
            # encoders.encode_base64(Apart)
            Apart.add_header('Content-Disposition', 'attachment', filename=os.path.basename(item))
            msg.attach(Apart)

        if starttls is False:
            try:
                smtpObj = smtplib.SMTP(server, port=port1, timeout=120)
                smtpObj.set_debuglevel(1)
                smtpObj.sendmail(message['From'], message['To'], msg.as_string())
                smtpObj.quit()
                logger.info('send email to {} via smtps success'.format(mail_to))
                return True, 'send email to {} via smtps success'.format(mail_to)
            except Exception as e:
                print(str(e))
                logger.info('send email to {} via smtps failed'.format(mail_to))
                return False, e
        else:
            try:
                port2 = 465
                smtpObj = smtplib.SMTP_SSL(server, port=port2, timeout=120)
                smtpObj.set_debuglevel(1)
                # smtpObj.starttls()
                smtpObj.login(mail_from, 'password')
                smtpObj.sendmail(message['From'], message['To'], msg.as_string())
                smtpObj.quit()
                logger.info('send email to {} via starttls success'.format(mail_to))
                return True, 'send email to {} via starttls success'.format(mail_to)
            except Exception as e:
                print(str(e))
                logger.debug('send email to {} via starttls failed'.format(mail_to))
                return False, e
    else:
        if starttls is False:
            try:
                smtpObj = smtplib.SMTP(server, port=port1, timeout=120)
                smtpObj.set_debuglevel(1)
                smtpObj.sendmail(message['From'], message['To'], message.as_string())
                smtpObj.quit()
                logger.info('send email to {} via smtps success'.format(mail_to))
                return True, 'send email to {} via smtps success'.format(mail_to)
            except Exception as e:
                print(str(e))
                logger.debug('send email to {} via smtps failed'.format(mail_to))
                return False, e
        else:
            try:
                port2 = 465
                smtpObj = smtplib.SMTP_SSL(server, port=port2, timeout=120)
                smtpObj.set_debuglevel(1)
                # smtpObj.starttls()
                smtpObj.login(mail_from, 'password')
                smtpObj.sendmail(message['From'], message['To'], message.as_string())
                smtpObj.quit()
                logger.info('send email to {} via starttls success'.format(mail_to))
                return True, 'send email to {} via starttls success'.format(mail_to)
            except Exception as e:
                print(str(e))
                logger.debug('send email to {} starttls failed'.format(mail_to))
                return False, e


def clear_remote_mailbox(mail_user, host_ip, mail_server_ssh):
    logger.info('Mail User:{}'.format(mail_user))
    logger.info('Host IP:{}'.format(host_ip))
    dir = '/home/' + mail_user + '/Maildir/cur'
    cmd = 'rm -f {}/*'.format(dir)
    logger.info("clear {}\'s mailbox : {}".format(mail_user, cmd))
    output1 = mail_server_ssh.send_command('ls /home/{}/Maildir/cur'.format(mail_user))
    logger.info('the mailbox before is below:{}'.format(output1))
    mail_server_ssh.send_command(cmd)
    output2 = mail_server_ssh.send_command('ls /home/{}/Maildir/cur'.format(mail_user))
    logger.info('the mailbox after is below:{}'.format(output2))
    print(type(output2))
    if output2 == "":
        return True
    else:
        return False


def get_mail_pop3(mailserver, user, ssl_pop3=False):
    password = 'password'
    if ssl_pop3:
        server = poplib.POP3_SSL(mailserver, 995)
    else:
        server = poplib.POP3(mailserver, 110)

    logger.info('connected successfully...')
    try:
        server.set_debuglevel(1)
        logger.info(server.getwelcome())
        # server.utf8()
        server.user(user)
        server.pass_(password)
        logger.info('Login to POP3 Server Successfully')

        mailcount = server.stat()
        logger.info('mail count:{}'.format(mailcount))
        num = len(server.list()[1])
        logger.info('num of messages:{}'.format(num))
        resp, lines, octets = server.retr(num)
        msg_content = b'\r\n'.join(lines).decode()
        msg = Parser().parsestr(msg_content)
        msg1 = print_info(msg)
        logger.info(msg1)
        return (msg)
    except Exception as e:
        logger.error(e)
        return False


def get_mail_imap(server, username, password, ssl_imap=False):
    # try:
    if ssl_imap:
        with imaplib.IMAP4_SSL(server, 993) as imap4:
            imap4.login(username, password)
            # result, mailboxes = imap4.list()
            imap4.select("inbox")
            typ, msgs = imap4.search(None, 'ALL')
            msgs = msgs[0].split()
            svdir = "/tmp/"
            for emailid in msgs:
                resp, data = imap4.fetch(emailid, "(RFC822)")
                email_body = data[0][1]
                m = email.message_from_bytes(email_body)
                if m.get_content_maintype() != 'multipart':
                    continue
                for part in m.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    if filename is not None:
                        sv_path = os.path.join(svdir, filename)
                        if not os.path.isfile(sv_path):
                            print(sv_path)
                            fp = open(sv_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
            print("get mail by imap successfully")
            return (msgs)
    else:
        with imaplib.IMAP4(server, 143) as imap4:
            imap4.login(username, password)
            # result, mailboxes = imap4.list()
            imap4.select("inbox")
            typ, msgs = imap4.search(None, 'ALL')
            msgs = msgs[0].split()
            svdir = "/tmp/"
            for emailid in msgs:
                resp, data = imap4.fetch(emailid, "(RFC822)")
                email_body = data[0][1]
                m = email.message_from_bytes(email_body)
                if m.get_content_maintype() != 'multipart':
                    continue
                for part in m.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    filename = part.get_filename()
                    if filename is not None:
                        sv_path = os.path.join(svdir, filename)
                        if not os.path.isfile(sv_path):
                            print(sv_path)
                            fp = open(sv_path, 'wb')
                            fp.write(part.get_payload(decode=True))
                            fp.close()
            print("get mail by imap successfully")
            return (msgs)


def delete_email(pop3_server, user, password, ssl_pop3=False):
    try:
        if ssl_pop3:
            server = poplib.POP3_SSL(pop3_server, 995)
        else:
            server = poplib.POP3(pop3_server, 110)
        server.set_debuglevel(1)
        server.user(user)
        server.pass_(password)
        resp, mails, octets = server.list()
        print(mails)
        index = len(mails)
        print('unread email', index)
        ret = ""
        for i in range(1, index + 1):
            print(i)
            ret = server.dele(i)
        print('6' * 60)
        print(ret)
        print('6' * 60)
        server.quit()
        return (ret)
    except Exception as err:
        print(err)


def print_info(msg):
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        if value:
            if header == 'Subject':
                value = decode_str(value)
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
        print('%s: %s' % (header, value))

    attachment_files = []
    for part in msg.walk():
        file_name = part.get_filename()
        logger.info('filename:{}'.format(file_name))
        contentType = part.get_content_type()
        mycode = part.get_content_charset()
        if file_name:
            h = Header(file_name)
            dh = decode_header(h)
            filename = dh[0][0]
            if dh[0][1]:
                filename = decode_str(str(filename, dh[0][1]))
            attachment_files.append(filename)
            data = part.get_payload(decode=True)
            with open(filename, 'wb') as f:
                print(f'attachment {filename} has done')
                logger.info('attachment msg:' + f.readlines())
        elif contentType == 'text/plain':  # or contentType == 'text/html':
            data = part.get_payload(decode=True)
            content = data.decode(mycode)
            print('text', content)
            return content
    print('attachment list', attachment_files)


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_email_headers(msg):
    headers = {}
    for header in ['From', 'To', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header == 'Date':
                headers['date'] = value
            if header == 'Subject':
                subject = decode_str(value)
                headers['subject'] = subject
            else:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
                if header == 'From':
                    from_address = value
                    headers['from'] = from_address
                else:
                    to_address = value
                    headers['to'] = to_address
    content_type = msg.get_content_type()
    print('head content_type: {}'.format(content_type))
    return headers


def time_out(interval):
    def decorator(func):
        def handler(signum, frame):
            raise TimeoutError

        def wrapper(*args, **kwargs):
            try:
                signal.signal(signal.SIGALRM, handler)
                signal.alarm(interval)
                result = func(*args, **kwargs)
                signal.alarm(0)
                return result
            except TimeoutError as e:
                print(e)

        return wrapper

    return decorator


@time_out(10)
def recv_email_by_imap4(
        rcve_email_address="test",
        rcve_email_password="password",
        rcve_imap_server_host="192.168.13.200",
        rcve_imap_server_port=993,
):
    try:
        email_server = imaplib.IMAP4_SSL(host=rcve_imap_server_host, port=rcve_imap_server_port)
        print("imap4----connect server success, now will check username")
    except:
        print("imap4----sorry the given email server address connect time out")
        return False
    try:
        email_server.login(rcve_email_address, rcve_email_password)
        print("imap4----username exist, now will check password")
    except:
        print("imap4----sorry the given email address or password seem do not correct")
        exit(1)
    email_server.select()
    email_count = len(email_server.search(None, "ALL")[1][0].split())
    try:
        typ, email_content = email_server.fetch(f"{email_count}".encode(), "(RFC822)")
        email_content = email_content[0][1].decode()
        print(email_content)
        if email_content != "":
            email_server.close()
            email_server.logout()
            return True
        email_server.close()
        email_server.logout()
    except:
        print("receive email failed")
        return False