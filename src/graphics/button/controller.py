#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.message.controller import rep
from skl_shared.graphics.button.gui import Button as guiButton


class Button(guiButton):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def change_font_size(self, delta=1):
        f = '[SharedQt] graphics.button.controller.Button.change_font_size'
        size = self.get_font_size()
        if not size:
            rep.empty(f)
            return
        if size + delta <= 0:
            rep.condition(f, f'{size} + {delta} > 0')
            return
        self.set_font_size(size + delta)
