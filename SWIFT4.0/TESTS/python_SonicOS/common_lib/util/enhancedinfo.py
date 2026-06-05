import json

from runner.settings import logger

def show_testcase_info(file=None, tc='', description=False):
    ''' show testplan in details.
        file: file name for the testplan
        tc: the testcase num
    '''

    info = ''
    try:
        with open(file,'r') as f:
            for line in f:
                info += line
    except Exception as e:
        logger.error('Can not open file {}: {}'.format(file, e), exc_info=True)
        return False
    info_dict = json.loads(info)
    if description:
        try:
            return info_dict[tc]
        except KeyError as e:
            logger.info('Testcase {} not exist in file {}.'.format(str(tc), file))
            return {'title':''}
    try:
        logger.info('Testcase ID: {}'.format(str(tc)))
        logger.info('Testcase Title: {}'.format(info_dict[tc]['title']))
        logger.info('Testcase details:' + '\n' +
            ' '*2 + 'Initial Steps:' + '\n' + info_dict[tc]['initial'] + '\n'*2 +
            ' '*2 + 'Executable Steps:' + '\n' + info_dict[tc]['steps'] + '\n'*2 +
            ' '*2 + 'Expect results:' + '\n' + info_dict[tc]['result'] + '\n'*2)
    except KeyError as e:
        logger.info('Testcase {} not exist in file {}.'.format(str(tc), file))
    try:
        logger.info('Description:' + '\n' + info_dict[tc]['description'])
        logger.info('ATM_ID: {}'.format(info_dict[tc]['atm_id'])) 
        logger.info('Priority: {}'.format(info_dict[tc]['priority'])) 
    except KeyError as e:
        pass
    
if __name__ == '__main__':
    file = '/SWIFT4.0/TESTS/SonicOS/6.5.4/Network/Web_proxy/Testplan/webproxy.json'
    show_testcase_info(file, tc='1')
    