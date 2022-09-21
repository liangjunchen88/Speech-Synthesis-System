# -*- coding:utf-8 -*-
#
#   author: iflytek
#
#  The running environment for this demo test is: Windows + Python3.7
#  The third-party libraries and their versions installed when the demo test runs successfully are as follows:
#   cffi==1.12.3
#   gevent==1.4.0
#   greenlet==0.4.15
#   pycparser==2.19
#   six==1.12.0
#   websocket==0.2.1
#   websocket-client==0.56.0
#   To synthesize small languages, it is necessary to transmit the small language text,
#   use the small language pronunciation person vcn, tte=unicode, and modify the text encoding method
#  Error code link: https://www.xfyun.cn/document/error-code (must be read when code returns error code)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import websocket
import datetime
import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import ssl
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import _thread as thread
import os
import wave
from playsound import playsound

STATUS_FIRST_FRAME = 0  # first frame ID
STATUS_CONTINUE_FRAME = 1  # Intermediate frame ID
STATUS_LAST_FRAME = 2  # last frame ID

PCM_PATH = "./demo.pcm"


class Ws_Param(object):
    # initialization
    def __init__(self):
        self.tts_vcn = ""
        self.tts_business_args = ""
        self.tts_common_args = ""
        self.tts_text_data = ""
        self.APPID = ""
        self.APIKey = ""
        self.APISecret = ""

    def set_tts_params(self, text, vcn):
        self.tts_vcn = vcn
        self.tts_business_args = {"aue": "raw", "auf": "audio/L16;rate=16000", "vcn": self.tts_vcn, "tte": "utf8"}
        self.tts_text_data = {"status": 2, "text": str(base64.b64encode(text.encode('utf-8')), "UTF8")}
        #The following methods must be used to use small languages.
        #Here, Unicode refers to the coding method of utf16 small end, namely "utf-16le"
        # self.tts_text_data = {"status": 2, "text": str(base64.b64encode(self.Text.encode('utf-16')), "UTF8")}

    def set_params(self, appid, api_seccret, api_key):
        if appid != "":
            self.APPID = appid
            self.tts_common_args = {"app_id": self.APPID}

        if api_key != "":
            self.APIKey = api_key

        if api_seccret != "":
            self.APISecret = api_seccret

    # Generate URL
    def create_url(self):
        url = 'wss://tts-api.xfyun.cn/v2/tts'
        #Generate timestamps in rfc1123 format
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        #Splicing strings
        signature_origin = "host: " + "ws-api.xfyun.cn" + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + "/v2/tts " + "HTTP/1.1"
        #Hmac-sha256 is used for encryption
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            self.APIKey, "hmac-sha256", "host date request-line", signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        #Combine the requested authentication parameters into a dictionary
        v = {
            "authorization": authorization,
            "date": date,
            "host": "ws-api.xfyun.cn"
        }
        url = url + '?' + urlencode(v)
        return url


def on_message(ws, message):
    try:
        message = json.loads(message)
        code = message["code"]
        sid = message["sid"]
        audio = message["data"]["audio"]
        audio = base64.b64decode(audio)
        status = message["data"]["status"]
        print(code, sid, status)
        if status == 2:
            print("ws is closed")
            ws.close()
        if code != 0:
            err_msg = message["message"]
            print("sid:%s call error:%s code is:%s" % (sid, err_msg, code))
        else:
            with open(PCM_PATH, 'ab') as f:
                f.write(audio)

    except Exception as e:
        print("receive msg,but parse exception:", e)


#Processing of websocket error received
def on_error(ws, error):
    print("### error:", error)


#Processing of closing websocket received
def on_close(ws):
    print("### closed ###")


#Receive the process of establishing websocket connection
def on_open(ws):
    def run(*args):
        d = {"common": wsParam.tts_common_args,
             "business": wsParam.tts_business_args,
             "data": wsParam.tts_text_data,
             }
        d = json.dumps(d)
        print("------>Start sending text data")
        ws.send(d)
        if os.path.exists(PCM_PATH):
            os.remove(PCM_PATH)

    thread.start_new_thread(run, ())


def text2wav(appid, api_secret, api_key, text, vcn, fname):
    wsParam.set_params(appid, api_secret, api_key)
    wsParam.set_tts_params(text, vcn)
    websocket.enableTrace(False)
    ws_url = wsParam.create_url()
    ws = websocket.WebSocketApp(ws_url, on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    pcm2wav(PCM_PATH, fname)
    #return fname



def pcm2wav(fname, dstname):
    with open(fname, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
        print(len(pcmdata))
    with wave.open(dstname, "wb") as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)


wsParam = Ws_Param()

# Note that you need to fill in your own appid, api_secret, api_key
if __name__ == "__main__":

    playsound( text2wav(appid='51060aa3',
             api_secret='NWU1Yjg1OGU0NGM3YjY0MTIwNTcxYTg5',
             api_key='fe25c066ae0c29a0d9027d3f0c611f83',
             text="it is a test  hhhh",
             vcn="aisjiuxu",
             fname="./demo.wav"))
