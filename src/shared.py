#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
import re
import io
import pyperclip
from skl_shared_qt.localize import _
import skl_shared_qt.logic as lg
import skl_shared_qt.gui as gi

GUI_MES = True
STOP_MES = False
FONT1 = 'Serif 14'
FONT2 = 'Sans 11'


class Font:
    
    def __init__(self,widget,family,size):
        self.Success = True
        self.font = None
        self.family = ''
        self.gui = gi.Font()
        self.widget = widget
        self.family = family
        self.size = size
        self.check()
    
    def fail(self,f,e):
        self.Success = False
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        objs.get_mes(f,mes).show_error()
    
    def set_parent(self):
        f = '[SharedQt] shared.Font.set_parent'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_parent(self.widget,self.font)
        except Exception as e:
            self.fail(f,e)
    
    def set_family(self):
        f = '[SharedQt] shared.Font.set_family'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_family(self.font,self.family)
        except Exception as e:
            self.fail(f,e)
    
    def set_size(self):
        f = '[SharedQt] shared.Font.set_size'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.gui.set_size(self.font,self.size)
        except Exception as e:
            self.fail(f,e)
    
    def set_font(self):
        f = '[SharedQt] shared.Font.set_font'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.font = self.gui.get_font()
        except Exception as e:
            self.fail(f,e)
        
    def check(self):
        f = '[SharedQt] shared.Font.check'
        if not self.widget:
            com.rep_empty(f)
            self.Success = False
            return
        if not self.family:
            com.rep_empty(f)
            self.Success = False
            return
        if not self.size:
            com.rep_empty(f)
            self.Success = False
            return
    
    def run(self):
        self.set_font()
        self.set_family()
        self.set_size()
        self.set_parent()



class Entry:
    
    def __init__(self):
        self.gui = gi.Entry()
        self.widget = self.gui.widget
    
    def set_min_width(self,width):
        self.gui.set_min_width(width)
    
    def bind(self,hotkey,action):
        self.gui.bind(hotkey,action)
    
    def clear(self):
        self.gui.clear()
    
    def get(self):
        return self.gui.get()
    
    def insert(self,text):
        self.gui.insert(str(text))
    
    def focus(self):
        self.gui.focus()



class Top:

    def __init__(self):
        self.gui = gi.Top()
        self.widget = self.gui.widget
    
    def add_widget(self,item):
        f = '[SharedQt] shared.Top.add_widget'
        if hasattr(item,'widget'):
            self.gui.add_widget(item.widget)
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f,mes,True).show_error()
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
    
    def bind(self,hotkey,action):
        self.gui.bind(hotkey,action)



class TestTop(Top):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_bindings()
    
    def set_bindings(self):
        self.bind('Ctrl+Q',self.close)
        self.bind('Esc',self.close)



class OptionMenu:
    
    def __init__(self,parent=None):
        self.parent = parent
        self.gui = gi.OptionMenu(self.parent)
        self.widget = self.gui.widget
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
        
    def set(self,item):
        f = '[SharedQt] shared.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.gui.set(item)
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(item,'; '.join(self.items))
            objs.get_mes(f,mes).show_error()
    
    def fill(self):
        self.gui.fill(self.items)

    def reset(self,items=[],default=None):
        self.items = [str(item) for item in items]
        self.fill()
        if default is not None:
            self.set(default)
        if len(self.items) < 2:
            self.disable()
        else:
            self.enable()

    def get(self):
        return self.gui.get()
    
    def get_index(self):
        return self.gui.get_index()
    
    def set_index(self,index_):
        return self.gui.set_index(index_)

    def set_prev(self):
        index_ = self.get_index()
        if index_ == 0:
            index_ = len(self.items) - 1
        else:
            index_ -= 1
        self.set_index(index_)

    def set_next(self):
        index_ = self.get_index()
        if index_ == len(self.items) - 1:
            index_ = 0
        else:
            index_ += 1
        self.set_index(index_)



class Button(gi.Button):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class DummyMessage:

    def __init__(self,*args):
        pass

    def show_debug(self):
        pass
    
    def show_error(self):
        pass

    def show_info(self):
        pass
                       
    def show_warning(self):
        pass

    def show_question(self):
        pass



