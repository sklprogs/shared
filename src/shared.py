#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys, os
import re
import io
import pyperclip
import skl_shared2.logic as lg
import skl_shared2.gui   as gi
from skl_shared2.localize import _

GUI_MES  = True
STOP_MES = False
FONT1    = 'Serif 14'
FONT2    = 'Sans 11'


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



class CreateInstance(lg.CreateInstance):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Config(lg.Config):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Decline(lg.Decline):
    
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



class References(lg.References):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Search(lg.Search):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Shortcut(lg.Shortcut):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Table(lg.Table):
    
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



class Words(lg.Words):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteBinary(lg.WriteBinary):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class WriteTextFile(lg.WriteTextFile):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)



class Panes:
    
    def __init__ (self,bg='old lace'
                 ,Extended=False,words1=None
                 ,words2=None,words3=None
                 ,words4=None
                 ):
        self.bg = bg
        self.Extend = Extended
        self.set_gui()
        if words1 and words2:
            self.reset (words1 = words1
                       ,words2 = words2
                       ,words3 = words3
                       ,words4 = words4
                       )
        
    def set_frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_top = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btm = Frame (parent = self.frm_prm
                             ,side   = 'bottom'
                             )
        self.frm_pn1 = Frame (parent = self.frm_top
                             ,side   = 'left'
                             ,propag = False
                             ,height = 1
                             )
        self.frm_pn2 = Frame (parent = self.frm_top
                             ,side   = 'right'
                             ,propag = False
                             ,height = 1
                             )
        if self.Extend:
            self.frm_pn3 = Frame (parent = self.frm_btm
                                 ,side   = 'left'
                                 ,propag = False
                                 ,height = 1
                                 )
            self.frm_pn4 = Frame (parent = self.frm_btm
                                 ,side   = 'right'
                                 ,propag = False
                                 ,height = 1
                                 )

    def set_panes(self):
        self.pane1 = TextBox(self.frm_pn1)
        self.pane2 = TextBox(self.frm_pn2)
        if self.Extend:
            self.pane3 = TextBox(self.frm_pn3)
            self.pane4 = TextBox(self.frm_pn4)
    
    def set_gui(self):
        icon = lg.objs.get_pdir().add ('..','resources'
                                      ,'icon_64x64_cpt.gif'
                                      )
        self.parent = Top (icon     = icon
                          ,title    = _('Compare texts:')
                          ,Maximize = True
                          )
        self.widget = self.parent.widget
        self.set_frames()
        self.set_panes()
        self.pane1.set_focus()
        if self.Extend:
            pane3 = self.pane3
            pane4 = self.pane4
        else:
            pane3, pane4 = None, None
        self.gui = gi.Panes (parent = self.parent
                            ,pane1  = self.pane1
                            ,pane2  = self.pane2
                            ,pane3  = pane3
                            ,pane4  = pane4
                            )
        if self.Extend:
            self.gui.config_pane1(bg=self.bg)
        self.set_bindings()
        
    def set_title(self,text):
        if not text:
            text = _('Compare texts:')
        self.gui.set_title(text)
        
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
        
    def set_bindings(self):
        ''' - We do not bind 'select1' to 'pane1' and 'select2' to
              'pane3' since we need to further synchronize references
              by LMB anyway, and this further binding will rewrite
              the current binding.
            - We do not use 'Control' for bindings. If we use it,
              Tkinter will execute its internal bindings for
              '<Control-Down/Up>' and '<Control-Left/Right>' before
              executing our own. Even though we can return 'break'
              in 'select1'-4, we should not do that because we need
              internal bindings for '<Control-Left>' and
              '<Control-Right>'. Thus, we should not use 'Control' at
              all because we cannot replace 'Alt' with 'Control'
              for all actions.
        '''
        com.bind (obj      = self.gui
                 ,bindings = ('<Control-q>','<Control-w>')
                 ,action   = self.close
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Escape>'
                 ,action   = Geometry(parent=self.gui).minimize
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Alt-Key-1>','<Control-Key-1>')
                 ,action   = self.select1
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Alt-Key-2>','<Control-Key-2>')
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane1
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = self.select1
                 )
        com.bind (obj      = self.pane2
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane1
                 ,bindings = '<Alt-Right>'
                 ,action   = self.select2
                 )
        com.bind (obj      = self.pane2
                 ,bindings = '<Alt-Left>'
                 ,action   = self.select1
                 )
        if self.Extend:
            com.bind (obj      = self.gui
                     ,bindings = ('<Alt-Key-3>','<Control-Key-3>')
                     ,action   = self.select3
                     )
            com.bind (obj      = self.gui
                     ,bindings = ('<Alt-Key-4>','<Control-Key-4>')
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<ButtonRelease-1>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<ButtonRelease-1>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Right>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Right>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Left>'
                     ,action   = self.select2
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<Alt-Left>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane1
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select3
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select4
                     )
            com.bind (obj      = self.pane3
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select1
                     )
            com.bind (obj      = self.pane4
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select2
                     )
        else:
            com.bind (obj      = self.pane1
                     ,bindings = '<Alt-Down>'
                     ,action   = self.select2
                     )
            com.bind (obj      = self.pane2
                     ,bindings = '<Alt-Up>'
                     ,action   = self.select1
                     )
             
    def decolorize(self):
        self.gui.config_pane1(bg='white')
        self.gui.config_pane2(bg='white')
        if self.Extended:
            self.gui.config_pane3(bg='white')
            self.gui.config_pane4(bg='white')
    
    def select1(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane1.set_focus()
        if self.Extend:
            self.decolorize()
            self.gui.config_pane1(bg=self.bg)
        
    def select2(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane2.set_focus()
        if self.Extend:
            self.decolorize()
            self.gui.config_pane2(bg=self.bg)
        
    def select3(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane3.set_focus()
        self.decolorize()
        self.gui.config_pane3(bg=self.bg)
        
    def select4(self,event=None):
        # Without this the search doesn't work (the pane is inactive)
        self.pane4.set_focus()
        self.decolorize()
        self.gui.config_pane4(bg=self.bg)
        
    def set_icon(self,path=None):
        if path:
            self.gui.set_icon(path)
        else:
            self.gui.set_icon (lg.objs.get_pdir().add ('..','resources'
                                                      ,'icon_64x64_cpt.gif'
                                                      )
                              )
                          
    def reset(self,words1,words2,words3=None,words4=None):
        self.pane1.reset(words=words1)
        self.pane2.reset(words=words2)
        if self.Extend:
            self.pane3.reset(words=words3)
            self.pane4.reset(words=words4)
            self.select1()



class SearchBox:
    ''' #NOTE: if duplicate spaces/line breaks are not deleted,
        text with and without punctuation will have a different number
        of words; thus, 'tkinter' will be supplied wrong positions upon
        Search. However, preserving extra spaces/line breaks causes
        the 'Words' algorithm to be much slower.
    '''
    def __init__ (self,obj,words=None
                 ,Strict=False,icon=''
                 ):
        self.type   = 'SearchBox'
        self.obj    = obj
        self.words  = words
        self.parent = self.obj.parent
        ''' We bind 'SearchBox' to a simple 'TextBox', so we don't have
            an icon yet.
        '''
        self.ientry = EntryC (title = _('Find:')
                             ,icon  = icon
                             )
        self.isel = obj.select
        self.reset (words  = self.words
                   ,Strict = Strict
                   )
        self.ientry.close()

    def reset(self,words=None,Strict=False):
        self.reset_logic (words  = words
                         ,Strict = Strict
                         )
    
    # Strict: case-sensitive, with punctuation
    def reset_logic(self,words=None,Strict=False):
        self.Success  = True
        self.prevloop = self.nextloop = self.pattern = self.pos1 \
                      = self.pos2 = self.text = None
        self.i        = 0
        self.words    = words
        self.Strict   = Strict
        if self.words:
            # Do not get text from the widget - it's not packed yet
            if self.Strict:
                self.text = self.words.textp
            else:
                self.text = self.words.textn
            self.isel.reset(words=self.words)
            self.isearch = lg.Search(text=self.text)
        else:
            self.Success = False

    def reset_data(self):
        f = '[shared] shared.SearchBox.reset_data'
        self.Success  = True
        self.prevloop = self.nextloop = self.pattern = self.pos1 \
                      = self.pos2 = None
        self.i        = 0
        self.search()
        if self.text and self.pattern:
            self.isearch.reset (text   = self.text
                               ,search = self.pattern
                               )
            self.isearch.get_next_loop()
            # Prevents from calling self.search() once again
            if not self.isearch.nextloop:
                mes = _('No matches!')
                objs.get_mes(f,mes).show_info()
                self.Success = False
        else:
            self.Success = False
            com.cancel(f)

    def get_loop(self):
        f = '[shared] shared.SearchBox.get_loop'
        if self.Success:
            if not self.isearch.nextloop:
                self.reset()
        else:
            com.cancel(f)
        return self.isearch.nextloop

    def add(self):
        f = '[shared] shared.SearchBox.add'
        if self.Success:
            if self.i < len(self.get_loop()) - 1:
                self.i += 1
        else:
            com.cancel(f)

    def subtract(self):
        f = '[shared] shared.SearchBox.subtract'
        if self.Success:
            if self.i > 0:
                self.i -= 1
        else:
            com.cancel(f)

    def get_new(self,event=None):
        self.reset_data()
        self.get_next()

    def select(self):
        f = '[shared] shared.SearchBox.select'
        if self.Success:
            if self.Strict:
                result1 = self.words.get_no_by_pos_p(pos=self.get_pos1())
                result2 = self.words.get_no_by_pos_p(pos=self.get_pos2())
            else:
                result1 = self.words.get_no_by_pos_n(pos=self.get_pos1())
                result2 = self.words.get_no_by_pos_n(pos=self.get_pos2())
            if result1 is None or result2 is None:
                mes = _('Wrong input data!')
                objs.get_mes(f,mes,True).show_error()
            else:
                pos1 = self.words.words[result1].get_tf()
                pos2 = self.words.words[result2].get_tl()
                self.isel.reset (pos1 = pos1
                                ,pos2 = pos2
                                ,bg   = 'green2'
                                )
                self.isel.set()
        else:
            com.cancel(f)

    def search(self):
        f = '[shared] shared.SearchBox.search'
        if self.Success:
            if self.words:
                if not self.pattern:
                    self.ientry.set_focus()
                    self.ientry.select_all()
                    self.ientry.show()
                    self.pattern = self.ientry.get()
                    if self.pattern and not self.Strict:
                        self.pattern = lg.Text (text = self.pattern
                                               ,Auto = False
                                               ).delete_punctuation()
                        self.pattern = lg.Text (text = self.pattern
                                               ,Auto = False
                                               ).delete_duplicate_spaces()
                        self.pattern = self.pattern.lower()
            else:
                com.rep_empty(f)
            return self.pattern
        else:
            com.cancel(f)

    def get_next(self,event=None):
        f = '[shared] shared.SearchBox.get_next'
        if self.Success:
            loop = self.get_loop()
            if loop:
                old_i = self.i
                self.add()
                if old_i == self.i:
                    if len(loop) == 1:
                        mes = _('Only one match has been found!')
                        objs.get_mes(f,mes).show_info()
                    else:
                        self.i = 0
                        mes = _('No more matches, continuing from the top!')
                        objs.get_mes(f,mes).show_info()
                self.select()
            else:
                mes = _('No matches!')
                objs.get_mes(f,mes).show_info()
        else:
            com.cancel(f)

    def get_prev(self,event=None):
        f = '[shared] shared.SearchBox.get_prev'
        if self.Success:
            loop = self.get_loop()
            if loop:
                old_i = self.i
                self.subtract()
                if old_i == self.i:
                    if len(loop) == 1:
                        mes = _('Only one match has been found!')
                        objs.get_mes(f,mes).show_info()
                    else:
                        # Not just -1
                        self.i = len(loop) - 1
                        mes = _('No more matches, continuing from the bottom!')
                        objs.get_mes(f,mes).show_info()
                self.select()
            else:
                mes = _('No matches!')
                objs.get_mes(f,mes).show_info()
        else:
            com.cancel(f)

    def get_pos1(self):
        f = '[shared] shared.SearchBox.get_pos1'
        if self.Success:
            if self.pos1 is None:
                self.get_loop()
                self.i = 0
            loop = self.get_loop()
            if loop:
                self.pos1 = loop[self.i]
            return self.pos1
        else:
            com.cancel(f)

    def get_pos2(self):
        f = '[shared] shared.SearchBox.get_pos2'
        if self.Success:
            if self.get_pos1() is not None:
                self.pos2 = self.pos1 + len(self.search())
            return self.pos2
        else:
            com.cancel(f)



# Select words only
class Selection:
    ''' Usage:
        com.bind(itxt,'<ButtonRelease-1>',action)

    def action(event=None):
        """ Refresh coordinates (or set isel.pos1, isel.pos2
            manually).
        """
        isel.get()
        isel.set()
    '''
    def __init__(self,itxt,words=None):
        self.itxt = itxt
        self.reset(words=words)

    def reset (self
              ,words = None
              ,pos1  = None
              ,pos2  = None
              ,bg    = None
              ,fg    = None
              ,tag   = 'tag'
              ):
        self.pos1 = pos1
        self.pos2 = pos2
        self.text = ''
        self.bg   = bg
        self.fg   = fg
        if not self.bg and not self.fg:
            self.bg = 'cyan'
        self.tag  = tag
        self.words = words

    def clear(self,tag='sel',pos1='1.0',pos2='end'):
        self.itxt.tag_remove (tag  = tag
                             ,pos1 = pos1
                             ,pos2 = pos2
                             )

    def get_pos1(self):
        if self.pos1 is None:
            self.get()
        return self.pos1

    def get_pos2(self):
        if self.pos2 is None:
            self.get()
        return self.pos2

    def get(self,event=None):
        f = '[shared] shared.Selection.get'
        try:
            self.pos1, self.pos2 = self.itxt.gui.get_sel_index()
        except Exception as e:
            self.pos1, self.pos2 = None, None
            # Too frequent
            #com.rep_failed(f,e)
        # Too frequent
        '''
        mes = '{}-{}'.format(self.pos1,self.pos2)
        objs.get_mes(f,mes,True).show_debug()
        '''
        return(self.pos1,self.pos2)

    def get_text(self):
        f = '[shared] shared.Selection.get_text'
        ''' #TODO: do not use self.variables so we don't have to reset
            this class (or, even better, delete this class from all
            projects).
        '''
        self.text = ''
        try:
            self.text = self.itxt.gui.get_sel()
            self.text = self.text.replace('\r','').replace('\n','')
        except:
            ''' Tkinter will throw an exception if there is no
                selection, so we just ignore this exception.
            '''
            pass
        return self.text

    def select_all(self):
        self.itxt.select_all()

    def set(self,DelPrev=True,AutoScroll=True):
        if self.get_pos1() and self.get_pos2():
            mark = self.pos1
            self.itxt.tag_add (pos1    = self.pos1
                              ,pos2    = self.pos2
                              ,tag     = self.tag
                              ,DelPrev = DelPrev
                              )
        else:
            # Just need to return something w/o warnings
            cursor = mark = self.itxt.get_cursor()
            self.itxt.tag_add (tag     = self.tag
                              ,pos1    = cursor
                              ,pos2    = cursor
                              ,DelPrev = DelPrev
                              )
        
        if self.bg:
            ''' This is not necessary for 'sel' tag which is hardcoded
                for selection and permanently colored with gray.
                A 'background' attribute cannot be changed for a 'sel'
                tag.
            '''
            self.itxt.tag_config (tag = self.tag
                                 ,bg  = self.bg
                                 )
        elif self.fg:
            self.itxt.tag_config (tag = self.tag
                                 ,fg  = self.fg
                                 )
        #TODO: select either 'see' or 'autoscroll'
        if AutoScroll:
            #self.itxt.see(mark)
            self.itxt.autoscroll(mark)



class TextBoxC:
    
    def __init__ (self,Maximize=False,title=''
                 ,icon='',words=None,font=FONT1
                 ):
        self.Active   = False
        self.Maximize = Maximize
        self.title    = title
        self.icon     = icon
        self.font     = font
        self.words    = words
        self.set_gui()
        self.set_focus()
    
    def mark_remove(self,mark='insert'):
        self.obj.mark_remove(mark)
    
    def mark_add(self,mark='insert',pos='1.0'):
        self.obj.mark_add (mark = mark
                          ,pos  = pos
                          )
    
    def clear_marks(self,event=None):
        self.obj.clear_marks()
    
    def clear_tags(self,event=None):
        self.obj.clear_tags()
    
    def tag_config (self,tag='sel',bg=None
                   ,fg=None,font=None
                   ):
        self.obj.tag_config (tag  = tag
                            ,bg   = bg
                            ,fg   = fg
                            ,font = font
                            )
    
    def tag_remove (self,tag='sel'
                   ,pos1='1.0'
                   ,pos2='end'
                   ):
        self.obj.tag_remove (tag  = tag
                            ,pos1 = pos1
                            ,pos2 = pos2
                            )
    
    def tag_add (self,tag='sel',pos1='1.0'
                ,pos2='end',DelPrev=True
                ):
        self.obj.tag_add (tag     = tag
                         ,pos1    = pos1
                         ,pos2    = pos2
                         ,DelPrev = DelPrev
                         )
    
    def enable(self,event=None):
        self.obj.enable()
    
    def disable(self,event=None):
        self.obj.disable()
    
    def set_focus(self,event=None):
        # Focus on 'tk.Text' instead of 'tk.Toplevel'
        self.obj.set_focus()
    
    def insert (self,text=''
               ,pos='1.0',mode=None
               ):
        self.obj.insert (text = text
                        ,pos  = pos
                        ,mode = mode
                        )
    
    def reset(self,words=None,title=''):
        self.words = words
        self.obj.reset(self.words)
        self.set_title(title)
    
    def set_gui(self):
        self.parent = Top (Maximize = self.Maximize
                          ,title    = self.title
                          ,icon     = self.icon
                          )
        self.widget = self.parent.widget
        self.gui = gi.TextBoxC(self.parent)
        self.obj = TextBox (parent  = self.parent
                           ,words   = self.words
                           ,ScrollX = False
                           ,ScrollY = True
                           ,icon    = self.icon
                           ,font    = self.font
                           )
        self.set_bindings()
    
    def check_spell(self):
        ''' Tags can be marked only after text is inserted; thus, call
            this procedure separately before '.show'.
        '''
        f = '[shared] shared.TextBox.check_spell'
        if self.words:
            self.words.get_sent_nos()
            result = []
            for i in range(self.words.get_len()):
                if not self.words.words[i].check_spell():
                    result.append(i)
            if result:
                self.clear_tags()
                for i in range(len(result)):
                    no   = self.words.no = result[i]
                    pos1 = self.words.words[no].get_tf()
                    pos2 = self.words.words[no].get_tl()
                    if pos1 and pos2:
                        self.tag_add (tag     = 'spell'
                                     ,pos1    = pos1
                                     ,pos2    = pos2
                                     ,DelPrev = False
                                     )
                
                mes = _('{} tags to assign').format(len(result))
                objs.get_mes(f,mes,True).show_debug()
                self.tag_config (tag = 'spell'
                                ,bg  = 'red'
                                )
            else:
                mes = _('Spelling seems to be correct.')
                objs.get_mes(f,mes,True).show_info()
        else:
            com.rep_empty(f)
    
    def set_icon(self,path=''):
        if path:
            self.icon = path
        self.gui.set_icon(self.icon)

    def set_title(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            self.title = text
        self.gui.set_title(self.title)
    
    def get(self,event=None):
        return self.obj.get()
    
    def show(self,event=None):
        self.Active = True
        self.gui.show()

    def close(self,event=None):
        self.Active = False
        self.gui.close()
    
    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Escape>','<Control-w>','<Control-q>')
                 ,action   = self.close
                 )
        # This is to remember the 'Active' status
        self.widget.protocol("WM_DELETE_WINDOW",self.close)



class TextBoxRO(TextBoxC):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ro_set_gui()
    
    def reset(self,words=None,title=''):
        self.enable()
        self.words = words
        self.obj.reset(self.words)
        self.set_title(title)
        self.disable()
    
    def insert (self,text=''
               ,pos='1.0',mode='top'
               ):
        self.enable()
        self.obj.insert (text = text
                        ,pos  = pos
                        ,mode = mode
                        )
        self.disable()
    
    def ro_set_buttons(self):
        self.btn_cls = Button (parent   = self.frm_btn
                              ,action   = self.close
                              ,text     = _('Close')
                              ,hint     = _('Close this window')
                              ,side     = 'left'
                              ,bindings = ('<Escape>','<Control-w>'
                                          ,'<Control-q>','<Return>'
                                          ,'<KP_Enter>'
                                          )
                              ,expand   = True
                              )
    
    def ro_set_gui(self):
        self.ro_set_frames()
        self.ro_set_buttons()
        self.ro_set_bindings()
    
    def ro_set_frames(self):
        self.frm_btn = Frame (parent = self.gui.parent
                             ,expand = False
                             ,side   = 'bottom'
                             )
    
    def ro_set_bindings(self):
        # Do not add a new line
        self.gui.unbind('<Return>')
        self.gui.unbind('<KP_Enter>')
        com.bind (obj      = self.gui
                 ,bindings = ('<Return>','<KP_Enter>')
                 ,action   = self.close
                 )



class TextBoxRW(TextBoxC):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.Save    = False
        self.rw_text = ''
        self.add_rw_gui()
    
    def insert (self,text=''
               ,pos='1.0',mode='top'
               ):
        self.rw_text = text
        self.obj.insert (text = text
                        ,pos  = pos
                        ,mode = mode
                        )
    
    def reset(self,words=None,title=''):
        self.Save  = False
        self.words = words
        self.obj.reset(self.words)
        self.set_title(title)
    
    def reload(self,event=None):
        self.reset()
        self.insert(self.rw_text)
    
    def get(self,event=None):
        if self.Save:
            return self.obj.get()
        else:
            return ''
    
    def save(self,event=None):
        self.Save = True
        self.close()
    
    def set_rw_buttons(self):
        self.btn_cls = Button (parent   = self.frm_btl
                              ,action   = self.close
                              ,text     = _('Close')
                              ,hint     = _('Reject and close')
                              ,side     = 'left'
                              ,bindings = ('<Escape>','<Control-w>'
                                          ,'<Control-q>'
                                          )
                              )
        self.btn_rst = Button (parent   = self.frm_btl
                              ,action   = self.reload
                              ,text     = _('Reset')
                              ,hint     = _('Restore the text')
                              ,side     = 'right'
                              ,bindings = ('<F5>','<Control-r>')
                              )
        self.btn_sav = Button (parent   = self.frm_btr
                              ,action   = self.save
                              ,text     = _('Save')
                              ,hint     = _('Accept and close')
                              ,side     = 'right'
                              ,bindings = ('<F2>','<Control-s>')
                              )
    
    def add_rw_gui(self):
        self.set_rw_frames()
        self.set_rw_buttons()
        self.set_rw_bindings()
    
    def set_rw_frames(self):
        self.frm_btn = Frame (parent = self.gui.parent
                             ,expand = False
                             ,side   = 'bottom'
                             )
        self.frm_btl = Frame (parent = self.frm_btn
                             ,side   = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btn
                             ,side   = 'right'
                             )
    
    def set_rw_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<F2>','<Control-s>')
                 ,action   = self.save
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<F5>','<Control-r>')
                 ,action   = self.reload
                 )



class TextBox:

    def __init__ (self,parent,expand=True
                 ,side=None,fill='both'
                 ,words=None,font=FONT1
                 ,ScrollX=False,ScrollY=True
                 ,wrap='word',icon=''
                 ):
        self.set_values()
        self.parent  = parent
        self.expand  = expand
        self.side    = side
        self.fill    = fill
        self.words   = words
        self.font    = font
        self.ScrollX = ScrollX
        self.ScrollY = ScrollY
        self.wrap    = wrap
        
        self.select = Selection (itxt  = self
                                ,words = self.words
                                )
        self.search = SearchBox (obj   = self
                                ,words = self.words
                                ,icon  = icon
                                )
        self.set_gui()

    def clear_marks(self,event=None):
        for mark in self.gui.get_marks():
            self.mark_remove(mark)
    
    def clear_tags(self,event=None):
        for tag in self.gui.get_tags():
            self.tag_remove(tag)
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()
    
    def set_values(self):
        self.type    = 'TextBox'
        self.scr_ver = None
        self.scr_hor = None

    def set_frames(self):
        self.frm_prm = Frame (parent = self.parent
                             ,side   = self.side
                             ,expand = self.expand
                             ,fill   = self.fill
                             )
        self.frm_sec = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_trt = Frame (parent = self.frm_sec
                             ,side   = 'left'
                             )
        self.frm_ver = Frame (parent = self.frm_sec
                             ,side   = 'right'
                             ,expand = False
                             ,fill   = 'y'
                             )
        self.frm_txt = Frame (parent = self.frm_trt
                             ,side   = 'top'
                             )
        self.frm_hor = Frame (parent = self.frm_trt
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
    
    def set_gui(self):
        self.set_frames()
        self.gui = gi.TextBox (parent = self.frm_txt
                              ,wrap   = self.wrap
                              ,expand = self.expand
                              ,side   = self.side
                              ,fill   = self.fill
                              ,font   = self.font
                              )
        self.widget = self.gui.widget
        if self.ScrollY:
            self.scr_ver = Scrollbar (parent = self.frm_ver
                                     ,scroll = self.gui
                                     )
        if self.ScrollX:
            self.scr_hor = Scrollbar (parent = self.frm_hor
                                     ,scroll = self.gui
                                     ,Horiz  = True
                                     )
        self.set_bindings()

    def reset(self,words=None):
        self.clear_text()
        self.clear_tags()
        self.clear_marks()
        if words:
            self.words = words
            # Selection is reset in 'SearchBox.reset'
            self.search.reset(self.words)

    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Control-f>','<Control-F3>')
                 ,action   = self.search.get_new
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<F3>'
                 ,action   = self.search.get_next
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Shift-F3>'
                 ,action   = self.search.get_prev
                 )
        # Custom selection
        com.bind (obj      = self.gui
                 ,bindings = '<Control-a>'
                 ,action   = self.select_all
                 )
        ''' Tkinter does not delete the selection before pasting, so we
            do custom pasting here.
        '''
        com.bind (obj      = self.gui
                 ,bindings = '<Control-v>'
                 ,action   = self.paste
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Control-Alt-u>'
                 ,action   = self.toggle_case
                 )

    def toggle_case(self,event=None):
        f = '[shared] shared.TextBox.toggle_case'
        text = Text(text=self.select.get_text()).toggle_case()
        pos1, pos2 = self.select.get()
        self.clear_sel()
        self.insert (text = text
                    ,pos  = self.cursor()
                    )
        if pos1 and pos2:
            self.select.reset (pos1 = pos1
                              ,pos2 = pos2
                              ,tag  = 'sel'
                              ,bg   = 'gray'
                              )
            self.select.set(DelPrev=0,AutoScroll=0)
        else:
            com.rep_empty(f)
        return 'break'

    def _get(self):
        f = '[shared] shared.TextBox._get'
        try:
            return self.gui.get()
        except Exception as e:
            com.rep_failed(f,e)

    def get(self,Strip=True):
        result = self._get()
        if result:
            if Strip:
                return result.strip()
            else:
                return result.strip('\n')
        else:
            # Always return a string
            return ''

    def insert (self,text='',pos='1.0'
               ,mode=None
               ):
        f = '[shared] shared.TextBox.insert'
        if text is None:
            text = ''
        try:
            self.gui.insert (text = text
                            ,pos  = pos
                            )
        except Exception as e:
            com.rep_failed(f,e)
        ''' #NOTE: 'Tkinter' does not go to the cursor position
            automatically, but we should not use 'self.scroll' each time
            'self.insert' is used because in that case pasting text in
            'TextBox' will cause scrolling and thereby some discomfort
            in using 'TextBox'-based widgets.
        '''
        if mode == 'top':
            # Move to the beginning
            self.mark_add()
            self.scroll('insert')
        elif mode == 'bottom':
            self.mark_add(pos='end')
            self.scroll('insert')
        elif mode in (True,1,'1'):
            self.scroll('insert')
        elif mode in (None,False,0,'0'):
            pass
        else:
            modes = ('top','bottom','',None,False,0,True,1)
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode,modes)
            ''' Do not use GUI here since 'MessageBuilder' depends on
                'TextBox'.
            '''
            objs.get_mes(f,mes,True).show_error()

    def paste(self,event=None):
        self.clear_sel()
        self.insert (text = Clipboard().paste()
                    ,pos  = self.cursor()
                    )
        return 'break'

    def select_all(self,event=None):
        ''' 'end-1c' allows to select text without the last newline
            (which is added automatically by 'tkinter'). For this
            to work correctly, strip the text first.
        '''
        self.tag_add (tag  = 'sel'
                     ,pos1 = '1.0'
                     ,pos2 = 'end-1c'
                     )
        self.mark_add()
        return 'break'

    def tag_remove(self,tag='sel',pos1='1.0',pos2='end'):
        f = '[shared] shared.TextBox.tag_remove'
        try:
            self.gui.tag_remove (tag  = tag
                                ,pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.rep_failed(f,e)

    def tag_add (self,tag='sel',pos1='1.0'
                ,pos2='end',DelPrev=True
                ):
        f = '[shared] shared.TextBox.tag_add'
        if DelPrev:
            self.tag_remove(tag)
        try:
            self.gui.tag_add (tag  = tag
                             ,pos1 = pos1
                             ,pos2 = pos2
                             )
        except Exception as e:
            com.rep_failed(f,e)

    def tag_config (self,tag='sel',bg=None
                   ,fg=None,font=None
                   ):
        f = '[shared] shared.TextBox.tag_config'
        try:
            self.gui.tag_config (tag  = tag
                                ,bg   = bg
                                ,fg   = fg
                                ,font = font
                                )
        except Exception as e:
            com.rep_failed(f,e)

    def mark_add(self,mark='insert',pos='1.0'):
        f = '[shared] shared.TextBox.mark_add'
        try:
            self.gui.mark_add (mark = mark
                              ,pos  = pos
                              )
        except Exception as e:
            com.rep_failed(f,e)

    def mark_remove(self,mark='insert'):
        f = '[shared] shared.TextBox.mark_remove'
        try:
            self.gui.mark_remove(mark)
        except Exception as e:
            com.rep_failed(f,e)

    def clear_text(self,pos1='1.0',pos2='end'):
        f = '[shared] shared.TextBox.clear_text'
        try:
            self.gui.clear_text (pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.rep_failed(f,e)

    def clear_sel(self,event=None):
        f = '[shared] shared.TextBox.clear_sel'
        pos1, pos2 = self.select.get()
        if pos1 and pos2:
            self.clear_text (pos1 = pos1
                            ,pos2 = pos2
                            )

    def goto(self,GoTo=''):
        f = '[shared] shared.TextBox.goto'
        if GoTo:
            try:
                goto_pos = self.gui.search(GoTo)
                self.mark_add('goto',goto_pos)
                self.mark_add('insert',goto_pos)
                self.gui.scroll('goto')
            except Exception as e:
                com.rep_failed(f,e)
        else:
            com.rep_lazy(f)

    # Scroll screen to a tkinter position or a mark (tags do not work)
    def scroll(self,mark):
        f = '[shared] shared.TextBox.scroll'
        try:
            self.gui.scroll(mark)
        except Exception as e:
            com.rep_failed(f,e)

    def autoscroll(self,mark='1.0'):
        ''' Scroll screen to a tkinter position or a mark if they
            are not visible (tags do not work).
        '''
        if not self.is_visible(mark):
            self.scroll(mark)

    #TODO: select either 'see' or 'autoscroll'
    def see(self,mark):
        f = '[shared] shared.TextBox.see'
        if mark is None:
            com.rep_empty(f)
        else:
            self.gui.see(mark)

    def is_visible(self,tk_pos):
        if self.widget.bbox(tk_pos):
            return True

    def get_cursor(self,event=None):
        f = '[shared] shared.TextBox.cursor'
        try:
            self.pos = self.gui.get_cursor()
        except Exception as e:
            self.pos = '1.0'
            com.rep_failed(f,e)
        return self.pos

    def set_focus(self,event=None):
        self.gui.set_focus()



class EntryC:
    
    def __init__(self,title='',icon='',ClearAll=False):
        self.type     = 'Entry'
        self.Save     = False
        self.title    = title
        self.icon     = icon
        self.ClearAll = ClearAll
        self.set_gui()
        self.reset()
    
    def insert(self,text='text',pos=0):
        self.obj.insert (text = text
                        ,pos  = pos
                        )
    
    def select_all(self,event=None):
        self.obj.select_all()
    
    def set_focus(self,event=None):
        self.gui.set_focus()
    
    def reset(self,title=''):
        self.Save = False
        if title:
            self.title = title
        self.set_title()
        self.clear()
    
    def clear_text (self,event=None
                   ,pos1=0,pos2='end'
                   ):
        self.obj.clear_text (pos1 = pos1
                            ,pos2 = pos2
                            )
    
    def clear (self,event=None
              ,pos1=0,pos2='end'
              ):
        self.clear_text (pos1 = pos1
                        ,pos2 = pos2
                        )
    
    def set_gui(self):
        self.parent = Top (AutoCr = False
                          ,title  = self.title
                          ,icon   = self.icon
                          )
        self.gui    = gi.EntryC(self.parent)
        self.widget = self.gui.widget
        self.set_frames()
        self.obj = Entry (parent   = self.frm_ent
                         ,expand   = True
                         ,fill     = 'x'
                         ,ClearAll = self.ClearAll
                         )
        self.set_buttons()
        self.set_bindings()
    
    def set_frames(self):
        self.frm_ent = Frame (parent = self.parent
                             ,side   = 'top'
                             ,expand = False
                             )
        self.frm_btn = Frame (parent = self.parent
                             ,side   = 'bottom'
                             ,expand = False
                             )
        self.frm_btl = Frame (parent = self.frm_btn
                             ,side   = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btn
                             ,side   = 'right'
                             )
    
    def get(self,event=None):
        if self.Save:
            return self.obj.get()
        else:
            return ''
    
    def set_icon(self,path=''):
        if path:
            self.icon = path
        self.gui.set_icon(self.icon)

    def set_title(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            self.title = text
        self.gui.set_title(self.title)
    
    def set_buttons(self):
        self.btn_cls = Button (parent = self.frm_btl
                              ,action = self.close
                              ,hint   = _('Reject and close')
                              ,text   = _('Close')
                              ,side   = 'left'
                              ,hdir   = 'bottom'
                              )
        self.btn_clr = Button (parent = self.frm_btl
                              ,action = self.clear
                              ,hint   = _('Clear the field')
                              ,text   = _('Clear')
                              ,side   = 'right'
                              ,hdir   = 'bottom'
                              )
        self.btn_sav = Button (parent = self.frm_btr
                              ,action = self.save
                              ,hint   = _('Accept and close')
                              ,text   = _('Save and close')
                              ,side   = 'right'
                              ,hdir   = 'bottom'
                              )
    
    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                 ,action   = self.close
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<F5>','<Control-r>')
                 ,action   = self.clear
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Return>','<KP_Enter>'
                             ,'<F2>','<Control-s>'
                             )
                 ,action   = self.save
                 )
    
    def save(self,event=None):
        self.Save = True
        self.close()
    
    def close(self,event=None):
        self.gui.close()
    
    def show(self,event=None):
        self.obj.set_focus()
        self.gui.show()



class Entry:
    # Does not support marks or tags
    def __init__ (self,parent,side=None
                 ,ipadx=None,ipady=None
                 ,fill=None,width=None
                 ,expand=None,font=FONT2
                 ,bg=None,fg=None,justify='left'
                 ,AddBind=True,ClearAll=False
                ):
        self.type     = 'Entry'
        self.parent   = parent
        self.side     = side
        self.ipadx    = ipadx
        self.ipady    = ipady
        self.fill_    = fill
        self.width    = width
        self.expand   = expand
        self.font     = font
        self.bg       = bg
        self.fg       = fg
        self.justify  = justify
        self.AddBind  = AddBind
        self.ClearAll = ClearAll
        self.set_gui()

    def get_sel(self,event=None):
        try:
            pos1, pos2 = self.gui.get_sel_index()
        except Exception as e:
            pos1 = 0
            pos2 = 0
        return(pos1,pos2)
    
    def get_cursor(self,event=None):
        f = '[shared] shared.Entry.get_cursor'
        try:
            pos = self.gui.get_cursor()
        except Exception as e:
            pos = 0
            com.rep_failed(f,e)
        return pos
    
    def paste(self,event=None):
        if self.ClearAll:
            pos1, pos2 = 0, 'end'
        else:
            pos1, pos2 = self.get_sel()
        self.clear (pos1 = pos1
                   ,pos2 = pos2
                   )
        self.insert (text = Clipboard().paste()
                    ,pos  = self.get_cursor()
                    )
        return 'break'
    
    def set_gui(self):
        self.gui = gi.Entry (parent  = self.parent
                            ,side    = self.side
                            ,ipadx   = self.ipadx
                            ,ipady   = self.ipady
                            ,fill    = self.fill_
                            ,width   = self.width
                            ,expand  = self.expand
                            ,font    = self.font
                            ,bg      = self.bg
                            ,fg      = self.fg
                            ,justify = self.justify
                            )
        self.widget = self.gui.widget
        self.set_bindings()
        self.set_extra_bind()
    
    def reset(self):
        self.clear_text()
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()

    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = '<Control-a>'
                 ,action   = self.select_all
                 )
        com.bind (obj      = self.gui
                 ,bindings = '<Control-v>'
                 ,action   = self.paste
                 )
    
    def set_extra_bind(self):
        if self.AddBind:
            com.bind (obj      = self.gui
                     ,bindings = '<ButtonRelease-2>'
                     ,action   = self.paste
                     )
            com.bind (obj      = self.gui
                     ,bindings = '<ButtonRelease-3>'
                     ,action   = self.clear
                     )

    def _get(self):
        f = '[shared] shared.Entry._get'
        try:
            return self.gui.get()
        except Exception as e:
            com.rep_failed(f,e)

    def get(self,Strip=False):
        f = '[shared] shared.Entry.get'
        result = self._get()
        if result is None:
            result = ''
        if Strip:
            return result.strip()
        else:
            return result.strip('\n')

    def insert(self,text='text',pos=0):
        f = '[shared] shared.Entry.insert'
        self.enable()
        try:
            self.widget.insert(pos,text)
        except Exception as e:
            com.rep_failed(f,e)

    def select_all(self,event=None):
        return self.gui.select_all()

    def clear (self,event=None
              ,pos1=0,pos2='end'
              ):
        self.clear_text (pos1 = pos1
                        ,pos2 = pos2
                        )
    
    def clear_text (self,event=None
                   ,pos1=0,pos2='end'
                   ):
        f = '[shared] shared.Entry.clear_text'
        try:
            self.gui.clear_text (pos1 = pos1
                                ,pos2 = pos2
                                )
        except Exception as e:
            com.rep_failed(f,e)

    def set_focus(self,event=None):
        return self.gui.set_focus()



class MultCBoxesC:
    
    def __init__ (self,text='',width=350
                 ,height=300,font=FONT2
                 ,MarkAll=False,icon=''
                 ):
        self.width  = width
        self.height = height
        self.icon   = icon
        self.font   = font
        self.set_gui()
        self.set_title()
        self.reset (text    = text
                   ,MarkAll = MarkAll
                   )
    
    def select_all(self,event=None):
        self.obj.select_all()
    
    def get_selected(self,event=None):
        return self.obj.get_selected()
    
    def toggle(self,event=None):
        self.obj.toggle()
    
    def set_bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close
                 )
        self.obj.cvs_prm.set_top_bindings (top  = self.parent
                                          ,Ctrl = False
                                          )
    
    def set_icon(self,path=''):
        if path:
            self.icon = path
        self.gui.set_icon(self.icon)
    
    def reset(self,text='',MarkAll=False):
        self.text = lg.com.sanitize(text)
        self.obj.reset (text    = text
                       ,MarkAll = MarkAll
                       )
    
    def set_frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_ver = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'y'
                             ,side   = 'right'
                             )
        self.frm_bth = Frame (parent = self.parent
                             ,expand = False
                             ,fill   = 'both'
                             )
        self.frm_hor = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm_sec = Frame (parent = self.frm_prm)
        
    def set_scroll(self):
        self.scr_hor = Scrollbar (parent = self.frm_hor
                                 ,scroll = self.obj.cvs_prm
                                 ,Horiz  = True
                                 )
        self.scr_ver = Scrollbar (parent = self.frm_ver
                                 ,scroll = self.obj.cvs_prm
                                 )
    
    def set_widgets(self):
        self.btn_sel = Button (parent = self.frm_bth
                              ,text   = _('Toggle all')
                              ,hint   = _('Mark/unmark all checkboxes')
                              ,side   = 'left'
                              ,action = self.toggle
                              )
        self.btn_cls = Button (parent = self.frm_bth
                              ,text   = _('Close')
                              ,hint   = _('Close this window')
                              ,side   = 'right'
                              ,action = self.close
                              )
    
    def set_gui(self):
        self.parent = Top()
        Geometry(parent=self.parent).set ('%dx%d' % (self.width
                                                    ,self.height
                                                    )
                                         )
        self.gui    = gi.MultCBoxesC(self.parent)
        self.widget = self.gui.widget
        self.set_frames()
        self.obj = MultCBoxes (parent  = self.frm_sec
                              ,font    = self.font
                              )
        self.set_widgets()
        self.set_scroll()
        self.btn_cls.set_focus()
        self.set_bindings()
        self.set_title()
        self.set_icon()
    
    def set_title(self,text=None):
        if not text:
            text = _('Select files:')
        self.gui.set_title(text)
    
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
        


