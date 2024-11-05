#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms
import skl_shared_qt.clipboard.gui as gi


class Clipboard:

    def __init__(self, Silent=False):
        self.Silent = Silent
        self.gui = gi.Clipboard()

    def copy(self, text, CopyEmpty=True):
        f = '[SharedQt] graphics.clipboard.controller.Clipboard.copy'
        if not (text or CopyEmpty):
            ms.rep.empty(f)
            return
        try:
            self.gui.copy(text)
        except Exception as e:
            ms.rep.failed(f, e, self.Silent)

    def paste(self):
        f = '[SharedQt] graphics.clipboard.controller.Clipboard.paste'
        try:
            text = self.gui.paste()
        except Exception as e:
            text = ''
            ms.rep.failed(f, e, self.Silent)
        # Further possible actions: strip, delete double line breaks
        return text
