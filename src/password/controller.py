#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh

from . import gui


class Password:
    
    def __init__(self,icon=None,title=_('Set your credentials:')):
        self.icon = icon
        self.title = title
        self.gui = None
    
    def interrupt(self,event=None):
        self.close()
        self.reset()
    
    def get_login(self):
        return self.get_gui().get_login()
    
    def get_password(self):
        return self.get_gui().get_password()
    
    def set_bindings(self):
        f = '[shared] shared.Password.set_bindings'
        if not self.gui:
            sh.com.rep_empty(f)
            return
        sh.com.bind (obj = self.gui.parent
                    ,bindings = ('<Escape>','<Control-q>','<Control-w>')
                    ,action = self.interrupt
                    )
        sh.com.bind (obj = self.gui.ent_lgn
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action = self.close
                    )
        sh.com.bind (obj = self.gui.ent_pwd
                    ,bindings = ('<Return>','<KP_Enter>')
                    ,action = self.close
                    )
        self.gui.btn_can.action = self.interrupt
        self.gui.btn_ok1.action = self.close
        self.gui.widget.protocol('WM_DELETE_WINDOW',self.interrupt)
    
    def reset(self):
        self.get_gui().reset()
    
    def get_gui(self):
        if self.gui is None:
            self.set_gui()
        return self.gui
    
    def set_gui(self):
        self.gui = gui.Password (icon = self.icon
                                ,title = self.title
                                )
        self.set_bindings()
    
    def show(self,event=None):
        # For security purposes
        self.reset()
        self.get_gui().show()
    
    def close(self,event=None):
        self.get_gui().close()


if __name__ == '__main__':
    f = '[shared] shared.__main__'
    sh.com.start()
    ipass = Password(ICON)
    ipass.show()
    login = ipass.get_login()
    password = ipass.get_password()
    mes = _('Login: "{}"').format(login)
    sh.objs.get_mes(f,mes,True).show_info()
    mes = _('Password: "{}"').format(password)
    sh.objs.get_mes(f,mes,True).show_info()
    sh.com.end()
