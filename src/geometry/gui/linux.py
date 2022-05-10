#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Geometry:
    
    def __init__(self,parent):
        self.parent = parent
    
    def enumerate(self,callback,keyword):
        # Not implemented yet
        pass
    
    def get_title(self,handle):
        # Not implemented yet
        return ''
    
    def activate(self,handle=''):
        # The input argument is for compliance with the general method
        self.parent.widget.deiconify()
        self.parent.widget.lift()
        # Cannot take focus without this, 'focus_set' is not enough
        self.parent.widget.focus_force()
    
    def get_handle(self,title):
        # Orphaned for now. Not implemented yet.
        return ''
    
    def focus(self):
        self.parent.widget.focus_set()
    
    def maximize(self):
        self.parent.widget.wm_attributes('-zoomed',True)
    
    def minimize(self):
        self.parent.widget.iconify()
    
    def update(self):
        objs.get_root().widget.update_idletasks()
    
    def set_geometry(self):
        return self.parent.widget.geometry()
    
    def restore(self,position):
        self.parent.widget.geometry(position)
