#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.graphics.root.gui as gi


class Root:
    
    def __init__(self):
        self.gui = gi.Root()
    
    def get_root(self):
        return self.gui.widget
    
    def get_clipboard(self):
        return self.gui.get_clipboard()
    
    def end(self):
        self.gui.end()


ROOT = Root()
