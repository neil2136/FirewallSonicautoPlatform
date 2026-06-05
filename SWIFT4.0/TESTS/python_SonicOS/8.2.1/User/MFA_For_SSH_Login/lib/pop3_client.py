from email.parser import Parser
from email.header import decode_header,Header
from email.utils import parseaddr
import poplib
import argparse

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def print_info(msg):
    # print from ,to ,subject
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
    # get content and attahments
    attachment_files = []
    try:
        for part in msg.walk():
            file_name = part.get_filename()
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
                with open("/tmp/" + filename, 'wb') as f:
                    f.write(data)
                print('attachment is downloaded')
            elif contentType == 'text/plain': #or contentType == 'text/html':
                data = part.get_payload(decode=True)
                content = data.decode(mycode)
                print(content)

        print('attachments:', attachment_files)
    except:
        print('failed to get attachemnts')


def get_email(pop3_server,user,password):
    try:
        server = poplib.POP3_SSL(pop3_server, 995)
        server.set_debuglevel(1)
        server.user(user)
        server.pass_(password)
        resp, mails, octets = server.list()
        print(mails)
        index = len(mails)
        print('unread email',index)
        resp, lines, octets = server.retr(index)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        print_info(msg)
        server.quit()
        return(msg)
    except Exception as err:
        print(err)

def delete_email(pop3_server,user,password):
    try:
        server = poplib.POP3_SSL(pop3_server, 995)
        server.set_debuglevel(1)
        server.user(user)
        server.pass_(password)
        resp, mails, octets = server.list()
        print(mails)
        index = len(mails)
        print('unread email',index)
        ret = ""
        for i in range(1,index+1):
            print(i)
            ret = server.dele(i)
        print('6' * 60)
        print(ret)
        print('6' * 60)
        server.quit()
        return(ret)
    except Exception as err:
        print(err)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='get email by pop3.')
    # parser.add_argument('-server', type=str, required=True, help='server, like: 13.0.0.5')
    # parser.add_argument('-user', type=str, required=True, help='email username, like: test1')
    # parser.add_argument('-password', type=str, required=True, help='email password, like:password')
    # args = parser.parse_args()
    # get_email(args.server, args.user, args.password)
    #get_email('172.17.1.5', 'test1', 'password')
    delete_email('172.17.1.5', 'test1', 'S0nic@uto')
