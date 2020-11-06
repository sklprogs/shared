#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import tkinter as tk
import tkinter.font
import tkinter.filedialog
import tkinter.ttk
# Load PIL only after loading tkinter
from PIL import Image as pilimage
from PIL import ImageTk as piltk
from skl_shared.localize import _


class Panes:
    
    def __init__ (self,parent,pane1,pane2
                 ,pane3=None,pane4=None
                 ):
        self.parent = parent
        self.widget = self.parent.widget
        self.pane1 = pane1
        self.pane2 = pane2
        self.pane3 = pane3
        self.pane4 = pane4
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)
    
    def set_title(self,text=''):
        self.parent.set_title(text=text)
        
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()
    
    def config_pane1(self,bg='old lace'):
        self.pane1.widget.config(bg=bg)
        # Ignore 'Alt-Up/Down'
        return 'break'
    
    def config_pane2(self,bg='old lace'):
        self.pane2.widget.config(bg=bg)
        # Ignore 'Alt-Up/Down'
        return 'break'
    
    def config_pane3(self,bg='old lace'):
        self.pane3.widget.config(bg=bg)
        # Ignore 'Alt-Up/Down'
        return 'break'
    
    def config_pane4(self,bg='old lace'):
        self.pane4.widget.config(bg=bg)
        # Ignore 'Alt-Up/Down'
        return 'break'



class TextBoxC:
    ''' #NOTE: there is no '.focus' method since we want to focus on
        'TextBox.widget' (tk.Text) instead of 'self.parent'
        (tk.Toplevel).
    '''
    def __init__(self,parent):
        self.parent = parent
        self.widget = self.parent.widget
    
    def get_sel_index(self):
        return (self.get_index('sel.first')
               ,self.get_index('sel.last')
               )
    
    def get_index(self,mark='insert'):
        return self.widget.index(mark)
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def unbind(self,hotkey='<Return>'):
        self.widget.unbind(hotkey)



class TextBox:
    
    def __init__ (self,parent,wrap='word'
                 ,expand=False,side=None
                 ,fill='both',font='Serif 14'
                 ):
        self.parent = parent
        self.widget = tk.Text (master = self.parent.widget
                              ,font = font
                              ,wrap = wrap
                              )
        self.widget.pack (expand = expand
                         ,fill = fill
                         ,side = side
                         )
    
    def get_marks(self):
        return self.widget.mark_names()
    
    def get_tags(self):
        return self.widget.tag_names()
    
    def get_sel_index(self):
        return (self.get_index('sel.first')
               ,self.get_index('sel.last')
               )
    
    def focus(self):
        self.widget.focus_set()
    
    def get_index(self,mark='insert'):
        return self.widget.index(mark)
    
    def get_cursor(self):
        return self.get_index('insert')
    
    def get_pointer(self):
        return self.get_index('current')
    
    def see(self,mark):
        self.widget.see(mark)
    
    def search(self,mark,pos1='1.0',pos2='end'):
        return self.widget.search(mark,pos1,pos2)
    
    def scroll(self,mark='goto'):
        self.widget.yview(mark)
    
    def clear_text(self,pos1='1.0',pos2='end'):
        self.widget.delete(pos1,pos2)
        return 'break'
    
    def mark_remove(self,mark='insert'):
        self.widget.mark_unset(mark)
    
    def mark_add(self,mark='insert',pos='1.0'):
        self.widget.mark_set(mark,pos)
    
    def tag_config (self,tag='sel',bg=None
                   ,fg=None,font=None
                   ):
        self.widget.tag_config (tagName = tag
                               ,background = bg
                               ,foreground = fg
                               ,font = font
                               )
    
    def tag_add (self,tag='sel',pos1='1.0'
                ,pos2='end'
                ):
        self.widget.tag_add(tag,pos1,pos2)
    
    def tag_remove (self,tag='sel'
                   ,pos1='1.0'
                   ,pos2='end'
                   ):
        self.widget.tag_remove(tag,pos1,pos2)
    
    def insert(self,text='',pos='1.0'):
        self.widget.insert(pos,text)
        return 'break'
    
    def get_sel (self,event=None
                ,pos1='sel.first'
                ,pos2='sel.last'
                ):
        ''' Tkinter will throw an exception if there is no selection,
            so use 'try-except' for this in the controller.
        '''
        return self.get (pos1 = pos1
                        ,pos2 = pos2
                        )
    
    def get(self,pos1='1.0',pos2='end',event=None):
        return self.widget.get(pos1,pos2)
    
    def disable(self,event=None):
        self.widget.config(state='disabled')
    
    def enable(self,event=None):
        self.widget.config(state='normal')



