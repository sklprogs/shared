#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
from skl_shared_qt.basic_text import Shorten
from skl_shared_qt.graphics.progress_bar.gui import ProgressBar as guiProgressBar


class ProgressBar:
    
    def __init__(self, title=_('Progress:')):
        self.gui = guiProgressBar()
    
    def set_title(self, title):
        self.gui.set_title(title)
    
    def set_info(self, info):
        info = Shorten(info, 34).run()
        self.gui.set_info(info)
    
    def show(self):
        self.gui.show()
    
    def close(self):
        self.gui.close()
