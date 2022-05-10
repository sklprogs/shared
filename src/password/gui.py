#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh


class Password:
    
    def __init__(self,icon=None,title=_('Set your credentials:')):
        self.icon = icon
        self.title = title
        self.set_gui()
    
    def get_login(self):
        return self.ent_lgn.get()
    
    def get_password(self):
        return self.ent_pwd.get()
    
    def reset(self):
        self.ent_lgn.reset()
        self.ent_pwd.reset()
        self.ent_lgn.focus()
    
    def set_widgets(self):
        self.set_frames()
        self.set_labels()
        self.set_entries()
        self.set_buttons()
    
    def set_buttons(self):
        self.btn_can = sh.Button (parent = self.frm_btm
                                 ,text = _('Cancel')
                                 ,side = 'left'
                                 )
        self.btn_ok1 = sh.Button (parent = self.frm_btm
                                 ,text = _('OK')
                                 ,side = 'right'
                                 )
    
    def set_entries(self):
        self.ent_lgn = sh.Entry (parent = self.frm_rht
                                ,side = 'top'
                                ,ClearAll = True
                                )
        self.ent_pwd = sh.Entry (parent = self.frm_rht
                                ,side = 'bottom'
                                ,ClearAll = True
                                ,Password = True
                                )
    
    def set_labels(self):
        self.lbl_lgn = sh.Label (parent = self.frm_lft
                                ,text = _('Login:')
                                ,side = 'top'
                                ,fill = 'both'
                                ,expand = True
                                )
        self.lbl_pwd = sh.Label (parent = self.frm_lft
                                ,text = _('Password:')
                                ,side = 'bottom'
                                ,fill = 'both'
                                ,expand = True
                                )
    
    def set_frames(self):
        self.frm_top = sh.Frame (parent = self.parent
                                ,side = 'top'
                                )
        self.frm_btm = sh.Frame (parent = self.parent
                                ,side = 'bottom'
                                )
        self.frm_lft = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                )
        self.frm_rht = sh.Frame (parent = self.frm_top
                                ,side = 'left'
                                )
    
    def set_gui(self):
        self.parent = sh.Top (icon = self.icon
                             ,title = self.title
                             )
        self.widget = self.parent.widget
        self.set_widgets()
        self.ent_lgn.focus()
    
    def show(self,event=None):
        self.parent.show()
    
    def close(self,event=None):
        self.parent.close()