#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Warning:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from message.warning.logic import WARN
        else:
            from message.warning.gui import WARN
        return WARN
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        iwarn = self.get()
        iwarn.set_message(self.message)
        if self.Block:
            iwarn.show_blocked()
        else:
            iwarn.show()