class MultCBoxes:

    def __init__ (self,parent,text=''
                 ,font=FONT2,MarkAll=False
                 ):
        self.parent = parent
        self.widget = self.parent.widget
        self.font   = font
        self.set_values()
        self.set_gui()
        self.reset (text    = text
                   ,MarkAll = MarkAll
                   )
    
    def select_all(self,event=None):
        for cbx in self.cboxes:
            cbx.enable()
    
    def get_selected(self,event=None):
        active = []
        for i in range(len(self.cboxes)):
            if self.cboxes[i].get():
                active.append(self.lbls[i].text)
        return active
    
    def set_region(self):
        f = '[shared] shared.MultCBoxes.set_region'
        if self.frms:
            objs.get_root().update_idle()
            self.cvs_prm.set_region (x       = self.frm_emb.get_reqwidth()
                                    ,y       = self.frm_emb.get_reqheight()
                                    ,xborder = 5
                                    ,yborder = 10
                                    )
            self.cvs_prm.scroll()
        else:
            com.rep_lazy(f)
        
    def set_values(self):
        self.frms   = []
        self.cboxes = []
        self.lbls   = []
        self.text   = ''
    
    def set_widgets(self):
        self.cvs_prm = Canvas(parent=self.parent)
        self.frm_emb = Frame(parent=self.parent)
        self.cvs_prm.embed(self.frm_emb)
        
    def add_row(self,text):
        frm = Frame (parent = self.frm_emb
                    ,expand = False
                    )
        cbx = CheckBox (parent = frm
                       ,side   = 'left'
                       )
        lbl = Label (parent = frm
                    ,text   = text
                    ,side   = 'left'
                    ,font   = self.font
                    )
        com.bind (obj      = lbl
                 ,bindings = '<ButtonRelease-1>'
                 ,action   = cbx.toggle
                 )
        self.frms.append(frm)
        self.cboxes.append(cbx)
        self.lbls.append(lbl)
        
    def toggle(self,event=None):
        Marked = False
        for cbox in self.cboxes:
            if cbox.get():
                Marked = True
                break
        if Marked:
            for cbox in self.cboxes:
                cbox.disable()
        else:
            for cbox in self.cboxes:
                cbox.enable()
    
    def reset(self,text='',MarkAll=False):
        for frame in self.frms:
            frame.kill()
        self.set_values()
        self.text = lg.com.sanitize(text)
        for item in self.text.splitlines():
            self.add_row(item)
        self.set_region()
        if MarkAll:
            self.select_all()
    
    def set_gui(self):
        self.set_widgets()



