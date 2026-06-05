__author__ = 'CHU'
from definition.settings import *

class TestConfigTB(Test):
    uuid = 'NonTC'
    description = "initial testbed"
    goto_teardown = True

    def test_00_00_global(self):
        logger.info(f" {Params.testbed} ".center(40, '-'))
        cmd1 = f'cp -f {TestPath}/confs/rsyslog {file_path1}'
        cmd2 = f'cp -f {TestPath}/confs/rsyslog.conf {file_path2}'
        logger.info(cmd1)
        logger.info(cmd2)
        os.system(cmd1)
        os.system(cmd2)

        rc = os.path.exists(file_path1)
        rc &= os.path.exists(file_path2)
        Assertion.assert_equal(rc, True, 'Copy file failed')

    def test_00_01_add_address_objects(self):
        logger.info(" Add address objects ".center(40, '-'))
        addrobj = copy.deepcopy(Obj)
        rc = True
        for item in servers:
            addrobj['name'] = item
            addrobj['value'] = item
            ret = LAddr_obj.config_addressobject(msg=True, **addrobj)
            if ret[0]:
                logger.info(f'Add {addrobj["name"]} address objects success.')
            elif 'Already exists' in ret[1]['status']['info'][0]['message']:
                logger.info('Local Address Object already exists')
            else:
                rc &= False
                logger.info(f'Add {addrobj["name"]} Failed')
        Assertion.assert_equal(rc, True, 'Add address objects Failed.')

