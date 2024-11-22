#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Question:
    
    def __init__(self):
        self.message = ''
    
    def set_message(self, message):
        self.message = str(message)
    
    def show(self):
        f = '[SharedQt] message.question.logic.Question'
        if not self.message:
            print(f, 'Empty message!')
            return
        try:
            answer = input(f'{self.message}: ')
            if answer.lower() in ('y', 'yes'):
                return True
            elif answer.lower() in ('n', 'no'):
                return
            else:
                #FIX: "No" is always returned
                self.show()
        except Exception as e:
            ''' Rarely somehing like "UnicodeEncodeError: 'utf-8' codec can't
                encode character '\udce9' in position 175: surrogates not
                allowed" occurs. Since there are too many Unicode exceptions to
                except, we do not specify an exception type.
            '''
            sub = f'Cannot print the message! ({e})'
            print(f'{f}:QUESTION:{sub}')
    
    def show_blocked(self):
        return self.show()


QUESTION = Question()
