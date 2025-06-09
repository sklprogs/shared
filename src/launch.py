#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import subprocess

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import OS
from skl_shared.paths import Path


class Launch:
    #NOTE: 'Block' works only when a 'custom_app' is set
    def __init__(self, target='', Block=False, GetOutput=False):
        self.set_values()
        self.target = target
        self.Block = Block
        # Do not shorten, Path is used further
        self.ipath = Path(self.target)
        self.ext = self.ipath.get_ext().lower()
        # We do not use the File class because the target can be a directory
        if self.target and os.path.exists(self.target):
            self.TargetExists = True
        else:
            self.TargetExists = False
        if GetOutput:
            if Block:
                mes = _('Reading standard output is not supported in a blocking mode!')
                Message(f, mes, True).show_error()
            else:
                self.stdout = subprocess.PIPE

    def set_values(self):
        self.custom_app = ''
        self.custom_args = []
        self.stdout = None
        self.process = None
    
    def get_output(self):
        ''' #NOTE: if the program being called is already running (and a new
            instance is not created), then the output will be provided to the
            terminal in which it is running. You may need to close the program
            first for this code to work. 
        '''
        f = '[shared] launch.Launch.get_output'
        if not self.process or not self.process.stdout:
            rep.empty(f)
            return ''
        result = self.process.stdout
        result = [str(item, 'utf-8') for item in result]
        return ''.join(result)
    
    def _launch(self):
        f = '[shared] launch.Launch._launch'
        if not self.custom_args:
            rep.empty(f)
            return
        mes = _('Custom arguments: "{}"').format(self.custom_args)
        Message(f, mes).show_debug()
        try:
            # Block the script till the called program is closed
            if self.Block:
                subprocess.call(self.custom_args, self.stdout)
            else:
                self.process = subprocess.Popen(args = self.custom_args
                                               ,stdout = self.stdout)
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            Message(f, mes, True).show_error()

    def _launch_lin(self):
        f = '[shared] launch.Launch._launch_lin'
        try:
            os.system("xdg-open " + self.ipath.escape() + "&")
            return True
        except OSError:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            Message(f, mes, True).show_error()

    def _launch_mac(self):
        f = '[shared] launch.Launch._launch_mac'
        try:
            os.system("open " + self.target)
            return True
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            Message(f, mes, True).show_error()

    def _launch_win(self):
        f = '[shared] launch.Launch._launch_win'
        try:
            os.startfile(self.target)
            return True
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            Message(f, mes, True).show_error()

    def launch_app(self, custom_app='', custom_args=[]):
        self.custom_app = custom_app
        self.custom_args = custom_args
        if self.custom_app:
            if self.custom_args and len(self.custom_args) > 0:
                self.custom_args.insert(0, self.custom_app)
                if self.TargetExists and not self.target in self.custom_args:
                    self.custom_args.append(self.target)
            else:
                self.custom_args = [self.custom_app]
        return self._launch()

    def launch_custom(self):
        f = '[shared] launch.Launch.launch_custom'
        if not self.TargetExists:
            rep.cancel(f)
            return
        self.custom_args = [self.custom_app, self.target]
        return self._launch()

    def launch_default(self):
        f = '[shared] launch.Launch.launch_default'
        if not self.TargetExists:
            rep.cancel(f)
            return
        if OS.is_lin():
            return self._launch_lin()
        elif OS.is_mac():
            return self._launch_mac()
        elif OS.is_win():
            return self._launch_win()
