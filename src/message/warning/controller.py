#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Warning:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, message, Graphical=False, Block=False):
        self.message = str(message)
        self.Graphical = Graphical
        self.Block = Block
    
    def get(self):
        if self.Graphical:
            from skl_shared_qt.message.warning.gui import WARN
        else:
            from skl_shared_qt.message.warning.logic import WARN
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
