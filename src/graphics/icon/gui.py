#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtGui import QIcon


class Icon:
    
    def get(self, path):
        return QIcon(path)
