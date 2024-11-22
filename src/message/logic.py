#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import termcolor


class Log:

    def __init__(self, Use=True, Short=False, limit=200):
        self.func = '[SharedQt] message.logic.Log.__init__'
        self.Success = True
        self.level = 'info'
        self.message = 'Test'
        self.count = 1
        self.Short = Short
        self.limit = limit
        if not Use:
            self.Success = False

    def _warn(self, mes):
        return termcolor.colored(mes, 'red')
    
    def _debug(self, mes):
        return termcolor.colored(mes, 'yellow')
    
    def _generate(self):
        return f'{self.count}:{self.func}:{self.level}:{self.message}'
    
    def print(self):
        f = '[SharedQt] message.logic.Log.print'
        if not self.Success:
            return
        try:
            if self.level in ('warning', 'error'):
                print(self._warn(self._generate()))
            elif self.Short:
                pass
            elif self.level == 'debug':
                print(self._debug(self._generate()))
            else:
                print(self._generate())
        except Exception as e:
            ''' Rarely somehing like "UnicodeEncodeError: 'utf-8' codec can't
                encode character '\udce9' in position 175: surrogates not
                allowed" occurs. Since there are too many Unicode exceptions to
                except, we do not specify an exception type.
            '''
            sub = f'Cannot print the message! ({e})'
            print(f'{f}:WARNING:{sub}')

    def append (self, func='[SharedQt] message.logic.Log.append', level='info'
               ,message='Test'
               ):
        if not self.Success:
            return
        if func and level and message:
            self.func = func
            self.level = level
            self.message = str(message)
            self.message = Text(self.message).shorten(self.limit)
            self.print()
            self.count += 1



class Message:

    def __init__(self, func, message, Silent=True):
        self.func = func
        self.message = message

    def show_error(self):
        log.append(self.func, 'error', self.message)
    
    def show_warning(self):
        log.append(self.func, 'warning', self.message)
    
    def show_info(self):
        log.append(self.func, 'info', self.message)
    
    def show_debug(self):
        log.append(self.func, 'debug', self.message)
    
    def show_question(self):
        log.append(self.func, 'question', self.message)
        try:
            answer = input()
        except (EOFError, KeyboardInterrupt):
            # The user pressed 'Ctrl-c' or 'Ctrl-d'
            answer = ''
        answer = answer.lower().strip()
        if answer in ('y', 'yes'):
            return True
        elif answer == 'n':
            return False
        else:
            self.show_question()
