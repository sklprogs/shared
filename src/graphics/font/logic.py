#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep


class Font:
    
    def __init__(self, name, xborder=0, yborder=0):
        self.set_values()
        if name:
            self.reset(name = name, xborder = xborder, yborder = yborder)
    
    def set_text(self, text):
        f = '[SharedQt] graphics.font.logic.Font.set_text'
        if not text:
            rep.empty(f)
            return
        self.text = text
    
    def set_values(self):
        self.font = None
        self.family = ''
        self.name = ''
        self.text = ''
        self.size = 0
        self.height = 0
        self.width = 0
        self.xborder = 0
        self.yborder = 0
    
    def set_width(self):
        if self.width:
            self.width += self.xborder
    
    def set_height(self):
        f = '[SharedQt] graphics.font.logic.Font.set_height'
        if not self.set_height:
            rep.empty(f)
            return
        lines = len(self.text.splitlines())
        if lines:
            self.height = self.height * lines
        self.height += self.yborder
    
    def reset(self, name, xborder=0, yborder=0):
        self.set_values()
        self.name = name
        self.xborder = xborder
        self.yborder = yborder
        self.set_attr()
    
    def set_attr(self):
        f = '[SharedQt] graphics.font.logic.Font.set_attr'
        if not self.name:
            rep.empty(f)
            return
        match = re.match('([aA-zZ].*) (\d+)', self.name)
        if not match:
            message = _('Wrong input data: "{}"!').format(self.name)
            Message(f, message, False).show_error()
            return
        self.family = match.group(1)
        self.size = int(match.group(2))
