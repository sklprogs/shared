#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.rewrite import rewrite


class Read:

    def __init__(self, file, Empty=False):
        self.set_values()
        self.file = file
        self.Empty = Empty
        self.check()
    
    def set_values(self):
        self.Success = True
        self.Empty = False
        self.text = ''
        self.file = ''
        self.lst = []
    
    def check(self):
        f = '[shared] text_file.Read.check'
        if not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_warning()
            return
        if not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            Message(f, mes, True).show_warning()
            return
        if not os.path.isfile(self.file):
            self.Success = False
            mes = _('The object "{}" is not a file!').format(self.file)
            Message(f, mes, True).show_warning()
        return True

    def _read(self, encoding):
        f = '[shared] text_file.Read._read'
        try:
            with open(self.file, 'r', encoding=encoding) as fl:
                self.text = fl.read()
        except Exception as e:
            # Avoid UnicodeDecodeError, access errors, etc.
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_warning()

    def delete_bom(self):
        f = '[shared] text_file.Read.delete_bom'
        if not self.Success:
            rep.cancel(f)
            return
        self.text = self.text.replace('\N{ZERO WIDTH NO-BREAK SPACE}', '')

    def get(self):
        # Return the text from memory (or load the file first)
        f = '[shared] text_file.Read.get'
        if not self.Success:
            rep.cancel(f)
            return self.text
        if not self.text:
            self.load()
        return self.text

    def get_lines(self):
        # Return a number of lines in the file. Returns 0 for an empty file.
        f = '[shared] text_file.Read.get_lines'
        if not self.Success:
            rep.cancel(f)
            return
        return len(self.get_list())

    def get_list(self):
        f = '[shared] text_file.Read.get_list'
        if not self.Success:
            rep.cancel(f)
            return self.lst
        if not self.lst:
            self.lst = self.get().splitlines()
        # len(None) causes an error
        return self.lst

    def load(self):
        f = '[shared] text_file.Read.load'
        if not self.Success:
            rep.cancel(f)
            return self.text
        mes = _('Load file "{}"').format(self.file)
        Message(f, mes).show_info()
        ''' We can try to define an encoding automatically, however, this often
            spoils some symbols, so we just proceed with try-except and the
            most popular encodings.
        '''
        self._read('UTF-8')
        if not self.text:
            self._read('windows-1251')
        if not self.text:
            self._read('windows-1252')
        if not self.text and not self.Empty:
            ''' The file cannot be read OR the file is empty (we usually don't
                need empty files)
                #TODO: Update the message
            '''
            self.Success = False
            mes = _('Unable to read file "{}"!').format(self.file)
            Message(f, mes, True).show_warning()
            return self.text
        self.delete_bom()
        return self.text



class Write:

    def __init__(self, file, Rewrite=False, Empty=False):
        self.set_values()
        self.file = file
        self.Rewrite = Rewrite
        self.Empty = Empty
        self.check()
    
    def set_values(self):
        self.Success = True
        self.text = ''
        self.file = ''
        self.Rewrite = False
        self.Empty = False
    
    def check(self):
        f = '[shared] text_file.Write.check'
        if not self.file:
            self.Success = False
            mes = _('Not enough input data!')
            Message(f, mes, True).show_warning()

    def _write(self, mode='w'):
        f = '[shared] text_file.Write._write'
        if mode != 'w' and mode != 'a':
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, 'a, w')
            Message(f, mes, True).show_error()
            return
        mes = _('Write file "{}"').format(self.file)
        Message(f, mes).show_info()
        try:
            with open(self.file, mode, encoding='UTF-8') as fl:
                fl.write(self.text)
        except:
            self.Success = False
            mes = _('Unable to write file "{}"!').format(self.file)
            Message(f, mes, True).show_error()
        return self.Success

    def append(self, text=''):
        f = '[shared] text_file.Write.append'
        if not self.Success:
            rep.cancel(f)
            return
        self.text = text
        if not self.text:
            ''' #TODO: In the append mode the file is created if it does not
                exist, but should we warn the user that we create it from
                scratch?
            '''
            mes = _('Not enough input data!')
            Message(f, mes, True).show_warning()
            return
        self._write('a')

    def write(self, text=''):
        f = '[shared] text_file.Write.write'
        if not self.Success:
            rep.cancel(f)
            return
        self.text = text
        if not self.text and not self.Empty:
            mes = _('Not enough input data!')
            Message(f, mes, True).show_warning()
            return
        if self.Rewrite:
            return self._write('w')
        if not rewrite(self.file):
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
            return
        return self._write('w')
