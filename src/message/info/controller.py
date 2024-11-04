#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Info:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from message.info.logic import INFO
        else:
            from message.info.gui import INFO
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
