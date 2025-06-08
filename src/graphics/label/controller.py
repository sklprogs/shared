#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.message.controller import rep
from skl_shared.graphics.label.gui import Label as guiLabel


class Label:
    
    def __init__(self, text='', font_family=None, font_size=None):
        self.gui = guiLabel()
        self.widget = self.gui.widget
        self.set_text(text)
        # Qt changes default font family upon receiving None
        if font_family and font_size:
            self.gui.set_font(font_family, font_size)
    
    def set_action(self, action=None):
        self.gui.set_action(action)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] graphics.label.controller.Label.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            rep.empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            rep.condition(f, mes)
            return
        self.gui.set_font_size(size + delta)
    
    def set_text(self, text):
        if not text:
            text = '[SharedQt] graphics.label.controller.Label.set_text'
        self.gui.set_text(text)
