#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms
import skl_shared_qt.graphics.entry.gui as gi


class Entry:
    
    def __init__(self):
        self.gui = gi.Entry()
        self.widget = self.gui.widget
    
    def select_all(self):
        self.gui.select_all()
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] graphics.entry.controller.Entry.change_font_size'
        size = self.gui.get_font_size()
        if not size:
            ms.rep.empty(f)
            return
        if size + delta <= 0:
            ms.rep.condition(f, f'{size} + {delta} > 0')
            return
        self.gui.set_font_size(size + delta)
    
    def disable(self):
        self.gui.disable()
    
    def enable(self):
        self.gui.enable()
    
    def get_width(self):
        return self.gui.get_width()
    
    def get_root_y(self):
        return self.gui.get_root_y()
    
    def get_x(self):
        return self.gui.get_x()
    
    def set_min_width(self, width):
        self.gui.set_min_width(width)
    
    def set_max_width(self, width):
        self.gui.set_max_width(width)
    
    def bind(self, hotkeys, action):
        self.gui.bind(hotkeys, action)
    
    def reset(self):
        self.clear()
    
    def clear(self):
        self.gui.clear()
    
    def get(self):
        return self.gui.get()
    
    def insert(self, text, GoStart=True):
        self.gui.insert(str(text))
        if GoStart:
            self.gui.go_start()
    
    def set_text(self, text):
        # Unlike with 'insert', no need to clear the entry first
        self.gui.set_text(str(text))
    
    def focus(self):
        self.gui.focus()
