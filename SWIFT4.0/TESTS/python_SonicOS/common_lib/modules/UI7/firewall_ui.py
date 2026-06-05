from runner.utils.assertion import Assertion
from modules.UI7.common_require import *


class Firewall_UI(
               CommonRequire,
               Browser, 
               Navigation, 
               Administration, 
               UIHelper, 
               #ServiceObject,
               AddressObjects,
               Diagnostics,
               ScheduleObjects,
               #NetworkDNS, 
               UISafemode,
               SystemTime, 
               DHCPObjects,
               #HighAvailabilitySettings,
               #HighAvailabilityStatus,
               #HighAvailabilityMonitoring,
               ClientSsl,
               Uboot_Upgrade,
               #ServerSsl,
               L2TPServer,
               ):
    def __init__(self):
        CommonRequire.__init__(self)
        Browser.__init__(self)
        Navigation.__init__(self)
        Administration.__init__(self)
        Uboot_Upgrade.__init__(self)
        #ServiceObject.__init__(self)
        AddressObjects.__init__(self)
        Diagnostics.__init__(self)
        ScheduleObjects.__init__(self)
        #NetworkDNS.__init__(self)
        SystemTime.__init__(self)
        DHCPObjects.__init__(self)
        #HighAvailabilitySettings.__init__(self)
        #HighAvailabilityStatus.__init__(self)
        #HighAvailabilityMonitoring.__init__(self)
        ClientSsl.__init__(self)
        UISafemode.__init__(self)
        #ServerSsl.__init__(self)
        L2TPServer.__init__(self)
        UIHelper.__init__(self)
        self.ui_wrapper = self
        self.navigation = self
        self.common = self
        self.ui_helper = self