class CheckBox:
    ''' #NOTE: For some reason, CheckBox that should be Active must be
        assigned to a variable (var = CheckBox(parent,Active=1))
    '''
    def __init__ (self,parent,Active=False
                 ,side=None,action=None
                 ):
        self.parent = parent
        self.side   = side
        self.action = action
        self.gui    = gi.CheckBox (parent = self.parent
                                  ,side   = self.side
                                  )
        self.widget = self.gui.widget
        self.reset (Active = Active
                   ,action = action
                   )

    def reset(self,Active=False,action=None):
        if Active:
            self.enable()
        else:
            self.disable()
        if action:
            self.action = action
            self.gui.set_action(self.action)

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def set_focus(self,event=None):
        self.gui.set_focus()

    def enable(self,event=None):
        self.gui.enable()

    def disable(self,event=None):
        self.gui.disable()

    def get(self,event=None):
        return self.gui.get()

    def toggle(self,event=None):
        self.gui.toggle()



class ProgressBar:
    
    def __init__ (self,width=750,height=200
                 ,YScroll=True,title=_('Download progress')
                 ,icon=''
                 ):
        self.set_values()
        self.width   = width
        self.height  = height
        self.icon    = icon
        self.title   = title
        self.YScroll = YScroll
        self.set_gui()
        
    def set_values(self):
        self.items  = []
        self.item   = None
        self.border = 80
    
    def set_frames(self):
        self.frm_prm = Frame (parent = self.parent)
        self.frm_hor = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'x'
                             ,side   = 'bottom'
                             )
        self.frm_ver = Frame (parent = self.frm_prm
                             ,expand = False
                             ,fill   = 'y'
                             ,side   = 'right'
                             )
        # This frame must be created after the bottom frame
        self.frm_sec = Frame (parent = self.frm_prm)
    
    def set_icon(self,path=''):
        if path:
            self.icon = path
        self.gui.set_icon(self.icon)
    
    def set_title(self,text=''):
        if text:
            self.title = text
        self.gui.set_title(self.title)
        
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()
    
    def set_gui(self):
        self.parent = self.obj = Top(Lock=False)
        self.widget = self.parent.widget
        Geometry(self.parent).set('%dx%d' % (self.width,self.height))
        self.set_frames()
        self.set_widgets()
        self.canvas.set_region (x = self.width
                               ,y = self.height
                               )
        self.canvas.scroll()
        self.gui = gi.ProgressBar(self.parent)
        self.set_bindings()
        self.set_title()
        self.set_icon()
        
    def set_bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close
                 )
        self.canvas.set_top_bindings (top  = self.parent
                                     ,Ctrl = False
                                     )
    
    def set_widgets(self):
        self.canvas = Canvas(parent = self.frm_sec)
        self.label  = Label (parent = self.frm_sec
                            ,text   = 'ProgressBar'
                            ,expand = True
                            ,fill   = 'both'
                            )
        self.canvas.embed(self.label)
        if self.YScroll:
            self.yscroll = Scrollbar (parent = self.frm_ver
                                     ,scroll = self.canvas
                                     )
        self.canvas.set_focus()
        
    def add(self,event=None):
        f = '[shared] shared.ProgressBar.add'
        self.item = ProgressBarItem (parent = self.label
                                    ,length = self.width - self.border
                                    )
        self.items.append(self.item)
        objs.get_root().update_idle()
        max_x = self.label.get_reqwidth()
        max_y = self.label.get_reqheight()
        '''
        sub = '{}x{}'.format(max_x,max_y)
        mes = _('Widget sizes: {}').format(sub)
        objs.get_mes(f,mes,True).show_debug()
        '''
        self.canvas.set_region (x       = max_x
                               ,y       = max_y
                               ,xborder = 50
                               ,yborder = 20
                               )
        self.canvas.move_bottom()
        return self.item



