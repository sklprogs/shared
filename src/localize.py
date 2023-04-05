#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import gettext

import skl_shared_qt.gettext_windows
skl_shared_qt.gettext_windows.setup_env()


class Localization:
    
    def __init__(self):
        ''' #NOTE: - do not localize messages in this class
                   - do not use shared functions
        '''
        self.Success = True
        self.iloc = None
        self.load()
    
    def translate(self,string):
        if not self.Success:
            return string
        try:
            return self.iloc.gettext(string)
        except Exception as e:
            ''' #NOTE: Do not set 'self.Success' here, we need an original
                input upon a failure.
            '''
            mes = 'Operation has failed!\n\nDetails: {}'.format(e)
            print(mes)
            return string
    
    def load(self):
        if not self.Success:
            print('Failed to localize the app!')
            return
        prefix = os.path.dirname(sys.argv[0])
        path = os.path.join(prefix,'..','resources','locale')
        path = os.path.realpath(path)
        print('Search the translation file in "{}"'.format(path))
        try:
            self.iloc = gettext.translation('transl',path)
        except Exception as e:
            self.Success = False                
            e = str(e)
            if 'No translation file found' in e:
                mes = 'No translation file has been found'
            else:
                mes = 'Operation has failed!\n\nDetails: {}'.format(e)
            print(mes)


_ = Localization().translate
