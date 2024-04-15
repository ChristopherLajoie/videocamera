import sys
import os
#from siyi_sdk import SIYISDK
from siyi_sdk.stream import SIYIRTSP, RTMPSender

if __name__=="__main__":
    rtsp = SIYIRTSP(rtsp_url="rtsp://192.168.144.25:8554/main.264",debug=False)
    rtsp.setShowWindow(True)
