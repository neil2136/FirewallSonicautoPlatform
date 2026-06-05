case_dict = {
    "SOSAIOT-TC-54871":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'radio-2400mhz', 'ssid p_24g', 'exit',
                    'radio-5000mhz', 'ssid p_5g', 'exit'],
            "syslog_check": ["'SonicPointN name'.*?auto_1.*?changed to \[auto_1\]",
                             "'SonicPointN main radio mode'.*?auto_1.*?changed to \[5GHz 802.11ax/ac/n/a Mixed\]",
                             "'SonicPointN SSID'.*?auto_1.*?changed to \[p_5g\]",
                             "'SonicPointNDR Main Radio Mode'.*? auto_1.*?changed to \[2.4GHz 802.11ax/n/g/b Mixed\]",
                             "SonicPointNDR SSID'.*?auto_1.*?changed to \[p_24g\]"],
            "auditlog_check": ["Sonic PointN.*?auto_1.*?'SonicPointN name'.*?auto_1",
                               "Sonic PointN.*?auto_1.*?'SonicPointN main radio mode'.*?5GHz 802.11ax/ac/n/a Mixed",
                               "Sonic PointN.*?auto_1.*?'SonicPointN SSID'.*?p_5g",
                               "Sonic PointN.*?auto_1.*?'SonicPointNDR Main Radio Mode'.*?2.4GHz 802.11ax/n/g/b Mixed",
                               "Sonic PointN.*?auto_1.*?'SonicPointNDR SSID'.*?p_24g", ],
            "log_check": ["'SonicPointN name'.*?auto_1.*?changed to \[auto_1\]",
                          "'SonicPointN main radio mode'.*?auto_1.*?changed to \[5GHz 802.11ax/ac/n/a Mixed\]",
                          "'SonicPointN SSID'.*?auto_1.*?changed to \[p_5g\]",
                          "'SonicPointNDR Main Radio Mode'.*?auto_1.*?changed to \[2.4GHz 802.11ax/n/g/b Mixed\]",
                          "'SonicPointNDR SSID'.*?auto_1.*?changed to \[p_24g\]"],
            'snmplog_check': ["'SonicPointN name'.*?auto_1.*?changed to \[auto_1\]",
                              "'SonicPointN main radio mode'.*?auto_1.*?changed to \[5GHz 802.11ax/ac/n/a Mixed\]",
                              "'SonicPointN SSID'.*?auto_1.*?changed to \[p_5g\]",
                              "'SonicPointNDR Main Radio Mode'.*? auto_1.*?changed to \[2.4GHz 802.11ax/n/g/b Mixed\]",
                              "SonicPointNDR SSID'.*?auto_1.*?changed to \[p_24g\]"],
        },
    "SOSAIOT-TC-54872":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'radio-5000mhz',
                    'access-list'],
            "syslog_check": ["'Enable ACL'.*?auto_1.*?changed from \[ACL Disabled\].*?changed to \[ACL Enabled\]"
                             ],
            "auditlog_check": ["Sonic PointN.*?'Enable ACL'.*?ACL Disabled.*?ACL Enabled"],
            "log_check": ["'Enable ACL'.*?auto_1.*?changed from \[ACL Disabled\].*?changed to \[ACL Enabled\]"
                          ],
            'snmplog_check': ["'Enable ACL'.*?auto_1.*?changed from \[ACL Disabled\].*?changed to \[ACL Enabled\]"
                              ],
        },
    "SOSAIOT-TC-54873":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'radio-5000mhz',
                    'rssi enable'],
            "syslog_check": ["'Enable RSSI'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                             ],
            "auditlog_check": ["Sonic PointN.*?auto_1.*?'Enable RSSI'.*?disabled.*?enabled", ],
            "log_check": ["'Enable RSSI'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                          ],
            'snmplog_check': ["'Enable RSSI'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                              ],
        },
    "SOSAIOT-TC-54874":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'radio-2400mhz', 'band 20'],
            "syslog_check": [
                "'SonicPointNDR Radio Band'.*?auto_1.*?changed from \[Auto\].*?changed to \[Standard - 20 MHz Channel\]",
            ],
            "auditlog_check": [
                "Sonic PointN.*?auto_1.*?'SonicPointNDR Radio Band'.*?Auto.*?Standard - 20 MHz Channel", ],
            "log_check": [
                "'SonicPointNDR Radio Band'.*?auto_1.*?changed from \[Auto\].*?changed to \[Standard - 20 MHz Channel\]",
            ],
            'snmplog_check': [
                "'SonicPointNDR Radio Band'.*?auto_1.*?changed from \[Auto\].*?changed to \[Standard - 20 MHz Channel\]",
            ],
        },
    "SOSAIOT-TC-54875":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'radio-2400mhz', 'max-clients 21'],
            "syslog_check": ["'SonicPointNDR Max Clients'.*?auto_1.*?changed from \[32\].*?changed to \[21\]",
                             ],
            "auditlog_check": ["Sonic PointN.*?auto_1.*?'SonicPointNDR Max Clients'.*?32.*?21",
                               ],
            "log_check": ["'SonicPointNDR Max Clients'.*?auto_1.*?changed from \[32\].*?changed to \[21\]",
                          ],
            'snmplog_check': ["'SonicPointNDR Max Clients'.*?auto_1.*?changed from \[32\].*?changed to \[21\]",
                              ],
        },
    "SOSAIOT-TC-54876":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'widp-sensor schedule always-on'],
            "syslog_check": ["'SonicPointN WIDP Sensor'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                             ],
            "auditlog_check": ["Sonic PointN.*?auto_1.*?'SonicPointN WIDP Sensor'.*?disabled.*?enabled",
                               ],
            "log_check": ["'SonicPointN WIDP Sensor'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                          ],
            'snmplog_check': ["'SonicPointN WIDP Sensor'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                              ],
        },
    "SOSAIOT-TC-54877":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'wwan enable', 'wwan bound-to X3:V15'],
            "syslog_check": ["'Enable 3G/4G/LTE Modem'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                             "'Vlan Interface'.*?auto_1.*?changed from \[Any\].*?changed to \[X3:V15\]"
                             ],
            "auditlog_check": ["Sonic PointN.*?auto_1.*?'Enable 3G/4G/LTE Modem'.*?disabled.*?enabled",
                               "Sonic PointN.*?auto_1.*?'Vlan Interface'.*?Any.*?X3:V15",
                               ],
            "log_check": ["'Enable 3G/4G/LTE Modem'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                          "'Vlan Interface'.*?auto_1.*?changed from \[Any\].*?changed to \[X3:V15\]"],
            'snmplog_check': ["'Enable 3G/4G/LTE Modem'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
                              "'Vlan Interface'.*?auto_1.*?changed from \[Any\].*?changed to \[X3:V15\]"],
        },
    "SOSAIOT-TC-54878":
        {
            "cli": ['configure', 'sonicpoint', 'profile waveax auto_1', 'ble advertisement'],
            "syslog_check": [
                "'SonicWave Bluetooth LE Advertisement Enabled'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            "auditlog_check": [
                "Sonic PointN.*?auto_1.*?'SonicWave Bluetooth LE Advertisement Enabled'.*?disabled.*?enabled",
            ],
            "log_check": [
                "'SonicWave Bluetooth LE Advertisement Enabled'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            'snmplog_check': [
                "'SonicWave Bluetooth LE Advertisement Enabled'.*?auto_1.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
        },
    "SOSAIOT-TC-54887":
        {
            "cli": ['configure', 'sonicpoint', 'floor-plan auto_test', 'scale 10'],
            "syslog_check": ["'Floor Plan Name'.*?auto_test.*?changed to \[auto_test\]",
                             "'Floor Plan Scale'.*?auto_test.*?changed to \[10.0\]",
                             ],
            "auditlog_check": [
                "Floor Plan.*?auto_test.*?'Floor Plan Scale'.*?10.0",
                "Floor Plan.*?auto_test.*?'Floor Plan Name'.*?auto_test",
            ],
            "log_check": ["'Floor Plan Name'.*?auto_test.*?changed to \[auto_test\]",
                          "'Floor Plan Scale'.*?auto_test.*?changed to \[10.0\]", ],
            'snmplog_check': ["'Floor Plan Name'.*?auto_test.*?changed to \[auto_test\]",
                              "'Floor Plan Scale'.*?auto_test.*?changed to \[10.0\]", ],
        },
    "SOSAIOT-TC-54888":
        {
            "cli": ['configure', 'sonicpoint', 'ids', 'scan all'],
            "syslog_check": [
                "Scan SonicPoint Ids AP",
            ],
            "auditlog_check": ["Scan SonicPoint Ids AP"],
            "log_check": ["Scan SonicPoint Ids AP"],
            'snmplog_check': ["Scan SonicPoint Ids AP"],
        },
    "SOSAIOT-TC-54889":
        {
            "cli": ['configure', 'sonicpoint', 'widp', 'enable'],
            "syslog_check": [
                "'Enable Rogue Access Point Detection'.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            "auditlog_check": ["'Enable Rogue Access Point Detection'.*?disabled.*?enabled", ],
            "log_check": ["'Enable Rogue Access Point Detection'.*?changed from \[disabled\].*?changed to \[enabled\]",
                          ],
            'snmplog_check': [
                "'Enable Rogue Access Point Detection'.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
        },
    "SOSAIOT-TC-54891":
        {
            "cli": ['configure', 'sonicpoint', 'virtual-access-point profile auto_p', ],
            "syslog_check": [
                "'Virtual Access Point/Group/NAME'.*?auto_p.*?changed to \[auto_p\]",
                "'Address Object type of Virtual Access Point entity'.*?auto_p.*?changed to \[Virtual Access Point Profile\]",
                "'Virtual Access Point Group type'.*?auto_p.*?changed to \[Sonic Point\]", ],
            "auditlog_check": ["Vap Object.*?auto_p.*?'Virtual Access Point Group type'.*?Sonic Point",
                               "Vap Object.*?auto_p.*?'Address Object type of Virtual Access Point entity'.*?Virtual Access Point Profile",
                               "Vap Object.*?auto_p.*?'Virtual Access Point/Group/NAME'.*?auto_p", ],
            "log_check": ["'Virtual Access Point/Group/NAME'.*?auto_p.*?changed to \[auto_p\]",
                          "'Address Object type of Virtual Access Point entity'.*?auto_p.*?changed to \[Virtual Access Point Profile\]",
                          "'Virtual Access Point Group type'.*?auto_p.*?changed to \[Sonic Point\]", ],
            'snmplog_check': ["'Virtual Access Point/Group/NAME'.*?auto_p.*?changed to \[auto_p\]",
                              "'Address Object type of Virtual Access Point entity'.*?auto_p.*?changed to \[Virtual Access Point Profile\]",
                              "'Virtual Access Point Group type'.*?auto_p.*?changed to \[Sonic Point\]", ],
        },
    "SOSAIOT-TC-54892":
        {
            "cli": ['configure', 'sonicpoint', 'rf-monitoring', 'no null-probe-response'],
            "syslog_check": [
                "'RFM: Enable Null Probe Response Detection'.*?changed from \[enabled\].*?changed to \[disabled\]",
            ],
            "auditlog_check": ["'RFM: Enable Null Probe Response Detection'.*?enabled.*?disabled", ],
            "log_check": [
                "'RFM: Enable Null Probe Response Detection'.*?changed from \[enabled\].*?changed to \[disabled\]",
            ],
            'snmplog_check': [
                "'RFM: Enable Null Probe Response Detection'.*?changed from \[enabled\].*?changed to \[disabled\]",
            ],
        },
    "SOSAIOT-TC-54893":
        {
            "cli": ['configure', 'sonicpoint', 'ids', 'scan all'],
            "syslog_check": [
                "Scan SonicPoint Ids AP",
            ],
            "auditlog_check": ["Scan SonicPoint Ids AP"],
            "log_check": ["Scan SonicPoint Ids AP"],
            'snmplog_check': ["Scan SonicPoint Ids AP"],
        },
    "SOSAIOT-TC-54894":
        {
            "cli": ['configure', 'sonicpoint', 'fairnet enable', ],
            "syslog_check": [
                "'Enable FairNet'.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            "auditlog_check": ["'Enable FairNet'.*?disabled.*?enabled", ],
            "log_check": ["'Enable FairNet'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
            'snmplog_check': ["'Enable FairNet'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
        },
    "SOSAIOT-TC-54895":
        {
            "cli": ['configure', 'sonicpoint', 'wmm profile auto_wmm', ],
            "syslog_check": [
                "'Wlan WMM Profile ID'.*?auto_wmm.*?changed to \[auto_wmm\]",
            ],
            "auditlog_check": ["Wmm.*?auto_wmm.*?'Wlan WMM Profile ID'.*?auto_wmm", ],
            "log_check": ["'Wlan WMM Profile ID'.*?auto_wmm.*?changed to \[auto_wmm\]", ],
            'snmplog_check': ["'Wlan WMM Profile ID'.*?auto_wmm.*?changed to \[auto_wmm\]", ],
        },
    "SOSAIOT-TC-54896":
        {
            "cli": ['configure', 'sonicpoint', 'rrm', 'enable'],
            "syslog_check": [
                "'Enable RRM'.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            "auditlog_check": ["'Enable RRM'.*?disabled.*?enabled", ],
            "log_check": ["'Enable RRM'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
            'snmplog_check': ["'Enable RRM'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
        },
    "SOSAIOT-TC-54897":
        {
            "cli": ['configure', 'sonicpoint', 'rrm', 'sta threshold 30', 'radio threshold 40'],
            "syslog_check": [
                "'Station Quality'.*?changed from \[20\].*?changed to \[30\]",
                "'Radio Quality'.*?changed from \[20\].*?changed to \[40\]"
            ],
            "auditlog_check": ["'Radio Quality'.*?20.*?40",
                               "'Station Quality'.*?20.*?30", ],
            "log_check": ["'Station Quality'.*?changed from \[20\].*?changed to \[30\]",
                          "'Radio Quality'.*?changed from \[20\].*?changed to \[40\]"],
            'snmplog_check': ["'Station Quality'.*?changed from \[20\].*?changed to \[30\]",
                              "'Radio Quality'.*?changed from \[20\].*?changed to \[40\]"],
        },
    "SOSAIOT-TC-54898":
        {
            "cli": ['configure', 'sonicpoint', 'rrm', 'dcs global'],
            "syslog_check": [
                "'Enable Auto Channel'.*?changed from \[disabled\].*?changed to \[enabled\]",
            ],
            "auditlog_check": ["'Enable Auto Channel'.*?disabled.*?enabled", ],
            "log_check": ["'Enable Auto Channel'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
            'snmplog_check': ["'Enable Auto Channel'.*?changed from \[disabled\].*?changed to \[enabled\]", ],
        },
    "SOSAIOT-TC-54899":
        {
            "cli": ['configure', 'sonicpoint', 'rrm', 'dcsscheme24g swift', 'dcsscheme5g steady'],
            "syslog_check": [
                "'Auto Channel 2.4G Mode'.*?changed from \[0\].*?changed to \[2\]",
                "'Auto Channel 5G Mode'.*?changed from \[0\].*?changed to \[1\]",
            ],
            "auditlog_check": ["'Auto Channel 5G Mode'.*?0.*?1",
                               "'Auto Channel 2.4G Mode'.*?0.*?2", ],
            "log_check": ["'Auto Channel 2.4G Mode'.*?changed from \[0\].*?changed to \[2\]",
                          "'Auto Channel 5G Mode'.*?changed from \[0\].*?changed to \[1\]", ],
            'snmplog_check': ["'Auto Channel 2.4G Mode'.*?changed from \[0\].*?changed to \[2\]",
                              "'Auto Channel 5G Mode'.*?changed from \[0\].*?changed to \[1\]", ],
        },
}
