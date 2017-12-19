#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import gettext, gettext_windows
gettext_windows.setup_env()
gettext.install('shared','./locale')

import tkinter as tk
import tkinter.filedialog as dialog
import sys, os
import shared as sh


# Привязать горячие клавиши или кнопки мыши к действию
def bind(obj,bindings,action): # object, str/list, function
    if hasattr(obj,'widget'):
        if isinstance(bindings,str) or isinstance(bindings,list):
            if isinstance(bindings,str):
                bindings = [bindings]
            for binding in bindings:
                try:
                    obj.widget.bind(binding,action)
                except tk.TclError:
                    Message (func    = 'bind'
                            ,level   = _('ERROR')
                            ,message = _('Failed to enable key combination "%s"!') % binding
                            )
        else:
            Message (func    = 'bind'
                    ,level   = _('ERROR')
                    ,message =_('Wrong input data: "%s"') % str(bindings)
                    )
    else:
        Message (func    = 'bind'
                ,level   = _('ERROR')
                ,message = _('Wrong input data!')
                )

def dialog_save_file(filetypes=()):
    file = ''
    if not filetypes:
        filetypes = ((_('Plain text (UTF-8)'),'.txt' )
                    ,( _('Web-page')         ,'.htm' )
                    ,( _('Web-page')         ,'.html')
                    ,( _('All files')        ,'*'    )
                    )
    options                = {}
    options['initialfile'] = ''
    options['filetypes']   = filetypes
    options['title']       = _('Save As:')
    try:
        file = dialog.asksaveasfilename(**options)
    except:
        Message (func    = 'dialog_save_file'
                ,level   = _('ERROR')
                ,message = _('Failed to select a file!')
                )
    return file
    
# Make a color (a color name (/usr/share/X11/rgb.txt) or a hex value) brighter (positive delta) or darker (negative delta)
def mod_color(color,delta=76): # ~30%
    if -255 <= delta <= 255:
        try:
            rgb = objs.root().widget.winfo_rgb(color=color)
            rgb = tuple(max(min(255,x/256+delta),0) for x in rgb)
            return '#%02x%02x%02x' % rgb
        except tk._tkinter.TclError:
            Message (func    = 'mod_color'
                    ,level   = _('WARNING')
                    ,message = _('An unknown color "%s"!') % str(color)
                    )
    else:
        Message (func    = 'mod_color'
                ,level   = _('WARNING')
                ,message = _('The condition "%s" is not observed!') % ('-255 <= %d <= 255' % delta)
                )



# Класс для оформления root как виджета
class Root:

    def __init__(self):
        self.type = 'Root'
        self.widget = tk.Tk()

    def run(self):
        self.widget.mainloop()

    def show(self):
        self.widget.deiconify()

    def close(self):
        self.widget.withdraw()

    def destroy(self):
        self.kill()

    def kill(self):
        self.widget.destroy()

    def update(self):
        self.widget.update()



class WidgetShared: # Do not use graphical logging there

    def focus(object,*args):
        object.widget.focus()

    def insert(object,text,pos):
        if text:
            if object.type == 'TextBox' or object.type == 'Entry':
                try:
                    object.widget.insert(pos,text)
                except tk.TclError:
                    try:
                        object.widget.insert(pos,_('Failed to insert the text!'))
                    except tk.TclError:
                        sh.log.append (func    = 'WidgetShared.insert'
                                      ,level   = _('ERROR')
                                      ,message = _('Failed to insert the text!')
                                      )
            else:
                sh.log.append (func    = 'WidgetShared.insert'
                              ,level   = _('ERROR')
                              ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                              )
        # Too frequent
        '''
        else:
            sh.log.append ('WidgetShared.insert'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        '''

    def font(object,font='Sans 11'): # font_style, sh.globs['var']['menu_font']
        if object.type == 'TextBox' or object.type == 'Entry':
            object.widget.config(font=font)
        else:
            sh.log.append (func    = 'WidgetShared.font'
                          ,level   = _('ERROR')
                          ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                          )

    def set_state(object,ReadOnly=False):
        if object.type == 'TextBox' or object.type == 'Entry':
            if ReadOnly:
                object.widget.config(state='disabled')
                object.state = 'disabled'
            else:
                object.widget.config(state='normal')
                object.state = 'normal'
        else:
            sh.log.append (func    = 'WidgetShared.set_state'
                          ,level   = _('ERROR')
                          ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                          )

    def title(object,text=_('Text:'),my_program_title=''): # Родительский виджет
        if object.type == 'Toplevel' or object.type == 'Root':
            object.widget.title(text + my_program_title)
        else:
            sh.log.append (func    = 'WidgetShared.title'
                          ,level   = _('ERROR')
                          ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                          )

    def custom_buttons(object):
        if not object.Composite:
            if object.parent_obj.type == 'Toplevel' or object.parent_obj.type == 'Root':
                if object.state == 'disabled':
                    object.parent_obj.close_button.widget.config(text=_('Quit'))
                else:
                    object.parent_obj.close_button.widget.config(text=_('Save and close'))
            else:
                sh.log.append (func    = 'WidgetShared.custom_buttons'
                              ,level   = _('ERROR')
                              ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                              )

    def icon(object,file): # Родительский объект
        if object.type == 'Toplevel' or object.type == 'Root':
            if file and os.path.exists(file):
                object.widget.tk.call('wm','iconphoto',object.widget._w,tk.PhotoImage(master=object.widget,file=file))
            else:
                sh.log.append (func    = 'WidgetShared.icon'
                              ,level   = _('ERROR')
                              ,message = _('File "%s" has not been found!') % str(file)
                              )
        else:
            sh.log.append (func    = 'WidgetShared.icon'
                          ,level   = _('ERROR')
                          ,message = _('A logic error: unknown object type: "%s"!') % str(object.type)
                          )



class Top:

    def __init__(self,parent_obj,Maximize=False,AutoCenter=True):
        self.values()
        self.parent_obj = parent_obj
        self.AutoCenter = AutoCenter
        self.widget     = tk.Toplevel(self.parent_obj.widget)
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
        if Maximize:
            Geometry(parent_obj=self).maximize()
        self.tk_trigger = tk.BooleanVar()
        
    def values(self):
        self.type  = 'Toplevel'
        # Lock = True - блокировать дальнейшее выполнение программы до попытки закрытия виджета. Lock = False позволяет создать одновременно несколько виджетов на экране. Они будут работать, однако, виджет с Lock = False будет закрыт при закрытии виджета с Lock = True. Кроме того, если ни один из виджетов не имеет Lock = True, то они все будут показаны и тут же закрыты.
        self.Lock  = False
        self.count = 0

    def close(self,*args):
        self.widget.withdraw()
        if self.Lock:
            self.tk_trigger.set(True)

    def show(self,Lock=True):
        self.count += 1
        self.widget.deiconify()
        # Changing geometry at a wrong time may prevent frames from autoresizing after 'pack_forget'
        if self.AutoCenter:
            self.center()
        self.Lock = Lock
        if self.Lock:
            self.tk_trigger = tk.BooleanVar()
            self.widget.wait_variable(self.tk_trigger)

    def title(self,text=_('Title:')):
        WidgetShared.title(self,text=text)

    def icon(self,path):
        WidgetShared.icon(self,path)

    def resolution(self):
        self.widget.update_idletasks()
        return (self.widget.winfo_screenwidth()
               ,self.widget.winfo_screenheight()
               )

    # todo: not centers without Force=True when Lock=False
    def center(self,Force=False):
        # Make child widget always centered at the first time and up to a user's choice any other time (if the widget is reused).
        if self.count == 1 or Force:
            width, height = self.resolution()
            size = tuple(int(item) for item in self.widget.geometry().split('+')[0].split('x'))
            x = width/2 - size[0]/2
            y = height/2 - size[1]/2
            self.widget.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def focus(self,*args):
        self.widget.focus_set()



