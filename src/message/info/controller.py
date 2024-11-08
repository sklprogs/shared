#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Info:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Graphical=False, Block=False):
        self.message = str(message)
        self.Graphical = Graphical
        self.Block = Block
    
    def get(self):
        if self.Graphical:
            from skl_shared_qt.message.info.gui import INFO
        else:
            from skl_shared_qt.message.info.logic import INFO
        return INFO
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        iinfo = self.get()
        iinfo.set_message(self.message)
        if self.Block:
            iinfo.show_blocked()
        else:
            iinfo.show()
