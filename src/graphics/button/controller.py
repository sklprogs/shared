#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms
import skl_shared_qt.graphics.button.gui as gi


class Button(gi.Button):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] graphics.button.controller.Button.change_font_size'
        size = self.get_font_size()
        if not size:
            ms.rep.empty(f)
            return
        if size + delta <= 0:
            mes = f'{size} + {delta} > 0'
            ms.rep.condition(f, mes)
            return
        self.set_font_size(size+delta)
