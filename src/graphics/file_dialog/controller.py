#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms
import skl_shared_qt.logic as lg
import skl_shared_qt.graphics.file_dialog.gui as gi


class FileDialog:
    
    def __init__(self):
        self.filter = _('All files (*.*)')
        self.caption = _('Save File As:')
        self.folder = ''
    
    def reset(self, folder='', filter_=_('All files (*.*)'), caption=_('Save File As:')):
        self.folder = folder
        self.filter = filter_
        self.caption = caption
        self.set_folder()
    
    def set_folder(self):
        if not self.folder or not lg.Directory(self.folder).Success:
            self.folder = lg.Home().get_home()
    
    def save(self):
        f = '[SharedQt] graphics.file_dialog.controller.FileDialog.save'
        try:
            file = gi.save (caption = self.caption, folder = self.folder
                           ,filter_ = self.filter)
        except Exception as e:
            file = ''
            ms.rep.third_party(f, e)
        return file


FILE_DIALOG = FileDialog()
