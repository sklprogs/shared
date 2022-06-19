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


class Entry:
    
    def __init__(self):
        self.gui = gi.Entry()
        self.widget = self.gui.widget
    
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
        f = '[shared] shared.Top.add_widget'
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
        f = '[shared] shared.OptionMenu.set'
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
        f = '[shared] shared.Clipboard.copy'
        if text or CopyEmpty:
            text = lg.com.sanitize(text)
            try:
                pyperclip.copy(text)
            except Exception as e:
                com.rep_failed(f,e,self.Silent)
        else:
            com.rep_empty(f)

    def paste(self):
        f = '[shared] shared.Clipboard.paste'
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
            self.error = MessageBuilder (level = _('ERROR')
                                        ,Single = True
                                        ,YesNo = False
                                        )
        return self.error
    
    def get_warning(self):
        if self.warning is None:
            self.warning = MessageBuilder (level = _('WARNING')
                                          ,Single = True
                                          ,YesNo = False
                                          )
        return self.warning
    
    def get_debug(self):
        # Reusing the same 'info' object may result in GUI glitches
        if self.debug is None:
            self.debug = MessageBuilder (level = _('INFO')
                                        ,Single = True
                                        ,YesNo = False
                                        )
        return self.debug
    
    def get_info(self):
        if self.info is None:
            self.info = MessageBuilder (level = _('INFO')
                                       ,Single = True
                                       ,YesNo = False
                                       )
        return self.info
    
    def get_question(self):
        if self.question is None:
            self.question = MessageBuilder (level = _('QUESTION')
                                           ,Single = False
                                           ,YesNo = True
                                           )
        return self.question



class MessageBuilder:

    def __init__(self,level,Single=True,YesNo=False):
        self.level = level
        self.Single = Single
        self.YesNo = YesNo
        self.logic = lg.MessageBuilder(self.level)
        self.parent = Top()
        self.widget = self.parent.widget
        self.gui = gi.MessageBuilder(self.parent)
        Geometry(parent=self.parent).set('400x250')
        self.set_frames()
        self.txt = TextBox(self.frm_tpr)
        self.set_buttons()
        self.set_icon()
        self.set_image()
        self.set_bindings()
    
    def update(self,text=''):
        #NOTE: Control-c does not work with read-only fields
        self.txt.clear_text()
        self.txt.insert(text)
    
    def set_bindings(self):
        com.bind (obj = self
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action = self.close_no
                 )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def set_frames(self):
        self.frm_prm = Frame (parent = self.gui.parent)
        self.frm_top = Frame (parent = self.frm_prm
                             ,side = 'top'
                             )
        self.frm_btm = Frame (parent = self.frm_prm
                             ,expand = False
                             ,side = 'bottom'
                             )
        self.frm_tpl = Frame (parent = self.frm_top
                             ,expand = False
                             ,side = 'left'
                             )
        self.frm_tpr = Frame (parent = self.frm_top
                             ,side = 'right'
                             ,propag = False
                             )
        self.frm_btl = Frame (parent = self.frm_btm
                             ,side = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btm
                             ,side = 'right'
                             )
    
    def set_buttons(self):
        if self.YesNo:
            YesName = _('Yes')
            NoName = _('No')
        else:
            YesName = 'OK'
            NoName = _('Cancel')
        if self.Single:
            self.btn_yes = Button (parent = self.frm_btl
                                  ,action = self.close_yes
                                  ,hint = _('Accept and close')
                                  ,text = YesName
                                  ,Focus = 1
                                  ,side = 'right'
                                  )
        else:
            self.btn_no = Button (parent = self.frm_btl
                                 ,action = self.close_no
                                 ,hint = _('Reject and close')
                                 ,text = NoName
                                 ,side = 'left'
                                 )
            self.btn_yes = Button (parent = self.frm_btr
                                  ,action = self.close_yes
                                  ,hint = _('Accept and close')
                                  ,text = YesName
                                  ,Focus = 1
                                  ,side = 'right'
                                  )
    
    def close_yes(self,event=None):
        self.Yes = True
        self.close()

    def close_no(self,event=None):
        self.Yes = False
        self.close()
    
    def ask(self,event=None):
        return self.Yes
    
    def show(self,event=None):
        self.btn_yes.focus()
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def reset(self,title='',text=''):
        self.logic.reset (text = text
                         ,title = title
                         )
        self.update(self.logic.text)
        self.set_title()
    
    def set_title(self):
        self.gui.set_title(self.logic.title)
    
    def set_icon(self):
        f = '[shared] shared.MessageBuilder.set_icon'
        if self.logic.icon and os.path.exists(self.logic.icon):
            self.gui.set_icon(self.logic.icon)
        else:
            com.rep_empty(f)

    def set_image(self,event=None):
        f = '[shared] shared.MessageBuilder.set_image'
        if self.logic.icon and os.path.exists(self.logic.icon):
            iimage = self.gui.set_image (path = self.logic.icon
                                        ,obj = self.frm_tpl
                                        )
            ''' We need to assign self.variable to Label, otherwise,
                it gets destroyed.
            '''
            self.lbl_img = Label (parent = self.frm_tpl
                                 ,image = iimage
                                 )
        else:
            com.rep_empty(f)



