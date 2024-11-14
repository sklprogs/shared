#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import skl_shared_qt.message.controller as ms
import skl_shared_qt.graphics.icon.gui as gi


class Icon:
    
    def __init__(self):
        self.icon = None
        self.gui = gi.Icon()
    
    def set(self, path):
        f = '[SharedQt] graphics.icon.controller.Icon.set'
        if not path:
            # This is called from a user app, so it's a warning, not 'rep.lazy'
            ms.rep.empty(f)
            return
        if not os.path.exists(path):
            ms.rep.wrong_input(f)
            return
        self.icon = self.gui.get(path)
    
    def get(self):
        return self.icon


ICON = Icon()