class EntryC:

    def __init__ (self,parent):
        self.parent = parent
        self.widget = self.parent.widget
    
    def focus(self,event=None):
        self.parent.focus()
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class Entry:

    def __init__ (self,parent,side=None
                 ,ipadx=None,ipady=None
                 ,fill=None,width=None
                 ,expand=None,font='Sans 11'
                 ,bg=None,fg=None
                 ,justify='left'
                 ):
        self.parent = parent
        self.widget = tk.Entry (master = self.parent.widget
                               ,font = font
                               ,bg = bg
                               ,fg = fg
                               ,width = width
                               ,justify = justify
                               )
        self.widget.pack (side = side
                         ,ipadx = ipadx
                         ,ipady = ipady
                         ,fill = fill
                         ,expand = expand
                         )
    
    def get_sel_index(self):
        return (self.get_index('sel.first')
               ,self.get_index('sel.last')
               )
    
    def get_index(self,mark='insert'):
        return self.widget.index(mark)
    
    def get_cursor(self):
        return self.get_index('insert')
    
    def focus(self,event=None):
        self.widget.focus_set()
        # Manual Tab focus (left to right widget)
        return 'break'
    
    def select_all(self,event=None):
        self.widget.select_clear()
        self.widget.select_range(0,'end')
        return 'break'
    
    def get(self,event=None):
        return self.widget.get()
    
    def disable(self,event=None):
        self.widget.config(state='disabled')
    
    def enable(self,event=None):
        self.widget.config(state='normal')
    
    def clear_text(self,event=None,pos1=0,pos2='end'):
        self.widget.selection_clear()
        self.widget.delete(pos1,pos2)



class MultCBoxesC:

    def __init__(self,parent):
        self.parent = parent
        self.widget = self.parent.widget
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def show(self,event=None):
        self.parent.show()
        
    def close(self,event=None):
        self.parent.close()



class CheckBox:
    ''' #NOTE: For some reason, CheckBox that should be Active must be
        assigned to a variable (var = CheckBox(parent,Active=1))
    '''
    def __init__(self,parent,side=None):
        self.parent = parent
        self.side = side
        self.status = tk.IntVar()
        self.set_gui()
    
    def toggle(self,event=None):
        self.widget.toggle()
    
    def get(self,event=None):
        return self.status.get()
    
    def disable(self,event=None):
        self.widget.deselect()
    
    def enable(self,event=None):
        self.widget.select()
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def close(self,event=None):
        self.parent.close()
    
    def show(self,event=None):
        self.parent.show()
    
    def set_gui(self):
        self.widget = tk.Checkbutton (master = self.parent.widget
                                     ,variable = self.status
                                     )
        self.widget.pack(side=self.side)
    
    def set_action(self,action=None):
        self.widget.config(command=action)



class ProgressBar:
    
    def __init__(self,parent):
        self.parent = parent
    
    def close(self,event=None):
        self.parent.close()
    
    def show(self,event=None):
        self.parent.show()
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)



class ProgressBarItem:
    
    def __init__ (self,parent,orient='horizontal'
                 ,length=100,mode='determinate'
                 ):
        self.parent = parent
        self.orient = orient
        self.length = length
        self.mode = mode
        self.set_gui()
    
    def set_gui(self):
        self.widget = tkinter.ttk.Progressbar (master = self.parent.widget
                                              ,orient = self.orient
                                              ,length = self.length
                                              ,mode = self.mode
                                              )
        self.widget.pack()



