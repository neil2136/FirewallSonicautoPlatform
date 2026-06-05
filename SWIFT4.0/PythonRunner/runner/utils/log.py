import subprocess
import socket
import os
from os import environ
from xml.dom import minidom
import re
import time
import requests
import sys
from runner.settings import SETUPTB,logger, python_logger, LOG_DIR, TIMENOW, Params,QBS_JOBNUM,OPENSTACK_SETUP,NFS_IP


class log:
    def __init__(self, resource, product, scmlabel, testbed, user, log_ftp_server='sj-conserver.eng.sonicwall.com', log_path='/tmp'):
        if re.search(r'VTB5|VTB7|VTB8', testbed, re.I) or re.search(r'10.6.\d+.\d+',subprocess.Popen('ifconfig', shell = True, stdout = subprocess.PIPE).communicate()[0].decode('ASCII')) :
            log_ftp_server = 'sh-conserver.eng.sonicwall.com'
            logger.debug(f'{log_ftp_server}')
        try:
            log_ftp_server= socket.gethostbyname(log_ftp_server)
        except:
            logger.debug(f'Fail to get ip for {log_ftp_server}.')
            log_ftp_server='10.6.1.200'
            logger.debug(f'Use {log_ftp_server} instead.')
        self.log_ftp_server = log_ftp_server
        self.log_path = log_path

