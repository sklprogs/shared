#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt5
import PyQt5.QtWidgets
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Entry:
    
    def __init__(self,parent=None):
        self.parent = None
        self.set_gui()
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self.widget).activated.connect(action)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QLineEdit(self.parent)
    
    def clear(self):
        self.widget.clear()
    
    def get(self):
        return self.widget.text()
    
    def insert(self,text):
        self.widget.setText(text)
    
    def focus(self):
        self.widget.setFocus()



class Top(PyQt5.QtWidgets.QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_gui()
    
    def add_widget(self,widget):
        self.layout.addWidget(widget)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self).activated.connect(action)
    
    def set_gui(self):
        self.widget = self
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)



class OptionMenu:
    
    def __init__(self,parent=None):
        self.parent = parent
        self.widget = PyQt5.QtWidgets.QComboBox(self.parent)
    
    def enable(self):
        self.widget.setEnabled(True)
    
    def disable(self):
        self.widget.setEnabled(False)
        
    def set(self,item):
        self.widget.setCurrentText(item)
    
    def fill(self,items):
        self.widget.clear()
        self.widget.addItems(items)

    def get(self):
        return self.widget.currentText()
    
    def get_index(self):
        return self.widget.currentIndex()
    
    def set_index(self,index_):
        return self.widget.setCurrentIndex(index_)



class Button:
    
    def __init__ (self,parent=None,text='',action=None,width=36
                 ,height=36,hint='',active='',inactive=''
                 ):
        self.Status = False
        self.parent = parent
        self.text = text
        self.action = action
        self.width = width
        self.height = height
        self.hint = hint
        self.active = active
        self.icon = self.inactive = inactive
        self.set_gui()
    
    def activate(self):
        if not self.Status:
            self.Status = True
            self.icon = self.active
            self.set_icon()

    def inactivate(self):
        if self.Status:
            self.Status = False
            self.icon = self.inactive
            self.set_icon()
    
    def set_hint(self):
        if self.hint:
            self.widget.setToolTip(self.hint)
    
    def resize(self):
        self.widget.resize(self.width,self.height)
    
    def set_icon(self):
        ''' Setting a button image with
            button.setStyleSheet('image: url({})'.format(path)) causes
            tooltip glitches.
        '''
        if self.icon:
            self.widget.setIcon(PyQt5.QtGui.QIcon(self.icon))
    
    def set_size(self):
        if self.width and self.height:
            self.widget.setIconSize(PyQt5.QtCore.QSize(self.width,self.height))
    
    def set_border(self):
        if self.icon:
            self.widget.setStyleSheet('border: 0px')
    
    def set_action(self):
        if self.action:
            self.widget.clicked.connect(self.action)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QPushButton(self.text,self.parent)
        self.resize()
        self.set_icon()
        self.set_size()
        self.set_border()
        self.set_hint()
        self.set_action()



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



class Message(PyQt5.QtWidgets.QMessageBox):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
    def set_text(self,text):
        self.setText(text)
    
    def set_title(self,text):
        self.setWindowTitle(text)
        
    def set_icon(self,obj):
        self.setIcon(obj)
    
    def get_error(self):
        self.set_title(_('Error'))
        self.set_icon(PyQt5.QtWidgets.QMessageBox.Critical)
        return self



class Objects:

    def __init__(self):
        self.root = self.warning = self.error = self.question \
                  = self.info = self.entry = None
    
    def get_root(self):
        if not self.root:
            self.root = PyQt5.QtWidgets.QApplication(sys.argv)
        return self.root

    def start(self):
        self.get_root()

    def end(self):
        sys.exit(self.root.exec())

    def get_warning(self):
        if not self.warning:
            self.warning = Message().get_warning()
        return self.warning

    def get_error(self):
        if not self.error:
            self.error = Message().get_error()
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



''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
objs = Objects()
com = Commands()


if __name__ == '__main__':
    objs.start()
    objs.end()
