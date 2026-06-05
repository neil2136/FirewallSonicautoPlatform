from definition.settings import *


def init_test_page(refresh=3):
    base_url = f'https://{Parameter.FIREWALL}/sonicui/7/m/mgmt/'
    url = base_url + 'policies/ngpe-access-rules'
    fw_page_ui.login_ui_with_head(browser_type='chrome', headless=True)
    fw_page_ui.go_to_url(url)
    fw_page_ui.wait_for_page_data_to_be_rendered()
    for i in range(refresh):
        logger.info(f'Refresh for {i + 1} time')
        fw_page_ui.refresh_browser()
        fw_page_ui.wait_for_page_data_to_be_rendered()
