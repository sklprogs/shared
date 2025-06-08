#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Error:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Graphical=False, Block=False):
        self.message = str(message)
        self.Graphical = Graphical
        self.Block = Block
    
    def get(self):
        if self.Graphical:
            from skl_shared.message.error.gui import ERROR
        else:
            from skl_shared.message.error.logic import ERROR
        return ERROR
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        ierror = self.get()
        ierror.set_message(self.message)
        if self.Block:
            ierror.show_blocked()
        else:
            ierror.show()
