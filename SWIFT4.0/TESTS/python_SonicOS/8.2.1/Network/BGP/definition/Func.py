__author__ = 'CHU'
from definition.settings import *


class Function():
    def clear_BGP_settings(self):
        logger.info(" {} ".center(20, '-').format('Clear DUT Settings for BGP'))
        commands1 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'no router bgp 1',
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc1, output) = cl1.do_cli_commands(commands1, 1)
        if 'Error' not in output:
            logger.info('Clear Local Settings Success!')

        logger.info(" {} ".center(20, '-').format('Clear Remote Settings for BGP'))
        commands2 = [
            'configure',
            'routing',
            'bgp',
            'configure terminal',
            'no router bgp 2',
            'end', 'write file ',
            'exit', 'commit', 'end', 'exit']
        (rc2, output) = cl2.do_cli_commands(commands2, 1)
        if 'Error' not in output:
            logger.info('Clear Remote Settings Success!')
        return rc1 and rc2