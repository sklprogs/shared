#!/usr/bin/python3
# -*- coding: UTF-8 -*-

STOP = False
GRAPHICAL = True
MAX_LEN = 200

from skl_shared_qt.message.info.controller import Info
from skl_shared_qt.message.debug.controller import Debug
from skl_shared_qt.message.warning.controller import Warning
from skl_shared_qt.message.error.controller import Error
from skl_shared_qt.message.question.controller import Question
from skl_shared_qt.localize import _
from skl_shared_qt.basic_text import Shorten


class Report:
    
    def failed(self, func='Logic error', output='Logic error', Graphical=True):
        mes = _('Operation has failed!\n\nDetails: {}').format(output)
        Message(func, mes, Graphical).show_error()
    
    def lazy(self, func=_('Logic error!')):
        Message(func, _('Nothing to do!')).show_debug()
    
    def cancel(self, func=_('Logic error!')):
        Message(func, _('Operation has been canceled.')).show_warning()
    
    def wrong_input(self, func=_('Logic error!'), data=None):
        if data:
            mes = _('Wrong input data: "{}"!').format(data)
        else:
            mes = _('Wrong input data!')
        Message(func, mes, True).show_warning()
    
    def empty(self, func=_('Logic error!'), Graphical=False):
        Message(func, _('Empty input is not allowed!'), Graphical).show_warning()
    
    def not_ready(self, func=_('Logic error!')):
        Message(func, _('Not implemented yet!')).show_info()
    
    def empty_output(self, func=_('Logic error!')):
        Message(func, _('Empty output is not allowed!')).show_warning()
    
    def deleted(self, func=_('Logic error!'), count=0):
        if count:
            message = _('{} blocks have been deleted').format(count)
            Message(func, message).show_debug()
    
    def matches(self, func=_('Logic error!'), count=0):
        if count:
            message = _('{} matches').format(count)
            Message(func, message).show_debug()
    
    def third_party(self, func=_('Logic error!'), message=_('Logic error!')):
        mes = _('Third-party module has failed!\n\nDetails: {}').format(message)
        Message(func, mes, True).show_error()
    
    def condition(self, func=_('Logic error!'), message=_('Logic error!')):
        message = _('The condition "{}" is not observed!').format(message)
        Message(func, message, True).show_warning()



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
    def __init__(self, func, message, Graphical=False, Block=False, limit=200):
        self.type_ = _('INFO')
        self.func = str(func)
        self.message = str(message)
        self.Graphical = GRAPHICAL and Graphical
        self.Block = Block
        self.limit = limit
        self.shorten()

    def shorten(self):
        self.message = Shorten(self.message, MAX_LEN, ShowGap=True).run()
    
    def get_silent(self):
        FORMAT.reset(self.func, self.message, self.type_)
        return FORMAT.run()
    
    def get_message(self):
        if not self.Graphical:
            return self.get_silent()
        sub = _('Code block: {}').format(self.func)
        return f'{self.message}\n\n{sub}'
    
    def duplicate(self, inst):
        # Duplicate the message to the console, if necessary
        if self.Graphical:
            inst.message = self.get_silent()
            inst.Graphical = False
            inst.show()
    
    def show_debug(self):
        if STOP:
            return
        self.type_ = _('DEBUG')
        idebug = Debug(self.get_message(), self.Graphical, self.Block)
        idebug.show()
        self.duplicate(idebug)
    
    def show_error(self):
        if STOP:
            return
        self.type_ = _('ERROR')
        ierror = Error(self.get_message(), self.Graphical, self.Block)
        ierror.show()
        self.duplicate(ierror)

    def show_info(self):
        if STOP:
            return
        self.type_ = _('INFO')
        iinfo = Info(self.get_message(), self.Graphical, self.Block)
        iinfo.show()
        self.duplicate(iinfo)
                       
    def show_warning(self):
        if STOP:
            return
        self.type_ = _('WARNING')
        iwarn = Warning(self.get_message(), self.Graphical, self.Block)
        iwarn.show()
        self.duplicate(iwarn)

    def show_question(self):
        if STOP:
            return
        self.type_ = _('QUESTION')
        iques = Question(self.get_message(), self.Graphical, self.Block)
        #TODO: Duplicate
        return iques.show()


FORMAT = Format()
rep = Report()


if __name__ == '__main__':
    f = '[SharedQt] message.controller.__main__'
    Graphical = True
    Block = False
    #mes = 'Please note this debug!'
    #import sys
    #from PyQt6.QtWidgets import QApplication
    #root = QApplication(sys.argv)
    #Message(f, mes, Graphical, Block).show_debug()
    #Message(f, 'Tactical error.', True).show_error()
    #Message(f, 'Get ready to test', True).show_warning()
    #Message(f, 'Hello, everyone', True).show_info()
    #, Graphical=False
    answer = Message(f, 'Have you read this?', Graphical, Block).show_question()
    if answer:
        answer = 'Yes'
    else:
        answer = 'No'
    mes = f'You have answered {answer}'
    Message(f, mes, Graphical, Block).show_info()
    #sys.exit(root.exec())
