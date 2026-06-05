'''
this file to generate a local certe via a sign_req cert.
para: sign_req --> it's the sign_req cert name
      sub --> set it ture to get subject
'''

import os

def gen_local_cert(sign_req, sub=False):
    cert_dir = "/tmp/logs"
    st_dir = os.environ["PYTHON_SONICOS_HOME"] + "/VPN/VPN_Tunnel_Statistics/cert"
    print ("begin to generate serial and index ......\n")
    try:
        os.system("rm -rf /tmp/logs/index.*")
        os.system("rm -rf /tmp/logs/serial*")
        os.popen("/usr/bin/expect {}/CAexp.exp 5 /tmp/logs".format(st_dir)).read()
        
        print("begin to generate local cert ......")
        os.system("rm -rf /tmp/logs/*.pem")
        resp = os.popen("/usr/bin/expect {}/CAexp.exp 2 {} {}".format(st_dir, st_dir, sign_req)).read()
    except RuntimeError:
        print('----------!!!! Generate the local cert is failed running  !!!!-----------')

    if ('Creat local certificate passed' in resp):
        rc = True
    else:
        rc = False

    if sub:
        local_cert = '/tmp/logs/01.pem'
        command = "openssl x509 -in {} -noout -subject".format(local_cert)
        subject = os.popen(command).read()
        return rc, subject

    return rc