class Message:

    def __init__(self,func,message,Silent=False):
        sub = _('Code block: {}').format(func)
        self.message = '{}\n\n{}'.format(message,sub)
        self.Silent = Silent

    def show_debug(self):
        if GUI_MES and not self.Silent:
            objs.get_debug().reset (title = self.func
                                   ,text = self.message
                                   )
            objs.debug.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_debug()
    
    def show_error(self):
        if GUI_MES and not self.Silent:
            objs.get_error().reset (title = self.func
                                   ,text = self.message
                                   )
            objs.error.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_error()

    def show_info(self):
        if GUI_MES and not self.Silent:
            objs.get_info().reset (title = self.func
                                  ,text = self.message
                                  )
            objs.info.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_info()
                       
    def show_warning(self):
        if GUI_MES and not self.Silent:
            objs.get_warning().reset (title = self.func
                                     ,text = self.message
                                     )
            objs.warning.show()
        # Duplicate the message to the console
        lg.Message (func = self.func
                   ,message = self.message
                   ).show_warning()

    def show_question(self):
        if GUI_MES and not self.Silent:
            objs.get_question().reset (title = self.func
                                      ,text = self.message
                                      )
            objs.question.show()
            lg.log.append (self.func
                          ,_('QUESTION')
                          ,self.message
                          )
            answer = objs.question.ask()
            lg.Message (func = self.func
                       ,message = str(answer)
                       ).show_debug()
            return answer
        else:
            return lg.Message (func = self.func
                              ,message = self.message
                              ).show_question()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()
        
    def get_image(self,path,width,height):
        f = '[shared] shared.Commands.get_image'
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
        f = '[shared] shared.Commands.debug_globs'
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
    
    def get_mod_color(self,color,delta=76): # ~30%
        ''' Make a color (a color name (/usr/share/X11/rgb.txt) or
            a hex value) brighter (positive delta) or darker
            (negative delta).
        '''
        f = '[shared] shared.Commands.get_mod_color'
        if -255 <= delta <= 255:
            rgb = gi.com.get_mod_color(color)
            if rgb:
                return lg.com.get_mod_color(rgb,delta)
            else:
                mes = _('An unknown color "{}"!').format(color)
                objs.get_mes(f,mes).show_error()
        else:
            sub = '-255 <= {} <= 255'.format(delta)
            mes = _('The condition "{}" is not observed!').format(sub)
            objs.get_mes(f,mes).show_warning()
    
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
        f = '[shared] shared.Commands.show_save_dialog'
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
        f = '[shared] shared.Commands.bind'
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



com = Commands()
objs = Objects()
# Use GUI dialogs for logic-only modules
lg.objs.mes = Message


if __name__ == '__main__':
    f = '[shared] shared.__main__'
    com.start()
    #lg.ReadTextFile('/tmp/aaa').get()
    Geometry(Top()).activate()
    com.end()
