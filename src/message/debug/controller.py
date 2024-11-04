#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Debug:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from message.debug.logic import DEBUG
        else:
            from message.debug.gui import DEBUG
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
