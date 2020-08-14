#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import sys
import threading

import Tkinter
import tkFileDialog
from Client import client


class Client_UI(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.username = sys.argv[3]
        self.cip = '127.0.0.1'
        self.cport = 'cPort-9025'
        self.sip = sys.argv[1]
        self.sport = sys.argv[2]
        self.initialize()
        # img = Tkinter.Image.open("V.png")

        threading.Thread(target=self.init_chat).start()


    def init_chat(self):
        self.s=client(self)


    def initialize(self):
        self.grid()
        self.title('GL4 - Hackers Chatroom')
        self.wm_title("GUI Demo")
        self.resizable('1', '1')

        self.ui_State = Tkinter.Text(
            master=self,
            wrap=Tkinter.WORD,
            width=30,  # In chars
            height=11,
            bg="gray6",
            fg="firebrick2")

        self.ui_label = Tkinter.Text(
            master=self,
            wrap=Tkinter.WORD,
            width=50,  # In chars
            height=25,
            bg='gray8',
            fg='chartreuse2')  # In chars

        self.ui_input = Tkinter.Text(
            master=self,
            wrap=Tkinter.WORD,
            width=50,
            height=4,
            bg='gray5',
            fg='snow')

        self.ui_button_send = Tkinter.Button(
            master=self,
            text="Send",
            command=self.sendMsg)

        self.ui_button_file = Tkinter.Button(
            master=self,
            text="File",
            command=self.sendFile)

        # informations about connection
        self.ui_State.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.ui_State.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.ui_State.insert(Tkinter.INSERT, "             Connection informations\n\n")
        self.ui_State.insert(Tkinter.INSERT, "Client IP           %s\n" %self.cip)
        self.ui_State.insert(Tkinter.INSERT, "Client PORT         %s\n"%self.cport)
        self.ui_State.insert(Tkinter.INSERT, "Server IP Address   %s\n"%self.sip)
        self.ui_State.insert(Tkinter.INSERT, "Server PORT         %s\n"%self.sport)
        self.ui_State.insert(Tkinter.INSERT, "Nick                %s\n"%self.username)
        self.ui_State.insert(Tkinter.INSERT, "Status              Connected\n")
        self.ui_State.insert(Tkinter.INSERT, "Available clients   ")

        #where to display msg
        self.ui_label.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)

        #where to write msg
        self.ui_input.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.ui_input.bind("<Return>", self.OnPressEnter)

        self.ui_button_send.pack(side=Tkinter.LEFT)
        self.ui_button_file.pack(side=Tkinter.RIGHT)

    def sendMsg(self):

        msg = self.ui_input.get("0.0", Tkinter.END + "-1c")

        self.ui_label.insert(Tkinter.INSERT, "%s\n" % ('[Me] '+msg))
        self.s.send('['+self.username+'] ' + msg)

        self.ui_input.delete(1.0, 'end')
        self.ui_input.focus_set()

    def OnPressEnter(self, event):
        self.sendMsg()

    def insert_message(self,message):
        self.ui_label.insert(Tkinter.INSERT, "%s\n" % (message))


    def newConnection(self, member):
        self.ui_State.insert(Tkinter.INSERT, "%s - " % (member))


    def sendFile(self):
        print('pressed')
        filename = tkFileDialog.askopenfilename(initialdir="/", title="Select file",
                                                     filetypes=(("all files", "*.*"), ("jpeg files", "*.jpg")))
        print(filename+' ...')
        file= open(filename,'r')
        content=file.read()
        self.insert_message('[ME]'+content)
        self.s.send('[' + self.username + '] ' + content)


if __name__ == "__main__":
    app = Client_UI(None)
    #app.username=app.s.username
    #app.title('GL4 - Hackers Chatroom')
    # app.insert_message('inserted!')
    # thread.start_new_thread (app.mainloop,[None,[]])
    app.mainloop()
    # print('a')