#        self.openstack_setup = {'VTB300-PC1': '1','VTB301-PC1': '1', 'VTB400-PC1': '1','VTB401-PC1': '1', 'VTB500-PC1': '1', 'VTB501-PC1': '1', 'VTB600-PC1': '1', 'VTB601-PC1': '1','VTB700-PC1': '1','VTB701-PC1': '1', 'VTB800-PC1': '1','VTB801-PC1': '1', 'VTB900-PC1': '1','VTB901-PC1': '1',}
        self.openstack = ''
        if environ.get('G_OPENSTACK') is not None:
            self.openstack = os.environ['G_OPENSTACK']

        self.resource = resource
        self.product = product
        self.scmlabel = scmlabel
        self.testbed = testbed
        self.user = user
        self.consoles = []
        self.logfile = {}
        self.index = {}
        self.uploaddir = '/logs/buildtestlogs/' + self.product + '/' + self.scmlabel + '/' + self.testbed + '/' + self.user + '/'+ self.user + '_' + self.testbed + '_' + TIMENOW 
        self.uploaddir_url = self.uploaddir.replace('/logs', '')
        self.uploaddir_url = 'http://' + NFS_IP + self.uploaddir_url
        if not environ.get('G_SETUPLOGDIR'):
            os.environ['G_SETUPLOGDIR'] =self.uploaddir_url
        self.uploaddir_url +=  '/' + os.path.basename(LOG_DIR) + '/'
        Params.server_log_location = self.uploaddir_url
        
    def copy_file_to_log_server(self, file_name):
        uploaddir = self.uploaddir
        dst = uploaddir
        src = file_name

        # if QBS_JOBNUM != '1234' and not SETUPTB:
        #     python_logger.write(f'cp /tmp/stderr.log to {src}'+ '\n' )
        #     subprocess.Popen(['cp'] + ['/tmp/stderr.log'] + [src+'/'], stdout=subprocess.PIPE).communicate()[0]

        self.log_to_html(src+'/commands.log', src+'/commands.html')
        params = ['-avz']
        params.extend((src, dst))
        python_logger.write('Entering utils::log::copy_file_to_log_server...'+ '\n' )
        python_logger.write(''*4 + 'Rsyncing logs rsync: '+ ' '.join(['rsync'] + params)+ '\n')

        try:
            if not os.path.exists(dst):
                os.makedirs(dst)
            p = subprocess.Popen(['rsync'] + params, stdout=subprocess.PIPE)
            time.sleep(3)
            logger.info('--------rsync ----')
            logger.info('poll1 '+str(p.poll()))
            rsync_result_string = p.communicate()[0]
            logger.info('poll2 '+str(p.poll()))
            p.wait()
            t=p.poll()
            if t !=0:
                for i in range(10):
                    logger.info('%%%%%1')
                    p1 = subprocess.Popen(['rsync'] + params, stdout=subprocess.PIPE)
                    p1.wait()
                    t1 = p1.poll()
                    rsync_result_string = p1.communicate()[0]
                    logger.info('poll3 '+str(t1))
                    if t1 == 0 :
                        break
                if t1 != 0:
                    cmd = ['cp','-r',params[1],params[2]]
                    
                    p2 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                    p2.wait()
                    logger.info('poll4 '+str(p2.poll()))
            # cmd = ' '.join(['rsync'] + params)
            # p = os.system(cmd)
            # logger.info('return code ' + str(p))
            # if p != 0:
            #     for i in range(5):
            #         time.sleep(3)
            #         p1 = os.system(cmd)
            #         logger.info('%%%%%1')
            #         logger.info('return code p1 ' + str(p1))
            #         if p1 == 0:
            #             break
            #mtab_params = ['/etc/mtab']
            python_logger.flush()
            logger.info(rsync_result_string)
            time.sleep(2)
        except:
            logger.error("Unable to rsync files or /logs nfs mount cannot be determined from /etc/mtab")
            return 1
        return uploaddir

    def get_dut_console_log_link(self):
        self.populate_console()
        console_links = []
        try:
            for tbcslname in self.consoles:
                console_link = 'http://' + self.log_ftp_server + '/console/' + tbcslname
                console_links.append(console_link.lower())
        except:
            logger.warning('Unable to get dut console log link.')

        return console_links


    def set_console_index(self, link):
        result = re.search(r'\/([\w-]+)$', link)
        console = result.group(1)

        try:
            response = requests.get(link)
            content = response.content.decode('ASCII')
            logfile = content.split('\n')

            self.logfile[console] = logfile
            self.index[console] = len(logfile)
        except:
            logger.error("ERROR: Unable to retrieve console logfile")
            return 1

        return self


    def create_dut_console_textfile(self, file_name):
        result = re.search(r'\/([\w-]+)\.\w+$', file_name)
        console = result.group(1)

        link = self.console_links[console]

        try:
            response = requests.get(link)
            content = response.content.decode('ASCII')
            logfile = content.split('\n')

            current_content = logfile[self.index[console]:]

            with open(file_name, "w", newline="") as file_handle:
                file_handle.writelines(current_content)
                file_handle.close()
        except:
            logger.error("Unable to write console textfile")
            return 1

        return 0

    def populate_console(self):
        testbed = self.testbed
        product = self.product
        product = re.sub(r'-prototype','pro',re.sub(r'nsa|octeon', '', product.lower()))

        tbdefcsl = ''
        if self.openstack != '1':
            tbdefcsl = testbed.lower() + '-' + product

            tqtest_resource = self.resource
            tqtest_resources = tqtest_resource.split(',')
            for element in tqtest_resources:
                element = re.sub(r':\d+$', '', element)
                logger.info("RESOURCE ELEMENT: " + element)

                if re.match(r'^(SHA|CLUSTER)$', element):
                    console = tbdefcsl
                    tbdefcsl = console + '-pri'
                    self.consoles.append(tbdefcsl)
                    tbdefcsl = console + '-sec'
        elif not self.testbed in OPENSTACK_SETUP:
            try:
                xml = self.testbed + '.xml'
                xml_path = 'http://osservices-sj.eng.sonicwall.com/topologies/' + xml

                content = self.log_path + '/' + xml
                cmd = ['/bin/rm', '-Rf', content]
                retval = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

                params = ['-P', self.log_path, xml_path]
                retval = subprocess.Popen(['wget'] + params, stdout=subprocess.PIPE).communicate()[0]

                doc = minidom.parse(content)
                rec = doc.getElementsByTagNameNS('*', 'topology')[0]
                console = rec.getElementsByTagName('node')[0]
                tbdefcsl = console.getElementsByTagName('topology-resource-name')[0].firstChild.data.strip(' ')
            except:
                logger.error("Unable to retrieve xml file from osservices")
                return 1

        self.consoles.append(tbdefcsl)

        return self

    def log_to_html(self,log_file, html_file):
        colors = {
            '[DEBUG]': 'orange',
            '[ERROR]': 'red',
            '[WARNING]': 'orange',
        }
        
        with open(log_file, 'r', encoding='utf-8') as f:
            log_lines = f.readlines()
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
    <html>
    <head>
        <title></title>
        <style>
            body {
                font-family: Consolas, monospace;
                background-color: #f5f5f5;
                margin: 20px;
            }
            pre {
                white-space: pre-wrap;
                word-wrap: break-word;
                background-color: white;
                padding: 10px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            .warning {
                color: orange;
                font-weight: bold;
            }
            .debug {
                color: orange;  
                font-weight: bold;
            #   background-color: #FFFFCC; 
            }
            .error {
                color: red;
                font-weight: bold;
            #   background-color: #FFCCCC; 
            }
            .others {
                color: #77CEEB;
                font-weight: bold;
            #   background-color: #FFCCCC; 
            }
        </style>
    </head>
    <body>
        <pre>
    ''')
            
            for line in log_lines:
                line = line.rstrip()  
                line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;') 
                
                if '[WARNING]' in line:
                    line = re.sub(r'(.*\[WARNING\].*)', r'<span class="warning">\1</span>', line)
                elif '[DEBUG]' in line:
                    line = re.sub(r'(.*\[DEBUG\].*)', r'<span class="debug">\1</span>', line)
                elif '[ERROR]' in line:
                    line = re.sub(r'(.*\[ERROR\].*)', r'<span class="error">\1</span>', line)
                elif '[INFO]' in line:
                    line = line
                else:
                    line = re.sub(r'(.*)', r'<span class="others">\1</span>', line)

                f.write(line + '\n')
            
            f.write('''    </pre>
    </body>
    </html>
    ''')
        logger.debug(f'Produce {log_file} to {html_file}')
# if __name__ == "__main__":
#     python_object = log()
#
#     file_name = '/home/gavin/Python_Runner_Logs/eu_test_suite.log'
#     url = python_object.copy_file_to_log_server(file_name)
#
#     print(url)
#
#     links = python_object.get_dut_console_log_link()
#     print(links)
#     for console_log in links:
#         python_object.set_console_index(console_log)
#
#     for console in python_object.consoles:
#         filename = '/home/gavin/Python_Runner_Logs/' + console + '.txt'
#         python_object.create_dut_console_textfile(filename)


# export PYTHONPATH
# export G_SCMLABEL=6.5.2.2-44n
# export G_PRODUCT=5600
# export G_TESTBED=TB24
# export G_USER=root
# export G_RESOURCE=CLUSTER:1
