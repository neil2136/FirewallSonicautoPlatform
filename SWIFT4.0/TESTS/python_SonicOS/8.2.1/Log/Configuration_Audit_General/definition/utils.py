from runner.settings import Params, logger


def compare_dict_contained(source_dict, contain_dict):
    res = False
    for auditlog in source_dict:
        logger.info(auditlog)
        if auditlog.items() >= contain_dict.items():
            res = True
            logger.info(f'march contains successful! \n '
                        f'contain_dict: {contain_dict}\n'
                        f'auditlog: {auditlog}')
            break
    if not res:
        logger.info('march contains failed!')
    return res


# def is_dict_contained(source_dict, contain_dict):
#     for key, value in contain_dict.items():
#         if key not in source_dict or source_dict[key] != value:
#             return False
#     return True
#
#

# need add to api/log.py  AuditlogMonitorApi
def email_audit_records(self, msg=False):
    head = OrderedDict([('Accept', 'application/json'),
                        ('Content-Type', 'application/json'),
                        ('Accept-Encoding', 'application/json'),
                        ('X-SNWL-API-Scope', 'extended'),
                        ('charset', 'UTF-8')])
    post_url = 'api/sonicos/raw'
    resp = self.fw.api_post(post_url, msg, data={"stream": "cgiaction=emailAuditRecord"}, headers=head)
    return resp


# need add to common_lib/tools/send_fetch_email.py   Email
# add parameter listres to get the mail contents
def get_mail_contents_via_letters(self, port='110', letters='latest'):
    mailcontents = []
    msg = MIMEText('Get mail contents from Mail Server with POP3 Protocol')
    logger.info(msg)
    if self.use_ssl:
        try:
            server = poplib.POP3_SSL(self.mail_server_ip, port)
            logger.info('Connected to mail server by ssl Successfully')
        except Exception as e:
            logger.error(f'Connected to mail server failed by ssl with error {e}')
            return False
    else:
        try:
            server = poplib.POP3(self.mail_server_ip, port)
            logger.info('Connected to mail server Successfully')
        except Exception as e:
            logger.error(f'Connected to mail server failed with error {e}')
            return False
    try:
        server.set_debuglevel(1)
        logger.info(server.getwelcome().decode('utf-8'))
        server.user(self.mail_user)
        server.pass_(self.mail_pwd)
        logger.info('Login to POP3 Server Successfully')
        logger.info(server.stat())
        logger.info('Messages: %s. Size: %s' % server.stat())
        resp, mails, octets = server.list()
        logger.info(f'all letters list: {mails}')
        numbermsg = len(server.list()[1])
        logger.info(f'the latest letter number: {numbermsg}')
        if letters == 'all':
            for i in range(numbermsg):
                mailstr = []
                for j in server.retr(i + 1)[1]:
                    mailstr.append(j.decode('UTF-8'))
                logger.info(mailstr)
                mailcontents.append(mailstr)
        elif letters == "latest":
            for j in server.retr(numbermsg)[1]:
                mailcontents.append(j.decode('UTF-8'))
            logger.info(mailcontents)
        else:
            logger.error('letters only support all/latest')
        server.quit()
    except Exception as e:
        logger.error(f'Fetching messages from Mail Server with POP3 failed {e}')
    return mailcontents