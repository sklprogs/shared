#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.basic_text import Shorten
from skl_shared.graphics.progress_bar.gui import ProgressBar as guiProgressBar
from skl_shared.logic import Input


class ProgressBar:
    
    def __init__(self):
        self.gui = guiProgressBar()
    
    def set_title(self, title=_('Progress:')):
        self.gui.set_title(title)
    
    def _set_info_mult(self, info, limit):
        info = info.splitlines()
        info = [item.strip() for item in info if item.strip()]
        if len(info) < 2:
            return
        limit = int(limit / len(info))
        if limit < 5:
            return
        info = [Shorten(item, limit).run() for item in info]
        return '\n'.join(info)
    
    def _set_info_auto(self, info, limit):
        return self._set_info_mult(info, limit) or Shorten(info, limit).run()
    
    def set_info(self, info, limit=34):
        self.gui.set_info(self._set_info_auto(info, limit))
    
    def get_value(self):
        return self.gui.get_value()
    
    def set_value(self, value):
        if value > self.gui.get_max():
            value = self.gui.get_max()
        self.gui.set_value(value)
    
    def inc(self):
        value = self.gui.get_value() + 1
        self.set_value(value)
    
    def get_max(self):
        return self.gui.get_max()
    
    def set_max(self, value):
        f = '[shared] graphics.progress_bar.controller.ProgressBar.set_max'
        value = Input(f, value).get_integer()
        self.gui.set_max(value)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()

    def update(self):
        self.gui.update()


PROGRESS = ProgressBar()
