#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtGui import QFont


class Font:
    
    def get_font(self):
        return QFont()
    
    def set_parent(self, widget, ifont):
        widget.setFont(ifont)
    
    def set_family(self, ifont, family):
        ifont.setFamily(family)
    
    def set_size(self, ifont, size):
        ifont.setPointSize(size)