class CreateConfig(lg.CreateConfig):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class CreateInstance(lg.CreateInstance):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Config(lg.Config):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Decline(lg.Decline):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class DefaultKeys(lg.DefaultKeys):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Dic(lg.Dic):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Diff(lg.Diff):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Directory(lg.Directory):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Email(lg.Email):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class FastTable(lg.FastTable):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class File(lg.File):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class FilterList(lg.FilterList):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class FixBaseName(lg.FixBaseName):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Get(lg.Get):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Grep(lg.Grep):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Home(lg.Home):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Hotkeys(lg.Hotkeys):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Input(lg.Input):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Launch(lg.Launch):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Links(lg.Links):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class List(lg.List):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Log(lg.Log):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class MessagePool(lg.MessagePool):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class OCR(lg.OCR):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class OSSpecific(lg.OSSpecific):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Online(lg.Online):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Path(lg.Path):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ProgramDir(lg.ProgramDir):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ReadBinary(lg.ReadBinary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class ReadTextFile(lg.ReadTextFile):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Search(lg.Search):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Shortcut(lg.Shortcut):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Text(lg.Text):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class TextDic(lg.TextDic):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Time(lg.Time):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Timer(lg.Timer):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteBinary(lg.WriteBinary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteTextFile(lg.WriteTextFile):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Clipboard:

    def __init__(self,Silent=False):
        ''' I use a combined approach of different methods here.
            On Linux text seems to be put in a wrong buffer when
            copying using Tkinter (Wine apps read clipboard filled
            by other Linux apps but *sometimes* fail to read mine
            (a previous buffer is returned)). At the same time,
            my Tkinter apps freeze upon Ctrl-V when pasting using
            pyperclip.paste(). So, I use pyperclip to copy and
            Tkinter to paste.
        '''
        self.Silent = Silent
        self.gui = gi.Clipboard()

    def copy(self,text,CopyEmpty=True):
        f = '[SharedQt] shared.Clipboard.copy'
        if text or CopyEmpty:
            text = lg.com.sanitize(text)
            try:
                pyperclip.copy(text)
            except Exception as e:
                com.rep_failed(f,e,self.Silent)
        else:
            com.rep_empty(f)

    def paste(self):
        f = '[SharedQt] shared.Clipboard.paste'
        try:
            text = str(self.gui.paste())
        except Exception as e:
            text = ''
            e = str(e)
            if "CLIPBOARD selection doesn't exist" in e:
                mes = _('Clipboard is empty!')
                objs.get_mes(f,mes,True).show_warning()
            else:
                com.rep_failed(f,e,self.Silent)
        # Further possible actions: strip, delete double line breaks
        return text



class Objects(lg.Objects):
    
    def __init__(self):
        ''' #NOTE: Since we use 'super' here, attributes of 'lg.Objects'
            set directly in the controller will not be reflected in
            'logic'. Use 'logic' methods to set attributes.
        '''
        super().__init__()
        self.question = self.info = self.warning = self.debug \
                      = self.error = self.mes = self.waitbox \
                      = self.txt = None
    
    def get_txt(self,font=FONT1,Maximize=False):
        if self.txt is None:
            self.txt = TextBoxRW (title = _('Test:')
                                 ,font = font
                                 ,Maximize = Maximize
                                 )
        return self.txt
    
    def get_mes (self,func='Logic error'
                ,message='Logic error'
                ,Silent=False
                ):
        if STOP_MES:
            return DummyMessage()
        if self.mes is None:
            self.mes = Message
        return self.mes(func,message,Silent)
    
    def get_waitbox(self,icon=''):
        if self.waitbox is None:
            if not icon:
                icon = self.icon
            self.waitbox = WaitBox(icon)
        return self.waitbox
    
    def get_root(self):
        return gi.objs.get_root()
    
    def get_error(self):
        if self.error is None:
            self.error = gi.Message().get_error()
        return self.error
    
    def get_warning(self):
        if self.warning is None:
            self.warning = gi.Message().get_warning()
        return self.warning
    
    def get_debug(self):
        # Reusing the same 'info' object may result in GUI glitches
        if self.debug is None:
            self.debug = gi.Message().get_debug()
        return self.debug
    
    def get_info(self):
        if self.info is None:
            self.info = gi.Message().get_info()
        return self.info
    
    def get_question(self):
        if self.question is None:
            self.question = gi.Message().get_question()
        return self.question



class Message:

    def __init__(self,func,message,Silent=False):
        self.func = func
        self.message = str(message)
        self.Silent = Silent
        self.set_detailed()

    def set_detailed(self):
        sub = _('Code block: {}').format(self.func)
        self.detailed = '{}\n\n{}'.format(self.message,sub)
    
    def show_debug(self):
        if GUI_MES and not self.Silent:
            objs.get_debug().set_text(self.detailed)
            objs.debug.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_debug()
    
    def show_error(self):
        if GUI_MES and not self.Silent:
            objs.get_error().set_text(self.detailed)
            objs.error.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_error()

    def show_info(self):
        if GUI_MES and not self.Silent:
            objs.get_info().set_text(self.detailed)
            objs.info.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_info()
                       
    def show_warning(self):
        if GUI_MES and not self.Silent:
            objs.get_warning().set_text(self.detailed)
            objs.warning.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_warning()

    def show_question(self):
        if GUI_MES and not self.Silent:
            objs.get_question().set_text(self.detailed)
            objs.question.show()
            lg.log.append(self.func,'question',self.message)
            #cur
            '''
            answer = objs.question.ask()
            lg.Message (func = self.func
                       ,message = str(answer)
                       ).show_debug()
            return answer
            '''
        else:
            return lg.Message (func = self.func
                              ,message = self.message
                              ).show_question()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()
        
    def get_image(self,path,width,height):
        f = '[SharedQt] shared.Commands.get_image'
        try:
            return gi.com.get_image (path = path
                                    ,width = width
                                    ,height = height
                                    )
        except Exception as e:
            mes = _('Third-party module has failed!\n\nDetails: {}')
            mes = mes.format(e)
            objs.get_mes(f,mes,True).show_warning()
    
    def debug_globs(self):
        f = '[SharedQt] shared.Commands.debug_globs'
        sections = []
        keys = []
        values = []
        mes = ''
        if lg.globs:
            for abbr in objs.get_sections().abbr:
                if 'dict' in str(type(lg.globs[abbr])):
                    for key in sorted(lg.globs[abbr].keys()):
                        sections.append(objs.sections.get_section(abbr))
                        keys.append(key)
                        values.append(lg.globs[abbr][key])
                else:
                    sections.append(objs.sections.get_section(abbr))
                    keys.append(_('N/A'))
                    values.append(lg.globs[abbr])
            if len(sections) > 1:
                i = 1
                cur_sec = sections[0]
                while i < len(sections):
                    if sections[i] == cur_sec:
                        sections[i] = ''
                    else:
                        cur_sec = sections[i]
                    i += 1
            iterable = [sections,keys,values]
            headers = (_('SECTION'),_('KEY'),_('VALUE'))
            mes = FastTable (iterable = iterable
                            ,headers = headers
                            ,maxrow = 50
                            ).run()
        else:
            com.rep_empty(f)
        return f + ':\n' + mes
    
    def get_mod_colors(self,color,factor=150):
        ''' Make a color (a color name (/usr/share/X11/rgb.txt) or a hex value)
            brighter and darker.
        '''
        f = '[SharedQt] shared.Commands.get_mod_colors'
        # Qt does not assign a color for an empty name, no error is thrown
        darker = lighter = ''
        if not color:
            com.rep_empty(f)
            return(darker,lighter)
        if factor <= 0:
            mes = '{} > {}'.format(factor,0)
            com.rep_condition(f,mes)
            return(darker,lighter)
        try:
            darker, lighter = gi.com.get_mod_colors(color,factor)
        except Exception as e:
            com.rep_third_party(f,e)
            return(darker,lighter)
        mes = _('Color: {}, darker: {}, lighter: {}')
        mes = mes.format(color,darker,lighter)
        objs.get_mes(f,mes,True).show_debug()
        return(darker,lighter)
    
    def run_fast_txt(self,text='',font=FONT1,Maximize=False):
        objs.get_txt(font,Maximize).reset()
        objs.txt.insert(text)
        objs.txt.show()
        return objs.txt.get()
    
    def run_fast_debug(self,title=_('Test:'),text=''):
        objs.get_txt (font = 'Mono 11'
                     ,Maximize = True
                     ).reset()
        objs.txt.set_title(title)
        objs.txt.insert(text)
        objs.txt.show()
    
    def show_save_dialog(self,types=()):
        f = '[SharedQt] shared.Commands.show_save_dialog'
        options = lg.com.show_save_dialog(types)
        try:
            file = gi.com.show_save_dialog(options)
        except Exception as e:
            file = ''
            mes = _('The operation has failed!\n\nDetails: {}')
            mes = mes.format(e)
            objs.get_mes(f,mes,True).show_error()
        return file
    
    def bind(self,obj,bindings,action):
        ''' Bind keyboard or mouse keys to an action
            Input: object, str/list, function
        '''
        f = '[SharedQt] shared.Commands.bind'
        if hasattr(obj,'widget'):
            if isinstance(bindings,str) or isinstance(bindings,list) \
            or isinstance(bindings,tuple):
                if isinstance(bindings,str):
                    bindings = [bindings]
                for binding in bindings:
                    if not gi.com.bind(obj,binding,action):
                        mes = _('Failed to enable key combination "{}"!')
                        mes = mes.format(binding)
                        objs.get_mes(f,mes,True).show_error()
            else:
                mes = _('Wrong input data: "{}"').format(bindings)
                objs.get_mes(f,mes,True).show_error()
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f,mes,True).show_error()
    
    def start(self):
        gi.objs.start()
    
    def end(self):
        gi.objs.end()



class CheckBox:
    
    def __init__(self,text=''):
        self.gui = gi.CheckBox()
        self.widget = self.gui.widget
        self.gui.set_text(text)
    
    def get(self):
        return self.gui.get()
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
    
    def toggle(self):
        self.gui.toggle()



class Label:
    
    def __init__(self,text=''):
        self.gui = gi.Label()
        self.widget = self.gui.widget
        self.set_text(text)
    
    def set_text(self,text):
        if not text:
            text = '[SharedQt] shared.Label.set_text'
        self.gui.set_text(text)



com = Commands()
objs = Objects()
# Use GUI dialogs for logic-only modules
lg.objs.mes = Message


if __name__ == '__main__':
    f = '[SharedQt] shared.__main__'
    com.start()
    #lg.ReadTextFile('/tmp/aaa').get()
    Geometry(Top()).activate()
    com.end()
