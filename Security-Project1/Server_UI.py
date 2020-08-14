import Tkinter
import threading

import Tkinter
from Server import Server
from __builtin__ import raw_input


class Server_UI(Tkinter.Tk):

    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        threading.Thread(target=self.init_chat).start()


    def init_chat(self):
        filename = raw_input('Enter the file name where you want to save log otherwise enter "NO"')
        self.s=Server(self,filename)

    def initialize(self):
        self.grid()
        self.title('GL4 - Hackers Server')

        self.resizable('1', '1')

        self.ui_chatlist = Tkinter.Text(
            master=self,
            wrap=Tkinter.WORD,
            width=60,
            height=15,
            bg="gainsboro",
            fg="gray1")

        self.ui_log = Tkinter.Text(
            master=self,
            wrap=Tkinter.WORD,
            width=60,
            height=25,
            bg="gray1",
            fg="red2")

        self.ui_chatlist.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)
        self.ui_log.pack(side=Tkinter.TOP, fill=Tkinter.BOTH)

    def setChatlist(self,chatlist):
        text='          Chat List - %s Connected clients\n'%str(len(chatlist))
        for member in chatlist:
            text=text+str(member)+'\n'

        self.ui_chatlist.delete(1.0, 'end')
        self.ui_chatlist.insert(Tkinter.INSERT, "%s\n" % text)

    def addlog(self,log):
        self.ui_log.insert(Tkinter.INSERT, "%s\n" % (log))


app = Server_UI(None)
app.mainloop()