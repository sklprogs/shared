#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.graphics.root import ROOT


class Clipboard:
    
    def __init__(self):
        self.clipboard = ROOT.clipboard()
    
    def copy(self, text):
        self.clipboard.setText(text)
    
    def paste(self):
        return self.clipboard.text()
