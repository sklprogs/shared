#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.logic as lg
import skl_shared_qt.gui as gi
import skl_shared_qt.message.controller as ms

FONT1 = 'Serif 14'
FONT2 = 'Sans 11'


class Directory(lg.Directory):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Email(lg.Email):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Table(lg.Table):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class File(lg.File):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Get(lg.Get):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Home(lg.Home):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Input(lg.Input):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Launch(lg.Launch):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class List(lg.List):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class OSSpecific(lg.OSSpecific):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Online(lg.Online):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ProgramDir(lg.ProgramDir):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Path(lg.Path):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class ReadTextFile(lg.ReadTextFile):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Search(lg.Search):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Text(lg.Text):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Time(lg.Time):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Timer(lg.Timer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class WriteTextFile(lg.WriteTextFile):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



class Objects(lg.Objects):
    
    def __init__(self):
        ''' #NOTE: Since we use 'super' here, attributes of 'lg.Objects'
            set directly in the controller will not be reflected in
            'logic'. Use 'logic' methods to set attributes.
        '''
        super().__init__()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()


com = Commands()
objs = Objects()


if __name__ == '__main__':
    f = '[SharedQt] shared.__main__'
    com.start()
    #lg.ReadTextFile('/tmp/aaa').get()
    #Geometry(Top()).activate()
    #idebug = Debug(f, 'Here should be some debug info')
    # This MUST be on a separate line, the widget will not be shown otherwise
    #idebug.show()
    Graphical = True
    Block = False
    '''
    mes = 'This is a standard message.'
    ms.Message(f, mes, Graphical).show_info()
    mes = 'Here should be some debug info'
    ms.Message(f, mes, Graphical).show_debug()
    mes = 'This is a warning'
    ms.Message(f, mes, Graphical).show_warning()
    mes = 'And this is an error!'
    ms.Message(f, mes, Graphical).show_error()
    '''
    mes = 'Have you read this?'
    answer = ms.Message(f, mes, Graphical, False).show_question()
    if answer:
        answer = 'Yes'
    else:
        answer = 'No'
    mes = f'Your answer is {answer}'
    ms.Message(f, mes, True).show_debug()
    # To quit correctly, the last GUI message must be non-blocking
    com.end()
