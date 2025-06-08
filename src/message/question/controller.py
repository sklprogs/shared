#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Question:
    ''' message.controller.Message.__init__ sets Graphical=False by default, so
        we have to reassign Graphical anyway when calling Question from shared.
        To quit an app correctly, the last GUI message must be non-blocking.
    '''
    def __init__(self, message, Graphical=False, Block=False):
        self.message = str(message)
        self.Graphical = Graphical
        self.Block = Block
    
    def get(self):
        if self.Graphical:
            from skl_shared.message.question.gui import QUESTION
        else:
            from skl_shared.message.question.logic import QUESTION
        return QUESTION
    
    def show(self):
        if not self.message:
            print('Empty message!')
            return
        iques = self.get()
        iques.set_message(self.message)
        return iques.show_blocked()
