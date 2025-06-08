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
    
    def set_info(self, info):
        info = Shorten(info, 34).run()
        self.gui.set_info(info)
    
    def set_value(self, value):
        if value > self.gui.get_max():
            value = self.gui.get_max()
        self.gui.set_value(value)
    
    def inc(self):
        value = self.gui.get_value() + 1
        self.set_value(value)
    
    def set_max(self, value):
        f = '[SharedQt] graphics.progress_bar.controller.ProgressBar.set_max'
        value = Input(f, value).get_integer()
        self.gui.set_max(value)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()

    def update(self):
        self.gui.update()


PROGRESS = ProgressBar()