class ProgressBarItem:
    
    def __init__ (self,parent,orient='horizontal'
                 ,length=100,mode='determinate'
                 ):
        self.parent = parent
        self.orient = orient
        self.length = length
        self.mode   = mode
        self.set_gui()
        
    def set_gui(self):
        self.set_frames()
        self.set_labels()
        self.set_text()
        self.gui = gi.ProgressBarItem (parent = self.frame2
                                      ,orient = self.orient
                                      ,length = self.length
                                      ,mode   = self.mode
                                      )
        self.widget = self.gui.widget
        
    def set_frames(self):
        self.frame  = Frame (parent = self.parent
                            ,expand = False
                            ,fill   = 'x'
                            )
        self.frame1 = Frame(parent=self.frame)
        self.frame2 = Frame(parent=self.frame)
        
    def set_labels(self):
        self.label = Label (parent = self.frame1
                           ,side   = 'left'
                           ,font   = 'Mono 11'
                           )

    def set_text (self,file='',cursize=0
                 ,total=0,rate=0,eta=0
                 ):
        mes = _('File: "{}"; {}/{} MB; Rate: {} kbps; ETA: {}s')
        mes = mes.format(file,int(cursize),int(total),rate,eta)
        self.label.set_text(mes)



class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
    '''
    def __init__(self):
        self.image = self.bytes_ = self.loader = None
        self.gui = gi.Image()
        
    def show_error(self,f,e):
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        objs.get_mes(f,mes).show_error()
    
    def save(self,path,ext='PNG'):
        f = '[shared] shared.Image.save'
        if self.loader:
            if com.rewrite(path):
                try:
                    self.loader.save(path,ext)
                except Exception as e:
                    self.show_error(f,e)
            else:
                mes = _('Operation has been canceled by the user.')
                objs.get_mes(f,mes,True).show_info()
        else:
            com.rep_empty(f)
    
    def open(self,path):
        if lg.File(file=path).Success:
            self.loader = self.gui.get_loader(path)
            self.image  = self.gui.get_image(self.loader)
        return self.image
            
    def get_loader(self):
        f = '[shared] shared.Image.get_loader'
        if self.bytes_:
            self.loader = self.gui.get_loader(io.BytesIO(self.bytes_))
        else:
            com.rep_empty(f)
        return self.loader
        
    def get_thumbnail(self,x,y):
        ''' Resize an image to x,y limits. PIL will keep an original
            aspect ratio.
        '''
        f = '[shared] shared.Image.get_thumbnail'
        if self.loader:
            try:
                self.loader.thumbnail([x,y])
            except Exception as e:
                self.show_error(f,e)
        else:
            com.rep_empty(f)
        return self.loader
    
    def get_image(self):
        f = '[shared] shared.Image.get_image'
        if self.loader:
            self.image = self.gui.get_image(self.loader)
        else:
            com.rep_empty(f)
        return self.image
        
    def get_bytes(self,ext='PNG'):
        if self.loader:
            bytes_ = io.BytesIO()
            try:
                self.loader.save(bytes_,format=ext)
                self.bytes_ = bytes_.getvalue()
            except Exception as e:
                self.show_error(f,e)
        else:
            com.rep_empty(f)
        return self.bytes_



class Canvas:
    
    def __init__(self,parent,expand=True
                ,side=None,region=None
                ,width=None,height=None
                ,fill='both'
                ):
        self.type   = 'Canvas'
        self.parent = parent
        self.expand = expand
        self.side   = side
        self.region = region
        self.width  = width
        self.height = height
        self.fill   = fill
        self.gui    = gi.Canvas(self.parent)
        self.widget = self.gui.widget
        
    def move_left_corner(self,event=None):
        self.gui.move_left_corner()
    
    def set_mouse_wheel(self,event=None):
        return self.gui.set_mouse_wheel(event)
    
    # These bindings are not enabled by default
    def set_top_bindings(self,top,Ctrl=True):
        f = '[shared] shared.Canvas.set_top_bindings'
        if top:
            com.bind (obj      = top
                     ,bindings = '<Down>'
                     ,action   = self.move_down
                     )
            com.bind (obj      = top
                     ,bindings = '<Up>'
                     ,action   = self.move_up
                     )
            com.bind (obj      = top
                     ,bindings = '<Left>'
                     ,action   = self.move_left
                     )
            com.bind (obj      = top
                     ,bindings = '<Right>'
                     ,action   = self.move_right
                     )
            com.bind (obj      = top
                     ,bindings = '<Next>'
                     ,action   = self.move_page_down
                     )
            com.bind (obj      = top
                     ,bindings = '<Prior>'
                     ,action   = self.move_page_up
                     )
            com.bind (obj      = top
                     ,bindings = ('<MouseWheel>','<Button 4>'
                                 ,'<Button 5>'
                                 )
                     ,action   = self.set_mouse_wheel
                     )
            if Ctrl:
                com.bind (obj      = top
                         ,bindings = '<Control-Home>'
                         ,action   = self.move_top
                         )
                com.bind (obj      = top
                         ,bindings = '<Control-End>'
                         ,action   = self.move_bottom
                         )
            else:
                com.bind (obj      = top
                         ,bindings = '<Home>'
                         ,action   = self.move_top
                         )
                com.bind (obj      = top
                         ,bindings = '<End>'
                         ,action   = self.move_bottom
                         )
        else:
            com.rep_empty(f)
    
    def move_up(self,event=None,value=-1):
        self.gui.move_up(value)
        
    def move_down(self,event=None,value=1):
        self.gui.move_down(value)
    
    def move_page_up(self,event=None,value=-1):
        self.gui.move_page_up(value)
        
    def move_page_down(self,event=None,value=1):
        self.gui.move_page_down(value)

    def move_left(self,event=None,value=-1):
        self.gui.move_left(value)
        
    def move_right(self,event=None,value=1):
        self.gui.move_right(value)
        
    def move_bottom(self,event=None):
        self.gui.move_bottom()
        
    def move_top(self,event=None):
        self.gui.move_top()
    
    def set_region (self,x=0,y=0
                   ,xborder=0,yborder=0
                   ):
        f = '[shared] shared.Canvas.set_region'
        # Both integer and float values are allowed at input
        if x and y:
            self.gui.set_region (x        = x
                                ,y        = y
                                ,xborder = xborder
                                ,yborder = yborder
                                )
        else:
            com.rep_empty(f)
    
    def scroll(self,event=None,x=0,y=0):
        self.gui.scroll (x = x
                        ,y = y
                        )
        
    def embed(self,obj):
        f = '[shared] shared.Canvas.embed'
        if hasattr(obj,'widget'):
            self.gui.embed(obj)
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f,mes,True).show_error()
        
    def set_focus(self,event=None):
        self.gui.set_focus()
    
    def show(self,event=None):
        self.gui.show()
        
    def close(self,event=None):
        self.gui.close()



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
        self.gui    = gi.Clipboard()

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
            com.rep_failed(f,e,self.Silent)
        # Further possible actions: strip, delete double line breaks
        return text



class SymbolMap:

    def __init__(self,items=(),title='',icon=''):
        self.parent  = Top()
        self.widget  = self.parent.widget
        self.frm_prm = None
        self.gui     = gi.SymbolMap(self.parent)
        self.set_bindings()
        self.reset (items = items
                   ,title = title
                   ,icon  = icon
                   )
    
    def get(self,event=None):
        return self.gui.get()
    
    def set_icon(self,path=''):
        self.gui.set_icon(path)
    
    def set_title(self,text=''):
        if not text:
            text = _('Paste a special symbol')
        self.gui.set_title(text)
        
    def reset(self,items=(),title='',icon=''):
        ''' It is better to run the whole class once again instead of
            doing the reset because frame sizes will not be restored
            after filling a different number of symbols.
        '''
        if not items:
            items = ['1','2','3','4','5']
        items = [lg.com.sanitize(item) for item in items]
        items = [item for item in items if item]
        self.set_title(title)
        self.set_icon(icon)
        if self.frm_prm:
            self.frm_prm.kill()
        self.frm_prm = Frame(self.parent)
        for i in range(len(items)):
            if i % 10 == 0:
                self.frm_row = Frame(self.frm_prm)
            self.gui.insert (frame = self.frm_row
                            ,items = items
                            ,i     = i
                            )

    def set_bindings(self):
        com.bind (obj      = self.parent
                 ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                 ,action   = self.close
                 )

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()



class OptionMenu:
    ''' - 'action' parameter defines an action triggered any time we
          select an OptionMenu item. Use 'com.bind' to set an action
          each time the entire OptionMenu (and not an item) is clicked.
          These bindings do not interfere with each other.
        - tk.OptionMenu will convert integers to strings, but we better
          do this here to avoid problems with iterating ("in requires
          int as the left operand") later (this happens when we pass
          a sequence of chars instead of a list of strings).
        - 'expand' seems to has no effect at the time, but I leave it
          for testing purposes.
    '''
    def __init__ (self
                 ,parent
                 ,items   = ('1','2','3','4','5')
                 ,side    = 'left'
                 ,anchor  = 'center'
                 ,action  = None
                 ,tfocus  = 1
                 ,default = None
                 ,Combo   = False
                 ,expand  = False
                 ,fill    = None
                 ,font    = None
                 ,width   = None
                 ):
        self.parent  = parent
        self.items   = items
        self.action  = action
        self.default = default
        self.Combo   = Combo
        self.side    = side
        self.anchor  = anchor
        self.expand  = expand
        self.fill_   = fill
        # Take focus; must be 1/True to be operational from keyboard
        self.tfocus  = tfocus
        self.font    = font
        self.width   = width
        
        self.gui = gi.OptionMenu (parent = self.parent
                                 ,Combo  = self.Combo
                                 ,side   = self.side
                                 ,anchor = self.anchor
                                 ,expand = self.expand
                                 ,fill   = self.fill_
                                 ,tfocus = self.tfocus
                                 ,font   = self.font
                                 ,width  = self.width
                                 )
        self.widget = self.gui.widget
        if self.Combo:
            com.bind (obj      = self
                     ,bindings = '<<ComboboxSelected>>'
                     ,action   = self.trigger
                     )
        
        self.reset (items   = self.items
                   ,default = self.default
                   ,action  = self.action
                   )
    
    def convert2str(self):
        if not self.items:
            # An error is thrown if 'items' is ()
            self.items = ('1','2','3','4','5')
        self.items = list(self.items)
        self.items = [lg.com.sanitize(item) for item in self.items]
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
    
    def trigger(self,event=None):
        f = '[shared] shared.OptionMenu.trigger'
        self._get()
        if self.Combo:
            self.gui.clear_sel()
        if self.action:
            self.action()
        else:
            com.rep_lazy(f)

    def _set_default(self):
        if len(self.items) > 0:
            self.gui.set(self.items[0])
            ''' Return a default value instead of 'None' if there was
                no interaction with the widget.
            '''
            self.choice = self.items[0]
            self.index  = 0

    def set_default(self):
        f = '[shared] shared.OptionMenu.set_default'
        if self.default is None:
            self._set_default()
        else:
            if self.default in self.items:
                self.gui.set(self.default)
                ''' Return a default value instead of 'None' if there
                    was no interaction with the widget.
                '''
                self.choice = self.default
                self.index  = self.items.index(self.choice)
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
                mes = mes.format(self.default,self.items)
                objs.get_mes(f,mes,True).show_error()
                self._set_default()

    def set(self,item,event=None):
        f = '[shared] shared.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.gui.set(item)
            self.choice = item
            self.index  = self.items.index(self.choice)
        else:
            mes = _('Wrong input data: "{}"!').format(item)
            objs.get_mes(f,mes,True).show_error()

    def fill(self):
        self.gui.fill (items  = self.items
                      ,action = self.trigger
                      )

    def reset (self,items=('1','2','3','4','5')
              ,default=None,action=None
              ):
        self.choice = None
        self.index  = 0
        self.items  = items
        if action:
            self.action = action
        self.convert2str()
        self.fill()
        if default is None:
            if self.choice in self.items:
                default = self.choice
        if default is not None:
            self.default = str(default)
        self.set_default()
        if len(self.items) == 1:
            self.gui.disable()
        else:
            self.gui.enable()

    # Auto updated (after selecting an item)
    def _get(self,event=None):
        f = '[shared] shared.OptionMenu._get'
        self.choice = self.gui.get()
        try:
            self.index = self.items.index(self.choice)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(self.choice)
            objs.get_mes(f,mes,True).show_error()

    def set_prev(self,event=None):
        if self.index == 0:
            self.index = len(self.items) - 1
        else:
            self.index -= 1
        self.choice = self.items[self.index]
        self.gui.set(self.choice)

    def set_next(self,event=None):
        if self.index == len(self.items) - 1:
            self.index = 0
        else:
            self.index += 1
        self.choice = self.items[self.index]
        self.gui.set(self.choice)

    def set_focus(self,event=None):
        self.gui.set_focus()



class ListBox:
    #TODO: configure a font
    def __init__(self
                ,parent
                ,Multiple = False
                ,lst      = []
                ,action   = None
                ,side     = None
                ,expand   = True
                ,fill     = 'both'
                ):
        self.type     = 'ListBox'
        self.state    = 'normal'
        self.parent   = parent
        self.Multiple = Multiple
        self.expand   = expand
        self.side     = side
        self.fill_    = fill
        ''' 'action': A user-defined function that is run when
            pressing Up/Down arrow keys and LMB. There is a problem
            binding it externally, so we bind it here.
        '''
        self.action = action
        
        self.gui = gi.ListBox (parent   = self.parent
                              ,Multiple = self.Multiple
                              ,side     = self.side
                              ,expand   = self.expand
                              ,fill     = self.fill_
                              )
        self.widget = self.gui.widget
        self.set_bindings()
        if lst or action:
            self.reset (lst    = lst
                       ,action = action
                       )

    def set_focus(self,event=None):
        self.gui.set_focus()
    
    def trigger(self,event=None):
        if self.action:
            ''' Binding just to '<Button-1>' does not work. We do not
                need binding Return/space/etc. because the function will
                be called each time the selection is changed. However,
                we still need to bind Up/Down.
            '''
            self.action()
    
    def delete(self,event=None):
        f = '[shared] shared.ListBox.delete'
        # Set an actual value
        self.index()
        try:
            del self.lst[self.index]
            # Set this after 'del' to be triggered only on success
            mes = _('Remove item #{}').format(self.index)
            objs.get_mes(f,mes,True).show_debug()
        except IndexError:
            mes = _('No item #{}!').format(self.index)
            objs.get_mes(f,mes,True).show_warning()
        else:
            self.reset(lst=self.lst)

    def insert(self,string,Top=False):
        # Empty lists are allowed
        if Top:
            pos = 0
        else:
            pos = len(self.lst)
        self.lst.insert(pos,string)
        self.reset(lst=self.lst)
    
    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = '<<ListboxSelect>>'
                 ,action   = self.trigger
                 )
        if not self.Multiple:
            com.bind (obj      = self.gui
                     ,bindings = ('<Up>','<Left>')
                     ,action   = self.move_up
                     )
            com.bind (obj      = self.gui
                     ,bindings = ('<Down>','<Right>')
                     ,action   = self.move_down
                     )

    def resize(self):
        # Autofit to contents
        self.gui.resize()

    def activate(self):
        self.gui.activate(self.index_)

    def clear(self):
        self.gui.clear()

    def clear_sel(self):
        self.gui.clear_sel()

    def reset(self,lst=[],action=None):
        self.clear()
        if lst is None:
            self.lst = []
        else:
            self.lst = list(lst)
        self.lst = [lg.com.sanitize(item) for item in self.lst if item]
        # Checking for None allows to keep an old function
        if action:
            self.action = action
        self.fill()
        self.resize()
        self.index = 0
        self.select()

    def select(self):
        self.clear_sel()
        self.gui.select(self.index)

    def set(self,item):
        f = '[shared] shared.ListBox.set'
        if item:
            if item in self.lst:
                self.index = self.lst.index(item)
                self.select()
            else:
                mes = _('Item "{}" is not in list!').format(item)
                objs.get_mes(f,mes,True).show_error()
        else:
            com.rep_empty(f)

    def fill(self):
        for item in self.lst:
            self.gui.insert(item)

    def get_index(self):
        selection = self.gui.get_sel()
        if selection and len(selection) > 0:
            ''' #NOTE: selection[0] is a number in Python 3.4, however,
                in older interpreters and builds based on them it is a
                string. In order to preserve compatibility, we convert
                it to a number.
            '''
            self.index = int(selection[0])
        else:
            self.index = 0
        return self.index

    def index_add(self):
        if self.get_index() < len(self.lst) - 1:
            self.index += 1
        else:
            self.index = 0

    def index_subtract(self):
        if self.get_index() > 0:
            self.index -= 1
        else:
            self.index = len(self.lst) - 1

    def get(self):
        result = [self.gui.get(idx) for idx in self.gui.get_sel()]
        if self.Multiple:
            return result
        elif len(result) > 0:
            return result[0]

    def move_down(self,event=None):
        self.index_add()
        self.select()
        self.trigger()

    def move_up(self,event=None):
        self.index_subtract()
        self.select()
        self.trigger()
        
    def move_top(self,event=None):
        if self.lst:
            self.index = 0
            self.select()
            self.trigger()
    
    def move_bottom(self,event=None):
        if self.lst:
            self.index = len(self.lst) - 1
            self.select()
            self.trigger()



class ListBoxC:
    ''' This widget is based on 'Top' which already sanitizes input and
        checks an icon path, so we don't do that.
    '''
    def __init__(self
                ,Multiple = False
                ,lst      = []
                ,action   = None
                ,side     = None
                ,expand   = True
                ,fill     = 'both'
                ,title    = 'Title:'
                ,icon     = None
                ,ScrollX  = True
                ,ScrollY  = True
                ,width    = 300
                ,height   = 350
                ):
        self.Save     = False
        self.Multiple = Multiple
        self.lst      = lst
        self.action   = action
        self.side     = side
        self.expand   = expand
        self.fill_    = fill
        self.title    = title
        self.icon     = icon
        self.ScrollX  = ScrollX
        self.ScrollY  = ScrollY
        self.width    = width
        self.height   = height
        self.set_gui()
    
    def set_bindings(self):
        com.bind (obj      = self.gui
                 ,bindings = ('<Return>','<KP_Enter>')
                 ,action   = self.save
                 )
        com.bind (obj      = self.gui
                 ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                 ,action   = self.close
                 )
    
    def get_index(self,event=None):
        return self.lbx_prm.index
    
    def clear(self,event=None):
        self.lbx_prm.clear()
    
    def set_focus(self,event=None):
        self.gui.set_focus()
    
    def set(self,item):
        self.lbx_prm.set(item)
    
    def clear_sel(self,event=None):
        self.lbx_prm.clear_sel()
    
    def reset (self,lst=(1,2,3,4,5)
              ,action=None,title=''
              ,icon=''
              ):
        self.Save = False
        self.lbx_prm.reset (lst    = lst
                           ,action = action
                           )
        self.set_title(title)
        self.set_icon(icon)
    
    def set_buttons(self):
        self.btn_cls = Button (parent   = self.frm_btn
                              ,action   = self.close
                              ,hint     = _('Reject and close')
                              ,text     = _('Close')
                              ,bindings = ('<Escape>','<Control-q>'
                                          ,'<Control-w>'
                                          )
                              )
        self.btn_sav = Button (parent   = self.frm_btn
                              ,action   = self.save
                              ,hint     = _('Accept and close')
                              ,text     = _('Save and close')
                              ,side     = 'right'
                              ,bindings = ('<Return>','<KP_Enter>')
                              )
    
    def get(self):
        if self.Save:
            return self.lbx_prm.get()
        else:
            # Always return a string
            return ''
    
    def set_scrollx(self):
        if self.ScrollX:
            Scrollbar (parent = self.frm_hor
                      ,scroll = self.lbx_prm
                      ,Horiz  = True
                      )
    
    def set_scrolly(self):
        if self.ScrollY:
            Scrollbar (parent = self.frm_ver
                      ,scroll = self.lbx_prm
                      )
    
    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def save(self,event=None):
        self.Save = True
        self.close()
    
    def set_frames(self):
        self.frm_prm = Frame(self.parent)
        self.frm_sec = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btn = Frame (parent = self.frm_prm
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
        self.frm_trt = Frame (parent = self.frm_sec
                             ,side   = 'left'
                             )
        self.frm_ver = Frame (parent = self.frm_sec
                             ,side   = 'right'
                             ,expand = False
                             ,fill   = 'y'
                             )
        ''' Set 'expand' to True and 'propag' to False here, otherwise,
            buttons will not be shown.
        '''
        self.frm_lbx = Frame (parent = self.frm_trt
                             ,side   = 'top'
                             ,propag = False
                             )
        self.frm_hor = Frame (parent = self.frm_trt
                             ,side   = 'bottom'
                             ,expand = False
                             ,fill   = 'x'
                             )
    
    def set_gui(self):
        self.parent = Top (title = self.title
                          ,icon  = self.icon
                          )
        self.widget = self.parent.widget
        geom = '{}x{}'.format(self.width,self.height)
        Geometry(self.parent).set(geom)
        self.set_frames()
        self.lbx_prm = ListBox (parent   = self.frm_lbx
                               ,Multiple = self.Multiple
                               ,lst      = self.lst
                               ,action   = self.action
                               ,side     = self.side
                               ,expand   = self.expand
                               ,fill     = self.fill_
                               )
        self.lbx_prm.set_focus()
        self.gui = gi.ListBoxC(self.parent)
        self.set_scrollx()
        self.set_scrolly()
        self.set_buttons()
        self.set_bindings()
    
    def set_title(self,text=''):
        if text:
            self.title = text
        self.gui.set_title(self.title)
    
    def set_icon(self,path=''):
        if path:
            self.icon = path
        self.gui.set_icon(self.icon)



class Scrollbar:
    
    def __init__(self,parent,scroll,Horiz=False):
        self.type   = 'Scrollbar'
        self.parent = parent
        self.scroll = scroll
        self.Horiz  = Horiz
        self.gui = gi.Scrollbar (parent = self.parent
                                ,scroll = self.scroll
                                )
        if self.check():
            if self.Horiz:
                self.gui.create_x()
                self.gui.config_x()
            else:
                self.gui.create_y()
                self.gui.config_y()
    
    def check(self):
        f = '[shared] shared.Scrollbar.check'
        if self.parent and self.scroll:
            if hasattr(self.parent,'widget') \
            and hasattr(self.scroll,'widget'):
                return True
            else:
                mes = _('Wrong input data!')
                objs.get_mes(f,mes,True).show_error()
        else:
            com.rep_empty(f)



# Pop-up tips; see also 'calltips'; based on idlelib.ToolTip
class ToolTipBase:

    def __init__(self,obj):
        self.obj    = obj
        self.widget = self.obj.widget
        self.gui    = gi.ToolTipBase(self.obj)
        self.tip    = None
        self.id     = None
        self.x      = 0
        self.y      = 0
        self.set_bindings()
    
    def set_bindings(self):
        self.bind_mouse()
                    
    def bind_mouse(self):
        com.bind (obj      = self.obj
                 ,bindings = '<Enter>'
                 ,action   = self.enter
                 )
        com.bind (obj      = self.obj
                 ,bindings = ('<Leave>','<ButtonPress>')
                 ,action   = self.leave
                 )

    def enter(self,event=None):
        self.schedule()

    def leave(self,event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.gui.schedule(self.delay,self.showtip)

    def unschedule(self):
        myid = self.id
        self.id = None
        if myid:
            self.gui.unschedule(myid)

    def showtip(self):
        f = '[shared] shared.ToolTipBase.showtip'
        if self.tip:
            return
        ''' The tip window must be completely outside the widget;
            otherwise, when the mouse enters the tip window we get
            a leave event and it disappears, and then we get an enter
            event and it reappears, and so on forever :-(
            Tip coordinates are calculated such that, despite different
            sizes, centers of a horizontal tip and button would match.
        '''
        x = self.gui.get_rootx() + self.gui.get_width()/2 - self.width/2
        if self.dir == 'bottom':
            y = self.gui.get_rooty() + self.gui.get_height() + 1
        elif self.dir == 'top':
            y = self.gui.get_rooty() - self.height - 1
        else:
            y = 0
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(self.dir,'top, bottom')
            objs.get_mes(f,mes,True).show_error()
        self.tip = Top(Lock=False)
        self.tip.widget.wm_overrideredirect(1)
        # "+%d+%d" is not enough!
        mes = _('Set the geometry to "{}x{}+{}+{}"').format (self.width
                                                            ,self.height
                                                            ,x,y
                                                            )
        objs.get_mes(f,mes,True).show_debug()
        self.tip.widget.wm_geometry ("%dx%d+%d+%d" % (self.width
                                                     ,self.height
                                                     ,x, y
                                                     )
                                    )
        self.showcontents()

    def hidetip(self):
        tw = self.tip
        self.tip = None
        if tw:
            tw.widget.destroy()



class ToolTip(ToolTipBase):

    def __init__(self,obj,text='Sample text'
                ,delay=800,bg='#ffffe0'
                ,hdir='top',bwidth=1
                ,bcolor='navy',font=FONT2
                ):
        self.height = 0
        self.width  = 0
        self.text   = text
        self.delay  = delay
        self.dir    = hdir
        self.bg     = bg
        self.bcolor = bcolor
        self.bwidth = bwidth
        self.font   = font
        self.calc_hint()
        ToolTipBase.__init__(self,obj=obj)

    def calc_hint(self):
        f = '[shared] shared.ToolTip.calc_hint'
        if not self.width or not self.height:
            if self.text:
                if not self.font:
                    self.font = FONT2
                ifont = Font(self.font)
                ifont.set_text(self.text)
                self.width  = ifont.get_width()
                self.height = ifont.get_height()
            else:
                com.rep_lazy(f)
    
    def showcontents(self):
        # Assign this boolean externally to stop showing hints
        self.frm = Frame (parent = self.tip
                         ,bg     = self.bcolor
                         ,bd     = self.bwidth
                         ,expand = False
                         )
        self.lbl = Label (parent  = self.frm
                         ,text    = self.text
                         ,bg      = self.bg
                         ,width   = self.width
                         ,height  = self.height
                         ,justify = 'center'
                         ,font    = self.font
                         )



class WaitBox:

    def __init__(self,icon=''):
        self.type   = 'WaitBox'
        self.parent = Top (Lock   = False
                          ,AutoCr = True
                          ,icon   = icon
                          )
        self.widget = self.parent.widget
        self.gui    = gi.WaitBox(self.parent)
        Geometry(self.parent).set('300x150')
        self.lbl_pls = Label (parent = self.parent
                             ,text   = _('Please wait...')
                             ,expand = True
                             )

    def set_icon(self,path=''):
        f = '[shared] shared.WaitBox.set_icon'
        if path:
            if os.path.exists(path):
                self.gui.set_icon(path)
            else:
                mes = _('File "{}" has not been found!').format(path)
                objs.get_mes(f,mes).show_warning()
        else:
            com.rep_empty(f)
    
    def update(self):
        ''' Tkinter works differently in Linux in Windows. This allows
            to evade focus problems in 'mclient'.
        '''
        if objs.get_os().is_win():
            objs.root().update_idle()
        else:
            self.lbl_pls.widget.update()
    
    # Use tuple for 'args' to pass multiple arguments
    def reset(self,func='',message=''):
        self.set_title(func)
        self.set_message(message)

    def show(self):
        self.gui.show()
        self.update()

    def close(self):
        self.gui.close()

    def set_title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.set_title(text)

    def set_message(self,text=''):
        text = lg.com.sanitize(text)
        if text:
            text += '\n\n' + _('Please wait...')
        else:
            text = _('Please wait...')
        self.lbl_pls.set_text(text)



class Button:

    def __init__ (self
                 ,parent
                 ,action   = None
                 ,hint     = None
                 ,inactive = None
                 ,active   = None
                 ,text     = 'Press me'
                 ,height   = 36
                 ,width    = 36
                 ,side     = 'left'
                 ,expand   = 0
                 ,bg       = None
                 ,bg_focus = None
                 ,fg       = None
                 ,fg_focus = None
                 ,bd       = 0
                 ,hdelay   = 800
                 ,hbg      = '#ffffe0'
                 ,hdir     = 'top'
                 ,hbwidth  = 1
                 ,hbcolor  = 'navy'
                 ,bindings = []
                 ,fill     = 'both'
                 ,Focus    = False
                 ,font     = None
                 ):
        self.Status    = False
        self.type      = 'Button'
        self.parent    = parent
        self.family    = 'Sans'
        self.size      = 12
        self.action    = action
        self.bd        = bd
        self.bg        = bg
        self.bg_focus  = bg_focus
        self.bindings  = bindings
        self.expand    = expand
        self.fg        = fg
        self.fg_focus  = fg_focus
        self.fill      = fill
        self.font      = font
        self.height    = height
        self.hbg       = hbg
        self.hdelay    = hdelay
        self.hdir      = hdir
        self.hint      = hint
        self.side      = side
        self.Focus     = Focus
        self.text      = lg.com.sanitize(text)
        self.width     = width
        if active:
            self.on_img = gi.com.get_image (path   = active
                                           ,width  = self.width
                                           ,height = self.height
                                           )
        else:
            self.on_img = None
        if inactive:
            self.off_img = gi.com.get_image (path   = inactive
                                            ,width  = self.width
                                            ,height = self.height
                                            )
        else:
            self.off_img = None
        self.gui = gi.Button (parent   = parent
                             ,height   = height
                             ,width    = width
                             ,side     = side
                             ,expand   = expand
                             ,bg       = bg
                             ,bg_focus = bg_focus
                             ,fg       = fg
                             ,fg_focus = fg_focus
                             ,bd       = bd
                             ,fill     = fill
                             ,font     = font
                             ,on_img   = self.on_img
                             ,off_img  = self.off_img
                             )
        self.widget = self.gui.widget
        self.set_title(self.text)
        self.set_bindings()
        if self.Focus:
            self.set_focus()
        self.set_hint()
    
    def set_bindings(self):
        com.bind (obj      = self
                 ,bindings = ('<ButtonRelease-1>','<space>'
                             ,'<Return>','<KP_Enter>'
                             )
                 ,action   = self.click
                 )

    def set_hint(self):
        if self.hint:
            if self.bindings:
                self.hextended = self.hint + '\n' \
                                 + lg.Hotkeys(self.bindings).run()
            else:
                self.hextended = self.hint
            self.tip = ToolTip (obj   = self.gui
                               ,text  = self.hextended
                               ,delay = self.hdelay
                               ,font  = self.font
                               ,bg    = self.hbg
                               ,hdir  = self.hdir
                               )
    
    def set_title(self,button_text='Press me'):
        button_text = lg.com.sanitize(button_text)
        self.gui.set_title(button_text)

    def click(self,*args):
        f = '[shared] shared.Button.click'
        if self.action:
            if len(args) > 0:
                self.action(args)
            else:
                self.action()
        else:
            com.rep_lazy(f)

    def activate(self):
        if not self.Status:
            self.Status = True
            if self.on_img:
                self.gui.activate()

    def inactivate(self):
        if self.Status:
            self.Status = False
            if self.off_img:
                self.gui.inactivate()

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def set_focus(self,event=None):
        self.gui.set_focus()
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()



class Frame:

    def __init__ (self,parent,expand=1
                 ,fill='both',side=None,padx=None
                 ,pady=None,ipadx=None,ipady=None
                 ,bd=None,bg=None,width=None
                 ,height=None,propag=True
                 ):
        self.type   = 'Frame'
        self.parent = parent
        self.gui = gi.Frame (parent = parent
                            ,expand = expand
                            ,fill   = fill
                            ,side   = side
                            ,padx   = padx
                            ,pady   = pady
                            ,ipadx  = ipadx
                            ,ipady  = ipady
                            ,bd     = bd
                            ,bg     = bg
                            ,width  = width
                            ,height = height
                            ,propag = propag
                            )
        self.widget = self.gui.widget

    def get_height(self):
        return self.gui.get_height()
    
    def get_width(self):
        return self.gui.get_width()
    
    def get_reqheight(self):
        return self.gui.get_reqheight()
    
    def get_reqwidth(self):
        return self.gui.get_reqwidth()
    
    def kill(self):
        self.gui.kill()
    
    def set_title(self,text=None):
        text = lg.com.sanitize(text)
        self.gui.set_title(text)

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()



class AttachWidget:
    # Make widget 'obj2' immediately adjacent to 'obj1'
    def __init__ (self,obj1,obj2
                 ,anchor='N'
                 ):
        self.set_values()
        self.obj1   = obj1
        self.obj2   = obj2
        self.anchor = anchor
        self.check()
        
    def set_values(self):
        self.anchors = ('N','NE','NW','E','EN','ES','S','SE','SW','W'
                       ,'WN','WS'
                       )
        self.Success = True
        self.w1 = 0
        self.h1 = 0
        self.w2 = 0
        self.h2 = 0
        self.x1 = 0
        self.y1 = 0
        self.x2 = 0
        self.y2 = 0
    
    def check(self):
        f = '[shared] shared.AttachWidget.check'
        if self.obj1 and self.obj2:
            if hasattr(self.obj1,'widget') \
            and hasattr(self.obj2,'widget'):
                self.widget1 = self.obj1.widget
                self.widget2 = self.obj2.widget
            else:
                self.Success = False
                mes = _('Wrong input data!')
                objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            com.rep_empty(f)
        if self.anchor not in self.anchors:
            self.Success = False
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".').format(self.anchor,self.anchors)
            objs.get_mes(f,mes).show_error()
    
    def _set_ne(self):
        self.x2 = self.x1
        self.y2 = self.y1 - self.h2
    
    def _set_n(self):
        self.x2 = self.x1 + self.w1/2 - self.w2/2
        self.y2 = self.y1 - self.h2
    
    def _set_nw(self):
        self.x2 = self.x1 + self.w1 - self.w2
        self.y2 = self.y1 - self.h2
                      
    def _set_en(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1
    
    def _set_e(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1 + self.h1/2 - self.h2/2
    
    def _set_es(self):
        self.x2 = self.x1 - self.w2
        self.y2 = self.y1 + self.h1 - self.h2
    
    def _set_se(self):
        self.x2 = self.x1
        self.y2 = self.y1 + self.h1

    def _set_s(self):
        self.x2 = self.x1 + self.w1/2 - self.w2/2
        self.y2 = self.y1 + self.h1
    
    def _set_sw(self):
        self.x2 = self.x1 + self.w1 - self.w2
        self.y2 = self.y1 + self.h1
    
    def _set_wn(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1
    
    def _set_w(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1 + self.h1/2 - self.h2/2
                      
    def _set_ws(self):
        self.x2 = self.x1 + self.w1
        self.y2 = self.y1 + self.h1 - self.h2
    
    def set(self):
        f = '[shared] shared.AttachWidget.set'
        if self.Success:
            if self.anchor == 'N':
                self._set_n()
            elif self.anchor == 'NE':
                self._set_ne()
            elif self.anchor == 'NW':
                self._set_nw()
            elif self.anchor == 'E':
                self._set_e()
            elif self.anchor == 'EN':
                self._set_en()
            elif self.anchor == 'ES':
                self._set_es()
            elif self.anchor == 'S':
                self._set_s()
            elif self.anchor == 'SE':
                self._set_se()
            elif self.anchor == 'SW':
                self._set_sw()
            elif self.anchor == 'W':
                self._set_w()
            elif self.anchor == 'WN':
                self._set_wn()
            elif self.anchor == 'WS':
                self._set_ws()
            else:
                mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".').format(self.anchor,self.anchors)
                objs.get_mes(f,mes).show_error()
            geom = Geometry(parent=self.obj2)
            ''' Do not use '.format' here since it produces floats
                and we need integers.
            '''
            geom.geom = '%dx%d+%d+%d' % (self.w2,self.h2
                                        ,self.x2,self.y2
                                        )
            geom.restore()
        else:
            com.cancel(f)
    
    def get(self):
        f = '[shared] sharedGUI.AttachWidget.get'
        if self.Success:
            self.x1 = self.widget1.winfo_rootx()
            self.x2 = self.widget2.winfo_rootx()
            self.y1 = self.widget1.winfo_rooty()
            self.y2 = self.widget2.winfo_rooty()
            self.w1 = self.widget1.winfo_width()
            self.w2 = self.widget2.winfo_width()
            self.h1 = self.widget1.winfo_height()
            self.h2 = self.widget2.winfo_height()
            mes = _('Widget 1 geometry: {}x{}+{}+{}').format (self.w1
                                                             ,self.h1
                                                             ,self.x1
                                                             ,self.y1
                                                             )
            objs.get_mes(f,mes,True).show_debug()
            mes = _('Widget 2 geometry: {}x{}+{}+{}').format (self.w2
                                                             ,self.h2
                                                             ,self.x2
                                                             ,self.y2
                                                             )
            objs.get_mes(f,mes,True).show_debug()
        else:
            com.cancel(f)
    
    def run(self,event=None):
        self.get()
        self.set()



class Label:
    ''' 1) Use fill='both' with 'expand=1', otherwise, 'expand' does
           not work
        2) Use 'anchor="w"' to left align text
        3) Parents are 'Top' and 'Root' (the last only with
           'wait_window()')
        4) Inappropriate use of 'config' may result in resetting 
           config options. List of them: http://effbot.org/tkinterbook/label.htm#Tkinter.Label.config-method
    '''
    def __init__ (self,parent,text='Text:'
                 ,font=FONT2,side=None,fill=None
                 ,expand=False,ipadx=None,ipady=None
                 ,image=None,fg=None,bg=None
                 ,anchor=None,width=None
                 ,height=None,justify=None
                 ,padx=None,pady=None
                 ):
        self.type   = 'Label'
        self.parent = parent
        self.side   = side
        self.fill   = fill
        self.expand = expand
        self.text   = text
        self.font   = font
        self.ipadx  = ipadx
        self.ipady  = ipady
        self.padx   = padx
        self.pady   = pady
        self.image  = image
        self.bg     = bg
        self.fg     = fg
        self.anchor = anchor
        self.width  = width
        self.height = height
        # Usually the alignment is done by tuning the parent
        self.justify = justify
        self.gui = gi.Label (parent  = self.parent
                            ,side    = self.side
                            ,fill    = self.fill
                            ,expand  = self.expand
                            ,ipadx   = self.ipadx
                            ,ipady   = self.ipady
                            ,padx    = self.padx
                            ,pady    = self.pady
                            ,image   = self.image
                            ,fg      = self.fg
                            ,bg      = self.bg
                            ,anchor  = self.anchor
                            ,width   = self.width
                            ,height  = self.height
                            ,justify = self.justify
                            )
        self.widget  = self.gui.widget
        self.set_text(self.text)
        self.set_font(self.font)
    
    def get_reqheight(self,event=None):
        return self.gui.get_reqheight()
    
    def get_reqwidth(self,event=None):
        return self.gui.get_reqwidth()
    
    def kill(self,event=None):
        self.gui.kill()
    
    def disable(self,event=None):
        self.gui.disable()
    
    def enable(self,event=None):
        self.gui.enable()

    def set_text(self,arg=None):
        if arg:
            self.text = arg
        self.text = lg.com.sanitize(arg)
        self.gui.set_text(self.text)

    def set_font(self,arg=None):
        f = '[shared] shared.Label.set_font'
        if arg:
            self.font = arg
        if not self.gui.set_font(self.font):
            mes = _('Wrong font: "{}"!').format(self.font)
            objs.get_mes(f,mes,True).show_error()
            self.font = FONT2

    def show(self,event=None):
        self.gui.show()

    def close(self,event=None):
        self.gui.close()

    def set_title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.set_title(text)
        
    def reset(self):
        ''' #NOTE #TODO For some reason, using 'config' externally may 
            reset config options. Use them altogether to prevent such 
            behavior.
        '''
        self.widget.config (text   = self.text
                           ,font   = self.font
                           #,image = self.image
                           ,bg     = self.bg
                           ,fg     = self.fg
                           ,anchor = self.anchor
                           ,width  = self.width
                           ,height = self.height
                           )



class Geometry:
    ''' Window behavior is not uniform through different platforms or
        even through different Windows versions.
    '''
    def __init__(self,parent=None,title=None,hwnd=None):
        self.parent = parent
        self.title  = title
        self.hwnd   = hwnd
        self.geom   = None
        self.gui    = gi.Geometry(parent)

    def update(self):
        self.gui.update()

    def save(self):
        f = '[shared] shared.Geometry.save'
        if self.parent:
            self.update()
            self.geom = self.gui.set_geometry()
            mes = _('Save geometry: {}').format(self.geom)
            objs.get_mes(f,mes,True).show_info()
        else:
            com.rep_empty(f)

    def restore(self):
        f = '[shared] shared.Geometry.restore'
        if self.parent:
            if self.geom:
                mes = _('Restore geometry: {}').format(self.geom)
                objs.get_mes(f,mes,True).show_debug()
                self.gui.restore(self.geom)
            else:
                mes = _('Failed to restore geometry!')
                objs.get_mes(f,mes,True).show_warning()
        else:
            com.rep_empty(f)

    def set_foreground(self,event=None):
        f = '[shared] shared.Geometry.set_foreground'
        if objs.get_os().is_win():
            if self.get_hwnd():
                ''' 'pywintypes.error', but needs to import this for
                    some reason
                '''
                try:
                    win32gui.SetForegroundWindow(self.hwnd)
                except:
                    ''' In Windows 'Message' can be raised foreground,
                        so we just log it
                    '''
                    mes = _('Failed to change window properties!')
                    objs.get_mes(f,mes,True).show_error()
            else:
                com.rep_empty(f)
        elif self.parent:
            self.gui.set_foreground()
        else:
            com.rep_empty(f)

    def minimize(self,event=None):
        f = '[shared] shared.Geometry.minimize'
        if self.parent:
            ''' # Does not always work
                if objs.get_os().is_win():
                    win32gui.ShowWindow (self.get_hwnd()
                                        ,win32con.SW_MINIMIZE
                                        )
                else:
            '''
            self.gui.minimize()
        else:
            com.rep_empty(f)

    def maximize(self,event=None):
        f = '[shared] shared.Geometry.maximize'
        if lg.objs.get_os().is_win():
            #win32gui.ShowWindow(self.get_hwnd(),win32con.SW_MAXIMIZE)
            self.gui.maximize_win()
        elif self.parent:
            self.gui.maximize_nix()
        else:
            com.rep_empty(f)

    def set_focus(self,event=None):
        f = '[shared] shared.Geometry.set_focus'
        if lg.objs.get_os().is_win():
            win32gui.SetActiveWindow(self.get_hwnd())
        elif self.parent:
            self.gui.set_focus()
        else:
            com.rep_empty(f)

    def lift(self,event=None):
        f = '[shared] shared.Geometry.lift'
        if self.parent:
            self.gui.lift()
        else:
            com.rep_empty(f)

    def _activate(self):
        f = '[shared] shared.Geometry._activate'
        if self.parent:
            self.gui._activate()
        else:
            com.rep_empty(f)

    def activate(self,event=None,MouseClicked=False):
        self._activate()
        if objs.get_os().is_win():
            #TODO: learn how to properly import modules
            import ctypes
            self.parent.widget.wm_attributes('-topmost',1)
            self.parent.widget.wm_attributes('-topmost',0)
            ''' Without this, a button click will fire a button action
                where it is not needed.
            '''
            if MouseClicked:
                ''' It's an ugly hack, but we cannot set a focus on
                    a widget without this (we manage without this
                    in Linux/Windows XP, however, this is required in
                    Windows 7/8).
                '''
                # Emulate a mouse button click
                # left mouse button down
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
                # left mouse button up
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

    def get_hwnd(self,event=None):
        f = '[shared] shared.Geometry.get_hwnd'
        if not self.hwnd:
            if self.title:
                try:
                    self.hwnd = win32gui.FindWindow(None,self.title)
                except win32ui.error:
                    mes = _('Failed to get the window handle!')
                    objs.get_mes(f,mes,True).show_error()
            else:
                com.rep_empty(f)
        return self.hwnd

    def set(self,arg='800x600'):
        self.geom = arg
        self.restore()



class Top:

    def __init__ (self,Maximize=False
                 ,AutoCr=True,Lock=True
                 ,icon='',title=''
                 ):
        ''' 'Lock = True': the further program execution is blocked
            until an attempt to close the widget. 'Lock = False' allows
            to create several widgets on the screen at the same time.
            They will be operational, however, the widget having
            'Lock = False' will be closed when closing with
            'Lock = True'. Moreover, if none of the widgets has
            'Lock = True', then they all will be shown and immediately
            closed.
        '''
        self.set_values()
        self.AutoCr = AutoCr
        self.gui    = gi.Top(Lock=Lock)
        self.widget = self.gui.widget
        if Maximize:
            Geometry(parent=self).maximize()
        if icon:
            self.set_icon(icon)
        elif objs.icon:
            self.set_icon(objs.icon)
        if title:
            self.set_title(title)
        
    def kill(self,event=None):
        self.widget.destroy()
    
    def update_idle(self,event=None):
        self.gui.update_idle()
    
    def set_icon(self,path=''):
        f = '[shared] shared.Top.set_icon'
        if path:
            if os.path.exists(path):
                self.gui.set_icon(path)
            else:
                mes = _('File "{}" has not been found!').format(path)
                objs.get_mes(f,mes).show_warning()
        else:
            com.rep_empty(f)
    
    def set_title(self,text=''):
        text = lg.com.sanitize(text)
        self.gui.set_title(text)
    
    def set_values(self):
        self.type  = 'Toplevel'
        self.count = 0

    def close(self,event=None):
        self.gui.close()

    def show(self):
        ''' Changing geometry at a wrong time may prevent frames
            from autoresizing after 'pack_forget'.
        '''
        if self.count == 0 and self.AutoCr:
            self.center()
        self.count += 1
        self.gui.show()

    def get_resolution(self):
        return self.gui.get_resolution()

    def center(self):
        ''' Make child widget always centered at the first time and up
            to a user's choice any other time (if the widget is reused).
            Only 'tk.Tk' and 'tk.Toplevel' types are supported.
        '''
        width, height = self.get_resolution()
        size = tuple(int(item) for item \
                in self.gui.set_geometry().split('+')[0].split('x'))
        x = width/2 - size[0]/2
        y = height/2 - size[1]/2
        self.gui.set_geometry("%dx%d+%d+%d" % (size + (x, y)))

    def set_focus(self,event=None):
        self.gui.set_focus()



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
            self.txt = TextBoxRW (title    = _('Test:')
                                 ,font     = font
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
            self.waitbox = WaitBox(icon)
        return self.waitbox
    
    def get_root(self,Close=True):
        return gi.objs.get_root(Close)
    
    def get_error(self):
        if self.error is None:
            self.error = MessageBuilder (level  = _('ERROR')
                                        ,Single = True
                                        ,YesNo  = False
                                        )
        return self.error
    
    def get_warning(self):
        if self.warning is None:
            self.warning = MessageBuilder (level  = _('WARNING')
                                          ,Single = True
                                          ,YesNo  = False
                                          )
        return self.warning
    
    def get_debug(self):
        # Reusing the same 'info' object may result in GUI glitches
        if self.debug is None:
            self.debug = MessageBuilder (level  = _('INFO')
                                        ,Single = True
                                        ,YesNo  = False
                                        )
        return self.debug
    
    def get_info(self):
        if self.info is None:
            self.info = MessageBuilder (level  = _('INFO')
                                       ,Single = True
                                       ,YesNo  = False
                                       )
        return self.info
    
    def get_question(self):
        if self.question is None:
            self.question = MessageBuilder (level  = _('QUESTION')
                                           ,Single = False
                                           ,YesNo  = True
                                           )
        return self.question



class MessageBuilder:
    ''' Not using tkinter.messagebox because it blocks main GUI (even
        if we specify a non-root parent).
    '''
    def __init__(self,level,Single=True,YesNo=False):
        self.level  = level
        self.Single = Single
        self.YesNo  = YesNo
        self.logic  = lg.MessageBuilder(self.level)
        self.parent = Top()
        self.widget = self.parent.widget
        self.gui    = gi.MessageBuilder(self.parent)
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
        com.bind (obj      = self
                 ,bindings = ('<Control-q>','<Control-w>','<Escape>')
                 ,action   = self.close_no
                 )
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def set_frames(self):
        self.frm_prm = Frame (parent = self.gui.parent)
        self.frm_top = Frame (parent = self.frm_prm
                             ,side   = 'top'
                             )
        self.frm_btm = Frame (parent = self.frm_prm
                             ,expand = False
                             ,side   = 'bottom'
                             )
        self.frm_tpl = Frame (parent = self.frm_top
                             ,expand = False
                             ,side   = 'left'
                             )
        self.frm_tpr = Frame (parent = self.frm_top
                             ,side   = 'right'
                             ,propag = False
                             )
        self.frm_btl = Frame (parent = self.frm_btm
                             ,side   = 'left'
                             )
        self.frm_btr = Frame (parent = self.frm_btm
                             ,side   = 'right'
                             )
    
    def set_buttons(self):
        if self.YesNo:
            YesName = _('Yes')
            NoName  = _('No')
        else:
            YesName = 'OK'
            NoName  = _('Cancel')
        if self.Single:
            self.btn_yes = Button (parent = self.frm_btl
                                  ,action = self.close_yes
                                  ,hint   = _('Accept and close')
                                  ,text   = YesName
                                  ,Focus  = 1
                                  ,side   = 'right'
                                  )
        else:
            self.btn_no  = Button (parent = self.frm_btl
                                  ,action = self.close_no
                                  ,hint   = _('Reject and close')
                                  ,text   = NoName
                                  ,side   = 'left'
                                  )
            self.btn_yes = Button (parent = self.frm_btr
                                  ,action = self.close_yes
                                  ,hint   = _('Accept and close')
                                  ,text   = YesName
                                  ,Focus  = 1
                                  ,side   = 'right'
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
        self.btn_yes.set_focus()
        self.gui.show()
    
    def close(self,event=None):
        self.gui.close()
    
    def reset(self,title='',text=''):
        self.logic.reset (text  = text
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
                                        ,obj  = self.frm_tpl
                                        )
            ''' We need to assign self.variable to Label, otherwise,
                it gets destroyed.
            '''
            self.lbl_img = Label (parent = self.frm_tpl
                                 ,image  = iimage
                                 )
        else:
            com.rep_empty(f)



class Message:

    def __init__(self,func,message,Silent=False):
        self.func    = func
        self.message = message
        self.Silent  = Silent

    def show_debug(self):
        if GUI_MES and not self.Silent:
            objs.get_debug().reset (title = self.func
                                   ,text  = self.message
                                   )
            objs.debug.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).show_debug()
    
    def show_error(self):
        if GUI_MES and not self.Silent:
            objs.get_error().reset (title = self.func
                                   ,text  = self.message
                                   )
            objs.error.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).show_error()

    def show_info(self):
        if GUI_MES and not self.Silent:
            objs.get_info().reset (title = self.func
                                  ,text  = self.message
                                  )
            objs.info.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).show_info()
                       
    def show_warning(self):
        if GUI_MES and not self.Silent:
            objs.get_warning().reset (title = self.func
                                     ,text  = self.message
                                     )
            objs.warning.show()
        # Duplicate the message to the console
        lg.Message (func    = self.func
                   ,message = self.message
                   ).show_warning()

    def show_question(self):
        if GUI_MES and not self.Silent:
            objs.get_question().reset (title = self.func
                                      ,text  = self.message
                                      )
            objs.question.show()
            lg.log.append (self.func
                          ,_('QUESTION')
                          ,self.message
                          )
            answer = objs.question.ask()
            lg.Message (func    = self.func
                       ,message = str(answer)
                       ).show_debug()
            return answer
        else:
            return lg.Message (func    = self.func
                              ,message = self.message
                              ).show_question()



class Commands(lg.Commands):
    
    def __init__(self):
        super().__init__()
    
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
    
    def run_fast_debug(self,text):
        objs.get_txt (font     = 'Mono 11'
                     ,Maximize = True
                     ).reset()
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
    
    def start(self,Close=True):
        gi.objs.start(Close)
    
    def end(self):
        gi.objs.end()



class Font:
    
    def __init__(self,name,xborder=20,yborder=20):
        self.font  = None
        self.gui   = gi.Font()
        self.logic = lg.Font (name    = name
                             ,xborder = xborder
                             ,yborder = yborder
                             )
    
    def reset(self,name,xborder=20,yborder=20):
        self.logic.reset (name    = name
                         ,xborder = xborder
                         ,yborder = yborder
                         )
    
    def set_text(self,text):
        self.logic.set_text(text)
    
    def get_font(self):
        f = '[shared] shared.Font.get_font'
        if not self.font:
            if self.logic.family and self.logic.size:
                self.font = self.gui.get_font (family = self.logic.family
                                              ,size   = self.logic.size
                                              )
            else:
                com.rep_empty(f)
        return self.font
    
    def get_height(self):
        f = '[shared] shared.Font.get_height'
        if not self.logic.height:
            if self.get_font():
                try:
                    self.logic.height = self.gui.get_height(self.font)
                except Exception as e:
                    objs.get_mes(f,str(e),True).show_error()
                self.logic.set_height()
            else:
                com.rep_empty(f)
        return self.logic.height
    
    def get_width(self):
        f = '[shared] shared.Font.get_width'
        if not self.logic.width:
            if self.get_font() and self.logic.text:
                try:
                    max_line = sorted (self.logic.text.splitlines()
                                      ,key     = len
                                      ,reverse = True
                                      )[0]
                    self.logic.width = self.gui.get_width (font     = self.font
                                                          ,max_line = max_line
                                                          )
                except Exception as e:
                    objs.get_mes(f,str(e),True).show_error()
                self.logic.set_width()
            else:
                com.rep_empty(f)
        return self.logic.width


com  = Commands()
objs = Objects()
# Use GUI dialogs for logic-only modules
lg.objs.mes = Message


if __name__ == '__main__':
    f = '[shared] shared.__main__'
    com.start()
    lg.ReadTextFile('/tmp/aaa').get()
    com.end()
