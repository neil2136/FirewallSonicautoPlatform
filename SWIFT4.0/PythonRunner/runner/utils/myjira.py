from runner.settings import logger
from jira import JIRA

def fetch_jira_status(jira_num=None):
    token='ATATT3xFfGF0vGgKG18VOFdDYTviTunhr51dmiNYYg8Vg6h4iJ9Sl2DtxwyCyTlVAI_S1Anj7IBAYex-MovU1fTiluZBchE2VVF_lAlz8RI9PSrZraUaCLmC5333bh5J3KdFpUr__8X8o4tg3uPBzVGDDYqjRQTHlr5t2tdfIMZe6t06ORGkGy8=B0AE8A84'
    try:
        jira = JIRA(server='https://sonicwall.atlassian.net', basic_auth=('atlassian_cloud_auto_svcDL@sonicwall.com', token), proxies={'https':'https://10.50.128.110:3128'},timeout=20)
    except Exception as err:
        logger.warning('Access sonicwall.atlassian.net fail. Try not to use proxy 10.50.128.110:3128')
        jira = JIRA(server='https://sonicwall.atlassian.net', basic_auth=('atlassian_cloud_auto_svcDL@sonicwall.com', token),timeout=20)
    try:
        myissue = jira.issue(jira_num)
        status =str(myissue.fields.status)
    except Exception as err:
        logger.info(f'{jira_num} not exist.', exc_info=True)
        logger.debug(err)
        return None
    return status
