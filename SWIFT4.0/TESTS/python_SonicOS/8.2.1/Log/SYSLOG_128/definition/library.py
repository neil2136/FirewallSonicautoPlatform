__author__ = 'CHU'

from definition.settings import *

class SyslogLib():
    def __init__(self,fw):
        self.fw = fw

    def check_tsr(self,kwd,reline,server):
        ret = diag_obj.download_tsr()
        if ret:
            logger.info('Download Failed')
            return False
        else:
            logger.info('Download Success!')
            comment = re.compile(reline, re.S)
            with open('/tmp/techSupport', 'r', encoding='utf-8') as f:
                lines = comment.findall(f.read())[0].split('\n')
                rc = False
                for line in lines:
                    if kwd in line:
                        if server in line:
                            rc = True
                            break
                        else:
                            logger.info('Check TSR failed')
                            logger.info('--- TSR resulte ---')
                            logger.info(line)
                            logger.info('-------------------')
                            rc = False
                if rc:
                    logger.info('Check TSR Success!')
            os.system('rm -f /tmp/techSupport')
            return rc