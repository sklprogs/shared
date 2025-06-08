#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Debug:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Graphical=False, Block=False):
        self.message = str(message)
        self.Graphical = Graphical
        self.Block = Block
    
    def get(self):
        if self.Graphical:
            from skl_shared.message.debug.gui import DEBUG
        else:
            from skl_shared.message.debug.logic import DEBUG
        return DEBUG
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        idebug = self.get()
        idebug.set_message(self.message)
        if self.Block:
            idebug.show_blocked()
        else:
            idebug.show()
