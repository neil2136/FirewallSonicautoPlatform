import imaplib
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pytest_resources.common_require import *
from inputs.constants import *


class MailModule:

    def get_otp_from_mail(self, smtp_username, smtp_password, smtp_server_ip, content=None, all_mail=None):
        try:
            # login to mailbox
            logger.info("logging in to mailbox")
            mail = imaplib.IMAP4(host=smtp_server_ip, port=smtp_port)
            mail.login(smtp_username, smtp_password, )
            mail.list()
            mail.select('inbox')

            # This will fetch all or latest unseen mail from the mail box
            logger.info("Fetching mail from mail box")
            if all_mail == True:
                result, data = mail.uid('search', None, "ALL")
            else:
                result, data = mail.uid('search', None, "UNSEEN")
            # Checking for latest valid OTP mail
            start_time = time.time()
            logger.info("Checking for valid OTP mail")
            while data[0] == b'' and time.time() - start_time < 120:
                time.sleep(3)
                result, data = mail.uid('search', None, "UNSEEN")
                logger.info("OTP is not received, waiting another 3 seconds")

            if data == [b'']:
                logger.info("OTP is not received even waiting for 120 seconds..")
                return False

            i = len(data[0].split())
            for x in range(0, 1):

                latest_email_uid = data[0].split()[-1]
                result, email_data = mail.uid('fetch', latest_email_uid, '(RFC822)')
                raw_email = email_data[0][1]
                raw_email_string = raw_email.decode('utf-8')
                email_message = email.message_from_string(raw_email_string)

                # Header Details
                date_tuple = email.utils.parsedate_tz(email_message['Date'])
                if date_tuple:
                    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                    local_message_date = "%s" % (str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
                email_from = str(email.header.make_header(email.header.decode_header(email_message['From'])))
                email_to = str(email.header.make_header(email.header.decode_header(email_message['To'])))
                subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
                print(email_from, email_to, email_message, subject)

                # Body details
                for part in email_message.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True)
                        message = body.decode('utf-8')
                        file_name = mount_mail_results + ".email"
                        output_file = open(file_name, 'w+')
                        output_file.write("From: %s\nTo: %s\nDate: %s\nSubject: %s\n\nBody: \n\n%s" % (
                            email_from, email_to, local_message_date, subject, body.decode('utf-8')))
                        output_file.close()
                        otp = message.split()[-1]
                        if content == True:
                            return otp, email_from, subject, body
                        else:
                            return otp
                    else:
                        continue
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Couldn't get the OTP from the Mail server")

    # this function is used to  read all un read mails
    def read_all_unread_mails(self, smtp_username, smtp_password, smtp_server_ip):
        try:
            mail = imaplib.IMAP4(host=smtp_server_ip, port=smtp_port)
            mail.login(smtp_username, smtp_password)
            mail.list()
            mail.select('inbox')
            logger.info("reading old unread mails")
            result, data = mail.uid('search', None, "UNSEEN")
            unread_mails = []
            unread_mails = data[0].decode('utf-8').split()
            number = len(unread_mails)
            logger.info("{} unread mails in mailbox".format(number))
            i = 1
            if data[0] != b'':
                logger.info("Reading all unread mails")
                for i in range(0, number):
                    result, email_data = mail.uid('fetch', unread_mails[i], '(RFC822)')
                    i = i + 1
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Couldn't connect to Mail server")

    # Function to send email with the combined CSV
    def send_email_with_attachment(self, sender_email, recipient_emails, subject, mail_body, attachment_path, file_name,
                                   smtp_server, smtp_port_number):
        try:
            # Create an email message object
            msg = MIMEMultipart('alternative')
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipient_emails)
            msg['Subject'] = subject
            msg.attach(MIMEText(mail_body, 'html'))

            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(attachment_path, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename={file_name}'.format(file_name=file_name))
            msg.attach(part)

            # Connect to the SMTP server and send the email
            with smtplib.SMTP(smtp_server, smtp_port_number) as server:
                login_status = server.connect(sv_web_mail_server)
                logger.info(login_status)
                response = server.send_message(msg)
                logger.info(response)
                logger.info("Email sent to: " + ', '.join(recipient_emails))
        except Exception as err:
            logger.error("Exception \t: " + str(err))
            logger.error("Couldn't connect to Mail server")

