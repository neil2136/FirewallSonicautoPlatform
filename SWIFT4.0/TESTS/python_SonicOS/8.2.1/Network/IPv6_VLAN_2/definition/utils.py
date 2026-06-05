from runner.settings import logger


def get_client_global_v6_addr(pc):
    try:
        out = pc.send_command(
            "ifconfig eth1 | grep '2013:' | awk '{print $2}'")
        logger.info(f"{pc.ip}'s eth1 ipv6 addr is {out.strip()}")
        if out:
            return out.strip()
        else:
            logger.error(f"{pc.ip} get ipv6 addr failed!")
            return ''
    except Exception as e:
        logger.error(f'error: {e}')
        logger.error('not found global v6 addr')
        return ''
