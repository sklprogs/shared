#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.graphics.root.gui import Root as guiRoot
from skl_shared.graphics.icon.controller import ICON
from skl_shared.message.controller import rep


class Root:
    
    def __init__(self):
        self.gui = guiRoot()
    
    def get_root(self):
        return self.gui.widget
    
    def get_clipboard(self):
        return self.gui.get_clipboard()
    
    def end(self):
        self.gui.end()
    
    def process_events(self):
        self.gui.process_events()
    
    def set_icon(self):
        # Set the same icon for all windows
        f = '[shared] graphics.root.controller.Root.set_icon'
        if not ICON.get():
            # None is not allowed
            rep.empty(f)
            return
        self.gui.set_icon(ICON.get())


ROOT = Root()
