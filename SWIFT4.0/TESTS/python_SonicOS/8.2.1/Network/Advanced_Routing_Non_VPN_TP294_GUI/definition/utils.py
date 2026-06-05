from runner.settings import Params, logger
import time
import csv


def _str_2_csv(text, decimal="|"):
    lines = csv.reader(text.split(decimal))
    return [line for line in lines][1:]


def check_routing_config(output, **kwargs):
    # items = 'isTunnelIf,isWlanTunnelIf,iface,ifName,pIface,pIfName,zoneName,rip,ripCfg'
    res = False
    allres = []
    if 'ifName' in kwargs.keys():
        try:
            convent_list = _str_2_csv(text=output['routedIfs'])
            logger.info(convent_list)
            for route in convent_list:
                if 'rip' in kwargs.keys():
                    if kwargs['ifName'] == 'ALL':
                        if route[3] == kwargs['ifName'] and route[7] == kwargs['rip']:
                            allres.append(True)
                        else:
                            allres.append(False)
                    elif route[3] == kwargs['ifName'] and route[7] == kwargs['rip']:
                        res = True
                        break
                elif 'ospf' in kwargs.keys():
                    if kwargs['ifName'] == 'ALL':
                        if route[3] == kwargs['ifName'] and route[7] == kwargs['ospf']:
                            allres.append(True)
                        else:
                            allres.append(False)
                    elif route[3] == kwargs['ifName'] and route[7] == kwargs['ospf']:
                        res = True
                        break
        except Exception as e:
            logger.info(repr(e))
    else:
        logger.info('the key ifName and rip not in kwargs.')
    if allres:
        logger.info(f'check all result: {allres}')
        res = all(allres)
    return res
