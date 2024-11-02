#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Question:
    ''' message.controller.Message.__init__ sets Silent=True by default, so we
        have to reassign Silent anyway when calling Question from shared.
    '''
    def __init__(self, message, Silent=True, Block=False):
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
    
    def get(self):
        if self.Silent:
            from question.logic import QUESTION
        else:
            from question.gui import QUESTION
        return QUESTION
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        iques = self.get()
        iques.set_message(self.message)
        return iques.show_blocked()
