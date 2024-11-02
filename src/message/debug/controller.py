#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Debug:
    
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from debug.logic import DEBUG
        else:
            from debug.gui import DEBUG
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
