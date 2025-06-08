#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
from skl_shared.message.controller import rep
from skl_shared.graphics.icon.gui import Icon as guiIcon


class Icon:
    
    def __init__(self):
        self.icon = None
        self.gui = guiIcon()
    
    def set(self, path):
        f = '[SharedQt] graphics.icon.controller.Icon.set'
        if not path:
            # This is called from a user app, so it's a warning, not 'rep.lazy'
            rep.empty(f)
            return
        if not os.path.exists(path):
            rep.wrong_input(f)
            return
        self.icon = self.gui.get(path)
    
    def get(self):
        return self.icon


ICON = Icon()
