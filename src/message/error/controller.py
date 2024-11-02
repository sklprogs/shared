#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Error:
    
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from error.logic import ERROR
        else:
            from error.gui import ERROR
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
