#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import PyQt5
import PyQt5.QtWidgets
from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Clipboard:
    
    def __init__(self):
        self.clipboard = objs.get_root().clipboard()
    
    def copy(self,text):
        self.clipboard.setText(text)
    
    def paste(self):
        return self.clipboard.text()



class Font:
    
    def get_font(self):
        return PyQt5.QtGui.QFont()
    
    def set_parent(self,widget,ifont):
        widget.setFont(ifont)
    
    def set_family(self,ifont,family):
        ifont.setFamily(family)
    
    def set_size(self,ifont,size):
        ifont.setPointSize(size)



class Entry:
    
    def __init__(self,parent=None):
        self.parent = None
        self.set_gui()
    
    def set_min_width(self,width):
        self.widget.setMinimumWidth(width)
    
    def bind(self,hotkey,action):
        PyQt5.QtWidgets.QShortcut(PyQt5.QtGui.QKeySequence(hotkey),self.widget).activated.connect(action)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QLineEdit(self.parent)
    
    def clear(self):
        self.widget.clear()
    
    def get(self):
        return self.widget.text()
    
    def insert(self,text):
        self.widget.insert(text)
    
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
    
    def __init__ (self,text='',action=None,parent=None,width=36
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
    
    def set_action(self,action=None):
        if action:
            self.action = action
        if self.action:
            self.widget.clicked.connect(self.action)
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QPushButton(self.text,self.parent)
        self.resize()
        self.set_icon()
        self.set_size()
        #FIX: this may cause the button to not show itself in complex widgets
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
        
    def get_mod_colors(self,color,factor):
        qcolor = PyQt5.QtGui.QColor(color)
        darker = qcolor.darker(factor).name()
        lighter = qcolor.lighter(factor).name()
        return(darker,lighter)
    
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
    
    def get_warning(self):
        self.set_title(_('Warning'))
        self.set_icon(PyQt5.QtWidgets.QMessageBox.Warning)
        return self
    
    def get_info(self):
        self.set_title(_('Info'))
        self.set_icon(PyQt5.QtWidgets.QMessageBox.Information)
        return self
    
    def get_debug(self):
        self.set_title(_('Debug'))
        self.set_icon(PyQt5.QtWidgets.QMessageBox.Information)
        return self
    
    def get_question(self):
        self.set_title(_('Question'))
        self.set_icon(PyQt5.QtWidgets.QMessageBox.Question)
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
        sys.exit(self.root.exec_())

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



class CheckBox:
    
    def __init__(self):
        self.set_gui()
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QCheckBox()
    
    def get(self):
        return self.widget.isChecked()
    
    def enable(self):
        self.widget.setChecked(True)
    
    def disable(self):
        self.widget.setChecked(False)
    
    def toggle(self):
        if self.get():
            self.disable()
        else:
            self.enable()
    
    def set_text(self,text=''):
        if text:
            self.widget.setText(text)



class Label:
    
    def __init__(self):
        self.set_gui()
    
    def set_gui(self):
        self.widget = PyQt5.QtWidgets.QLabel()
    
    def set_text(self,text):
        self.widget.setText(text)



''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
objs = Objects()
com = Commands()


if __name__ == '__main__':
    objs.start()
    objs.end()
