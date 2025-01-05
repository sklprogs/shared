#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
from PyQt6.QtWidgets import QApplication


class Root:
    
    def __init__(self):
        self.widget = QApplication(sys.argv)
    
    def get_clipboard(self):
        return self.widget.clipboard()
    
    def end(self):
        sys.exit(self.widget.exec())
    
    def process_events(self):
        self.widget.processEvents()
    
    def set_icon(self, qicon):
        # None is not allowed
        self.widget.setWindowIcon(qicon)
