#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Info:
    
    def __init__(self):
        self.message = ''
    
    def set_message(self, message):
        self.message = str(message)
    
    def show(self):
        f = '[shared] message.info.logic.Info'
        if not self.message:
            print(f, 'Empty message!')
            return
        try:
            print(self.message)
        except Exception as e:
            ''' Rarely somehing like "UnicodeEncodeError: 'utf-8' codec can't
                encode character '\udce9' in position 175: surrogates not
                allowed" occurs. Since there are too many Unicode exceptions to
                except, we do not specify an exception type.
            '''
            sub = f'Cannot print the message! ({e})'
            print(f'{f}:INFO:{sub}')
    
    def show_blocked(self):
        self.show()


INFO = Info()
