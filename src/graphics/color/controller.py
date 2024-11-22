#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.graphics.color.gui import Color as guiColor


class Color:
    # Accepts a color name (/usr/share/X11/rgb.txt) or a hex value
    def __init__(self, color):
        self.color = color
        self.gui = guiColor(color)
    
    def get_hex(self):
        f = '[SharedQt] graphics.color.controller.Color.get_hex'
        # Both None and '' are accepted by Qt, but we need transparency here
        if not self.color:
            rep.empty(f)
        return self.gui.get_hex()
    
    def modify(self, factor=150):
        ''' Make a color (a color name (/usr/share/X11/rgb.txt) or a hex value)
            brighter and darker.
        '''
        f = '[SharedQt] graphics.color.controller.Color.modify'
        # Qt does not throw errors on empty input
        darker = lighter = ''
        if not self.color:
            rep.empty(f)
            return(darker, lighter)
        if factor <= 0:
            mes = f'{factor} > 0'
            rep.condition(f, mes)
            return(darker, lighter)
        try:
            darker, lighter = self.gui.modify(factor)
        except Exception as e:
            rep.third_party(f, e)
            return(darker, lighter)
        mes = _('Color: {}, darker: {}, lighter: {}')
        mes = mes.format(self.color, darker, lighter)
        Message(f, mes).show_debug()
        return(darker, lighter)
