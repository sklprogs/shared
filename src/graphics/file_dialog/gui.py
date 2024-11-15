#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QFileDialog


def save(folder, filter_, caption):
    # Empty output is ('', '')
    return QFileDialog.getSaveFileName (caption = caption, directory = folder
                                       ,filter = filter_
                                       )[0]
