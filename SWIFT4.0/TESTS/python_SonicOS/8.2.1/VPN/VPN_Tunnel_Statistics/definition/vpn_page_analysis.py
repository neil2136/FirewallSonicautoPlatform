from definition.settings import *

def tunnel_statistics(options):
    msg_url = "api/sonicos/dynamic-file/getStatsData.json?restype=11&datatype=1"
    logger.info(" {} ".center(20, '-').format('Get the value of spi in the Tunnel stastics url'))
    msg_res = fw_api.api_get(url=msg_url)
    spi = msg_res["data"]["activeIPsecSAs"][0]["statsLink"]
    statis_url = "api/sonicos/dynamic-file/getIpsecTunnelStats.json?spi=" 
    logger.info(" {} ".center(20, '-').format('Get the Tunnel stastics url'),statis_url+spi)
    logger.info(" {} ".center(20, '-').format('Get the Tunnel stastics Json'))
    statis_res1 =( fw_api.api_get(url = statis_url + spi))["data"]

    if options == "TRAFFIC":
        logger.info(" {} ".center(20, '-').format('The Option is TRAFFIC'))
        logger.info(" {} ".center(20, '-').format('Get the value of rxpkt, txpkts, rxbytes, txbytes before ping'))
        rxpkt1, txpkts1, rxbytes1, txbytes1 = int(statis_res1['rxPkts']), int(statis_res1['txPkts']), int(statis_res1['rxBytes']),  int(statis_res1['txBytes'])
        
        PC1.send_command("ping {} -c 6".format(PC2_IP))
        
        logger.info(" {} ".center(20, '-').format('Get the value of rxpkt, txpkts, rxbytes, txbytes after ping'))
        statis_res2 = (fw_api.api_get(url = statis_url + spi))["data"]
        rxpkt2, txpkts2, rxbytes2, txbytes2 = int(statis_res2['rxPkts']), int(statis_res2['txPkts']), int(statis_res2['rxBytes']),  int(statis_res2['txBytes'])
        
        if (rxpkt2 - rxpkt1) > 0 and (txpkts2 - txpkts1) > 0 \
            and (rxbytes2 - rxbytes1) > 0 and (txbytes2 - txbytes1 > 0):
            rc = True
        else:
            rc = False
        
    elif options == "ICON":
        logger.info(" {} ".center(20, '-').format('The Option is ICON'))
        createTm = statis_res1['createTm']
        expiry = statis_res1['expiry']
        logger.info(" {} ".center(20, '-').format('Get the value of createTm and expiry'),createTm,expiry)
        
        if re.search('\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', createTm) \
            and re.search('\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}', expiry):
            rc = True
        else:
            rc = False
        
    elif options == "RENEGOTIATE":
        logger.info(" {} ".center(20, '-').format('The Option is RENEGOTIATE'))
        
        in_spi = str(msg_res["data"]["activeIPsecSAs"][0]["inSpi"])
        headers = OrderedDict([('Accept', 'application/json'),
                    ('Content-Type', 'application/json'),
                    ('Accept-Encoding', 'application/json'),
                    ('X-SNWL-API-Scope', 'extended'),
                    ('charset', 'UTF-8')])
        cgi = {
        "stream": "cgiaction=ikeNegotiate&ikeSrcAddrType=4&ikeSrcNet=192.168.168.0&ikeSrcMask=255.255.255.0&ikeDstAddrType=4&ikeDstNet=172.16.1.0&ikeDstMask=255.255.255.0&ikeDstGw=12.12.1.201&ikeDstGwPort=500&InitCookie=JZbKrYOXmCk=&ikeIsDhcpClient=0&ikeInSpi="+in_spi
        }
        
        logger.info(" {} ".center(20, '-').format('Post the cgi to reset the tunnel statistics'))
        renegotiate = fw_api.api_post(url="api/sonicos/raw",data=cgi,headers=headers)
        logger.info(" {} ".center(20, '-').format('Get the statistics json after RENEGOTIATE'))
        statis_res2 = fw_api.api_get(url=msg_url)
        spi = statis_res2["data"]["activeIPsecSAs"][0]["statsLink"]
        statis_res2 = (fw_api.api_get(url=statis_url + spi))["data"]
        rxpkt, txpkts, rxbytes, txbytes,rxfrags, txfrag = int(statis_res2['rxPkts']), \
            int(statis_res2['txPkts']), int(statis_res2['rxBytes']),  int(statis_res2['txBytes']), \
            int(statis_res2['rxFrags']), int(statis_res2['txFrags'])

        if rxpkt==0 and txpkts == 0 and rxbytes == 0 and txbytes == 0 and \
            rxfrags ==0 and txfrag == 0:
            rc = True
        else:
            rc = False
    return rc
        

