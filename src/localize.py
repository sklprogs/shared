#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import gettext


class Localization:
    
    def __init__(self):
        ''' #NOTE: - do not localize messages in this class
                   - do not use shared functions
        '''
        self.Success = True
        self.iloc    = None
        self.load()
    
    def translate(self,string):
        if self.Success:
            try:
                return self.iloc.gettext(string)
            except Exception as e:
                ''' #NOTE: Do not set 'self.Success' here, we need
                   an original input upon a failure.
                '''
                mes = 'Operation has failed!\n\nDetails: {}'
                mes = mes.format(str(e))
                print(mes)
                return string
        else:
            return string
    
    def load(self):
        if self.Success:
            path = os.path.join('..','resources','locale')
            path = os.path.realpath(path)
            try:
                self.iloc = gettext.translation('transl',path)
            except Exception as e:
                self.Success = False                
                mes = 'Operation has failed!\n\nDetails: {}'
                mes = mes.format(str(e))
                print(mes)
        else:
            print('Failed to localize the app!')


_ = Localization().translate