class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
    '''
    # Accepts both path and 'io.BytesIO(image_bytes)'
    def get_loader(self,path):
        return pilimage.open(path)
    
    def get_image(self,loader):
        return piltk.PhotoImage(loader)



class Canvas:
    
    def __init__ (self,parent,region=None
                 ,width=None,height=None
                 ,expand=True,side=None
                 ,fill='both'
                 ):
        self.parent = parent
        self.region = region
        self.width = width
        self.height = height
        self.expand = expand
        self.side = side
        self.fill = fill
        self.set_gui()
    
    def close(self,event=None):
        self.parent.close()
    
    def show(self,event=None):
        self.parent.show()
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def embed(self,obj):
        self.widget.create_window(0,0,window=obj.widget)
    
    def scroll(self,event=None,x=0,y=0):
        self.widget.xview_moveto(x)
        self.widget.yview_moveto(y)
    
    def set_region (self,x=0,y=0
                   ,xborder=0
                   ,yborder=0
                   ):
        self.widget.configure (scrollregion = (-x/2 - xborder
                                              ,-y/2 - yborder
                                              , x/2 + xborder
                                              , y/2 + yborder
                                              )
                              )
    
    def move_bottom(self,event=None):
        self.widget.yview_moveto('1.0')
    
    def move_right(self,event=None,value=1):
        self.widget.xview_scroll(value,'units')
    
    def move_left(self,event=None,value=-1):
        self.widget.xview_scroll(value,'units')
    
    def move_page_down(self,event=None,value=1):
        self.widget.yview_scroll(value,'pages')
    
    def move_page_up(self,event=None,value=-1):
        self.widget.yview_scroll(value,'pages')
    
    def move_down(self,event=None,value=1):
        self.widget.yview_scroll(value,'units')
    
    def move_up(self,event=None,value=-1):
        self.widget.yview_scroll(value,'units')
    
    def set_mouse_wheel(self,event=None):
        ''' Windows XP has the delta of -120, however, it differs
            depending on the version.
        '''
        if event:
            if event.num == 5 or event.delta < 0:
                self.move_down()
            if event.num == 4 or event.delta > 0:
                self.move_up()
        return 'break'
    
    def move_left_corner(self,event=None):
        self.move_top()
        self.widget.xview_moveto(0)
    
    def set_gui(self):
        self.widget = tk.Canvas (master = self.parent.widget
                                ,scrollregion = self.region
                                ,width = self.width
                                ,height = self.height
                                )
        self.widget.pack (expand = self.expand
                         ,side = self.side
                         ,fill = self.fill
                         )
    
    def move_top(self,event=None):
        self.widget.yview_moveto(0)



class Clipboard:
    
    def __init__(self):
        pass
    
    def paste(self):
        return objs.get_root().widget.clipboard_get()
    
    def copy(self,text):
        objs.get_root().widget.clipboard_append(text)
    
    def clear(self):
        objs.get_root().widget.clipboard_clear()



class SymbolMap:

    def __init__(self,parent):
        self.symbol = ''
        self.parent = parent

    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def get(self,event=None):
        return self.symbol
    
    def set(self,sym,event=None):
        self.symbol = sym
        self.close()
    
    def insert(self,frame,items,i):
        ''' - 'lambda' will work properly only in case of an instant
              packing which is not supported by 'create_button'
              (the instant packing returns 'None' instead of a widget),
              therefore, we do not use this function.
            - By the same reason, '<Return>' and '<KP_Enter>' cannot be
              bound to the buttons, only '<space>' and
              '<ButtonRelease-1>' that are bound by default will work.
            - In Windows, GUI looks better when 'width' and 'height'
              are set.
        '''
        return tk.Button (master = frame.widget
                         ,text = items[i]
                         ,command = lambda i=i:self.set(items[i])
                         ,width = 2
                         ,height = 2
                         ).pack (side = 'left'
                                ,expand = True
                                )
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)
    
    def set_title(self,text=''):
        self.parent.set_title(text)



class OptionMenu:
    
    def __init__ (self,parent,Combo=False
                 ,side='left',anchor='center'
                 ,expand=False,fill=None
                 ,tfocus=1,font=None
                 ,width=None
                 ):
        self.parent = parent
        self.Combo = Combo
        self.side = side
        self.anchor = anchor
        self.expand = expand
        self.fill_ = fill
        self.tfocus = tfocus
        self.font = font
        self.width = width
        self.var = tk.StringVar(self.parent.widget)
        self.set_gui()
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def get(self):
        return self.var.get()
    
    def fill(self,items=('1','2','3','4','5'),action=None):
        if self.Combo:
            self.widget.config(values=items)
        else:
            self.widget['menu'].delete(0,'end')
            for item in items:
                self.widget["menu"].add_command (label = item
                                                ,command = tk._setit (self.var
                                                                     ,item
                                                                     ,action
                                                                     )
                                                )
    
    def set(self,value):
        self.var.set(value)
    
    def clear_sel(self):
        self.widget.selection_clear()
    
    def enable(self):
        self.widget.config(state='normal')
    
    def disable(self):
        self.widget.config(state='disabled')
    
    def set_gui(self):
        if self.Combo:
            self.widget = tkinter.ttk.Combobox (master = self.parent.widget
                                               ,textvariable = self.var
                                               )
        else:
            # Cannot use a starred expression as a keyword argument
            self.widget = tk.OptionMenu (self.parent.widget
                                        ,self.var
                                        ,*('1','2','3','4','5')
                                        ,command = None
                                        )
        self.widget.pack (side = self.side
                         ,anchor = self.anchor
                         ,expand = self.expand
                         ,fill = self.fill_
                         )
        self.widget.configure (takefocus = self.tfocus
                              ,font = self.font
                              ,width = self.width
                              )



class ListBoxC:
    
    def __init__(self,parent):
        self.parent = parent
        self.widget = self.parent.widget
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def set_icon(self,path=''):
        self.parent.set_icon(path)



class ListBox:
    #TODO: configure a font
    def __init__ (self,parent,Multiple=False
                 ,side=None,expand=1,fill='both'
                 ):
        self.parent = parent
        self.Multiple = Multiple
        self.expand = expand
        self.side = side
        self.fill_ = fill
        self.set_gui()
    
    def get(self,ind):
        return self.widget.get(ind)
    
    def get_sel(self):
        return self.widget.curselection()
    
    def insert(self,item,pos=tk.END):
        self.widget.insert(pos,item)
    
    def select(self,ind):
        self.widget.selection_set(ind)
        self.widget.see(ind)
    
    def clear_sel(self):
        self.widget.selection_clear(0,tk.END)
    
    def clear(self):
        self.widget.delete(0,tk.END)
    
    def activate(self,ind):
        self.widget.activate(ind)
    
    def resize(self):
        # Autofit to contents
        self.widget.config(width=0,height=0)
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def set_gui(self):
        if self.Multiple:
            self.widget = tk.Listbox (master = self.parent.widget
                                     ,exportselection = 0
                                     ,selectmode = tk.MULTIPLE
                                     )
        else:
            self.widget = tk.Listbox (master = self.parent.widget
                                     ,exportselection = 0
                                     ,selectmode = tk.SINGLE
                                     )
        self.widget.pack (expand = self.expand
                         ,fill = self.fill_
                         ,side = self.side
                         )



class Scrollbar:
    
    def __init__(self,parent,scroll):
        self.parent = parent
        self.scroll = scroll
    
    def config_y(self):
        self.scroll.widget.config(yscrollcommand=self.widget.set)
        self.widget.config(command=self.scroll.widget.yview)
    
    def config_x(self):
        self.scroll.widget.config(xscrollcommand=self.widget.set)
        self.widget.config(command=self.scroll.widget.xview)
    
    def create_x(self):
        self.widget = tk.Scrollbar (master = self.parent.widget
                                   ,orient = tk.HORIZONTAL
                                   )
        self.widget.pack (expand = True
                         ,fill = 'x'
                         ,side = None
                         )
    
    def create_y(self):
        self.widget = tk.Scrollbar (master = self.parent.widget
                                   ,orient = tk.VERTICAL
                                   )
        self.widget.pack (expand = True
                         ,fill = 'y'
                         ,side = 'right'
                         )



class ToolTipBase:

    def __init__(self,obj):
        self.obj = obj
        self.widget = self.obj.widget
    
    def get_height(self):
        return self.widget.winfo_height()
    
    def get_width(self):
        return self.widget.winfo_width()
    
    def get_rootx(self):
        return self.widget.winfo_rootx()
    
    def get_rooty(self):
        return self.widget.winfo_rooty()
    
    def schedule(self,hint_delay,showtip):
        return self.widget.after(hint_delay,showtip)
    
    def unschedule(self,myid):
        self.widget.after_cancel(myid)



class WaitBox:
    
    def __init__(self,parent):
        self.parent = parent
        self.widget = self.parent.widget

    def set_icon(self,file):
        image = tk.PhotoImage (master = self.widget
                              ,file = file
                              )
        self.widget.tk.call('wm','iconphoto',self.widget._w,image)
    
    def set_title(self,text=''):
        self.parent.set_title(text)
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()



class Button:

    def __init__ (self,parent,off_img=None,on_img=None
                 ,height=36,width=36,side='left'
                 ,expand=0,bg=None,bg_focus=None
                 ,fg=None,fg_focus=None,bd=0,fill='both'
                 ,font=None
                 ):
        self.parent = parent
        self.bd = bd
        self.bg = bg
        self.bg_focus = bg_focus
        self.expand = expand
        self.fg = fg
        self.fg_focus = fg_focus
        self.fill = fill
        self.font = font
        self.height = height
        self.side = side
        self.width = width
        self.on_img = on_img
        self.off_img = off_img
        self.set_gui()
    
    def set_gui(self):
        if self.off_img:
            self.widget = tk.Button (master = self.parent.widget
                                    ,image = self.off_img
                                    ,height = self.height
                                    ,width = self.width
                                    ,bd = self.bd
                                    ,bg = self.bg
                                    ,fg = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    ,font = self.font
                                    )
        else:
            ''' A text button does not require setting a default width
                and height in most cases, they are defined
                automatically. Moreover, a border should be used for
                text buttons in a majority of cases.
            '''
            self.widget = tk.Button (master = self.parent.widget
                                    ,bd = 1
                                    ,bg = self.bg
                                    ,fg = self.fg
                                    ,activebackground = self.bg_focus
                                    ,activeforeground = self.fg_focus
                                    ,font = self.font
                                    )
        self.widget.pack (expand = self.expand
                         ,side = self.side
                         ,fill = self.fill
                         )
    
    def set_title(self,button_text=''):
        self.widget.config(text=button_text)

    def activate(self):
        self.widget.config(image=self.on_img)
        self.widget.flag_img = self.on_img

    def inactivate(self):
        self.widget.config(image=self.off_img)
        self.widget.flag_img = self.off_img

    def show(self,event=None):
        self.parent.show()

    def close(self,event=None):
        self.parent.close()

    def focus(self,event=None):
        self.widget.focus_set()
    
    def enable(self):
        self.widget.config(state='normal')
    
    def disable(self):
        self.widget.config(state='disabled')



class Frame:

    def __init__ (self,parent,expand=1
                 ,fill='both',side=None,padx=None
                 ,pady=None,ipadx=None,ipady=None
                 ,bd=None,bg=None,width=None
                 ,height=None,propag=True
                 ):
        self.parent = parent
        self.widget = tk.Frame (master = self.parent.widget
                               ,bd = bd
                               ,bg = bg
                               ,width = width
                               ,height = height
                               )
        ''' 'pack_propagate' should be set before 'pack' to 'False'
            if you want to set widget sizes manually. 'height' and
            'width' options will not work otherwise. If there are two
            frames packed one after another, and we need to set sizes
            of the second frame, then we should apply 'pack_propagate',
            'width' and 'height' to the first frame too.
        '''
        self.widget.pack_propagate(propag)
        self.widget.pack (expand = expand
                         ,fill = fill
                         ,side = side
                         ,padx = padx
                         ,pady = pady
                         ,ipadx = ipadx
                         ,ipady = ipady
                         )

    def get_height(self):
        return self.widget.winfo_height()
    
    def get_width(self):
        return self.widget.winfo_width()
    
    def get_reqheight(self):
        return self.widget.winfo_reqheight()
    
    def get_reqwidth(self):
        return self.widget.winfo_reqwidth()
    
    def kill(self):
        self.widget.destroy()
    
    def set_title(self,text=''):
        self.parent.set_title(text)

    def show(self):
        self.parent.show()

    def close(self):
        self.parent.close()



class Label:
    
    def __init__ (self,parent,side=None,fill=None
                 ,expand=False,ipadx=None,ipady=None
                 ,image=None,fg=None,bg=None
                 ,anchor=None,width=None
                 ,height=None,justify=None
                 ,padx=None,pady=None
                 ):
        self.parent = parent
        self.side = side
        self.fill = fill
        self.expand = expand
        self.ipadx = ipadx
        self.ipady = ipady
        self.padx = padx
        self.pady = pady
        self.image = image
        self.bg = bg
        self.fg = fg
        self.anchor = anchor
        self.width = width
        self.height = height
        # Usually the alignment is done by tuning the parent
        self.justify = justify
        self.set_gui()
    
    def get_reqheight(self):
        return self.widget.winfo_reqheight()
    
    def get_reqwidth(self):
        return self.widget.winfo_reqwidth()
    
    def kill(self):
        self.widget.destroy()
    
    def set_title(self,text=''):
        self.parent.set_title(text=text)
    
    def close(self,event=None):
        self.parent.close()
    
    def show(self,event=None):
        self.parent.show()
    
    def set_font(self,arg=''):
        try:
            self.widget.config(font=arg)
            return True
        except tk.TclError:
            pass
    
    def set_text(self,arg=''):
        self.widget.config(text=arg)
    
    def enable(self,event=None):
        self.widget.config(state='normal')
    
    def disable(self,event=None):
        self.widget.config(state='disabled')
    
    def set_gui(self):
        self.widget = tk.Label (master = self.parent.widget
                               ,image = self.image
                               ,bg = self.bg
                               ,fg = self.fg
                               ,width = self.width
                               ,height = self.height
                               )
        self.widget.pack (side = self.side
                         ,fill = self.fill
                         ,expand = self.expand
                         ,ipadx = self.ipadx
                         ,ipady = self.ipady
                         ,padx = self.padx
                         ,pady = self.pady
                         ,anchor = self.anchor
                         )



class Geometry:
    
    def __init__(self,parent):
        self.parent = parent
    
    def _activate(self):
        self.parent.widget.deiconify()
        #self.parent.widget.focus_set()
        self.parent.widget.lift()
    
    def lift(self):
        self.parent.widget.lift()
    
    def focus(self):
        self.parent.widget.focus_set()
    
    def maximize_win(self):
        self.parent.widget.wm_state(newstate='zoomed')
    
    def maximize_nix(self):
        self.parent.widget.wm_attributes('-zoomed',True)
    
    def minimize(self):
        self.parent.widget.iconify()
    
    def set_foreground(self):
        self.parent.widget.lift()
    
    def update(self):
        objs.get_root().widget.update_idletasks()
    
    def set_geometry(self):
        return self.parent.widget.geometry()
    
    def restore(self,position):
        self.parent.widget.geometry(position)



class Top:
    
    def __init__(self,Lock=True):
        self.parent = objs.get_root()
        self.Lock = Lock
        self.widget = tk.Toplevel(self.parent.widget)
        self.tk_trigger = tk.BooleanVar()
        self.widget.protocol("WM_DELETE_WINDOW",self.close)
    
    def set_icon(self,file):
        image = tk.PhotoImage (master = self.widget
                              ,file = file
                              )
        self.widget.tk.call('wm','iconphoto',self.widget._w,image)
    
    def update_idle(self):
        self.widget.update_idletasks()
    
    def set_geometry(self,position=None):
        # This method can both retrieve and set coordinates
        return self.widget.geometry(position)
    
    def focus(self,event=None):
        self.widget.focus_set()
    
    def get_resolution(self):
        self.update_idle()
        return (self.widget.winfo_screenwidth()
               ,self.widget.winfo_screenheight()
               )
    
    def show(self,event=None):
        self.widget.deiconify()
        if self.Lock:
            self.tk_trigger = tk.BooleanVar()
            self.widget.wait_variable(self.tk_trigger)
    
    def set_title(self,text):
        self.widget.title(text)
    
    def close(self,event=None):
        self.widget.withdraw()
        if self.Lock:
            self.tk_trigger.set(True)



class Commands:
    
    def get_image(self,path,width,height):
        return tk.PhotoImage (file = path
                             ,master = objs.get_root().widget
                             ,width = width
                             ,height = height
                             )
        
    def get_mod_color(self,color):
        try:
            return objs.get_root().widget.winfo_rgb(color=color)
        except tk._tkinter.TclError:
            pass
    
    def show_save_dialog(self,options=()):
        return tkinter.filedialog.asksaveasfilename(**options)
    
    def bind(self,obj,binding,action):
        try:
            obj.widget.bind(binding,action)
            return True
        except tk.TclError:
            pass



class MessageBuilder:
    ''' Not using tkinter.messagebox because it blocks main GUI (even
        if we specify a non-root parent).
    '''
    def __init__(self,parent):
        self.parent = parent
        self.widget = self.parent.widget
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()
    
    def set_image(self,path,obj):
        ''' Without explicitly indicating 'master', we get
            "image pyimage1 doesn't exist".
        '''
        return tk.PhotoImage (master = obj.widget
                             ,file = path
                             )
        
    def set_title(self,text=''):
        self.parent.set_title(text)
        
    def set_icon(self,path):
        self.parent.set_icon(path)



class Font:
    
    def get_width(self,font,max_line):
        return font.measure(max_line)
    
    def get_height(self,font):
        return font.metrics("linespace")
    
    def get_font(self,family,size):
        ''' If an "AttributeError: 'NoneType' object has no attribute
            'call'" is thrown there, then we forgot to run 'tk.Tk()'
            first (no 'gi.objs.start').
        '''
        return tkinter.font.Font (family = family
                                 ,size = size
                                 )



class Root:

    def __init__(self):
        self.type = 'Root'
        self.widget = tk.Tk()

    def set_icon(self,file):
        image = tk.PhotoImage (master = self.widget
                              ,file = file
                              )
        self.widget.tk.call('wm','iconphoto',self.widget._w,image)

    def set_title(self,text):
        self.widget.title(text)
    
    def get_resolution(self):
        self.update_idle()
        return (self.widget.winfo_screenwidth()
               ,self.widget.winfo_screenheight()
               )
    
    def update_idle(self):
        self.widget.update_idletasks()
    
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
        
    def wait(self):
        self.widget.wait_window()



class Objects:

    def __init__(self):
        self.root = self.warning = self.error = self.question \
                  = self.info = self.entry = None
    
    def get_root(self,Close=True):
        if not self.root:
            self.root = Root()
            if Close:
                self.root.close()
        return self.root

    def start(self,Close=True):
        self.get_root(Close=Close)

    def end(self):
        self.get_root().kill()
        self.root.run()

    def get_warning(self):
        if not self.warning:
            self.warning = MessageBuilder (parent = self.get_root()
                                          ,level = _('WARNING')
                                          )
        return self.warning

    def get_error(self):
        if not self.error:
            self.error = MessageBuilder (parent = self.get_root()
                                        ,level = _('ERROR')
                                        )
        return self.error

    def get_question(self):
        if not self.question:
            self.question = MessageBuilder (parent = self.get_root()
                                           ,level = _('QUESTION')
                                           )
        return self.question

    def get_info(self):
        if not self.info:
            self.info = MessageBuilder (parent = self.get_root()
                                       ,level = _('INFO')
                                       )
        return self.info



class WidgetObject:
    
    def __init__(self,widget):
        self.widget = widget



''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
objs = Objects()
com = Commands()


if __name__ == '__main__':
    objs.start()
    objs.end()
