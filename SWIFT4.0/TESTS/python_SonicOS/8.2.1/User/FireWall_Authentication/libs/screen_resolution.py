import ctypes
from ctypes import wintypes

# Define constants
DM_PELSWIDTH = 0x00080000
DM_PELSHEIGHT = 0x00100000
CDS_UPDATEREGISTRY = 0x01
CDS_TEST = 0x02
DISP_CHANGE_SUCCESSFUL = 0
DISP_CHANGE_RESTART = 1


# Define DEVMODE structure
class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", ctypes.c_short),
        ("dmPaperSize", ctypes.c_short),
        ("dmPaperLength", ctypes.c_short),
        ("dmPaperWidth", ctypes.c_short),
        ("dmScale", ctypes.c_short),
        ("dmCopies", ctypes.c_short),
        ("dmDefaultSource", ctypes.c_short),
        ("dmPrintQuality", ctypes.c_short),
        ("dmColor", ctypes.c_short),
        ("dmDuplex", ctypes.c_short),
        ("dmYResolution", ctypes.c_short),
        ("dmTTOption", ctypes.c_short),
        ("dmCollate", ctypes.c_short),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD)
    ]

    # Function to change display settings
    def change_resolution(self, width, height):
        dm = DEVMODE()
        dm.dmSize = ctypes.sizeof(DEVMODE)
        dm.dmPelsWidth = width
        dm.dmPelsHeight = height
        dm.dmFields = DM_PELSWIDTH | DM_PELSHEIGHT

        result = ctypes.windll.user32.ChangeDisplaySettingsW(ctypes.byref(dm), CDS_UPDATEREGISTRY)

        if result == DISP_CHANGE_SUCCESSFUL:
            print("Screen resolution changed successfully")
        elif result == DISP_CHANGE_RESTART:
            print("You need to restart your computer for the changes to take effect")
        else:
            print("Failed to change screen resolution")

