#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
from skl_shared.message.controller import rep
from skl_shared.paths import Directory, Home
from skl_shared.graphics.file_dialog.gui import save as guiSave


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
        if not self.folder or not Directory(self.folder).Success:
            self.folder = Home().get_home()
    
    def save(self):
        f = '[shared] graphics.file_dialog.controller.FileDialog.save'
        try:
            file = guiSave(caption = self.caption, folder = self.folder
                          ,filter_ = self.filter)
        except Exception as e:
            file = ''
            rep.third_party(f, e)
        return file


FILE_DIALOG = FileDialog()
