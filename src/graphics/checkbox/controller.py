#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms
import skl_shared_qt.graphics.checkbox.gui as gi


class CheckBox:
    
    def __init__(self, text='', font_family=None, font_size=None):
        self.gui = gi.CheckBox()
        self.widget = self.gui.widget
        self.gui.set_text(text)
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] graphics.checkbox.controller.CheckBox.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            ms.rep.empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            ms.rep.condition(f, mes)
            return
        self.gui.set_font_size(size+delta)
    
    def get(self):
        return self.gui.get()
    
    def set(self, value):
        if value:
            self.enable()
        else:
            self.disable()
    
    def enable(self):
        self.gui.enable()
    
    def disable(self):
        self.gui.disable()
    
    def toggle(self):
        self.gui.toggle()
