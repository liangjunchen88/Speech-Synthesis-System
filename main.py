import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import os
import sys
import time
from tts_ws_python3_demo import text2wav
from playsound import playsound


class TtsPlay:
    #Simple preparation of speech synthesis system
    def __init__(self):
        self.vcn = 'xiaoyan'
        #Establish a connection with the server of iFLYTEK open platform
        self.APP_ID = '51060aa3' # put into appid
        self.SECRET_KEY = 'NWU1Yjg1OGU0NGM3YjY0MTIwNTcxYTg5'  # put into apisecret
        self.API_KEY = 'fe25c066ae0c29a0d9027d3f0c611f83' # put into apikey

        #Design of graphics window in speech synthesis system
        self.fname = ""
        self.root = tk.Tk()  # Initialization window
        self.root.title("NLP Speech Synthesis System")  # Name of window
        self.root.geometry("600x550")  # Set window size
        self.root.resizable(0, 0)   # In order to fix the window size conveniently
        self.tk_lb = tk.Label(self.root, text='Choose the doctor you like')  # lable
        self.tk_text = tk.Text(self.root, width=77, height=30)  # Multiline text box
        self.tk_cb_vcn = ttk.Combobox(self.root, width=30)  # Drop down list box
        # Set the contents of the drop-down list box
        self.tk_cb_vcn['values'] = ("Sweet girl - Xiaoyan", "Friendly man - Xujiu", "Intellectual girl - Xiaoping",
                                    "Lovely children - Xuxiaobao", "Kind girl - Xiaoqing")
        self.tk_cb_vcn.current(0)  #Set the current selection status to 0, which is the first item
        self.tk_cb_vcn.bind("<<ComboboxSelected>>", self.select_vcn)
        self.tk_tts_file = tk.Label(self.root, text='Generate file name')
        self.b1 = tk.Button(self.root, text='Speech synthesis', width=20, height=1, command=self.xfyun_tts)  # button1
        self.tk_play = tk.Button(self.root, text='Play', width=10, height=1, command=self.play_sound)  # button2
        #Location of each component
        self.tk_tts_file.place(x=30, y=480)
        self.b1.place(x=300, y=500)
        self.tk_play.place(x=500, y=500)
        self.tk_lb.place(x=30, y=30)
        self.tk_cb_vcn.place(x=200, y=30)
        self.tk_text.place(x=30, y=60)
        self.root.mainloop()

    def select_vcn(self, *args):
        if self.tk_cb_vcn.get() == 'Sweet girl - Xiaoyan':
            self.vcn = "xiaoyan"
        elif self.tk_cb_vcn.get() == 'Friendly man - Xujiu':
            self.vcn = "aisjiuxu"
        elif self.tk_cb_vcn.get() == 'Intellectual girl - Xiaoping':
            self.vcn = "aisxping"
        elif self.tk_cb_vcn.get() == 'Lovely children - Xuxiaobao':
            self.vcn = "aisbabyxu"
        elif self.tk_cb_vcn.get() == 'Kind girl - Xiaoqing':
            self.vcn = "aisjinger"

    def xfyun_tts(self):
        tts_text = self.tk_text.get('0.0', 'end')  #Get text content
        #Spaces before and after and line breaks
        tts_text = tts_text.strip('\r\n')
        tts_text = tts_text.strip('\n')
        tts_text = tts_text.strip(' ')

        if not tts_text:
            tkinter.messagebox.showinfo("Tips", "Please enter the text content")
            return

        fname = time.strftime("%Y%m%d%H%M%S", time.localtime())
        self.fname = os.path.dirname(sys.argv[0]) + "/" + fname + ".wav"
        #print(self.fname)
        self.tk_tts_file["text"] = self.fname
        text2wav(self.APP_ID, self.SECRET_KEY, self.API_KEY, tts_text, self.vcn, self.fname)



    def play_sound(self):
        playsound(self.fname)


if __name__ == "__main__":
    TtsPlay()