# todo (?): fix: if duplicate spaces/line breaks are not deleted, text with and without punctuation will have a different number of words; thus, tkinter will be supplied wrong positions upon Search
class SearchBox:

    def __init__(self,obj):
        self.type       = 'SearchBox'
        self.obj        = obj
        self.parent_obj = self.obj.parent_obj
        h_top           = Top(self.parent_obj)
        self.h_entry    = Entry(h_top)
        self.h_entry.title(text=_('Find:'))
        self.h_entry.close()
        self.h_sel      = Selection(self.obj)

    def reset_logic(self,words=None,Strict=False): # Strict: case-sensitive, with punctuation
        self.Success    = True
        self._prev_loop = self._next_loop = self._search = self._pos1 = self._pos2 = self._text = None
        self.i          = 0
        self.words      = words
        self.Strict     = Strict
        if self.words:
            if self.Strict: # Do not get text from the widget - it's not packed yet
                self._text = self.words._text_p
            else:
                self._text = self.words._text_n
            self.h_sel.reset_logic(words=self.words)
            self.h_search = sh.Search(text=self._text)
        else:
            self.Success = False
            # Too frequent
            '''
            Message (func    = 'SearchBox.reset_logic'
                    ,level   = _('WARNING')
                    ,message = _('Not enough input data!')
                    ,Silent  = True
                    )
            '''

    def reset_data(self):
        self.Success    = True
        self._prev_loop = self._next_loop = self._search = self._pos1 = self._pos2 = None
        self.i          = 0
        self.search()
        if self._text and self._search:
            self.h_search.reset(text=self._text,search=self._search)
            self.h_search.next_loop()
            if not self.h_search._next_loop: # Prevents from calling self.search() once again
                Message (func    = 'SearchBox.reset_data'
                        ,level   = _('INFO')
                        ,message = _('No matches!')
                        )
                self.Success = False
        else:
            self.Success = False
            sh.log.append ('SearchBox.reset_data'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def reset(self,mode='data',words=None,Strict=False):
        if mode == 'data':
            self.reset_data()
        else:
            self.reset_logic(words=words,Strict=Strict)

    def loop(self):
        if self.Success:
            if not self.h_search._next_loop:
                self.reset()
        else:
            sh.log.append ('SearchBox.loop'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )
        return self.h_search._next_loop

    def add(self):
        if self.Success:
            if self.i < len(self.loop()) - 1:
                self.i += 1
        else:
            sh.log.append ('SearchBox.add'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def subtract(self):
        if self.Success:
            if self.i > 0:
                self.i -= 1
        else:
            sh.log.append ('SearchBox.subtract'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def new(self,*args):
        self.reset_data()
        self.next()

    def select(self):
        if self.Success:
            if self.Strict:
                result1 = self.words.no_by_pos_p(pos=self.pos1())
                result2 = self.words.no_by_pos_p(pos=self.pos2())
            else:
                result1 = self.words.no_by_pos_n(pos=self.pos1())
                result2 = self.words.no_by_pos_n(pos=self.pos2())
            if result1 is None or result2 is None:
                sh.log.append ('SearchBox.select'
                              ,_('ERROR')
                              ,_('Wrong input data!')
                              )
            else:
                _pos1tk = self.words.words[result1].tf()
                _pos2tk = self.words.words[result2].tl()
                self.h_sel.reset(pos1tk=_pos1tk,pos2tk=_pos2tk,background='green')
                self.h_sel.set()
        else:
            sh.log.append ('SearchBox.select'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def search(self):
        if self.Success:
            if self.words and not self._search:
                self.h_entry.focus()
                self.h_entry.select_all()
                self.h_entry.show()
                self._search = self.h_entry.get()
                if self._search and not self.Strict:
                    self._search = sh.Text(text=self._search,Auto=False).delete_punctuation()
                    self._search = sh.Text(text=self._search,Auto=False).delete_duplicate_spaces()
                    self._search = self._search.lower()
            return self._search
        else:
            sh.log.append ('SearchBox.search'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def next(self,*args):
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.add()
                if old_i == self.i:
                    if len(_loop) == 1:
                        Message (func    = 'SearchBox.next'
                                ,level   = _('INFO')
                                ,message = _('Only one match has been found!')
                                )
                    else:
                        Message (func    = 'SearchBox.next'
                                ,level   = _('INFO')
                                ,message = _('No more matches, continuing from the top!')
                                )
                        self.i = 0
                self.select()
            else:
                Message (func    = 'SearchBox.next'
                        ,level   = _('INFO')
                        ,message = _('No matches!')
                        )
        else:
            sh.log.append ('SearchBox.next'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def prev(self,*args):
        if self.Success:
            _loop = self.loop()
            if _loop:
                old_i = self.i
                self.subtract()
                if old_i == self.i:
                    if len(_loop) == 1:
                        Message (func    = 'SearchBox.prev'
                                ,level   = _('INFO')
                                ,message = _('Only one match has been found!')
                                )
                    else:
                        Message (func    = 'SearchBox.prev'
                                ,level   = _('INFO')
                                ,message = _('No more matches, continuing from the bottom!')
                                )
                        self.i = len(_loop) - 1 # Not just -1
                self.select()
            else:
                Message (func    = 'SearchBox.prev'
                        ,level   = _('INFO')
                        ,message = _('No matches!')
                        )
        else:
            sh.log.append ('SearchBox.prev'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def pos1(self):
        if self.Success:
            if self._pos1 is None:
                self.loop()
                self.i = 0
            _loop = self.loop()
            if _loop:
                self._pos1 = _loop[self.i]
            return self._pos1
        else:
            sh.log.append ('SearchBox.pos1'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )

    def pos2(self):
        if self.Success:
            if self.pos1() is not None:
                self._pos2 = self._pos1 + len(self.search())
            return self._pos2
        else:
            sh.log.append ('SearchBox.pos2'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



class TextBox:

    def __init__(self,parent_obj,Composite=False
                ,expand=1,side=None,fill='both'
                ,words=None,font='Serif 14'
                ,ScrollX=False,SpecialReturn=True
                ,state='normal'
                ):
        self.type      = 'TextBox'
        self.Composite = Composite
        self.ScrollX   = ScrollX
        self.font      = font
        self.state     = state # 'normal' - обычный режим; 'disabled' - отключить редактирование; выберите 'disabled', чтобы надпись на кнопке была другой
        self.SpecialReturn = SpecialReturn
        # (optional, external) Prevent resetting the active (already shown) widget
        self.Active     = False
        self.Save       = False
        self.tags       = []
        self.marks      = []
        self.parent_obj = parent_obj
        self.expand     = expand
        self.side       = side
        self.fill       = fill
        self.selection  = Selection(h_widget=self)
        self.gui()
        self.reset_logic(words=words)
        if not self.Composite:
            self.focus()

    def _gui_txt(self):
        if self.parent_obj.type in ('Root','Toplevel'):
            self.widget = tk.Text (self.parent_obj.widget
                                  ,font   = self.font
                                  ,wrap   = 'word'
                                  ,height = 1
                                  )
        else:
            self.widget = tk.Text (self.parent_obj.widget
                                  ,font = self.font
                                  ,wrap = 'word'
                                  )
        self.widget.pack (expand = self.expand
                         ,fill   = self.fill
                         ,side   = self.side
                         )

    def _gui_scroll_hor(self):
        frame = Frame (parent_obj = self.parent_obj
                      ,expand     = 0
                      ,fill       = 'x'
                      ,side       = 'top'
                      )
        self.scrollbar_hor = tk.Scrollbar (frame.widget
                                          ,orient    = tk.HORIZONTAL
                                          ,jump      = 0
                                          ,takefocus = False
                                          )
        self.widget.config(xscrollcommand=self.scrollbar_hor.set)
        self.scrollbar_hor.config(command=self.widget.xview)
        self.scrollbar_hor.pack(expand=1,fill='x')

    def _gui_scroll_ver(self):
        self.scrollbar = tk.Scrollbar (master    = self.widget
                                      ,jump      = 0
                                      ,takefocus = False
                                      )
        self.widget.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.widget.yview)
        self.scrollbar.pack(side='right',fill='y')

    def gui(self):
        self._gui_txt()
        self._gui_scroll_ver()
        if self.ScrollX:
            self._gui_scroll_hor()
        if not self.Composite and not hasattr(self.parent_obj,'close_button'):
            if self.parent_obj.type == 'Toplevel' or self.parent_obj.type == 'Root':
                self.parent_obj.close_button = Button (self.parent_obj
                                                      ,text   = _('Quit')
                                                      ,hint   = _('Quit')
                                                      ,action = self.close
                                                      ,expand = 0
                                                      ,side   = 'bottom'
                                                      )
        self.search_box = SearchBox(self)
        WidgetShared.custom_buttons(self)
        self.bindings()

    def reset(self,mode='data',words=None):
        if mode == 'data':
            self.reset_data()
        else:
            self.reset_logic(words=words)

    def reset_logic(self,words=None):
        self.words = words
        self.search_box.reset_logic(words=self.words)
        self.selection.reset_data()
        self.selection.reset_logic(words=self.words)

    # Delete text, tags, marks
    def reset_data(self,*args):
        self.clear_text()
        self.clear_tags()
        self.clear_marks()

    # Setting ReadOnly state works only after filling text. Only tk.Text, tk.Entry and not tk.Toplevel are supported.
    def read_only(self,ReadOnly=True):
        WidgetShared.set_state(self,ReadOnly=ReadOnly)

    def show(self):
        self.Active = True
        self.parent_obj.show()

    def close(self,*args):
        self.Save   = True
        self.Active = False
        self.parent_obj.close()
        return 'break'

    def bindings(self):
        bind (obj      = self
             ,bindings = ['<Control-f>','<Control-F3>']
             ,action   = self.search_box.new
             )
        bind (obj      = self
             ,bindings = '<F3>'
             ,action   = self.search_box.next
             )
        bind (obj      = self
             ,bindings = '<Shift-F3>'
             ,action   = self.search_box.prev
             )
        # Только для несоставных виджетов
        if not self.Composite:
            self.widget.unbind('<Return>')
            if self.state == 'disabled' or self.SpecialReturn:
                # Разрешать считывать текст после нажатия Escape (в Entry запрещено)
                bind (obj      = self.parent_obj
                     ,bindings = ['<Return>','<KP_Enter>','<Escape>']
                     ,action   = self.close
                     )
                # We need to bind 'Return' to the widget anyway even if we have already bound this to 'parent_obj', because we need to return 'break'
                bind (obj      = self
                     ,bindings = ['<Return>','<KP_Enter>']
                     ,action   = self.close
                     )
            else:
                bind (obj      = self.parent_obj
                     ,bindings = '<Escape>'
                     ,action   = self.close
                     )
        bind (obj      = self
             ,bindings = '<Control-a>'
             ,action   = self.select_all
             )
        bind (obj      = self
             ,bindings = '<Control-v>'
             ,action   = self.insert_clipboard
             )
        bind (obj      = self
             ,bindings = '<Key>'
             ,action   = self.clear_on_key
             )
        bind (obj      = self
             ,bindings = '<Control-Alt-u>'
             ,action   = self.toggle_case
             )
        if hasattr(self.parent_obj,'type') and self.parent_obj.type == 'Toplevel':
            self.parent_obj.widget.protocol("WM_DELETE_WINDOW",self.close)

    def toggle_case(self,*args):
        text = sh.Text(text=self.selection.text()).toggle_case()
        pos1, pos2 = self.selection.get()
        self.clear_selection()
        self.insert(text=text,pos=self.cursor(),MoveTop=0)
        if pos1 and pos2:
            self.selection.reset (pos1tk     = pos1
                                 ,pos2tk     = pos2
                                 ,tag        = 'sel'
                                 ,background = 'gray'
                                 )
            self.selection.set(DeletePrevious=0,AutoScroll=0)
        else:
            sh.log.append ('TextBox.toggle_case'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        return 'break'

    def _get(self):
        try:
            return self.widget.get('1.0','end')
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append ('TextBox._get'
                          ,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def get(self,Strip=True):
        result = self._get()
        if result:
            if Strip:
                return result.strip()
            else:
                return result.strip('\n')

    def insert(self,text='text',pos='1.0',MoveTop=True):
        WidgetShared.insert(self,text=text,pos=pos)
        if MoveTop:
            self.mark_add() # Move to the beginning
        else:
            self.scroll(mark='insert')

    ''' Fix (probable) Tkinter bug(s) after pressing '<Control-v>':
        1) Fix weird scrolling
        2) Delete selected text before pasting
    '''
    def insert_clipboard(self,*args):
        self.clear_selection()
        # For some reason, 'self.insert' does not work here with 'break'
        #self.insert(text=Clipboard().paste(),MoveTop=False)
        self.widget.insert(self.cursor(),Clipboard().paste())
        return 'break'

    def select_all(self,*args):
        self.tag_add()
        self.mark_add()
        return 'break'

    def _tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        try:
            self.widget.tag_remove(tag_name,pos1tk,pos2tk)
        except tk.TclError:
            sh.log.append ('TextBox.tag_remove'
                          ,_('WARNING')
                          ,_('Failed to remove the tag %s in the widget %s in positions %s-%s!') % (tag_name,str(widget),pos1tk,pos2tk)
                          )

    def tag_remove(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        self._tag_remove(tag_name=tag_name,pos1tk=pos1tk,pos2tk=pos2tk)
        if self.tags:
            try:
                self.tags.remove(tag_name)
            except ValueError:
                # todo: Что тут не работает?
                sh.log.append ('TextBox.tag_remove'
                              ,_('DEBUG-ERROR')
                              ,_('Element "%s" has not been found in fragment "%s"!') % (tag_name,str(self.tags))
                              )

    # Tk.Entry не поддерживает тэги и метки
    def tag_add (self,tag_name='sel',pos1tk='1.0'
                ,pos2tk='end',DeletePrevious=True
                ):
        if DeletePrevious:
            self.tag_remove(tag_name)
        try:
            self.widget.tag_add(tag_name,pos1tk,pos2tk)
        except tk.TclError:
            sh.log.append ('TextBox.tag_add'
                          ,_('ERROR')
                          ,_('Failed to add tag "%s" for positions %s-%s!') % (tag_name,pos1tk,pos2tk)
                          )
        self.tags.append(tag_name)

    def tag_config (self,tag_name='sel',background=None
                   ,foreground=None,font=None):
        if background:
            try:
                self.widget.tag_config(tag_name,background=background)
            except tk.TclError:
                sh.log.append ('TextBox.tag_config'
                              ,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the background of color "%s"!') % (str(tag_name),str(background))
                              )
        if foreground:
            try:
                self.widget.tag_config(tag_name,foreground=foreground)
            except tk.TclError:
                sh.log.append ('TextBox.tag_config'
                              ,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the foreground of color "%s"!') % (str(tag_name),str(foreground))
                              )
        if font:
            try:
                self.widget.tag_config(tag_name,font=font)
            except tk.TclError:
                sh.log.append ('TextBox.tag_config'
                              ,_('ERROR')
                              ,_('Failed to configure tag "%s" to have the font "%s"!') % (str(tag_name),str(font))
                              )

    # Tk.Entry не поддерживает тэги и метки
    def mark_add(self,mark_name='insert',postk='1.0'):
        try:
            self.widget.mark_set(mark_name,postk)
            '''
            sh.log.append ('TextBox.mark_add'
                          ,_('DEBUG')
                          ,_('Mark "%s" has been inserted in position "%s".') % (mark_name,postk)
                          )
            '''
        except tk.TclError:
            sh.log.append ('TextBox.tag_add'
                          ,_('ERROR')
                          ,_('Failed to insert mark "%s" in position "%s"!') % (mark_name,postk)
                          )
        self.marks.append(mark_name)

    def mark_remove(self,mark_name='insert'):
        try:
            self.widget.mark_unset(mark_name)
            '''
            sh.log.append ('TextBox.mark_remove'
                          ,_('DEBUG')
                          ,_('Mark "%s" has been removed.') % (mark_name)
                          )
            '''
        except tk.TclError:
            sh.log.append ('TextBox.mark_remove'
                          ,_('ERROR')
                          ,_('Failed to remove mark "%s"!') % mark_name
                          )
        try:
            self.marks.remove(mark_name)
        except ValueError:
            sh.log.append ('TextBox.mark_remove'
                          ,_('ERROR')
                          ,_('Element "%s" has not been found in fragment "%s"!') % (mark_name,str(self.marks))
                          )

    def clear_text(self,pos1='1.0',pos2='end'):
        try:
            self.widget.delete(pos1,pos2)
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append ('TextBox.clear_text'
                          ,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    # Fix Tkinter limitations
    def clear_on_key(self,event=None):
        if event and event.char:
            if event.char.isspace() or event.char in sh.lat_alphabet or event.char in sh.ru_alphabet or event.char in sh.digits or event.char in sh.punc_array or event.char in sh.punc_ext_array:
                # todo: suppress excessive logging (Selection.get, TextBox.clear_selection, TextBox.cursor, Clipboard.paste, Words.no_by_tk)
                self.clear_selection()

    def clear_selection(self,*args):
        pos1tk, pos2tk = self.selection.get()
        if pos1tk and pos2tk:
            self.clear_text(pos1=pos1tk,pos2=pos2tk)
            return 'break'
        # Too frequent
        '''
        else:
            sh.log.append ('TextBox.clear_selection'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        '''

    def clear_tags(self):
        i = len(self.tags) - 1
        while i >= 0:
            self.tag_remove(self.tags[i])
            i -= 1

    def clear_marks(self):
        i = len(self.marks) - 1
        while i >= 0:
            self.mark_remove(self.marks[i])
            i -= 1

    def goto(self,GoTo=''):
        if GoTo:
            try:
                goto_pos = self.widget.search(GoTo,'1.0','end')
                self.mark_add('goto',goto_pos)
                self.mark_add('insert',goto_pos)
                self.widget.yview('goto')
            except:
                sh.log.append ('TextBox.goto'
                              ,_('ERROR')
                              ,_('Failed to shift screen to label "%s"!') % 'goto'
                              )

    # Сместить экран до позиции tkinter или до метки (тэги не работают)
    def scroll(self,mark):
        try:
            self.widget.yview(mark)
        except tk.TclError:
            sh.log.append ('TextBox.scroll'
                          ,_('WARNING')
                          ,_('Failed to shift screen to label "%s"!') % str(mark)
                          )

    # Сместить экран до позиции tkinter или до метки, если они не видны (тэги не работают)
    def autoscroll(self,mark='1.0'):
        if not self.visible(mark):
            self.scroll(mark)

    # todo: select either 'see' or 'autoscroll'
    def see(self,mark):
        if mark is None:
            sh.log.append ('TextBox.see'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )
        else:
            self.widget.see(mark)

    def title(self,text=_('Title:')):
        WidgetShared.title(self.parent_obj,text)

    def icon(self,path):
        WidgetShared.icon(self.parent_obj,path)

    def visible(self,tk_pos):
        if self.widget.bbox(tk_pos):
            return True

    def cursor(self,*args):
        try:
            self._pos = self.widget.index('insert')
            sh.log.append ('TextBox.cursor'
                          ,_('DEBUG')
                          ,_('Got position: "%s"') % str(self._pos)
                          )
        except tk.TclError:
            self._pos = '1.0'
            sh.log.append ('TextBox.cursor'
                          ,_('WARNING')
                          ,_('Cannot return a cursor position!')
                          )
        return self._pos

    def focus_set(self,*args):
        self.focus()

    def focus(self,*args):
        self.widget.focus_set()

    # Tags can be marked only after text in inserted; thus, call this procedure separately before '.show'
    def spelling(self):
        if self.words:
            self.words.sent_nos()
            result = []
            for i in range(self.words.len()):
                if not self.words.words[i].spell_ru():
                    result.append(i)
            if result:
                self.clear_tags()
                for i in range(len(result)):
                    no = self.words._no = result[i]
                    pos1tk = self.words.words[no].tf()
                    pos2tk = self.words.words[no].tl()
                    # todo: apply IGNORE_SPELLING
                    if pos1tk and pos2tk:
                        self.tag_add (tag_name       = 'spell'
                                     ,pos1tk         = pos1tk
                                     ,pos2tk         = pos2tk
                                     ,DeletePrevious = False
                                     )
                sh.log.append ('TextBox.spelling'
                              ,_('DEBUG')
                              ,_('%d tags to assign') % len(result)
                              )
                self.tag_config(tag_name='spell',background='red')
            else:
                sh.log.append ('TextBox.spelling'
                              ,_('INFO')
                              ,_('Spelling seems to be correct.')
                              )
        else:
            Message (func    = 'TextBox.spelling'
                    ,level   = _('WARNING')
                    ,message = _('Not enough input data!')
                    ,Silent  = True
                    )

    def zzz(self):
        pass



class Entry:

    def __init__(self,parent_obj,Composite=False
                ,side=None,ipadx=None,ipady=None
                ,fill=None,width=None,expand=None
                ):
        self.type       = 'Entry'
        self.Composite  = Composite
        self.state      = 'normal' # 'disabled' - отключить редактирование
        self.Save       = False
        self.parent_obj = parent_obj
        self.widget     = tk.Entry (self.parent_obj.widget
                                   ,font  = 'Sans 11'
                                   ,width = width
                                   )
        bind (obj      = self
             ,bindings = '<Control-a>'
             ,action   = self.select_all
             )
        self.widget.pack (side   = side
                         ,ipadx  = ipadx
                         ,ipady  = ipady
                         ,fill   = fill
                         ,expand = expand
                         )
        if not self.Composite:
            # Тип родительского виджета может быть любым
            if not hasattr(self.parent_obj,'close_button'):
                self.parent_obj.close_button = Button (self.parent_obj
                                                      ,text   = _('Quit')
                                                      ,hint   = _('Quit')
                                                      ,action = self.close
                                                      ,expand = 0
                                                      ,side   = 'bottom'
                                                      )
            WidgetShared.custom_buttons(self)
        self.bindings()

    # Setting ReadOnly state works only after filling text. Only tk.Text, tk.Entry and not tk.Toplevel are supported.
    def read_only(self,ReadOnly=True):
        WidgetShared.set_state(self,ReadOnly=ReadOnly)

    def bindings(self):
        if self.Composite:
            self.clear_text()
        else:
            bind (obj      = self
                 ,bindings = ['<Return>','<KP_Enter>']
                 ,action   = self.close
                 )
            bind (obj      = self
                 ,bindings = '<Escape>'
                 ,action   = self.parent_obj.close
                 )

    def show(self,*args):
        self.parent_obj.show()

    def close(self,*args):
        self.Save = True
        self.parent_obj.close()

    def _get(self):
        try:
            return self.widget.get()
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append ('Entry.clear_text'
                          ,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def get(self,Strip=False):
        result = sh.Input(val=self._get()).not_none() # None != 'None' != ''
        if Strip:
            return result.strip()
        else:
            return result.strip('\n')

    def insert(self,text='text',pos=0):
        WidgetShared.insert(self,text=text,pos=pos)

    def select_all(self,*args):
        self.widget.select_clear()
        self.widget.select_range(0,'end')
        return 'break'

    def clear_text(self,pos1=0,pos2='end'):
        try:
            self.widget.selection_clear()
            self.widget.delete(pos1,pos2)
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append ('Entry.clear_text'
                          ,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )

    def icon(self,path):
        WidgetShared.icon(self.parent_obj,path)

    def title(self,text='Title:'):
        WidgetShared.title(self.parent_obj,text)

    def focus_set(self,*args):
        self.focus()
        return 'break' # Manual Tab focus (left to right widget)

    def focus(self,*args):
        self.widget.focus_set()
        return 'break' # Manual Tab focus (left to right widget)



class Frame:

    def __init__ (self,parent_obj,expand=1
                 ,fill='both',side=None,padx=None
                 ,pady=None,ipadx=None,ipady=None
                 ,bd=None,bg=None
                 ):
        self.type       = 'Frame'
        self.parent_obj = parent_obj
        self.widget     = tk.Frame(self.parent_obj.widget,bd=bd,bg=bg)
        self.widget.pack (expand = expand
                         ,fill   = fill
                         ,side   = side
                         ,padx   = padx
                         ,pady   = pady
                         ,ipadx  = ipadx
                         ,ipady  = ipady
                         )

    def title(self,text=None):
        if text:
            self.parent_obj.title(text)
        else:
            self.parent_obj.title()

    def show(self):
        self.parent_obj.show()

    def close(self):
        self.parent_obj.close()



# todo: Нужно ли на входе ,bindings=[]?
class Button:

    def __init__ (self
                 ,parent_obj
                 ,action
                 ,hint                = None
                 ,inactive_image_path = None
                 ,active_image_path   = None
                 ,text                = 'Press me'
                 ,height              = 36
                 ,width               = 36
                 ,side                = 'left'
                 ,expand              = 0
                 ,bg                  = None
                 ,bg_focus            = None
                 ,fg                  = None
                 ,fg_focus            = None
                 ,bd                  = 0
                 ,hint_delay          = 800
                 ,hint_width          = 280
                 ,hint_height         = 40
                 ,hint_background     = '#ffffe0'
                 ,hint_direction      = 'top'
                 ,hint_border_width   = 1
                 ,hint_border_color   = 'navy'
                 ,bindings            = []
                 ,fill                = 'both'
                 ,TakeFocus           = False
                 ):
        self.Status          = False
        self.parent_obj      = parent_obj
        self.action          = action
        self.height          = height
        self.width           = width
        self.side            = side
        self.expand          = expand
        self.fill            = fill
        self.text            = text
        self._bindings       = bindings
        self.TakeFocus       = TakeFocus
        self.bd              = bd
        self.bg              = bg
        self.bg_focus        = bg_focus
        self.fg              = fg
        self.fg_focus        = fg_focus
        self.hint            = hint
        self.hint_delay      = hint_delay
        self.hint_width      = hint_width
        self.hint_height     = hint_height
        self.hint_background = hint_background
        self.hint_direction  = hint_direction
        self.side            = side
        self.inactive_image  = self.image(inactive_image_path)
        self.active_image    = self.image(active_image_path)
        
        self.gui()
        
    def bindings(self):
        bind (obj      = self
             ,bindings = ['<ButtonRelease-1>'
                         ,'<space>'
                         ,'<Return>'
                         ,'<KP_Enter>'
                         ]
             ,action   = self.click
             )
    
    def gui(self):
        if self.inactive_image:
            self.widget = tk.Button (master           = self.parent_obj.widget
                                    ,image            = self.inactive_image
                                    ,height           = self.height
                                    ,width            = self.width
                                    ,bd               = self.bd
                                    ,bg               = self.bg
                                    ,fg               = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    )
        else:
            # В большинстве случаев текстовая кнопка не требует задания высоты и ширины по умолчанию, они определяются автоматически. Также в большинстве случаев для текстовых кнопок следует использовать рамку.
            self.widget = tk.Button (master           = self.parent_obj.widget
                                    ,bd               = 1
                                    ,bg               = self.bg
                                    ,fg               = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    )
        self.title(button_text=self.text)
        if self.hint:
            if self._bindings:
                self.hint_extended = self.hint + '\n' + str(self._bindings).replace('[','').replace(']','').replace('<','').replace('>','').replace("'",'')
            else:
                self.hint_extended = self.hint
            self.tip = ToolTip (button          = self.widget
                               ,text            = self.hint_extended
                               ,hint_delay      = self.hint_delay
                               ,hint_width      = self.hint_width
                               ,hint_height     = self.hint_height
                               ,hint_background = self.hint_background
                               ,hint_direction  = self.hint_direction
                               ,button_side     = self.side
                               )
        self.show()
        self.bindings()
        if self.TakeFocus:
            self.widget.focus_set()

    def title(self,button_text='Press me'):
        if button_text:
            self.widget.config(text=button_text)

    def image(self,button_image_path=None):
        # Без 'file=' не сработает!
        if button_image_path and os.path.exists(button_image_path):
            button_image = tk.PhotoImage (file   = button_image_path
                                         ,master = self.parent_obj.widget
                                         ,width  = self.width
                                         ,height = self.height
                                         )
        else:
            button_image = None
        return button_image

    def click(self,*args):
        if len(args) > 0:
            self.action(args)
        else:
            self.action()

    def active(self):
        if not self.Status:
            self.Status = True
            if self.active_image:
                self.widget.config(image=self.active_image)
                self.widget.flag_img = self.active_image
            #self.widget.config(text="I'm Active")

    def inactive(self):
        if self.Status:
            self.Status = False
            if self.inactive_image:
                self.widget.config(image=self.inactive_image)
                self.widget.flag_img = self.inactive_image
            #self.widget.config(text="I'm Inactive")

    def show(self):
        self.widget.pack (expand = self.expand
                         ,side   = self.side
                         ,fill   = self.fill
                         )

    def close(self):
        self.widget.pack_forget()

    def focus(self,*args):
        self.widget.focus_set()
        



# Всплывающие подсказки для кнопок
# see also 'calltips'
# based on idlelib.ToolTip
class ToolTipBase:

    def __init__(self,button):
        self.button = button
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self._id1 = self.button.bind("<Enter>",self.enter)
        self._id2 = self.button.bind("<Leave>",self.leave)
        self._id3 = self.button.bind("<ButtonPress>",self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.button.after(self.hint_delay,self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.button.after_cancel(id)

    def showtip(self):
        if self.tipwindow:
            return
        # The tip window must be completely outside the button; otherwise when the mouse enters the tip window we get a leave event and it disappears, and then we get an enter event and it reappears, and so on forever :-(
        # Координаты подсказки рассчитываются так, чтобы по горизонтали подсказка и кнопка, несмотря на разные размеры, совпадали бы центрами.
        x = self.button.winfo_rootx() + self.button.winfo_width()/2 - self.hint_width/2
        if self.hint_direction == 'bottom':
            y = self.button.winfo_rooty() + self.button.winfo_height() + 1
        elif self.hint_direction == 'top':
            y = self.button.winfo_rooty() - self.hint_height - 1
        else:
            Message (func    = 'ToolTipBase.showtip'
                    ,level   = _('ERROR')
                    ,message = _('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(self.hint_direction),'top, bottom')
                    )
        self.tipwindow = tw = tk.Toplevel(self.button)
        tw.wm_overrideredirect(1)
        # "+%d+%d" is not enough!
        sh.log.append ('ToolTipBase.showtip'
                      ,_('INFO')
                      ,_('Changing "%s" widget geometry to "%dx%d+%d+%d"') % ('tw',self.hint_width,self.hint_height,x,y)
                      )
        tw.wm_geometry("%dx%d+%d+%d" % (self.hint_width,self.hint_height,x, y))
        self.showcontents()

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()



class ToolTip(ToolTipBase):

    def __init__(self,button,text='Sample text',hint_delay=800
                ,hint_width=280,hint_height=40,hint_background='#ffffe0'
                ,hint_direction='top',hint_border_width=1
                ,hint_border_color='navy',button_side='left'):
        self.text              = text
        self.hint_delay        = hint_delay
        self.hint_direction    = hint_direction
        self.hint_background   = hint_background
        self.hint_border_color = hint_border_color
        self.hint_height       = hint_height
        self.hint_width        = hint_width
        self.hint_border_width = hint_border_width
        self.button_side       = button_side
        ToolTipBase.__init__(self,button)

    def showcontents(self):
        frame = tk.Frame (self.tipwindow
                         ,background  = self.hint_border_color
                         ,borderwidth = self.hint_border_width
                         )
        frame.pack()
        self.label = tk.Label (frame
                              ,text       = self.text
                              ,justify    = 'center'
                              ,background = self.hint_background
                              ,width      = self.hint_width
                              ,height     = self.hint_height
                              )
        self.label.pack() #expand=1,fill='x'



class ListBox:
    # todo: configure a font
    def __init__(self
                ,parent_obj
                ,Multiple        = False
                ,lst             = []
                ,title           = 'Title:'
                ,icon            = None
                ,SelectionCloses = True
                ,Composite       = False
                ,SingleClick     = True
                ,user_function   = None
                ,side            = None
                ,Scrollbar       = True
                ,expand          = 1
                ,fill            = 'both'
                ):
        self.state = 'normal' # See 'WidgetShared'
        # 'user_function': A user-defined function that is run when pressing Up/Down arrow keys and LMB. There is a problem binding it externally, so we bind it here.
        self.parent_obj      = parent_obj
        self.Multiple        = Multiple
        self.expand          = expand
        self.Composite       = Composite
        self.Scrollbar       = Scrollbar
        self.side            = side
        self._fill           = fill
        self.user_function   = user_function
        self.SelectionCloses = SelectionCloses
        self.SingleClick     = SingleClick
        self._icon           = icon
        self.gui()
        self.reset(lst=lst,title=title)

    def bindings(self):
        if self.user_function:
            # Binding just to '<Button-1>' does not work. We do not need binding Return/space/etc. because the function will be called each time the selection is changed. However, we still need to bind Up/Down.
            bind (obj      = self
                 ,bindings = '<<ListboxSelect>>'
                 ,action   = self.user_function
                 )
        elif self.SelectionCloses:
            # todo: test <KP_Enter> in Windows
            bind (obj      = self
                 ,bindings = ['<Return>','<KP_Enter>','<Double-Button-1>']
                 ,action   = self.close
                 )
            if self.SingleClick and not self.Multiple:
                # Binding to '<Button-1>' does not allow to select an entry before closing
                bind (obj      = self
                     ,bindings = '<<ListboxSelect>>'
                     ,action   = self.close
                     )
        if not self.Multiple:
            bind (obj      = self
                 ,bindings = '<Up>'
                 ,action   = self.move_up
                 )
            bind(self,'<Down>',self.move_down)
        if not self.Composite: # todo: test
            bind (obj      = self
                 ,bindings = ['<Escape>','<Control-q>','<Control-w>']
                 ,action   = self.interrupt
                 )
            if hasattr(self.parent_obj,'type') and self.parent_obj.type == 'Toplevel':
                self.parent_obj.widget.protocol("WM_DELETE_WINDOW",self.interrupt)

    def gui(self):
        self._scroll()
        if self.Multiple:
            self.widget = tk.Listbox (self.parent_obj.widget
                                     ,exportselection = 0
                                     ,selectmode      = tk.MULTIPLE
                                     )
        else:
            self.widget = tk.Listbox (self.parent_obj.widget
                                     ,exportselection = 0
                                     ,selectmode      = tk.SINGLE
                                     )
        self.widget.pack(expand=self.expand,fill=self._fill,side=self.side)
        self._resize()
        self._scroll_config()
        self.icon(path=self._icon)
        self.widget.focus_set()
        self.bindings()
        if not self.Composite:
            # Тип родительского виджета может быть любым
            if not hasattr(self.parent_obj,'close_button'):
                self.parent_obj.close_button = Button (
                    parent_obj = self.parent_obj
                   ,text       = _('Quit')
                   ,hint       = _('Quit')
                   ,action     = self.close
                   ,expand     = 0
                   ,side       = 'bottom'
                                                      )
            WidgetShared.custom_buttons(self)

    def _scroll(self):
        if self.Scrollbar:
            self.scrollbar = tk.Scrollbar(self.parent_obj.widget)
            self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

    def _scroll_config(self):
        if self.Scrollbar:
            self.scrollbar.config(command=self.widget.yview)
            self.widget.config(yscrollcommand=self.scrollbar.set)

    def _resize(self):
        # Autofit to contents
        self.widget.config(width=0)
        self.widget.config(height=0)

    def activate(self):
        self.widget.activate(self._index)

    def clear(self):
        self.widget.delete(0,tk.END)

    def clear_selection(self):
        self.widget.selection_clear(0,tk.END)

    def reset(self,lst=[],title=None):
        self._title = title
        self.clear()
        if lst is None:
            self.lst = []
        else:
            self.lst = list(lst)
        self.title(text=self._title)
        self.fill()
        self._resize()
        # Do not set '_index' to 0, because we need 'self.interrupt'. Other functions use 'self.index()', which returns an actual value.
        self._get, self._index = '', None
        self.select()

    def select(self):
        self.clear_selection()
        # Use an index changed with keyboard arrows. If it is not set, use current index (returned by 'self.index()').
        if self._index is None:
            self.index()
        if self._index is None:
            Message (func    = 'ListBox.select'
                    ,level   = _('ERROR')
                    ,message = _('Empty input is not allowed!')
                    )
        else:
            self._select()

    def _select(self):
        self.widget.selection_set(self._index)
        self.widget.see(self._index)

    def set(self,item):
        if item:
            if item in self.lst:
                self._index = self.lst.index(item)
                self._select()
            else:
                Message ('ListBox.set'
                        ,_('ERROR')
                        ,_('Item "%s" is not in list!') % str(item)
                        )
        else:
            sh.log.append ('ListBox.set'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def show(self,*args):
        self.parent_obj.show()

    def interrupt(self,*args):
        # Do not set '_index' to 0, because we need 'self.interrupt'. Other functions use 'self.index()', which returns an actual value.
        self._get, self._index = '', None
        self.parent_obj.close()

    def close(self,*args):
        self.index()
        self.get()
        self.parent_obj.close()

    def fill(self):
        for i in range(len(self.lst)):
            self.widget.insert(tk.END,self.lst[i])

    def title(self,text=None):
        if text:
            self.parent_obj.title(text=text)

    def icon(self,path=None):
        if path:
            WidgetShared.icon(self.parent_obj,path)

    # Read 'self._index' instead of calling this because we need 0 in case of 'self.interrupt', and this always returns an actual value
    def index(self):
        selection = self.widget.curselection()
        if selection and len(selection) > 0:
            # note: selection[0] is a number in Python 3.4, however, in older interpreters and builds based on them it is a string. In order to preserve compatibility, we convert it to a number.
            self._index = int(selection[0])
        else:
            self._index = 0
        return self._index

    def index_add(self):
        if self.index() < len(self.lst) - 1:
            self._index += 1
        else:
            self._index = 0

    def index_subtract(self):
        if self.index() > 0:
            self._index -= 1
        else:
            self._index = len(self.lst) - 1

    # Read 'self._get' instead of calling this because we need '' in case of 'self.interrupt', and this always returns an actual value
    def get(self):
        result = [self.widget.get(idx) for idx in self.widget.curselection()]
        if self.Multiple:
            self._get = result
        elif len(result) > 0:
            self._get = result[0]
        return self._get

    def move_down(self,*args):
        self.index_add()
        self.select()
        if self.user_function:
            self.user_function()

    def move_up(self,*args):
        self.index_subtract()
        self.select()
        if self.user_function:
            self.user_function()



class OptionMenu:

    ''' tk.OptionMenu will convert integers to strings,
    but we better do this here to avoid problems with
    iterating ("in requires int as the left operand")
    later (this happens when we pass a sequence of 
    chars instead of a list of strings).
    '''
    def __init__ (self
                 ,parent_obj
                 ,items      = ('1','2','3','4','5')
                 ,side       = 'left'
                 ,anchor     = 'center'
                 ,command    = None
                 ,takefocus  = 1
                 ,default    = None
                 ):
        self.parent_obj = parent_obj
        self.items      = items
        self.command    = command
        self.default    = default
        self.choice     = None
        self.index      = 0
        self.var        = tk.StringVar(self.parent_obj.widget)
        # An error is thrown if 'items' is ()
        if not self.items:
            self.items = ('1','2','3','4','5')
        self.widget    = tk.OptionMenu (self.parent_obj.widget
                                       ,self.var
                                       ,*self.items
                                       ,command = self.trigger
                                       )
        self.widget.pack(side=side,anchor=anchor)
        self.widget.configure(takefocus=takefocus) # Must be 1/True to be operational from keyboard
        self.default_set()

    def trigger(self,*args):
        self._get()
        if self.command:
            self.command()

    def _default_set(self):
        if len(self.items) > 0:
            self.var.set(self.items[0])
            # Return a default value instead of 'None' if there was no interaction with the widget
            self.choice = self.items[0]
            self.index  = 0

    def default_set(self):
        if self.default is None:
            self._default_set()
        else:
            if self.default in self.items:
                self.var.set(self.default)
                # Return a default value instead of 'None' if there was no interaction with the widget
                self.choice = self.default
                self.index  = self.items.index(self.choice)
            else:
                Message ('OptionMenu.default_set'
                        ,_('ERROR')
                        ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(self.default),';'.join(self.items))
                        )
                self._default_set()

    def set(self,item,*args):
        if item in self.items:
            self.var.set(item)
            self.choice = item
            self.index  = self.items.index(self.choice)
        else:
            Message (func    = 'OptionMenu.set'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data: "%s"') % str(item)
                    )

    def fill(self):
        self.widget['menu'].delete(0,'end')
        for item in self.items:
            self.widget['menu'].add_command (label   = item
                                            ,command = lambda v=self.var
                                            ,l       = item:v.set(l)
                                            )

    def reset(self,items=('1','2','3','4','5'),default=None):
        self.items = items
        # An error is thrown if 'items' is ()
        if not self.items:
            self.items = ('1','2','3','4','5')
        self.fill()
        if default is None:
            if self.choice in self.items:
                default = self.choice
        self.default = default
        self.default_set()
        if len(items) == 1:
            self.widget.config(state='disabled')
        else:
            self.widget.config(state='normal')

    def _get(self,*args): # Auto updated (after selecting an item)
        self.choice = self.var.get()
        # 'OptionMenu' always returns a string
        if self.choice not in self.items:
            self.choice = sh.Input (func_title = 'OptionMenu._get'
                                   ,val        = self.choice
                                   ).integer()
        try:
            self.index = self.items.index(self.choice)
        except ValueError:
            Message (func    = 'OptionMenu._get'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data: "%s"') % str(self.choice)
                    )

    def set_prev(self,*args):
        if self.index == 0:
            self.index = len(self.items) - 1
        else:
            self.index -= 1
        self.var.set(self.items[self.index])

    def set_next(self,*args):
        if self.index == len(self.items) - 1:
            self.index = 0
        else:
            self.index += 1
        self.var.set(self.items[self.index])

    def focus(self,*args):
        self.widget.focus_set()



''' Usage:
    bind(h_txt.widget,'<ButtonRelease-1>',action)

def action(*args):
    h_selection.get() # Refresh coordinates (or set h_selection._pos1tk, h_selection._pos2tk manually)
    h_selection.set()
'''
class Selection: # Selecting words only

    def __init__(self,h_widget,words=None):
        self.h_widget = h_widget
        self.reset_logic(words=words)
        self.reset_data()

    def reset (self
              ,mode       = 'data'
              ,words      = None
              ,pos1tk     = None
              ,pos2tk     = None
              ,background = None
              ,foreground = None
              ,tag        = 'tag'
              ):
        if mode == 'data':
            self.reset_data (pos1tk     = pos1tk
                            ,pos2tk     = pos2tk
                            ,background = background
                            ,foreground = foreground
                            ,tag        = tag
                            )
        else:
            self.reset_logic(words=words)

    def reset_logic(self,words):
        self.words = words

    def reset_data (self
                   ,pos1tk     = None
                   ,pos2tk     = None
                   ,background = None
                   ,foreground = None
                   ,tag        = 'tag'
                   ):
        self._pos1tk = pos1tk
        self._pos2tk = pos2tk
        self._text = ''
        self._bg = background
        self._fg = foreground
        if not self._bg and not self._fg:
            self._bg = 'cyan'
        self._tag = tag

    def clear(self,tag_name='sel',pos1tk='1.0',pos2tk='end'):
        self.h_widget._tag_remove (tag_name = tag_name
                                  ,pos1tk   = pos1tk
                                  ,pos2tk   = pos2tk
                                  )

    def pos1tk(self):
        if self._pos1tk is None:
            self.get()
        return self._pos1tk

    def pos2tk(self):
        if self._pos2tk is None:
            self.get()
        return self._pos2tk

    def get(self,*args):
        try:
            self._pos1tk = self.h_widget.widget.index('sel.first')
            self._pos2tk = self.h_widget.widget.index('sel.last')
        except tk.TclError:
            self._pos1tk, self._pos2tk = None, None
            # Too frequent
            '''
            sh.log.append ('Selection.get'
                          ,_('WARNING')
                          ,_('Nothing is selected in window %d, therefore, it is not possible to return coordinates!') % 1
                          )
            '''
        # Too frequent
        '''
        sh.log.append ('Selection.get'
                      ,_('DEBUG')
                      ,str((self._pos1tk,self._pos2tk))
                      )
        '''
        return(self._pos1tk,self._pos2tk)

    def text(self):
        try:
            self._text = self.h_widget.widget.get('sel.first','sel.last').replace('\r','').replace('\n','')
        except tk.TclError:
            self._text = ''
            sh.log.append ('Selection.text'
                          ,_('ERROR')
                          ,_('Failed to return selection in the Tkinter widget!')
                          )
        return self._text

    def cursor(self):
        return self.h_widget.cursor()

    def select_all(self):
        self.h_widget.select_all()

    def set(self,DeletePrevious=True,AutoScroll=True):
        if self.pos1tk() and self.pos2tk():
            mark = self._pos1tk
            self.h_widget.tag_add (pos1tk         = self._pos1tk
                                  ,pos2tk         = self._pos2tk
                                  ,tag_name       = self._tag
                                  ,DeletePrevious = DeletePrevious
                                  )
        else:
            # Just need to return something w/o warnings
            _cursor = mark = self.cursor()
            self.h_widget.tag_add (tag_name       = self._tag
                                  ,pos1tk         = _cursor
                                  ,pos2tk         = _cursor
                                  ,DeletePrevious = DeletePrevious
                                  )
        if self._bg:
            # This is not necessary for 'sel' tag which is hardcoded for selection and permanently colored with gray. A 'background' attribute cannot be changed for a 'sel' tag.
            self.h_widget.widget.tag_config (tagName    = self._tag
                                            ,background = self._bg
                                            )
        elif self._fg:
            self.h_widget.widget.tag_config (tagName    = self._tag
                                            ,foreground = self._fg
                                            )
        if AutoScroll: # todo: select either 'see' or 'autoscroll'
            #self.h_widget.see(mark)
            self.h_widget.autoscroll(mark)



# A modified mclient class
class SymbolMap:

    def __init__(self,parent_obj):
        self.symbol     = 'EMPTY'
        self.parent_obj = parent_obj
        self.gui()
        self.bindings()
        
    def gui(self):
        self.obj    = Top(self.parent_obj)
        self.widget = self.obj.widget
        self.frame  = Frame(self.obj,expand=1)
        self.obj.title(_('Paste a special symbol'))
        for i in range(len(sh.globs['var']['spec_syms'])):
            if i % 10 == 0:
                self.frame = Frame(self.obj,expand=1)
            # lambda сработает правильно только при моментальной упаковке, которая не поддерживается create_button (моментальная упаковка возвращает None вместо виджета), поэтому не используем эту функцию. По этой же причине нельзя привязать кнопкам '<Return>' и '<KP_Enter>', сработают только встроенные '<space>' и '<ButtonRelease-1>'.
            # width и height нужны для Windows
            self.button = tk.Button (self.frame.widget
                                    ,text=sh.globs['var']['spec_syms'][i]
                                    ,command=lambda i=i:self.set(sh.globs['var']['spec_syms'][i])
                                    ,width=2,height=2).pack(side='left',expand=1)
        self.close()

    def bindings(self):
        bind (obj      = self.obj
             ,bindings = ['<Escape>','<Control-q>','<Control-w>']
             ,action   = self.close
             )
    
    def set(self,sym,*args):
        self.symbol = sym
        self.close()

    def get(self,*args):
        self.show()
        return self.symbol

    def show(self,*args):
        self.obj.show()

    def close(self,*args):
        self.obj.close()



# Window behavior is not uniform through different platforms or even through different Windows versions, so we bypass Tkinter's commands here
class Geometry: # Requires sh.oss, objs

    def __init__(self,parent_obj=None,title=None,hwnd=None):
        self.parent_obj = parent_obj
        self._title = title
        self._hwnd = hwnd
        self._geom = None

    def update(self):
        objs.root().widget.update_idletasks()

    def save(self):
        if self.parent_obj:
            self.update()
            self._geom = self.parent_obj.widget.geometry()
            sh.log.append ('Geometry.save'
                          ,_('INFO')
                          ,_('Saved geometry: %s') % self._geom
                          )
        else:
            Message (func    = 'Geometry.save'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def restore(self):
        if self.parent_obj:
            if self._geom:
                sh.log.append ('Geometry.restore'
                              ,_('INFO')
                              ,_('Restoring geometry: %s') % self._geom
                              )
                self.parent_obj.widget.geometry(self._geom)
            else:
                Message (func    = 'Geometry.update'
                        ,level   = _('WARNING')
                        ,message = _('Failed to restore geometry!')
                        )
        else:
            Message (func    = 'Geometry.restore'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def foreground(self,*args):
        if sh.oss.win():
            if self.hwnd():
                try:
                    win32gui.SetForegroundWindow(self._hwnd)
                except: # 'pywintypes.error', but needs to import this for some reason
                    # In Windows 'Message' can be raised foreground, so we just log it
                    sh.log.append ('Geometry.foreground'
                                  ,_('ERROR')
                                  ,_('Failed to change window properties!')
                                  )
            else:
                Message (func    = 'Geometry.foreground'
                        ,level   = _('ERROR')
                        ,message = _('Wrong input data!')
                        )
        elif self.parent_obj:
            self.parent_obj.widget.lift()
        else:
            Message (func    = 'Geometry.foreground'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def minimize(self,*args):
        if self.parent_obj:
            ''' # Does not always work
            if sh.oss.win():
                win32gui.ShowWindow(self.hwnd(),win32con.SW_MINIMIZE)
            else:
            '''
            self.parent_obj.widget.iconify()
        else:
            Message (func    = 'Geometry.minimize'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def maximize(self,*args):
        if sh.oss.win():
            #win32gui.ShowWindow(self.hwnd(),win32con.SW_MAXIMIZE)
            self.parent_obj.widget.wm_state(newstate='zoomed')
        elif self.parent_obj:
            self.parent_obj.widget.wm_attributes('-zoomed',True)
        else:
            Message (func    = 'Geometry.maximize'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def focus(self,*args):
        if sh.oss.win():
            win32gui.SetActiveWindow(self.hwnd())
        elif self.parent_obj:
            self.parent_obj.widget.focus_set()
        else:
            Message (func    = 'Geometry.focus'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def lift(self,*args):
        if self.parent_obj:
            self.parent_obj.widget.lift()
        else:
            Message (func    = 'Geometry.list'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def _activate(self):
        if self.parent_obj:
            self.parent_obj.widget.deiconify()
            #self.parent_obj.widget.focus_set()
            self.parent_obj.widget.lift()
        else:
            Message (func    = 'Geometry._activate'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )

    def activate(self,MouseClicked=False,*args):
        self._activate()
        if sh.oss.win():
            # todo: learn how to properly import modules
            import ctypes
            self.parent_obj.widget.wm_attributes('-topmost',1)
            self.parent_obj.widget.wm_attributes('-topmost',0)
            # Иначе нажатие кнопки будет вызывать переход по ссылке там, где это не надо
            if MouseClicked:
                # Уродливый хак, но иначе никак не поставить фокус на виджет (в Linux/Windows XP обходимся без этого, в Windows 7/8 - необходимо)
                # Cимулируем нажатие кнопки мыши
                ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0) # left mouse button down
                ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0) # left mouse button up

    def hwnd(self,*args):
        if not self._hwnd:
            if self._title:
                try:
                    self._hwnd = win32gui.FindWindow(None,self._title)
                except win32ui.error:
                    Message (func    = 'Geometry.hwnd'
                            ,level   = _('ERROR')
                            ,message = _('Failed to get the window handle!')
                            )
            else:
                Message (func    = 'Geometry.hwnd'
                        ,level   = _('ERROR')
                        ,message = _('Not enough input data!')
                        )
        return self._hwnd

    def set(self,arg='800x600'):
        self._geom = arg
        self.restore()



class WaitBox:

    def __init__(self,parent_obj):
        self.type = 'WaitBox'
        self.parent_obj = parent_obj
        self._func = self._title = self._args = self._message = None
        self.obj = Top (parent_obj = self.parent_obj
                       ,Maximize   = False
                       ,AutoCenter = True
                       )
        # todo: fix centering in Top.center() when Lock=False
        #self.obj.center(Force=1)
        self.widget = self.obj.widget
        self.widget.geometry('300x150')
        self.label = tk.Label(self.widget,text=_('Please wait...'))
        self.label.pack(expand=True)
        self.close()

    def reset (self,func_title=None,func=None
              ,args=None,message=None
              ): # Use tuple for 'args' to pass multiple arguments
        self._func    = func
        self._title   = func_title
        self._args    = args
        self._message = message
        self.title()
        self.message()

    def run(self):
        self.show()
        if self._func:
            if self._args:
                func_res = self._func(self._args)
            else:
                func_res = self._func()
        else:
            Message (func    = 'WaitBox.run'
                    ,level   = _('ERROR')
                    ,message = _('Wrong input data!')
                    )
        self.close()
        return func_res

    def show(self):
        self.obj.show(Lock=False)
        self.obj.center(Force=1) # cur

    def close(self):
        self.obj.close()

    def title(self,text=None):
        if text:
            self._title = text
        if self._title:
            self.obj.title(self._title)

    def message(self,message=None):
        if message:
            self._message = message
        if self._message:
            self.label.config(text=self._message + '\n\n' + _('Please wait...'))
        else:
            self.label.config(text=_('Please wait...'))



class Label:

    # Use fill='both' with 'expand=1', otherwise, 'expand' does not work
    def __init__(self,parent_obj,text='Text:'
                ,font='Sans 11',side=None,fill=None
                ,expand=False,ipadx=None,ipady=None
                ,image=None,fg=None,bg=None
                ): # 'Top' and 'Root' (the last only with 'wait_window()')
        self.type       = 'Label'
        self.parent_obj = parent_obj
        self.side       = side
        self.fill       = fill
        self.expand     = expand
        self._text      = text
        self._font      = font
        self.ipadx      = ipadx
        self.ipady      = ipady
        self.image      = image
        self.bg         = bg
        self.fg         = fg
        self.gui()
        self.close()

    def gui(self):
        self.widget = tk.Label (master = self.parent_obj.widget
                               ,image  = self.image
                               ,bg     = self.bg
                               ,fg     = self.fg
                               )
        self.text()
        self.font()
        self.widget.pack (side   = self.side
                         ,fill   = self.fill
                         ,expand = self.expand
                         ,ipadx  = self.ipadx
                         ,ipady  = self.ipady
                         )

    def text(self,arg=None):
        if arg:
            self._text = arg
        self.widget.config(text=self._text)

    def font(self,arg=None):
        if arg:
            self._font = arg
        try:
            self.widget.config(font=self._font)
        except tk.TclError:
            Message (func    = 'Label.font'
                    ,level   = _('ERROR')
                    ,message = _('Wrong font: "%s"!') % str(self._font)
                    )
            self._font = 'Sans 11'

    def show(self):
        self.parent_obj.show()

    def close(self):
        self.parent_obj.close()

    def title(self,text='Title:'):
        self.parent_obj.title(text=text)



class CheckBox:

    # note: For some reason, CheckBox that should be Active must be assigned to a variable (var = CheckBox(parent_obj,Active=1))
    def __init__ (self,parent_obj,Active=False
                 ,side=None,action=None
                 ):
        self.parent_obj = parent_obj
        self.side = side
        self.action = action
        self.status = tk.IntVar()
        self.gui()
        self.reset(Active=Active)

    def reset(self,Active=False):
        if Active:
            self.enable()
        else:
            self.disable()

    def gui(self):
        self.widget = tk.Checkbutton (self.parent_obj.widget
                                     ,variable = self.status
                                     ,command  = self.action
                                     )
        self.widget.pack(side=self.side)
        self.obj = self

    def show(self):
        self.parent_obj.show()

    def close(self):
        self.parent_obj.close()

    def focus(self,*args):
        self.widget.focus_set()

    def enable(self):
        self.widget.select()

    def disable(self):
        self.widget.deselect()

    def get(self,*args):
        return self.status.get()

    def toggle(self,*args):
        self.widget.toggle()



class Message:

    def __init__ (self,func='MAIN',level=_('WARNING')
                 ,message=_('Message'),Silent=False
                 ):
        self.Success = True
        self.Yes     = False
        self.func    = func
        self.message = message
        self.level   = level
        self.Silent  = Silent
        if not self.func or not self.message:
            self.Success = False
            sh.log.append ('Message.__init__'
                          ,_('ERROR')
                          ,_('Not enough input data!')
                          )
        if self.level == _('INFO'):
            self.info()
        elif self.level == _('WARNING'):
            self.warning()
        elif self.level in (_('ERROR'),_('CRITICAL')):
            self.error()
        elif self.level == _('QUESTION'):
            self.question()
        else:
            sh.log.append ('Message.__init__'
                          ,_('ERROR')
                          ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(self.level)
                          ,_('INFO') + ', ' + _('WARNING') + ', ' + _('ERROR') + ', ' + _('QUESTION'))
                          )

    def error(self):
        if self.Success:
            if not self.Silent:
                objs.error().reset (title = self.func + ':'
                                   ,text  = self.message
                                   ).show()
            sh.log.append (func    = self.func
                          ,level   = _('ERROR')
                          ,message = self.message
                          )
        else:
            sh.log.append ('Message.error'
                          ,_('ERROR')
                          ,_('Operation has been canceled.')
                          )

    def info(self):
        if self.Success:
            if not self.Silent:
                objs.info().reset (title = self.func + ':'
                                  ,text  = self.message
                                  ).show()
            sh.log.append (func    = self.func
                          ,level   = _('INFO')
                          ,message = self.message
                          )
        else:
            sh.log.append ('Message.info'
                          ,_('INFO')
                          ,_('Operation has been canceled.')
                          )

    def question(self):
        if self.Success:
            objs.question().reset (title = self.func + ':'
                                  ,text  = self.message
                                  ).show()
            self.Yes = objs._question.Yes
            sh.log.append (func    = self.func
                          ,level   = _('QUESTION')
                          ,message = self.message
                          )
        else:
            sh.log.append ('Message.question'
                          ,_('QUESTION')
                          ,_('Operation has been canceled.')
                          )

    def warning(self):
        if self.Success:
            if not self.Silent:
                objs.warning().reset (title = self.func + ':'
                                     ,text  = self.message
                                     ).show()
            sh.log.append (func    = self.func
                          ,level   = _('WARNING')
                          ,message = self.message
                          )
        else:
            sh.log.append ('Message.warning'
                          ,_('WARNING')
                          ,_('Operation has been canceled.')
                          )



# Not using tkinter.messagebox because it blocks main GUI (even if we specify a non-root parent)
class MessageBuilder: # Requires 'constants'

    def __init__ (self,parent_obj,level
                 ,Single=True,YesNo=False
                 ): # Most often: 'root'
        self.Yes    = False
        self.YesNo  = YesNo
        self.Single = Single
        self.level  = level
        self.Lock   = False
        self.paths()
        self.parent_obj = parent_obj
        self.obj        = Top(parent_obj=self.parent_obj)
        self.widget     = self.obj.widget
        self.icon()
        self.frames()
        self.picture()
        self.txt = TextBox (parent_obj = self.top_right
                           ,Composite  = True
                           )
        self.buttons()
        self.bindings()
        Geometry(parent_obj=self.obj).set('400x250')
        self.close()

    def bindings(self):
        bind (obj      = self
             ,bindings = ['<Control-q>','<Control-w>','<Escape>']
             ,action   = self.close_no
             )
        if hasattr(self.parent_obj,'type') and self.parent_obj.type == 'Toplevel':
            self.widget.protocol("WM_DELETE_WINDOW",self.close)

    def paths(self):
        if self.level == _('WARNING'):
            self.path = sh.objs.pdir().add('resources','warning.gif')
        elif self.level == _('INFO'):
            self.path = sh.objs.pdir().add('resources','info.gif')
        elif self.level == _('QUESTION'):
            self.path = sh.objs.pdir().add('resources','question.gif')
        elif self.level == _('ERROR'):
            self.path = sh.objs.pdir().add('resources','error.gif')
        else:
            sh.log.append('MessageBuilder.paths'
                         ,_('ERROR')
                         ,_('An unknown mode "%s"!\n\nThe following modes are supported: "%s".') % (str(self.path),', '.join([_('WARNING'),_('ERROR'),_('QUESTION'),_('INFO')]))
                         )

    def icon(self,path=None):
        if path:
            self.obj.icon(path=path)
        else:
            self.obj.icon(path=self.path)

    def frames(self):
        frame = Frame (parent_obj = self.obj
                      ,expand     = 1
                      )
        top = Frame (parent_obj = frame
                    ,expand     = 1
                    ,side       = 'top'
                    )
        bottom = Frame (parent_obj = frame
                       ,expand     = 0
                       ,side       = 'bottom'
                       )
        self.top_left = Frame (parent_obj = top
                              ,expand     = 0
                              ,side       = 'left'
                              )
        self.top_right = Frame (parent_obj = top
                               ,expand     = 1
                               ,side       = 'right'
                               )
        self.bottom_left = Frame (parent_obj = bottom
                                 ,expand     = 1
                                 ,side       = 'left'
                                 )
        self.bottom_right = Frame (parent_obj = bottom
                                  ,expand     = 1
                                  ,side       = 'right'
                                  )

    def buttons(self):
        if self.YesNo or self.level == _('QUESTION'):
            YesName = _('Yes')
            NoName  = _('No')
        else:
            YesName = 'OK'
            NoName  = _('Cancel')
        if self.Single and self.level != _('QUESTION'):
            Button (parent_obj = self.bottom_left
                   ,action     = self.close_yes
                   ,hint       = _('Accept and close')
                   ,text       = YesName
                   ,TakeFocus  = 1
                   ,side       = 'right'
                   )
        else:
            Button (parent_obj = self.bottom_left
                   ,action     = self.close_no
                   ,hint       = _('Reject and close')
                   ,text       = NoName
                   ,side       = 'left'
                   )
            Button (parent_obj = self.bottom_right
                   ,action     = self.close_yes
                   ,hint       = _('Accept and close')
                   ,text       = YesName
                   ,TakeFocus  = 1
                   ,side       = 'right'
                   )

    def title(self,text=None):
        if not text:
            text = _('Title:')
        self.obj.title(text=text)

    def update(self,text=_('Message')):
        # todo: Control-c does not work with 'ReadOnly=True'
        # Otherwise, updating text will not work
        #self.txt.read_only(ReadOnly=False)
        self.txt.clear_text()
        self.txt.insert(text=text)
        #self.txt.read_only(ReadOnly=True)

    def reset(self,text=_('Message'),title=_('Title:'),icon=None):
        self.update(text=text)
        self.title(text=title)
        self.icon(path=icon)
        return self

    def show(self,Lock=False,*args):
        self.obj.show()

    def close(self,*args):
        self.obj.close()

    def close_yes(self,*args):
        self.Yes = True
        self.close()

    def close_no(self,*args):
        self.Yes = False
        self.close()

    def picture(self,*args):
        if os.path.exists(self.path):
            # We need to assign self.variable to Label, otherwise, it gets destroyed
            # Without explicitly indicating 'master', we get "image pyimage1 doesn't exist"
            self.label = Label (parent_obj = self.top_left
                               ,image      = tk.PhotoImage(master = self.top_left.widget
                                                          ,file   = self.path
                                                          )
                               )
        else:
            sh.log.append ('MessageBuilder.picture'
                          ,_('ERROR')
                          ,_('Picture "%s" was not found!') % self.path
                          )



class Clipboard: # Requires 'objs'

    def __init__(self,Silent=False):
        self.Silent = Silent

    def copy(self,text,CopyEmpty=True):
        if text or CopyEmpty:
            text = str(sh.Input(val=text).not_none())
            objs.root().widget.clipboard_clear()
            objs._root.widget.clipboard_append(text)
            try:
                objs._root.widget.clipboard_clear()
                objs._root.widget.clipboard_append(text)
            except tk.TclError:
                # todo: Show a window to manually copy from
                Message (func    = 'Clipboard.copy'
                        ,level   = _('ERROR')
                        ,message = _('A clipboard error has occurred!')
                        ,Silent  = self.Silent
                        )
            except tk._tkinter.TclError:
                # Do not use GUI
                sh.log.append ('Clipboard.copy'
                              ,_('WARNING')
                              ,_('The parent has already been destroyed.')
                              )
            except:
                sh.log.append ('Clipboard.copy'
                              ,_('ERROR')
                              ,_('An unknown error has occurred.')
                              )
            sh.log.append('Clipboard.copy',_('DEBUG'),text)
        else:
            sh.log.append ('Clipboard.copy'
                          ,_('WARNING')
                          ,_('Empty input is not allowed!')
                          )

    def paste(self):
        text = ''
        try:
            text = str(objs.root().widget.clipboard_get())
        except tk.TclError:
            Message (func    = 'Clipboard.paste'
                    ,level   = _('ERROR')
                    ,message = _('Failed to paste the clipboard contents!')
                    ,Silent  = self.Silent
                    )
        except tk._tkinter.TclError:
            # Do not use GUI
            sh.log.append ('Clipboard.paste'
                          ,_('WARNING')
                          ,_('The parent has already been destroyed.')
                          )
        except:
            sh.log.append ('Clipboard.paste'
                          ,_('ERROR')
                          ,_('An unknown error has occurred.')
                          )
        # Further actions: strip, delete double line breaks
        sh.log.append ('Clipboard.paste'
                      ,_('DEBUG')
                      ,text
                      )
        return text



class Canvas:
    
    def __init__(self,parent_obj,expand=True
                ,side=None,scrollregion=None
                ,width=None,height=None,fill='both'
                ):
        self.parent_obj   = parent_obj
        self.expand       = expand
        self.side         = side
        self.scrollregion = scrollregion
        self.width        = width
        self.height       = height
        self.fill         = fill
        self.gui()
        
    def gui(self):
        self.widget = tk.Canvas (master       = self.parent_obj.widget
                                ,scrollregion = self.scrollregion
                                ,width        = self.width
                                ,height       = self.height
                                )
        self.widget.pack (expand = self.expand
                         ,side   = self.side
                         ,fill   = self.fill
                         )
        
    def embed(self,obj):
        if hasattr(obj,'widget'):
            self.widget.create_window(0,0,window=obj.widget)
        else:
            Message (func    = 'Canvas.embed'
                    ,level   = _('WARNING')
                    ,message = _('Wrong input data!')
                    ,Silent  = False
                    )
        
    def show(self,*args):
        self.parent_obj.show()
        
    def close(self,*args):
        self.parent_obj.close()



class Objects:

    def __init__(self):
        self._root = self._warning = self._error = self._question = self._info = self._waitbox = self._txt = self._entry = self._clipboard = None
        self._lst = []

    def root(self,Close=True):
        if not self._root:
            self._root = Root()
            if Close:
                self._root.close()
        return self._root

    def start(self):
        self.root()
        self._root.close()

    def end(self):
        self.root().kill()
        self._root.run()

    def add(self,obj):
        sh.log.append ('Objects.add'
                      ,_('INFO')
                      ,_('Add %s') % type(obj)
                      )
        self._lst.append(obj)

    def warning(self):
        if not self._warning:
            self._warning = MessageBuilder (parent_obj = self.root()
                                           ,level      = _('WARNING')
                                           )
            self._lst.append(self._warning)
        return self._warning

    def error(self):
        if not self._error:
            self._error = MessageBuilder (parent_obj = self.root()
                                         ,level      = _('ERROR')
                                         )
            self._lst.append(self._error)
        return self._error

    def question(self):
        if not self._question:
            self._question = MessageBuilder (parent_obj = self.root()
                                            ,level      = _('QUESTION')
                                            )
            self._lst.append(self._question)
        return self._question

    def info(self):
        if not self._info:
            self._info = MessageBuilder (parent_obj = self.root()
                                        ,level      = _('INFO')
                                        )
            self._lst.append(self._info)
        return self._info

    def close_all(self):
        sh.log.append ('Objects.close_all'
                      ,_('INFO')
                      ,_('Close %d objs') % len(self._lst)
                      )
        for i in range(len(self._lst)):
            if hasattr(self._lst[i],'close'):
                self._lst[i].close()
            else:
                sh.log.append ('Objects.close_all'
                              ,_('ERROR')
                              ,_('Widget "%s" does not have a "close" action!') % type(self._lst[i])
                              )

    def new_top(self,Maximize=1,AutoCenter=1):
        return Top (parent_obj = self.root()
                   ,Maximize   = Maximize
                   ,AutoCenter = AutoCenter
                   )

    # It is better to use this for temporary widgets only
    def txt(self,Maximize=True,words=None):
        if not self._txt:
            h_top = Top (parent_obj = self.root()
                        ,Maximize   = Maximize
                        )
            self._txt = TextBox (parent_obj = h_top
                                ,words      = words
                                )
            self._txt.focus()
            self._lst.append(self._txt)
        return self._txt

    def entry(self):
        if not self._entry:
            h_top = Top(parent_obj=self.root())
            self._entry = Entry(parent_obj=h_top)
            self._entry.focus()
            self._lst.append(self._entry)
        return self._entry

    def waitbox(self):
        if not self._waitbox:
            self._waitbox = WaitBox(parent_obj=self.root())
            self._lst.append(self._waitbox)
        return self._waitbox



# A read-only widget for displaying texts with numbered lines
class TextIndex:
    
    def __init__(self,parent_obj):
        self.parent_obj = parent_obj
        self.gui()
        
    ''' Redraw line numbers. This is a simplified version,
    preferably for read-only text widgets. See the full version: https://stackoverflow.com/questions/16369470/tkinter-adding-line-number-to-text-widget
    '''
    def update(self,*args):
        self.canvas.widget.delete("all")
        i = self.obj.widget.index("@0,0")
        while True:
            dline = self.obj.widget.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.canvas.widget.create_text(2,y,anchor="nw",text=linenum)
            i = self.obj.widget.index("%s+1line" % i)
    
    def bindings(self):
        bind (obj      = self.obj
             ,bindings = ['<ButtonRelease-1>'
                         ,'<ButtonRelease-2>'
                         ,'<Up>'
                         ,'<Down>'
                         ,'<Prior>'
                         ,'<Next>'
                         ]
             ,action   = self.update
             )
        if sh.oss.win() or sh.oss.mac():
            bind (obj      = self.parent_obj
                 ,bindings = '<MouseWheel>'
                 ,action   = self.update
                 )
        else:
            bind (obj      = self.parent_obj
                 ,bindings = ['<Button 4>'
                             ,'<Button 5>'
                             ]
                 ,action   = self.update
                 )
    
    def gui(self):
        self.canvas = Canvas (parent_obj = self.parent_obj
                             ,expand     = False
                             ,width      = 30
                             ,side       = 'left'
                             )
        self.obj = TextBox (parent_obj = self.parent_obj
                           ,Composite  = True
                           ,side       = 'left'
                           ,state      = 'disabled'
                           ,SpecialReturn = False
                           )
        self.widget = self.obj.widget
        self.bindings()
        self.obj.focus()
                                   
    def show(self,*args):
        self.parent_obj.show()
        
    def close(self,*args):
        self.parent_obj.close()
        
    def reset_logic(self,words=None):
        self.obj.words = words
        self.obj.search_box.reset_logic(words=self.obj.words)
        self.obj.selection.reset_data()
        self.obj.selection.reset_logic(words=self.obj.words)

    # Delete text, tags, marks
    def reset_data(self,*args):
        self.obj.clear_text()
        self.obj.clear_tags()
        self.obj.clear_marks()
        
    def fill(self,text):
        self.obj.read_only(ReadOnly=False)
        self.reset_data()
        self.obj.insert(text=text)
        self.obj.read_only(ReadOnly=True)
        self.update()



class SimpleCompare:
    
    def __init__(self):
        self._bg = 'old lace'
        self.gui()
        
    def reset(self,words1,words2,words3,words4):
        self.w1 = words1
        self.w2 = words2
        self.w3 = words3
        self.w4 = words4
        self.w1.sent_nos()
        self.w2.sent_nos()
        self.w3.sent_nos()
        self.w4.sent_nos()
        self.pane1.reset_logic(words=self.w1)
        self.pane2.reset_logic(words=self.w2)
        self.pane3.reset_logic(words=self.w3)
        self.pane4.reset_logic(words=self.w4)
        self.pane3.reset_data()
        self.pane4.reset_data()
        self.fill()
        
    def frames(self):
        self.frame1 = Frame (parent_obj = self.obj
                            ,side       = 'top'
                            ,expand     = False
                            ,fill       = 'both'
                            )
        self.frame2 = Frame (parent_obj = self.obj
                            ,side       = 'bottom'
                            ,expand     = True
                            ,fill       = 'both'
                            )
                               
    def panes(self):
        self.pane1 = TextIndex(parent_obj=self.frame1)
        self.pane2 = TextIndex(parent_obj=self.frame1)
        self.pane3 = TextBox (parent_obj = self.frame2
                             ,Composite  = True
                             ,side       = 'left'
                             )
        self.pane4 = TextBox (parent_obj = self.frame2
                             ,Composite  = True
                             ,side       = 'left'
                             )
    
    def gui(self):
        self.obj = objs.new_top()
        self.widget = self.obj.widget
        self.frames()
        self.panes()
        self.pane1.obj.focus()
        self.icon()
        self.title()
        self.bindings()
        
    def title(self,text=_('Compare texts:')):
        self.obj.title(text=text)
        
    def show(self,*args):
        self.obj.show()
        
    def close(self,*args):
        self.obj.close()
        
    def fill(self):
        self.pane1.fill(text=self.w1._text_orig)
        self.pane2.fill(text=self.w2._text_orig)
        self.pane3.insert(text=self.w3._text_orig)
        self.pane4.insert(text=self.w4._text_orig)
        
    def bindings(self):
        bind (obj      = self
             ,bindings = ['<Control-q>','<Control-w>']
             ,action   = self.close
             )
        bind (obj      = self
             ,bindings = '<Escape>'
             ,action   = Geometry(parent_obj=self.obj).minimize
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-1>','<Control-Key-1>']
             ,action   = self.select1
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-2>','<Control-Key-2>']
             ,action   = self.select2
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-3>','<Control-Key-3>']
             ,action   = self.select3
             )
        bind (obj      = self
             ,bindings = ['<Alt-Key-4>','<Control-Key-4>']
             ,action   = self.select4
             )
        # cur # todo: avoid conflicts
        '''
        bind (obj      = self.pane1
             ,bindings = '<ButtonRelease-1>'
             ,action   = self.select1
             )
        bind (obj      = self.pane2
             ,bindings = '<ButtonRelease-1>'
             ,action   = self.select2
             )
        bind (obj      = self.pane3
             ,bindings = '<ButtonRelease-1>'
             ,action   = self.select3
             )
        bind (obj      = self.pane4
             ,bindings = '<ButtonRelease-1>'
             ,action   = self.select4
             )
        '''
             
    def decolorize(self):
        self.pane1.obj.widget.config(bg='white')
        self.pane2.obj.widget.config(bg='white')
        self.pane3.widget.config(bg='white')
        self.pane4.widget.config(bg='white')
    
    def select1(self,*args):
        self.pane1.obj.focus() # Without this the search doesn't work (the pane is inactive)
        self.decolorize()
        self.pane1.obj.widget.config(bg=self._bg)
        
    def select2(self,*args):
        self.pane2.obj.focus() # Without this the search doesn't work (the pane is inactive)
        self.decolorize()
        self.pane2.obj.widget.config(bg=self._bg)
        
    def select3(self,*args):
        self.pane3.focus() # Without this the search doesn't work (the pane is inactive)
        self.decolorize()
        self.pane3.widget.config(bg=self._bg)
        
    def select4(self,*args):
        self.pane4.focus() # Without this the search doesn't work (the pane is inactive)
        self.decolorize()
        self.pane4.widget.config(bg=self._bg)
        
    def icon(self,path=None):
        if path:
            self.obj.icon(path)
        else:
            self.obj.icon (os.path.join (sys.path[0]
                                        ,'resources'
                                        ,'icon_64x64_cpt.gif'
                                        )
                          )


objs = Objects() # If there are problems with import or tkinter's wait_variable, put this beneath 'if __name__'


if __name__ == '__main__':
    objs.start()
    text = '''Something funny with this guy
    I am glad he is not my test
    Glad is so angry'''
    words = sh.Words(text)
    h_top = Top(parent_obj=objs.root())
    h_txt = TextBox (parent_obj = h_top
                    ,words      = words
                    )
    h_txt.title(text='My text is:')
    h_txt.insert(text)
    h_txt.widget.focus_set()
    Geometry(parent_obj=h_top).set('500x350')
    h_txt.show()
    objs.end()
