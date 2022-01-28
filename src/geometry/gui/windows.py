#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import win32gui
import win32con


class Geometry:
    
    def __init__(self,parent):
        self.parent = parent
    
    def enumerate(self,callback,keyword):
        win32gui.EnumWindows(callback,keyword)
    
    def get_title(self,handle):
        return win32gui.GetWindowText(handle)
    
    def get_handle(self,title):
        # Orphaned for now
        return win32gui.FindWindow(None,title)
    
    def focus(self):
        self.parent.widget.focus_set()
    
    def activate(self,handle=''):
        ''' It is important to choose the right flag, the window may not
            be shown otherwise.
        '''
        if win32gui.GetWindowPlacement(handle)[1] == win32con.SW_SHOWMINIMIZED:
            win32gui.ShowWindow(handle,win32con.SW_RESTORE)
        else:
            win32gui.ShowWindow(handle,win32con.SW_SHOW)
        win32gui.SetForegroundWindow(handle)
    
    def maximize(self):
        self.parent.widget.wm_state(newstate='zoomed')
    
    def minimize(self):
        self.parent.widget.iconify()
    
    def update(self):
        objs.get_root().widget.update_idletasks()
    
    def set_geometry(self):
        return self.parent.widget.geometry()
    
    def restore(self,position):
        self.parent.widget.geometry(position)
