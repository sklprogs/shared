#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.graphics.option_menu.gui import OptionMenu as guiOptionMenu


class OptionMenu:
    
    def __init__(self, items=[], default=None, action=None, font_family=None, font_size=None):
        self.items = []
        self.default = None
        self.action = action
        self.gui = guiOptionMenu()
        self.widget = self.gui.widget
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
        if items:
            self.reset(items, default)
        self.set_action(self.action)
        
    def reset(self, items=[], default=None, action=None):
        self.items = [str(item) for item in items]
        self.fill()
        if default is not None:
            self.set(default)
        if len(self.items) < 2:
            self.disable()
        else:
            self.enable()
        self.set_action(action)

    def set_action(self, action=None):
        if not action:
            return
        self.action = action
        self.widget.activated.connect(self.action)
    
    def change_font_size(self, delta=1):
        f = '[shared] graphics.option_menu.controller.OptionMenu.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            rep.empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            rep.condition(f, mes)
            return
        self.gui.set_font_size(size + delta)
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
        
    def set(self, item):
        f = '[shared] graphics.option_menu.controller.OptionMenu.set'
        item = str(item)
        if item in self.items:
            self.gui.set(item)
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(item, '; '.join(self.items))
            Message(f, mes, True).show_error()
    
    def fill(self):
        self.gui.fill(self.items)

    def get(self):
        return self.gui.get()
    
    def get_index(self):
        return self.gui.get_index()
    
    def set_index(self, index_):
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
