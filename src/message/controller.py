#!/usr/bin/python3
# -*- coding: UTF-8 -*-

STOP_MES = False

import message.info.controller
import message.debug.controller
import message.warning.controller
import message.error.controller
import message.question.controller
from skl_shared_qt.localize import _
from skl_shared_qt.basic_text import Shorten


class Format:
    
    def __init__(self):
        self.count = 0
        self.type_ = _('INFO')
        self.func = _('Unknown procedure')
        self.message = ''
    
    def reset(self, func, message, type_):
        self.func = func
        self.message = message
        self.type_ = type_
    
    def increment(self):
        self.count += 1
    
    def get(self):
        return f'{self.count}:{self.func}:{self.type_}:{self.message}'
    
    def run(self):
        self.increment()
        return self.get()



class Message:
    # To quit an app correctly, the last GUI message must be non-blocking
    def __init__(self, func, message, Silent=True, Block=False, limit=200):
        self.type_ = _('INFO')
        self.func = str(func)
        self.message = str(message)
        self.Silent = Silent
        self.Block = Block
        self.limit = limit
        self.shorten()

    def shorten(self):
        self.message = Shorten(self.message, 200, ShowGap=True).run()
    
    def get_silent(self):
        FORMAT.reset(self.func, self.message, self.type_)
        return FORMAT.run()
    
    def get_message(self):
        if self.Silent:
            return self.get_silent()
        sub = _('Code block: {}').format(self.func)
        return f'{self.message}\n\n{sub}'
    
    def duplicate(self, inst):
        # Duplicate the message to the console, if necessary
        if not self.Silent:
            inst.message = self.get_silent()
            inst.Silent = True
            inst.show()
    
    def show_debug(self):
        if STOP_MES:
            return
        self.type_ = _('DEBUG')
        idebug = message.debug.controller.Debug(self.get_message(), self.Silent, self.Block)
        idebug.show()
        self.duplicate(idebug)
    
    def show_error(self):
        if STOP_MES:
            return
        self.type_ = _('ERROR')
        ierror = message.error.controller.Error(self.get_message(), self.Silent, self.Block)
        ierror.show()
        self.duplicate(ierror)

    def show_info(self):
        if STOP_MES:
            return
        self.type_ = _('INFO')
        iinfo = message.info.controller.Info(self.get_message(), self.Silent, self.Block)
        iinfo.show()
        self.duplicate(iinfo)
                       
    def show_warning(self):
        if STOP_MES:
            return
        self.type_ = _('WARNING')
        iwarn = message.warning.controller.Warning(self.get_message(), self.Silent, self.Block)
        iwarn.show()
        self.duplicate(iwarn)

    def show_question(self):
        if STOP_MES:
            return
        self.type_ = _('QUESTION')
        iques = message.question.controller.Question(self.get_message(), self.Silent, self.Block)
        #TODO: Duplicate
        return iques.show()


FORMAT = Format()


if __name__ == '__main__':
    f = '[SharedQt] message.controller.__main__'
    Silent = True
    Block = False
    #mes = 'Please note this debug!'
    #import sys
    #from PyQt6.QtWidgets import QApplication
    #root = QApplication(sys.argv)
    #Message(f, mes, Silent, Block).show_debug()
    #Message(f, 'Tactical error.', True).show_error()
    #Message(f, 'Get ready to test', True).show_warning()
    #Message(f, 'Hello, everyone', True).show_info()
    #, Silent=False
    answer = Message(f, 'Have you read this?', Silent, Block).show_question()
    if answer:
        answer = 'Yes'
    else:
        answer = 'No'
    mes = f'You have answered {answer}'
    Message(f, mes, Silent, Block).show_info()
    #sys.exit(root.exec())
