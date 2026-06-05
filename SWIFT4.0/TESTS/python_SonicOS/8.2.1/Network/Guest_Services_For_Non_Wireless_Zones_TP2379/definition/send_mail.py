import smtplib
import poplib
import sys
import argparse
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.header import Header
from email.mime.text import MIMEText
from runner.settings import logger

# sys.path.append(os.environ["PYTHON_COMMON_HOME"])
sys.path.append('/SWIFT4.0/TESTS/python_SonicOS/common_lib')

# DEFAULT_PORT = {
#     "smtp":{False: 25, True: 465}
#     "pop3": {False: 110, True: 995},
#     "imap4": {False: 143, True: 993},
# }
# when mail server disable SSL,
# sending mail from client using smtp,default port is 25
# fetching mail from server using pop3,default port is 110
# fetching mail from server using imap,default port is 143
# when mail server enbale SSL,
# sending mail from client using smtp,default port is 465
# fetching mail from server using pop3,default port is 995
# fetching mail from server using imap,default port is 993

mail_server_ip = "10.6.0.69"


class Email():
    '''Start sending and fetching mail
    :param server: mail server (host, host:port)
    :param use_ssl: True if use SSL else False
    '''

    def __init__(self, mail_server_ip, mail_user, mail_pwd):
        self.mail_server_ip = mail_server_ip
        self.mail_user = mail_user
        self.mail_pwd = mail_pwd

    def send_mail(self, port):
        #msg = MIMEText('Sending messages from Mail Client with SMTP Protocol')
        try:
            server = smtplib.SMTP(self.mail_server_ip, port)
            logger.info('Connected to mail server Successfully')
        except Exception as e:
            logger.error(
                'Connected to mail server failed with error {}'.format(e))
            return False
        try:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login("test@sonicauto.com", 'password')
            server.sendmail("test@sonicauto.com", "root@sonicauto.com", '')
            server.quit()
            logger.info(f'send email to  via starttls success')
        except Exception as e:
            logger.error(
                'Send messages to mailserver failed with error {}'.format(e))
            return False
        return True

    def get_mail(self, mailserver, user):
        password = 'password'
        # user = Parameter.MAIL_USER2
        port1 = 110
        server = poplib.POP3(self.mail_server_ip, port1)
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
            msg1 = self.print_info(msg)
            logger.info(msg1)
            MAIL_BODY = 'body'
            if MAIL_BODY in msg1:
                logger.info("find target mail\'s content:{}".format(msg1))
                server.quit()
                return True
            else:
                logger.info('not find target mail..')
                server.quit()
                return False
        except Exception as e:
            server.quit()
            logger.error(e)
            return False

    def print_info(self, msg):

        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header == 'Subject':
                    value = self.decode_str(value)
                else:
                    hdr, addr = parseaddr(value)
                    name = self.decode_str(hdr)
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
                    filename = self.decode_str(str(filename, dh[0][1]))
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

    def decode_str(self, s):
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send Mail Parameter')
    parser.add_argument('-protocol', type=str, dest='protocol', required=True, help='protocol for email',
                        default="smtp")
    args = parser.parse_args()
    mail_obj = Email(
        mail_server_ip,
        "test@sonicauto.com",
        "password"
    )
    if args.protocol == "pop3":
        mail_obj.get_mail(mail_server_ip, "test")
    else:
        mail_obj.send_mail("25")
