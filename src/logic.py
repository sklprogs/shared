#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import skl_shared_qt.message.controller as ms

copyright = 'Copyright 2015-2024, Peter Sklyar'
license = 'GPL v.3'
email = 'skl.progs@gmail.com'

import re
import io
import os
import sys
import calendar
import datetime
import difflib
import shlex
import shutil
import ssl
import subprocess
import tempfile
import time
import termcolor
import webbrowser
# 'import urllib' does not work in Python 3, importing must be as follows:
import urllib.request, urllib.parse
import locale
from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms


gpl3_url_en = 'http://www.gnu.org/licenses/gpl.html'
gpl3_url_ru = 'http://antirao.ru/gpltrans/gplru.pdf'

nbspace = ' '

ru_alphabet = '№АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'
# Some vowels are put at the start for the faster search
ru_alphabet_low = 'аеиоубявгдёжзйклмнпрстфхцчшщыъьэю№'
lat_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
lat_alphabet_low = 'abcdefghijklmnopqrstuvwxyz'
greek_alphabet = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
greek_alphabet_low = 'αβγδεζηθικλμνξοπρστυφχψω'
other_alphabet = 'ÀÁÂÆÇÈÉÊÑÒÓÔÖŒÙÚÛÜàáâæßçèéêñòóôöœùúûü'
other_alphabet_low = 'àáâæßçèéêñòóôöœùúûü'
digits = '0123456789'

punc_array = ['.', ',', '!', '?', ':', ';']
#TODO: why there were no opening brackets?
#punc_ext_array = ['"', '”', '»', ']', '}', ')']
punc_ext_array = ['"', '“', '”', '', '«', '»', '[', ']', '{', '}', '(', ')'
                 ,'’', "'", '*'
                 ]

forbidden_win = '/\?%*:|"<>'
forbidden_lin = '/'
forbidden_mac = '/\?*:|"<>'
reserved_win = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4'
               ,'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3'
               ,'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
               ]



class FastTable:
    
    def __init__(self, iterable=[], headers=[], sep=' ', Transpose=False
                ,maxrow=0, FromEnd=False, maxrows=0, encloser='', ShowGap=True):
        # #NOTE: In case of tuple, do not forget to add commas, e.g.: ((1,),)
        self.Success = True
        self.lens = []
        self.encloser = encloser
        self.FromEnd = FromEnd
        self.headers = headers
        self.lst = iterable
        self.maxrow = maxrow
        self.maxrows = maxrows
        self.sep = sep
        self.Transpose = Transpose
        self.ShowGap = ShowGap
    
    def set_max_rows(self):
        f = '[SharedQt] logic.FastTable.set_max_rows'
        if not self.Success:
            com.cancel(f)
            return
        if self.maxrows <= 0:
            return
        mes = _('Set the max number of rows to {}').format(self.maxrows)
        ms.Message(f, mes).show_debug()
        for i in range(len(self.lst)):
            # +1 for a header
            self.lst[i] = self.lst[i][0:self.maxrows+1]
    
    def set_max_width(self):
        f = '[SharedQt] logic.FastTable.set_max_width'
        if not self.Success:
            com.cancel(f)
            return
        if self.maxrow <= 0:
            return
        mes = _('Set the max column width to {} symbols').format(self.maxrow)
        ms.Message(f, mes).show_debug()
        if self.encloser:
            max_len = self.maxrow - len(self.encloser)
            if max_len < 0:
                max_len = 0
        else:
            max_len = self.maxrow
        for i in range(len(self.lst)):
            for j in range(len(self.lst[i])):
                self.lst[i][j] = Text(str(self.lst[i][j])).shorten (max_len = max_len
                                                                   ,FromEnd = self.FromEnd
                                                                   ,ShowGap = self.ShowGap
                                                                   )
    
    def enclose(self):
        ''' Passing 'encloser' in 'Text.shorten' is not enough since it
            does not enclose items shorter than 'max_len'.
        '''
        f = '[SharedQt] logic.FastTable.enclose'
        if not self.Success:
            com.cancel(f)
            return
        if not self.enclose:
            return
        for i in range(len(self.lst)):
            j = 1
            while j < len(self.lst[i]):
                self.lst[i][j] = Text(self.lst[i][j]).enclose(self.encloser)
                j += 1
    
    def transpose(self):
        f = '[SharedQt] logic.FastTable.transpose'
        if not self.Success:
            com.cancel(f)
            return
        if self.Transpose:
            self.lst = [*zip(*self.lst)]
            # 'zip' produces tuples
            self.lst = [list(item) for item in self.lst]
    
    def set_headers(self):
        f = '[SharedQt] logic.FastTable.set_headers'
        if not self.Success:
            com.cancel(f)
            return
        if not self.headers:
            com.rep_lazy(f)
            return
        ''' If there is a condition mismatch when everything is seemingly
            correct, check that headers are provided in the form of
            ('NO1', 'NO2') instead of ('NO1, NO2').
        '''
        if len(self.headers) == len(self.lst):
            for i in range(len(self.lst)):
                self.lst[i].insert(0, self.headers[i])
        else:
            sub = '{} == {}'.format (len(self.headers)
                                    ,len(self.lst)
                                    )
            mes = _('The condition "{}" is not observed!').format(sub)
            ms.Message(f, mes, True).show_warning()
    
    def report(self):
        f = '[SharedQt] logic.FastTable.report'
        result = ''
        if not self.Success:
            com.cancel(f)
            return
        iwrite = io.StringIO()
        for j in range(len(self.lst[0])):
            for i in range(len(self.lst)):
                delta = self.lens[i] - len(self.lst[i][j])
                iwrite.write(self.lst[i][j])
                iwrite.write(' ' * delta)
                if i + 1 < len(self.lst):
                    iwrite.write(self.sep)
            iwrite.write('\n')
        result = iwrite.getvalue()
        iwrite.close()
        return result
    
    def add_gap(self):
        f = '[SharedQt] logic.FastTable.add_gap'
        if not self.Success:
            com.cancel(f)
            return
        lst = [len(item) for item in self.lst]
        if not lst:
            self.Success = False
            com.rep_empty(f)
            return
        maxl = max(lst)
        for i in range(len(self.lst)):
            delta = maxl - len(self.lst[i])
            for j in range(delta):
                self.lst[i].append('')
    
    def get_lens(self):
        f = '[SharedQt] logic.FastTable.get_lens'
        if not self.Success:
            com.cancel(f)
            return
        for item in self.lst:
            tmp = sorted(item, key=len, reverse=True)
            self.lens.append(len(tmp[0]))
    
    def make_list(self):
        f = '[SharedQt] logic.FastTable.make_list'
        if not self.Success:
            com.cancel(f)
            return
        if not self.lst:
            self.Success = False
            com.rep_empty(f)
            return
        try:
            self.lst = list(self.lst)
            for i in range(len(self.lst)):
                self.lst[i] = [str(item) for item in self.lst[i]]
        except TypeError:
            self.Success = False
            mes = _('Only iterable objects are supported!')
            ms.Message(f, mes, True).show_warning()
    
    def run(self):
        self.make_list()
        self.transpose()
        self.set_headers()
        self.set_max_rows()
        self.set_max_width()
        self.enclose()
        self.add_gap()
        self.get_lens()
        return self.report()



class Font:
    
    def __init__(self, name, xborder=0, yborder=0):
        self.set_values()
        if name:
            self.reset (name = name
                       ,xborder = xborder
                       ,yborder = yborder
                       )
    
    def set_text(self, text):
        f = '[SharedQt] logic.Font.set_text'
        if not text:
            com.rep_empty(f)
            return
        self.text = text
    
    def set_values(self):
        self.font = None
        self.family = ''
        self.name = ''
        self.text = ''
        self.size = 0
        self.height = 0
        self.width = 0
        self.xborder = 0
        self.yborder = 0
    
    def set_width(self):
        if self.width:
            self.width += self.xborder
    
    def set_height(self):
        f = '[SharedQt] logic.Font.set_height'
        if not self.set_height:
            com.rep_empty(f)
            return
        lines = len(self.text.splitlines())
        if lines:
            self.height = self.height * lines
        self.height += self.yborder
    
    def reset(self, name, xborder=0, yborder=0):
        self.set_values()
        self.name = name
        self.xborder = xborder
        self.yborder = yborder
        self.set_attr()
    
    def set_attr(self):
        f = '[SharedQt] logic.Font.set_attr'
        if not self.name:
            com.rep_empty(f)
            return
        match = re.match('([aA-zZ].*) (\d+)', self.name)
        if not match:
            message = _('Wrong input data: "{}"!').format(self.name)
            ms.Message(f, message, False).show_error()
            return
        self.family = match.group(1)
        self.size = int(match.group(2))



class OSSpecific:

    def __init__(self):
        self.name = ''

    def is_win(self):
        return 'win' in sys.platform

    def is_lin(self):
        return 'lin' in sys.platform

    def is_mac(self):
        return 'mac' in sys.platform

    def get_name(self):
        if self.name:
            return self.name
        if self.is_win():
            self.name = 'win'
        elif self.is_lin():
            self.name = 'lin'
        elif self.is_mac():
            self.name = 'mac'
        else:
            self.name = 'unknown'
        return self.name



class Launch:
    #NOTE: 'Block' works only when a 'custom_app' is set
    def __init__(self, target='', Block=False, GetOutput=False):
        self.set_values()
        self.target = target
        self.Block = Block
        # Do not shorten, Path is used further
        self.ipath = Path(self.target)
        self.ext = self.ipath.get_ext().lower()
        ''' We do not use the File class because the target can be a
            directory.
        '''
        if self.target and os.path.exists(self.target):
            self.TargetExists = True
        else:
            self.TargetExists = False
        if GetOutput:
            if Block:
                mes = _('Reading standard output is not supported in a blocking mode!')
                ms.Message(f, mes, True).show_error()
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
        f = '[SharedQt] logic.Launch.get_output'
        if not self.process or not self.process.stdout:
            com.rep_empty(f)
            return ''
        result = self.process.stdout
        result = [str(item, 'utf-8') for item in result]
        return ''.join(result)
    
    def _launch(self):
        f = '[SharedQt] logic.Launch._launch'
        if not self.custom_args:
            com.rep_empty(f)
            return
        mes = _('Custom arguments: "{}"').format(self.custom_args)
        ms.Message(f, mes).show_debug()
        try:
            # Block the script till the called program is closed
            if self.Block:
                subprocess.call(self.custom_args, self.stdout)
            else:
                self.process = subprocess.Popen (args = self.custom_args
                                                ,stdout = self.stdout
                                                )
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            ms.Message(f, mes, True).show_error()

    def _launch_lin(self):
        f = '[SharedQt] logic.Launch._launch_lin'
        try:
            os.system("xdg-open " + self.ipath.escape() + "&")
            return True
        except OSError:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            ms.Message(f, mes, True).show_error()

    def _launch_mac(self):
        f = '[SharedQt] logic.Launch._launch_mac'
        try:
            os.system("open " + self.target)
            return True
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            ms.Message(f, mes, True).show_error()

    def _launch_win(self):
        f = '[SharedQt] logic.Launch._launch_win'
        try:
            os.startfile(self.target)
            return True
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            ms.Message(f, mes, True).show_error()

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
        f = '[SharedQt] logic.Launch.launch_custom'
        if not self.TargetExists:
            com.cancel(f)
            return
        self.custom_args = [self.custom_app, self.target]
        return self._launch()

    def launch_default(self):
        f = '[SharedQt] logic.Launch.launch_default'
        if not self.TargetExists:
            com.cancel(f)
            return
        if objs.get_os().is_lin():
            return self._launch_lin()
        elif objs.os.is_mac():
            return self._launch_mac()
        elif objs.os.is_win():
            return self._launch_win()



class WriteTextFile:

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
        f = '[SharedQt] logic.WriteTextFile.check'
        if not self.file:
            self.Success = False
            mes = _('Not enough input data!')
            ms.Message(f, mes, True).show_warning()

    def _write(self, mode='w'):
        f = '[SharedQt] logic.WriteTextFile._write'
        if mode != 'w' and mode != 'a':
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode, 'a, w')
            ms.Message(f, mes, True).show_error()
            return
        mes = _('Write file "{}"').format(self.file)
        ms.Message(f, mes).show_info()
        try:
            with open(self.file, mode, encoding='UTF-8') as fl:
                fl.write(self.text)
        except:
            self.Success = False
            mes = _('Unable to write file "{}"!').format(self.file)
            ms.Message(f, mes, True).show_error()
        return self.Success

    def append(self, text=''):
        f = '[SharedQt] logic.WriteTextFile.append'
        if not self.Success:
            com.cancel(f)
            return
        self.text = text
        if not self.text:
            ''' #TODO: In the append mode the file is created if it does not
                exist, but should we warn the user that we create it from
                scratch?
            '''
            mes = _('Not enough input data!')
            ms.Message(f, mes, True).show_warning()
            return
        self._write('a')

    def write(self, text=''):
        f = '[SharedQt] logic.WriteTextFile.write'
        if not self.Success:
            com.cancel(f)
            return
        self.text = text
        if not self.text and not self.Empty:
            mes = _('Not enough input data!')
            ms.Message(f, mes, True).show_warning()
            return
        if com.rewrite (file = self.file
                       ,Rewrite = self.Rewrite
                       ):
            return self._write('w')



class ReadTextFile:

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
        f = '[SharedQt] logic.ReadTextFile.check'
        if self.file and os.path.isfile(self.file):
            pass
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            ms.Message(f, mes, True).show_warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            ms.Message(f, mes, True).show_warning()
        else:
            self.Success = False
            mes = _('Wrong input data!')
            ms.Message(f, mes, True).show_warning()

    def _read(self, encoding):
        f = '[SharedQt] logic.ReadTextFile._read'
        try:
            with open(self.file, 'r', encoding=encoding) as fl:
                self.text = fl.read()
        except Exception as e:
            # Avoid UnicodeDecodeError, access errors, etc.
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_warning()

    def delete_bom(self):
        f = '[SharedQt] logic.ReadTextFile.delete_bom'
        if not self.Success:
            com.cancel(f)
            return
        self.text = self.text.replace('\N{ZERO WIDTH NO-BREAK SPACE}', '')

    def get(self):
        # Return the text from memory (or load the file first)
        f = '[SharedQt] logic.ReadTextFile.get'
        if not self.Success:
            com.cancel(f)
            return self.text
        if not self.text:
            self.load()
        return self.text

    def get_lines(self):
        # Return a number of lines in the file. Returns 0 for an empty file.
        f = '[SharedQt] logic.ReadTextFile.get_lines'
        if not self.Success:
            com.cancel(f)
            return
        return len(self.get_list())

    def get_list(self):
        f = '[SharedQt] logic.ReadTextFile.get_list'
        if not self.Success:
            com.cancel(f)
            return self.lst
        if not self.lst:
            self.lst = self.get().splitlines()
        # len(None) causes an error
        return self.lst

    def load(self):
        f = '[SharedQt] logic.ReadTextFile.load'
        if not self.Success:
            com.cancel(f)
            return self.text
        mes = _('Load file "{}"').format(self.file)
        ms.Message(f, mes).show_info()
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
            ms.Message(f, mes, True).show_warning()
            return self.text
        self.delete_bom()
        return self.text



class Input:

    def __init__(self, title='Input', value=''):
        self.title = title
        self.value = value

    def get_float(self):
        ''' Try-except method allows to convert value from integers and strings
            (useful for configuration files).
        '''
        try:
            return float(self.value)
        except ValueError:
            mes = _('Float is required at input, but found "{}"! Return 0.0')
            mes = mes.format(self.value)
            ms.Message(self.title, mes, False).show_warning()
            self.value = 0.0
        return self.value
    
    def get_list(self):
        if not isinstance(self.value, list):
            mes = _('Wrong input data!')
            ms.Message(self.title, mes).show_warning()
            return []
        return self.value
    
    def get_integer(self, Negative=False):
        if isinstance(self.value, int):
            return self.value
        # Avoid exceptions if the input is not an integer or string
        self.value = str(self.value)
        if self.value.isdigit():
            self.value = int(self.value)
            # Too frequent, almost useless
            #mes = _('Convert "{}" to an integer').format(self.value)
            #ms.Message(self.title, mes).show_debug()
        elif Negative and re.match('-\d+$', self.value):
            ''' 'isinstance' will detect negative integers too, however, we can
                also have a string at input.
            '''
            old = self.value
            self.value = int(self.value.replace('-', '', 1))
            self.value -= self.value * 2
            mes = _('Convert "{}" to an integer').format(old)
            ms.Message(self.title, mes).show_debug()
        else:
            mes = _('Integer is required at input, but found "{}"! Return 0')
            mes = mes.format(self.value)
            ms.Message(self.title, mes, False).show_warning()
            self.value = 0
        return self.value

    # Insert '' instead of 'None' into text widgets
    def get_not_none(self):
        if not self.value:
            self.value = ''
        return self.value



class Text:

    def __init__(self, text, Auto=False):
        self.punc = ("'", '"', ',', '.', '!', '?', ';')
        self.opening = ('“', '«', '(', '{', '[')
        self.closing = ('”', '»', ')', '}', ']')
        self.text = text
        self.text = Input('Text.__init__', self.text).get_not_none()
        # This can be useful in many cases, e.g. after OCR
        if Auto:
            self.convert_line_breaks()
            self.strip_lines()
            self.delete_duplicate_line_breaks()
            self.delete_duplicate_spaces()
            self.delete_space_with_punctuation()
            ''' This is necessary even if we do strip for each line (we
                need to strip '\n' at the beginning/end).
            '''
            self.text = self.text.strip()

    def join(self, text):
        self.text = self.text.rstrip()
        text = str(text).lstrip()
        if not self.text:
            self.text = text
            return self.text
        if not text:
            return self.text
        if self.text[-1] in self.opening or text[0] in self.closing:
            self.text = self.text + text
            return self.text
        if self.text[-1] in self.punc:
            self.text += ' ' + text
            return self.text
        if text[0] in self.punc:
            self.text += text
            return self.text
        self.text += ' ' + text
        return self.text
    
    def center(self, limit):
        f = '[SharedQt] logic.Text.center'
        delta = limit - len(self.text)
        if delta < 2:
            mes = f'{limit} - {len(self.text)} > 2'
            com.rep_condition(f, mes)
            return self.text
        delta = int(delta / 2)
        self.text = delta * ' ' + self.text + delta * ' '
        return self.text
    
    def split_by_len(self, len_):
        return [self.text[i:i+len_] for i in range(0, len(self.text), len_)]
    
    def delete_embraced_figs(self):
        self.text = re.sub('\s\(\d+\)', '', self.text)
        self.text = re.sub('\s\[\d+\]', '', self.text)
        self.text = re.sub('\s\{\d+\}', '', self.text)
        return self.text
    
    def replace_sim_syms(self):
        ''' Replace Cyrillic letters with similar Latin ones. This can be
            useful for English words in mostly Russian text.
        '''
        sim_cyr = ('А', 'В', 'Е', 'К', 'Н', 'О', 'Р', 'С', 'Т', 'Х', 'а', 'е'
                  ,'о', 'р', 'с', 'у', 'х'
                  )
        sim_lat = ('A', 'B', 'E', 'K', 'H', 'O', 'P', 'C', 'T', 'X', 'a', 'e'
                  ,'o', 'p', 'c', 'y', 'x'
                  )
        for i in range(len(sim_cyr)):
            self.text = self.text.replace(sim_cyr[i], sim_lat[i])
        return self.text
    
    def has_digits(self):
        for sym in self.text:
            if sym in digits:
                return True
    
    def delete_comments(self):
        self.text = self.text.splitlines()
        self.text = [line for line in self.text \
                     if not line.startswith('#')
                    ]
        self.text = '\n'.join(self.text)
        return self.text
    
    def delete_trash(self):
        # Getting rid of some useless symbols
        self.text = self.text.replace('· ', '').replace('• ', '')
        self.text = self.text.replace('¬', '')
    
    def toggle_case(self):
        if self.text == self.text.lower():
            self.text = self.text.upper()
        else:
            self.text = self.text.lower()
        return self.text

    def replace_quotes(self):
        self.text = re.sub(r'"([a-zA-Z\d\(\[\{\(])', r'“\1', self.text)
        self.text = re.sub(r'([a-zA-Z\d\.\?\!\)])"', r'\1”', self.text)
        self.text = re.sub(r'"(\.\.\.[a-zA-Z\d])', r'“\1', self.text)
        return self.text

    def delete_space_with_figure(self):
        expr = '[-\s]\d+'
        match = re.search(expr, self.text)
        while match:
            old = self.text
            self.text = self.text.replace(match.group(0), '')
            if old == self.text:
                break
            match = re.search(expr, self.text)
        return self.text

    def get_country(self):
        if len(self.text) > 4 and self.text[-4:-2] == ', ' and \
        self.text[-1].isalpha() and self.text[-1].isupper() \
        and self.text[-2].isalpha() and self.text[-2].isupper():
            return self.text[-2:]

    def reset(self, text):
        self.text = text

    def replace_x(self):
        # \xa0 is a non-breaking space in Latin1 (ISO 8859-1)
        self.text = self.text.replace('\xa0', ' ').replace('\x07', ' ')
        return self.text

    def delete_alphabetic_numeration(self):
        #TODO: check
        my_expr = ' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
        match = re.search(my_expr, self.text)
        while match:
            self.text = self.text.replace(match.group(0), match.group(1))
            match = re.search(my_expr, self.text)
        return self.text

    def delete_embraced_text(self, opening_sym='(', closing_sym=')'):
        ''' If there are some brackets left after performing this operation,
            ensure that all of them are in the right place (even when the
            number of opening and closing brackets is the same).
        '''
        f = '[SharedQt] logic.Text.delete_embraced_text'
        if self.text.count(opening_sym) != self.text.count(closing_sym):
            mes = _('Different number of opening and closing brackets: "{}": {}; "{}": {}!')
            mes = mes.format (opening_sym
                             ,self.text.count(opening_sym)
                             ,closing_sym
                             ,self.text.count(closing_sym)
                             )
            ms.Message(f, mes, True).show_warning()
            return self.text
        opening_parentheses = []
        closing_parentheses = []
        for i in range(len(self.text)):
            if self.text[i] == opening_sym:
                opening_parentheses.append(i)
            elif self.text[i] == closing_sym:
                closing_parentheses.append(i)

        min_val = min(len(opening_parentheses), len(closing_parentheses))

        opening_parentheses = opening_parentheses[::-1]
        closing_parentheses = closing_parentheses[::-1]

        # Ignore non-matching parentheses
        i = 0
        while i < min_val:
            if opening_parentheses[i] >= closing_parentheses[i]:
                del closing_parentheses[i]
                i -= 1
                min_val -= 1
            i += 1

        self.text = list(self.text)
        for i in range(min_val):
            if opening_parentheses[i] < closing_parentheses[i]:
                self.text = self.text[0:opening_parentheses[i]] \
                          + self.text[closing_parentheses[i]+1:]
        self.text = ''.join(self.text)
        # Further steps: self.delete_duplicate_spaces(), self.text.strip()
        return self.text

    def convert_line_breaks(self):
        self.text = self.text.replace('\r\n', '\n').replace('\r', '\n')
        return self.text

    def delete_line_breaks(self, rep=' '):
        # Apply 'convert_line_breaks' first
        self.text = self.text.replace('\n', rep)
        return self.text

    def delete_duplicate_line_breaks(self):
        while '\n\n' in self.text:
            self.text = self.text.replace('\n\n', '\n')
        return self.text

    def delete_duplicate_spaces(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ', ' ')
        return self.text

    def delete_end_punc(self, Extended=False):
        ''' Delete a space and punctuation marks in the end of a line
            (useful when extracting features with CompareField).
        '''
        f = '[SharedQt] logic.Text.delete_end_punc'
        if len(self.text) <= 0:
            com.rep_empty(f)
            return self.text
        if Extended:
            while self.text[-1] == ' ' or self.text[-1] in punc_array \
            or self.text[-1] in punc_ext_array:
                self.text = self.text[:-1]
        else:
            while self.text[-1] == ' ' or self.text[-1] in punc_array:
                self.text = self.text[:-1]
        return self.text

    def delete_figures(self):
        self.text = re.sub('\d+', '', self.text)
        return self.text

    def delete_cyrillic(self):
        self.text = ''.join ([sym for sym in self.text if sym not \
                              in ru_alphabet
                             ]
                            )
        return self.text

    def delete_punctuation(self):
        for sym in punc_array:
            self.text = self.text.replace(sym, '')
        for sym in punc_ext_array:
            self.text = self.text.replace(sym, '')
        return self.text

    def delete_space_with_punctuation(self):
        # Delete duplicate spaces first
        for i in range(len(punc_array)):
            self.text = self.text.replace(' ' + punc_array[i], punc_array[i])
        self.text = self.text.replace('“ ', '“').replace(' ”', '”')
        self.text = self.text.replace('( ', '(').replace(' )', ')')
        self.text = self.text.replace('[ ', '[').replace(' ]', ']')
        self.text = self.text.replace('{ ', '{').replace(' }', '}')
        return self.text

    def extract_date(self):
        # Only for pattern '(YYYY-MM-DD)'
        expr = '\((\d\d\d\d-\d\d-\d\d)\)'
        if self.text:
            match = re.search(expr, self.text)
            if match:
                return match.group(1)

    def grow(self, max_len=20, FromEnd=False, sym=' '):
        delta = max_len - len(self.text)
        if delta > 0:
            if FromEnd:
                self.text += delta * sym
            else:
                self.text = delta * sym + self.text
        return self.text
        
    def fit(self, max_len=20, FromEnd=False, sym=' '):
        self.shorten (max_len = max_len
                     ,FromEnd = FromEnd
                     ,ShowGap = False
                     )
        self.grow (max_len = max_len
                  ,FromEnd = FromEnd
                  ,sym = sym
                  )
        return self.text

    def split_by_comma(self):
        ''' Replace commas or semicolons with line breaks or line breaks
            with commas.
        '''
        f = '[SharedQt] logic.Text.split_by_comma'
        if (';' in self.text or ',' in self.text) and '\n' in self.text:
            mes = _('Commas and/or semicolons or line breaks can be used, but not altogether!')
            ms.Message(f, mes, True).show_warning()
        elif ';' in self.text or ',' in self.text:
            self.text = self.text.replace(',', '\n')
            self.text = self.text.replace(';', '\n')
            self.strip_lines()
        elif '\n' in self.text:
            self.delete_duplicate_line_breaks()
            # Delete a line break at the beginning/end
            self.text.strip()
            self.text = self.text.splitlines()
            for i in range(len(self.text)):
                self.text[i] = self.text[i].strip()
            self.text = ', '.join(self.text)
            if self.text.endswith(', '):
                self.text = self.text.strip(', ')
        return self.text

    def str2int(self):
        f = '[SharedQt] logic.Text.str2int'
        par = 0
        try:
            par = int(self.text)
        except(ValueError, TypeError):
            mes = _('Failed to convert "{}" to an integer!').format(self.text)
            ms.Message(f, mes).show_warning()
        return par

    def str2float(self):
        f = '[SharedQt] logic.Text.str2float'
        par = 0.0
        try:
            par = float(self.text)
        except(ValueError, TypeError):
            mes = _('Failed to convert "{}" to a floating-point number!')
            mes = mes.format(self.text)
            ms.Message(f, mes).show_warning()
        return par

    def strip_lines(self):
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            self.text[i] = self.text[i].strip()
        self.text = '\n'.join(self.text)
        return self.text

    def tabs2spaces(self):
        self.text = self.text.replace('\t', ' ')
        return self.text

    def replace_yo(self):
        # This allows to shorten dictionaries
        self.text = self.text.replace('Ё', 'Е')
        self.text = self.text.replace('ё', 'е')
        return self.text

    def get_alphanum(self):
        # Delete everything but alphas and digits
        self.text = ''.join([x for x in self.text if x.isalnum()])
        return self.text
        
    def has_greek(self):
        for sym in self.text:
            if sym in greek_alphabet:
                return True
    
    def has_latin(self):
        for sym in self.text:
            if sym in lat_alphabet:
                return True
                
    def has_cyrillic(self):
        for sym in self.text:
            if sym in ru_alphabet:
                return True



class List:

    def __init__(self, lst1=[], lst2=[]):
        if lst1 is None:
            self.lst1 = []
        else:
            self.lst1 = list(lst1)
        if lst2 is None:
            self.lst2 = []
        else:
            self.lst2 = list(lst2)
    
    def split_by_item(self, item):
        f = '[SharedQt] logic.List.split_by_item'
        try:
            index_ = self.lst1.index(item)
            self.lst2 = self.lst1[index_:]
            self.lst1 = self.lst1[:index_]
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(item)
            ms.Message(f, mes).show_warning()
        return(self.lst1, self.lst2)
    
    def split_by_len(self, len_):
        # Get successive len_-sized chunks
        return [self.lst1[i:i+len_] for i in range(0, len(self.lst1), len_)]
    
    def split_by_gaps(self):
        ''' Split an integer sequence where the next item does not
            increment the preceding one.
        '''
        if len(self.lst1) <= 0:
            return self.lst1
        cuts = []
        cut = [self.lst1[0]]
        i = 1
        while i < len(self.lst1):
            if self.lst1[i-1] + 1 == self.lst1[i]:
                cut.append(self.lst1[i])
            else:
                cuts.append(cut)
                cut = [self.lst1[i]]
            i += 1
        if cut:
            cuts.append(cut)
        return cuts

    def find_by_count(self, max_count=1):
        count = 0
        old = list(self.lst1)
        start = 0
        while True:
            self.lst1 = old[start:]
            poses = self.find()
            if not poses:
                break
            count += 1
            poses[0] += start
            poses[1] += start
            start = poses[1] + 1
            if count == max_count:
                break
        self.lst1 = old
        return poses
    
    def find_all(self):
        old = list(self.lst1)
        start = 0
        poses = []
        while True:
            self.lst1 = old[start:]
            res = self.find()
            if not res:
                break
            res[0] += start
            res[1] += start
            start = res[1] + 1
            poses.append(res)
        self.lst1 = old
        return poses
    
    def find(self):
        len_ = len(self.lst2)
        for index_ in (i for i, e in enumerate(self.lst1) if e == self.lst2[0]):
            if self.lst1[index_:index_+len_] == self.lst2:
                return([index_, index_ + len_ - 1])
    
    def get_shared(self):
        return [item for item in self.lst2 if item in self.lst1]
    
    def eats(self):
        # Check if 'lst1' fully comprises 'lst2'
        for item in self.lst2:
            if not item in self.lst1:
                return False
        return True
    
    def get_duplicates_low(self):
        ''' Remove (case-insensitively) duplicate items (positioned after
            original items). Both lists must consist of strings.
        '''
        cilst = [item.lower() for item in self.lst1]
        i = len(cilst) - 1
        while i >= 0:
            ind = cilst.index(cilst[i])
            if ind < i:
                del cilst[i]
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    def delete_duplicates(self):
        # Remove duplicate items (positioned after original items)
        i = len(self.lst1) - 1
        while i >= 0:
            ind = self.lst1.index(self.lst1[i])
            if ind < i:
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    def space_items(self):
        # Add a space where necessary and convert to a string
        lst1 = [str(item) for item in self.lst1]
        lst2 = [str(item) for item in self.lst2]
        lst = lst1 + lst2
        if not lst:
            return ''
        itext = Text(lst[0])
        i = 1
        while i < len(lst):
            itext.join(lst[i])
            i += 1
        return itext.text

    def equalize(self):
        # Adjust the lists at input to have the same length
        max_range = max(len(self.lst1), len(self.lst2))
        if max_range == len(self.lst1):
            for i in range(len(self.lst1)-len(self.lst2)):
                self.lst2.append('')
        else:
            for i in range(len(self.lst2)-len(self.lst1)):
                self.lst1.append('')
        return(self.lst1, self.lst2)

    def get_diff(self):
        # Find different elements (strict order)
        # Based on http://stackoverflow.com/a/788780
        seqm = difflib.SequenceMatcher(a=self.lst1, b=self.lst2)
        output = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode != 'equal':
                output += seqm.a[a0:a1]
        return output



class Time:
    # We constantly recalculate each value because they depend on each other
    def __init__(self, tstamp=None, pattern='%Y-%m-%d'):
        self.reset (tstamp = tstamp
                   ,pattern = pattern
                   )
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Set time parameters are incorrect or not supported.\n\nDetails: {}')
        mes = mes.format(e)
        ms.Message(f, mes, True).show_error()

    def set_values(self):
        self.Success = True
        self.date = self.year = self.month_abbr = self.month_name = ''
        self.inst = None
    
    def reset(self, tstamp=None, pattern='%Y-%m-%d'):
        self.set_values()
        self.pattern = pattern
        self.tstamp = tstamp
        # Prevent recursion
        if self.tstamp is None:
            self.get_todays_date()
        else:
            self.get_instance()

    def add_days(self, days_delta):
        f = '[SharedQt] logic.Time.add_days'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.inst = self.get_instance() \
                      + datetime.timedelta(days=days_delta)
        except Exception as e:
            self.fail(f, e)

    def get_date(self):
        f = '[SharedQt] logic.Time.get_date'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.date = self.get_instance().strftime(self.pattern)
        except Exception as e:
            self.fail(f, e)
        return self.date

    def get_instance(self):
        f = '[SharedQt] logic.Time.get_instance'
        if not self.Success:
            com.cancel(f)
            return
        if self.inst is None:
            if self.tstamp is None:
                self.get_timestamp()
            try:
                self.inst = datetime.datetime.fromtimestamp(self.tstamp)
            except Exception as e:
                self.fail(f, e)
        return self.inst

    def get_timestamp(self):
        f = '[SharedQt] logic.Time.get_timestamp'
        if not self.Success:
            com.cancel(f)
            return
        if not self.date:
            self.get_date()
        try:
            self.tstamp = time.mktime(datetime.datetime.strptime(self.date, self.pattern).timetuple())
        except Exception as e:
            self.fail(f, e)
        return self.tstamp

    def is_monday(self):
        f = '[SharedQt] logic.Time.is_monday'
        if not self.Success:
            com.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        if datetime.datetime.weekday(self.inst) == 0:
            return True

    def get_month_name(self):
        f = '[SharedQt] logic.Time.get_month_name'
        if not self.Success:
            com.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        self.month_name = calendar.month_name \
                            [Text (text = self.inst.strftime("%m")
                                  ,Auto = False
                                  ).str2int()
                            ]
        return self.month_name

    def localize_month_abbr(self):
        f = '[SharedQt] logic.Time.localize_month_abbr'
        if self.month_abbr == 'Jan':
            self.month_abbr = _('Jan')
        elif self.month_abbr == 'Feb':
            self.month_abbr = _('Feb')
        elif self.month_abbr == 'Mar':
            self.month_abbr = _('Mar')
        elif self.month_abbr == 'Apr':
            self.month_abbr = _('Apr')
        elif self.month_abbr == 'May':
            self.month_abbr = _('May')
        elif self.month_abbr == 'Jun':
            self.month_abbr = _('Jun')
        elif self.month_abbr == 'Jul':
            self.month_abbr = _('Jul')
        elif self.month_abbr == 'Aug':
            self.month_abbr = _('Aug')
        elif self.month_abbr == 'Sep':
            self.month_abbr = _('Sep')
        elif self.month_abbr == 'Oct':
            self.month_abbr = _('Oct')
        elif self.month_abbr == 'Nov':
            self.month_abbr = _('Nov')
        elif self.month_abbr == 'Dec':
            self.month_abbr = _('Dec')
        else:
            mes = _('Wrong input data!')
            ms.Message(f, mes).show_warning()
        return self.month_abbr
    
    def get_month_abbr(self):
        f = '[SharedQt] logic.Time.get_month_abbr'
        if not self.Success:
            com.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        self.month_abbr = calendar.month_abbr \
                            [Text (text = self.inst.strftime("%m")
                                  ,Auto = False
                                  ).str2int()
                              ]
        return self.month_abbr

    def get_todays_date(self):
        self.inst = datetime.datetime.today()

    def get_year(self):
        f = '[SharedQt] logic.Time.get_year'
        if not self.Success:
            com.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        try:
            self.year = self.inst.strftime("%Y")
        except Exception as e:
            self.fail(f, e)
        return self.year



class File:

    def __init__(self, file, dest=None, Rewrite=False):
        f = '[SharedQt] logic.File.__init__'
        self.Success = True
        self.Rewrite = Rewrite
        self.file = file
        self.dest = dest
        # This will allow to skip some checks for destination
        if not self.dest:
            self.dest = self.file
        self.atime = ''
        self.mtime = ''
        # This already checks existence
        if self.file and os.path.isfile(self.file):
            ''' If the destination directory does not exist, this will be
                caught in try-except while copying/moving.
            '''
            if os.path.isdir(self.dest):
                self.dest = os.path.join (self.dest
                                         ,Path(self.file).basename()
                                         )
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            ms.Message(f, mes, True).show_warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            ms.Message(f, mes, True).show_warning()
        else:
            self.Success = False
            mes = _('The object "{}" is not a file!').format(self.file)
            ms.Message(f, mes, True).show_warning()

    def get_size(self, Follow=True):
        f = '[SharedQt] logic.File.get_size'
        result = 0
        if not self.Success:
            com.cancel(f)
            return
        try:
            if Follow:
                cond = not os.path.islink(self.file)
            else:
                cond = True
            if cond:
                result = os.path.getsize(self.file)
        except Exception as e:
            ''' Along with other errors, 'No such file or directory' error will
                be raised if Follow=False and this is a broken symbolic link.
            '''
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_warning()
        return result
    
    def _copy(self):
        f = '[SharedQt] logic.File._copy'
        Success = True
        mes = _('Copy "{}" to "{}"').format(self.file, self.dest)
        ms.Message(f, mes).show_info()
        try:
            shutil.copyfile(self.file, self.dest)
        except:
            Success = False
            mes = _('Failed to copy file "{}" to "{}"!')
            mes = mes.format(self.file, self.dest)
            ms.Message(f, mes, True).show_error()
        return Success

    def _move(self):
        f = '[SharedQt] logic.File._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.file, self.dest)
        ms.Message(f, mes).show_info()
        try:
            shutil.move(self.file, self.dest)
        except Exception as e:
            Success = False
            mes = _('Failed to move "{}" to "{}"!\n\nDetails: {}')
            mes = mes.format(self.file, self.dest, e)
            ms.Message(f, mes, True).show_error()
        return Success

    def get_access_time(self):
        f = '[SharedQt] logic.File.get_access_time'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.atime = os.path.getatime(self.file)
            # Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
            return self.atime
        except:
            mes = _('Failed to get the date of the file "{}"!')
            mes = mes.format(self.file)
            ms.Message(f, mes, True).show_error()

    def copy(self):
        f = '[SharedQt] logic.File.copy'
        Success = True
        if not self.Success:
            com.cancel(f)
            return
        if self.file.lower() == self.dest.lower():
            mes = _('Unable to copy the file "{}" to iself!').format(self.file)
            ms.Message(f, mes, True).show_error()
        elif com.rewrite (file = self.dest
                         ,Rewrite = self.Rewrite
                         ):
            Success = self._copy()
        else:
            mes = _('Operation has been canceled by the user.')
            ms.Message(f, mes).show_info()
        return Success

    def delete(self):
        f = '[SharedQt] logic.File.delete'
        if not self.Success:
            com.cancel(f)
            return
        mes = _('Delete "{}"').format(self.file)
        ms.Message(f, mes).show_info()
        try:
            os.remove(self.file)
            return True
        except:
            mes = _('Failed to delete file "{}"!').format(self.file)
            ms.Message(f, mes, True).show_error()

    def get_modification_time(self):
        f = '[SharedQt] logic.File.get_modification_time'
        if not self.Success:
            com.cancel(f)
            return
        try:
            self.mtime = os.path.getmtime(self.file)
            # Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
            return self.mtime
        except:
            mes = _('Failed to get the date of the file "{}"!')
            mes = mes.format(self.file)
            ms.Message(f, mes, True).show_error()

    def move(self):
        f = '[SharedQt] logic.File.move'
        Success = True
        if not self.Success:
            com.cancel(f)
            return
        if self.file.lower() == self.dest.lower():
            mes = _('Moving is not necessary, because the source and destination are identical ({}).')
            mes = mes.format(self.file)
            ms.Message(f, mes, True).show_warning()
        elif com.rewrite (file = self.dest
                         ,Rewrite = self.Rewrite
                         ):
            Success = self._move()
        else:
            mes = _('Operation has been canceled by the user.')
            ms.Message(f, mes).show_info()
        return self.Success and Success

    def set_time(self):
        f = '[SharedQt] logic.File.set_time'
        if not self.Success:
            com.cancel(f)
            return
        if not self.atime or not self.mtime:
            return
        mes = _('Change the time of the file "{}" to {}')
        mes = mes.format(self.file, (self.atime, self.mtime))
        ms.Message(f, mes).show_info()
        try:
            os.utime(self.file, (self.atime, self.mtime))
        except:
            mes = _('Failed to change the time of the file "{}" to "{}"!')
            mes = mes.format(self.file, (self.atime, self.mtime))
            ms.Message(f, mes, True).show_error()



class Path:

    def __init__(self, path):
        self.reset(path)

    def get_free_space(self):
        f = '[SharedQt] logic.Path.get_free_space'
        result = 0
        if not self.path:
            com.rep_empty(f)
            return result
        if not os.path.exists(self.path):
            mes = _('Wrong input data: "{}"!').format(self.path)
            ms.Message(f, mes, True).show_warning()
            return result
        try:
            istat = os.statvfs(self.path)
            result = istat.f_bavail * istat.f_bsize
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_error()
        return result
    
    def _split_path(self):
        if not self.split:
            self.split = os.path.splitext(self.get_basename())
        return self.split

    def get_basename(self):
        if not self.basename:
            self.basename = os.path.basename(self.path)
        return self.basename
    
    def get_basename_low(self):
        return self.get_basename().lower()

    def create(self):
        # This will recursively (by design) create self.path
        # We actually don't need to fail the class globally
        f = '[SharedQt] logic.Path.create'
        Success = True
        if not self.path:
            Success = False
            com.rep_empty(f)
            return Success
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                mes = _('Directory "{}" already exists.').format(self.path)
                ms.Message(f, mes).show_info()
            else:
                Success = False
                mes = _('The path "{}" is invalid!').format(self.path)
                ms.Message(f, mes, True).show_warning()
        else:
            mes = _('Create directory "{}"').format(self.path)
            ms.Message(f, mes).show_info()
            try:
                #TODO: consider os.mkdir
                os.makedirs(self.path)
            except:
                Success = False
                mes = _('Failed to create directory "{}"!').format(self.path)
                ms.Message(f, mes, True).show_error()
        return Success

    def delete_inappropriate_symbols(self):
        ''' These symbols may pose a problem while opening files
            #TODO: check whether this is really necessary
        '''
        return self.get_filename().replace("'", '').replace("&", '')

    def get_dirname(self):
        if not self.dirname:
            self.dirname = os.path.dirname(self.path)
        return self.dirname

    def escape(self):
        # In order to use xdg-open, we need to escape some characters first
        self.path = shlex.quote(self.path)
        return self.path

    def get_ext(self):
        # An extension with a dot
        if not self.extension:
            if len(self._split_path()) > 1:
                self.extension = self._split_path()[1]
        return self.extension
    
    def get_ext_low(self):
        return self.get_ext().lower()

    def get_filename(self):
        if not self.filename:
            if len(self._split_path()) >= 1:
                self.filename = self._split_path()[0]
        return self.filename

    def reset(self, path):
        # Prevent 'NoneType'
        if path:
            self.path = path
        else:
            self.path = ''
        ''' Building paths in Windows:
            - Use raw strings (e.g., set path as r'C:\1.txt')
            - Use os.path.join(mydir, myfile) or os.path.normpath(path)
              instead of os.path.sep
            - As an alternative, import ntpath, posixpath
        '''
        ''' We remove a separator from the end, because basename and dirname
            work differently in this case ('' and the last directory,
            correspondingly).
        '''
        if self.path != '/':
            self.path = self.path.rstrip('//')
        self.basename = self.dirname = self.extension = self.filename \
                      = self.split = self.date = ''
        self.parts = []

    def split(self):
        if self.parts:
            return self.parts
        #TODO: use os.path.split
        self.parts = self.path.split(os.path.sep)
        i = 0
        tmp_str = ''
        while i < len(self.parts):
            if self.parts[i]:
                self.parts[i] = tmp_str + self.parts[i]
                tmp_str = ''
            else:
                tmp_str += os.path.sep
                del self.parts[i]
                i -= 1
            i += 1
        return self.parts
    
    def get_absolute(self):
        return os.path.abspath(self.path)



class Directory:
    #TODO: fix: does not work with a root dir ('/')
    def __init__(self, path, dest=''):
        f = '[SharedQt] logic.Directory.__init__'
        self.set_values()
        if path:
            ''' Remove trailing slashes and follow symlinks. No error is thrown
                for broken symlinks, but further checks will fail for them.
                Failing a real path (e.g., pointing to the volume that is not
                mounted yet) is more apprehensible than failing a symlink.
            '''
            self.dir = os.path.realpath(path)
        else:
            self.dir = ''
        if dest:
            self.dest = Path(dest).path
        else:
            self.dest = self.dir
        if not os.path.isdir(self.dir):
            self.Success = False
            mes = _('Wrong input data: "{}"!').format(self.dir)
            ms.Message(f, mes, True).show_warning()
    
    def _move(self):
        f = '[SharedQt] logic.Directory._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.dir, self.dest)
        ms.Message(f, mes).show_info()
        try:
            shutil.move(self.dir, self.dest)
        except Exception as e:
            Success = False
            mes = _('Failed to move "{}" to "{}"!\n\nDetails: {}')
            mes = mes.format(self.dir, self.dest, e)
            ms.Message(f, mes, True).show_error()
        return Success

    def move(self):
        f = '[SharedQt] logic.Directory.move'
        Success = True
        if not self.Success:
            com.cancel(f)
            return
        if os.path.exists(self.dest):
            mes = _('Path "{}" already exists!').format(self.dest)
            ms.Message(f, mes).show_warning()
            Success = False
        elif self.dir.lower() == self.dest.lower():
            mes = _('Moving is not necessary, because the source and destination are identical ({}).')
            mes = mes.format(self.dir)
            ms.Message(f, mes, True).show_warning()
        else:
            Success = self._move()
        return self.Success and Success
    
    def get_subfiles(self, Follow=True):
        # Include files in subfolders
        f = '[SharedQt] logic.Directory.get_subfiles'
        if not self.Success:
            com.cancel(f)
            return []
        if self.subfiles:
            return self.subfiles
        try:
            for dirpath, dirnames, fnames \
            in os.walk(self.dir, followlinks=Follow):
                for name in fnames:
                    obj = os.path.join(dirpath, name)
                    if os.path.isfile(obj):
                        self.subfiles.append(obj)
            self.subfiles.sort(key=lambda x: x.lower())
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_error()
        return self.subfiles
    
    def get_size(self, Follow=True):
        f = '[SharedQt] logic.Directory.get_size'
        result = 0
        if not self.Success:
            return result
        try:
            for dirpath, dirnames, filenames in os.walk(self.dir):
                for name in filenames:
                    obj = os.path.join(dirpath, name)
                    if Follow:
                        cond = not os.path.islink(obj)
                    else:
                        cond = True
                    if cond:
                        result += os.path.getsize(obj)
        except Exception as e:
            ''' Along with other errors, 'No such file or directory' error will
                be raised if Follow=False and there are broken symbolic links.
            '''
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_error()
        return result
    
    def set_values(self):
        self.Success = True
        # Assigning lists must be one per line
        self.lst = []
        self.rellist = []
        self.files = []
        self.relfiles = []
        self.dirs = []
        self.reldirs = []
        self.exts = []
        self.extslow = []
        self.subfiles = []
    
    def get_ext(self): # with a dot
        f = '[SharedQt] logic.Directory.get_ext'
        if not self.Success:
            com.cancel(f)
            return self.exts
        if not self.exts:
            for file in self.get_rel_files():
                ext = Path(path=file).get_ext()
                self.exts.append(ext)
                self.extslow.append(ext.lower())
        return self.exts

    def get_ext_low(self): # with a dot
        f = '[SharedQt] logic.Directory.get_ext_low'
        if not self.Success:
            com.cancel(f)
            return self.extslow
        if not self.extslow:
            self.get_ext()
        return self.extslow

    def delete_empty(self):
        f = '[SharedQt] logic.Directory.delete_empty'
        if not self.Success:
            com.cancel(f)
            return
        # Do not delete nested folders
        if not os.listdir(self.dir):
            self.delete()
    
    def delete(self):
        f = '[SharedQt] logic.Directory.delete'
        if not self.Success:
            com.cancel(f)
            return
        mes = _('Delete "{}"').format(self.dir)
        ms.Message(f, mes).show_info()
        try:
            shutil.rmtree(self.dir)
            return True
        except:
            mes = _('Failed to delete directory "{}"! Delete it manually.')
            mes = mes.format(self.dir)
            ms.Message(f, mes, True).show_error()

    def get_rel_list(self):
        # Create a list of objects with a relative path
        f = '[SharedQt] logic.Directory.get_rel_list'
        if not self.Success:
            com.cancel(f)
            return
        if not self.rellist:
            self.get_list()
        return self.rellist

    def get_list(self):
        # Create a list of objects with an absolute path
        f = '[SharedQt] logic.Directory.get_list'
        if not self.Success:
            com.cancel(f)
            return self.lst
        if self.lst:
            return self.lst
        try:
            self.lst = os.listdir(self.dir)
        except Exception as e:
            # We can encounter, e.g., PermissionError here
            self.Success = False
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_error()
        self.lst.sort(key=lambda x: x.lower())
        self.rellist = list(self.lst)
        for i in range(len(self.lst)):
            self.lst[i] = os.path.join(self.dir, self.lst[i])
        return self.lst

    def get_rel_dirs(self):
        f = '[SharedQt] logic.Directory.get_rel_dirs'
        if not self.Success:
            com.cancel(f)
            return self.reldirs
        if not self.reldirs:
            self.dirs()
        return self.reldirs

    def get_rel_files(self):
        f = '[SharedQt] logic.Directory.get_rel_files'
        if not self.Success:
            com.cancel(f)
            return self.relfiles
        if not self.relfiles:
            self.get_files()
        return self.relfiles

    def get_dirs(self):
        # Needs absolute path
        f = '[SharedQt] logic.Directory.get_dirs'
        if not self.Success:
            com.cancel(f)
            return self.dirs
        if self.dirs:
            return self.dirs
        for i in range(len(self.get_list())):
            if os.path.isdir(self.lst[i]):
                self.dirs.append(self.lst[i])
                self.reldirs.append(self.rellist[i])
        return self.dirs

    def get_files(self):
        # Needs absolute path
        f = '[SharedQt] logic.Directory.get_files'
        if not self.Success:
            com.cancel(f)
            return self.files
        if self.files:
            return self.files
        for i in range(len(self.get_list())):
            if os.path.isfile(self.lst[i]):
                self.files.append(self.lst[i])
                self.relfiles.append(self.rellist[i])
        return self.files

    def copy(self):
        f = '[SharedQt] logic.Directory.copy'
        if not self.Success:
            com.cancel(f)
            return
        if self.dir.lower() == self.dest.lower():
            mes = _('Unable to copy "{}" to iself!').format(self.dir)
            ms.Message(f, mes, True).show_error()
        elif os.path.isdir(self.dest):
            mes = _('Directory "{}" already exists.').format(self.dest)
            ms.Message(f, mes, True).show_info()
        else:
            self._copy()

    def _copy(self):
        f = '[SharedQt] logic.Directory._copy'
        mes = _('Copy "{}" to "{}"').format(self.dir, self.dest)
        ms.Message(f, mes).show_info()
        try:
            shutil.copytree(self.dir, self.dest)
        except:
            self.Success = False
            mes = _('Failed to copy "{}" to "{}"!').format(self.dir, self.dest)
            ms.Message(f, mes, True).show_error()



class Online:
    ''' If you get 'TypeError("quote_from_bytes() expected bytes")', then you
        probably forgot to call 'self.reset' here or in children classes.
    '''
    def __init__(self, base='%s', pattern='', coding='UTF-8'):
        self.reset (base = base
                   ,pattern = pattern
                   ,coding = coding
                   )

    def get_bytes(self):
        if not self.bytes:
            self.bytes = bytes(self.pattern, encoding=self.coding)
        return self.bytes

    # Open a URL in a default browser
    def browse(self):
        f = '[SharedQt] logic.Online.browse'
        try:
            webbrowser.open (url = self.get_url()
                            ,new = 2
                            ,autoraise = True
                            )
        except Exception as e:
            mes = _('Failed to open URL "{}" in a default browser!\n\nDetails: {}')
            mes = mes.format(self.url, e)
            ms.Message(f, mes, True).show_error()

    # Create a correct online link (URI => URL)
    def get_url(self):
        f = '[SharedQt] logic.Online.get_url'
        if not self.url:
            self.url = self.base % urllib.parse.quote(self.get_bytes())
            mes = str(self.url)
            ms.Message(f, mes).show_debug()
        return self.url

    def reset(self, base='', pattern='', coding='UTF-8'):
        self.bytes = None
        self.url = None
        self.coding = coding
        self.base = base
        self.pattern = pattern



class Email:
    ''' Invoke a default email client with the required input.
        Since there is no conventional way to programatically add an attachment
        in the default email client, we attempt to call Thunderbird, then
        Outlook, and finally mailto.
        Using 'webbrowser.open' has the following shortcomings:
        - a web browser is used to parse 'mailto' (we need to launch it first);
        - instead of passing arguments to a mail agent, the web browser can
          search all input online which is a security breach;
        - (AFAIK) using this method, there is no standard way to add an
          attachment. Currently, I managed to add attachments only using
          CentOS6 + Palemoon + Thunderbird.
    '''
    def __init__(self, email='', subject='', message='', attach=''):
        if email:
            self.reset (email = email
                       ,subject = subject
                       ,message = message
                       ,attach = attach
                       )
    
    def reset(self, email, subject='', message='', attach=''):
        f = '[SharedQt] logic.Email.reset'
        self.Success = True
        ''' A single address or multiple comma-separated addresses (not all
            mail agents support ';'). #NOTE that, however, Outlook supports
            ONLY ';' and Evolution - only ','!
        '''
        self.email = email
        self.subject = Input(f, subject).get_not_none()
        self.message = Input(f, message).get_not_none()
        self.attach = attach
        if not self.email:
            self.Success = False
            com.rep_empty(f)
        if self.attach:
            self.Success = File(file=self.attach).Success
            if not self.Success:
                com.cancel(f)

    def sanitize(self, value):
        # Escape symbols that may cause problems when composing 'mailto'
        f = '[SharedQt] logic.Email.sanitize'
        if not self.Success:
            com.cancel(f)
            return
        return str(Online(pattern=value).get_url())
    
    def browser(self):
        f = '[SharedQt] logic.Email.browser'
        if not self.Success:
            com.cancel(f)
            return
        try:
            if self.attach:
                ''' - This is the last resort. Attaching a file worked for
                      me only with CentOS6 + Palemoon + Thunderbird. Using
                      another OS/browser/email client will probably call a
                      default email client without the attachment.
                    - Quotes are necessary for attachments only, they will
                      stay visible otherwise.
                '''
                webbrowser.open ('mailto:%s?subject=%s&body=%s&attach="%s"'\
                                % (self.email, self.subject, self.message
                                  ,self.attach
                                  )
                                )
            else:
                webbrowser.open ('mailto:%s?subject=%s&body=%s' \
                                % (self.email, self.subject, self.message)
                                )
        except:
            mes = _('Failed to load an e-mail client.')
            ms.Message(f, mes, True).show_error()
    
    def create(self):
        f = '[SharedQt] logic.Email.create'
        if not self.Success:
            com.cancel(f)
            return
        if not self.run_evolution() and not self.run_thunderbird() \
        and not self.run_outlook():
            self.subject = self.sanitize(self.subject)
            self.message = self.sanitize(self.message)
            self.attach = self.sanitize(self.attach)
            self.browser()
                       
    def run_outlook(self):
        #NOTE: this does not work in wine!
        f = '[SharedQt] logic.Email.run_outlook'
        if not objs.get_os().is_win():
            mes = _('This operation cannot be executed on your operating system.')
            ms.Message(f, mes, True).show_info()
            return
        try:
            import win32com.client
            #https://stackoverflow.com/a/51993450
            outlook = win32com.client.dynamic.Dispatch('outlook.application')
            mail = outlook.CreateItem(0)
            mail.To = self.email.replace(',', ';')
            mail.Subject = self.subject
            mail.HtmlBody = '<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">%s</body></html>'\
                            % self.message
            if self.attach:
                mail.Attachments.Add(self.attach)
            mail.Display(True)
            return True
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            ms.Message(f, mes, True).show_error()
    
    def run_thunderbird(self):
        f = '[SharedQt] logic.Email.run_thunderbird'
        if not self.Success:
            com.cancel(f)
            return
        app = '/usr/bin/thunderbird'
        if not os.path.isfile(app):
            return
        if self.attach:
            self.custom_args = [app, '-compose', "to='%s',subject='%s',body='%s',attachment='%s'"\
                               % (self.email, self.subject
                                 ,self.message, self.attach
                                 )
                               ]
        else:
            self.custom_args = [app, '-compose', "to='%s',subject='%s',body='%s'"\
                               % (self.email, self.subject
                                 ,self.message
                                 )
                               ]
        try:
            subprocess.Popen(self.custom_args)
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            ms.Message(f, mes, True).show_error()
    
    def run_evolution(self):
        f = '[SharedQt] logic.Email.run_evolution'
        if not self.Success:
            com.cancel(f)
            return
        app = '/usr/bin/evolution'
        if not os.path.isfile(app):
            return
        if self.attach:
            self.custom_args = [app, 'mailto:%s?subject=%s&body=%s&attach=%s'\
                               % (self.email.replace(';', ','), self.subject
                                 ,self.message, self.attach
                                 )
                               ]
        else:
            self.custom_args = [app, 'mailto:%s?subject=%s&body=%s'\
                               % (self.email.replace(';', ','), self.subject
                                 ,self.message
                                 )
                               ]
        try:
            subprocess.Popen(self.custom_args)
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            ms.Message(f, mes, True).show_error()



class Search:

    def __init__(self, text=None, pattern=None):
        self.Success = False
        self.i = 0
        self.nextloop = []
        self.prevloop = []
        if text and pattern:
            self.reset (text = text
                       ,pattern = pattern
                       )

    def reset(self, text, pattern):
        f = '[SharedQt] logic.Search.reset'
        self.Success = True
        self.i = 0
        self.nextloop = []
        self.prevloop = []
        self.text = text
        self.pattern = pattern
        if not self.pattern or not self.text:
            self.Success = False
            mes = _('Wrong input data!')
            ms.Message(f, mes).show_warning()

    def add(self):
        f = '[SharedQt] logic.Search.add'
        if not self.Success:
            com.cancel(f)
            return
        if len(self.text) > self.i + len(self.pattern) - 1:
            self.i += len(self.pattern)

    def get_next(self):
        f = '[SharedQt] logic.Search.get_next'
        if not self.Success:
            com.cancel(f)
            return
        result = self.text.find(self.pattern, self.i)
        if result != -1:
            self.i = result
            self.add()
            # Do not allow -1 as output
            return result

    def get_prev(self):
        f = '[SharedQt] logic.Search.get_prev'
        if not self.Success:
            com.cancel(f)
            return
        ''' rfind, unlike find, does not include limits, so we can use it to
            search backwards.
        '''
        result = self.text.rfind(self.pattern, 0, self.i)
        if result != -1:
            self.i = result
        return result

    def get_next_loop(self):
        f = '[SharedQt] logic.Search.get_next_loop'
        if not self.Success:
            com.cancel(f)
            return self.nextloop
        if self.nextloop:
            return self.nextloop
        self.i = 0
        while True:
            result = self.get_next()
            if result is None:
                break
            else:
                self.nextloop.append(result)
        return self.nextloop

    def get_prev_loop(self):
        f = '[SharedQt] logic.Search.get_prev_loop'
        if not self.Success:
            com.cancel(f)
            return self.prevloop
        if self.prevloop:
            return self.prevloop
        self.i = len(self.text)
        while True:
            result = self.get_prev()
            if result is None:
                break
            else:
                self.prevloop.append(result)
        return self.prevloop



class Objects:
    ''' Values here will be kept through different modules (but not through
        different programs all of them using 'shared.py').
    '''
    def __init__(self):
        self.pretty_table = self.pdir = self.online = self.tmpfile = self.os \
                          = self.mes = None
        self.icon = ''
    
    def get_os(self):
        if self.os is None:
            self.os = OSSpecific()
        return self.os
    
    def get_tmpfile(self, suffix='.htm', Delete=0):
        if self.tmpfile is None:
            self.tmpfile = com.get_tmpfile (suffix = suffix
                                           ,Delete = Delete
                                           )
        return self.tmpfile
    
    def get_online(self):
        if self.online is None:
            self.online = Online()
        return self.online
    
    def get_pdir(self):
        if not self.pdir:
            self.pdir = ProgramDir()
        return self.pdir



class ProgramDir:

    def __init__(self):
        self.dir = sys.path[0]
        # We run app, not interpreter
        if os.path.isfile(self.dir):
            self.dir = Path(path=self.dir).get_dirname()

    def add(self, *args):
        return os.path.join(self.dir, *args)



class Timer:

    def __init__(self, func_title='__main__'):
        self.startv = 0
        self.func_title = func_title

    def start(self):
        self.startv = time.time()

    def end(self):
        delta = float(time.time() - self.startv)
        mes = _('The operation has taken {} s.').format(delta)
        ms.Message(self.func_title, mes).show_debug()
        return delta



class Get:
    
    def __init__ (self, url, coding='UTF-8', Verbose=True, Verify=False
                 ,timeout=6
                 ):
        self.html = ''
        self.timeout = timeout
        self.url = url
        self.coding = coding
        self.Verbose = Verbose
        self.Verify = Verify
        self.use_unverified()
    
    def read(self):
        ''' This is a dummy function to return the final result. It is needed
            merely to use 'json' which calls 'read' for input object.
        '''
        return self.html
    
    def use_unverified(self):
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        f = '[SharedQt] logic.Get.unverified'
        if not self.Verify:
            if hasattr(ssl, '_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            else:
                mes = _('Unable to use unverified certificates!')
                ms.Message(f, mes).show_warning()
        
    def _get(self):
        ''' Changing UA allows us to avoid a bot protection
            ('Error 403: Forbidden').
        '''
        f = '[SharedQt] logic.Get._get'
        try:
            req = urllib.request.Request (url = self.url
                                         ,data = None
                                         ,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
                                         )
            self.html = urllib.request.urlopen(req, timeout=self.timeout).read()
            if self.Verbose:
                mes = _('[OK]: "{}"').format(self.url)
                ms.Message(f, mes).show_info()
        # Too many possible exceptions
        except Exception as e:
            mes = _('[FAILED]: "{}". Details: {}').format(self.url, e)
            ms.Message(f, mes).show_warning()
    
    def decode(self):
        ''' Set 'coding' to None to cancel decoding. This is useful if we are
            downloading a non-text content.
        '''
        f = '[SharedQt] logic.Get.decode'
        if not self.coding:
            return self.html
        if not self.html:
            com.rep_empty(f)
            return
        try:
            self.html = self.html.decode(encoding=self.coding)
        except UnicodeDecodeError:
            self.html = str(self.html)
            mes = _('Unable to decode "{}"!').format(self.url)
            ms.Message(f, mes).show_warning()
    
    def run(self):
        f = '[SharedQt] logic.Get.run'
        if not self.url:
            com.rep_empty(f)
            return
        # Safely use URL as a string
        if not isinstance(self.url, str):
            mes = _('Wrong input data: {}!').format(self.url)
            ms.Message(f, mes, True).show_warning()
            return
        if self.Verbose:
            timer = Timer(f)
            timer.start()
        self._get()
        self.decode()
        if self.Verbose:
            timer.end()
        return self.html



class Home:

    def __init__(self, app_name='myapp'):
        self.appname = app_name
        self.confdir = self.sharedir = ''
        
    def add_share(self, *args):
        return os.path.join(self.get_share_dir(), *args)
    
    def create_share(self):
        return Path(path=self.get_share_dir()).create()
    
    def get_share_dir(self):
        if not self.sharedir:
            if objs.get_os().is_win():
                os_folder = 'Application Data'
            else:
                os_folder = os.path.join('.local', 'share')
            self.sharedir = os.path.join (self.get_home()
                                         ,os_folder
                                         ,self.appname
                                         )
        return self.sharedir
    
    def create_conf(self):
        return Path(path=self.get_conf_dir()).create()
    
    def get_home(self):
        return os.path.expanduser('~')
        
    def get_conf_dir(self):
        if not self.confdir:
            if objs.get_os().is_win():
                os_folder = 'Application Data'
            else:
                os_folder = '.config'
            self.confdir = os.path.join (self.get_home()
                                        ,os_folder
                                        ,self.appname
                                        )
        return self.confdir
    
    def add(self, *args):
        return os.path.join(self.get_home(), *args)
    
    def add_config(self, *args):
        return os.path.join(self.get_conf_dir(), *args)



class Commands:

    def __init__(self):
        self.lang = 'en'
        self.license_url = gpl3_url_en
        self.set_lang()
    
    def get_additives(self, number):
        f = '[SharedQt] logic.Commands.get_additives'
        ''' Return integers by which a set integer is divisible (except for 1
            and itself).
        '''
        if not str(number).isdigit():
            mes = _('Wrong input data: "{}"!').format(number)
            ms.Message(f, mes, True).show_warning()
            return []
        result = []
        i = 2
        while i < number:
            if number % i == 0:
                result.append(i)
            i += 1
        return result
    
    def set_figure_commas(self, figure):
        figure = str(figure)
        if figure.startswith('-'):
            Minus = True
            figure = figure[1:]
        else:
            Minus = False
        if figure.isdigit():
            figure = list(figure)
            figure = figure[::-1]
            i = 0
            while i < len(figure):
                if (i + 1) % 4 == 0:
                    figure.insert(i, _(','))
                i += 1
            figure = figure[::-1]
            figure = ''.join(figure)
        if Minus:
            figure = '-' + figure
        return figure
    
    def rep_failed(self, f='Logic error', e='Logic error', Graphical=True):
        mes = _('Operation has failed!\n\nDetails: {}').format(e)
        ms.Message(f, mes, Graphical).show_error()
    
    def rep_lazy(self, func=_('Logic error!')):
        ms.Message(func, _('Nothing to do!')).show_debug()
    
    def get_human_size(self, bsize, LargeOnly=False):
        # IEC standard
        result = '0 {}'.format(_('B'))
        if not bsize:
            return result
        tebibytes = bsize // pow(2, 40)
        cursize = tebibytes * pow(2, 40)
        gibibytes = (bsize - cursize) // pow(2, 30)
        cursize += gibibytes * pow(2, 30)
        mebibytes = (bsize - cursize) // pow(2, 20)
        cursize += mebibytes * pow(2, 20)
        kibibytes = (bsize - cursize) // pow(2, 10)
        cursize += kibibytes * pow(2, 10)
        rbytes = bsize - cursize
        mes = []
        if tebibytes:
            mes.append('%d %s' % (tebibytes, _('TiB')))
        if gibibytes:
            mes.append('%d %s' % (gibibytes, _('GiB')))
        if mebibytes:
            mes.append('%d %s' % (mebibytes, _('MiB')))
        if not (LargeOnly and bsize // pow(2, 20)):
            if kibibytes:
                mes.append('%d %s' % (kibibytes, _('KiB')))
            if rbytes:
                mes.append('%d %s' % (rbytes, _('B')))
        if mes:
            result = ' '.join(mes)
        return result
    
    def split_time(self, length=0):
        hours = length // 3600
        all_sec = hours * 3600
        minutes = (length - all_sec) // 60
        all_sec += minutes * 60
        seconds = length - all_sec
        return(hours, minutes, seconds)
    
    def get_easy_time(self, length=0):
        f = '[SharedQt] logic.Commands.get_easy_time'
        if not length:
            com.rep_empty(f)
            return '00:00:00'
        hours, minutes, seconds = self.split_time(length)
        mes = []
        if hours:
            mes.append(str(hours))
        item = str(minutes)
        if hours and len(item) == 1:
            item = '0' + item
        mes.append(item)
        item = str(seconds)
        if len(item) == 1:
            item = '0' + item
        mes.append(item)
        return ':'.join(mes)
    
    def get_yt_date(self, date):
        # Convert a date provided by Youtube API to a timestamp
        f = '[SharedQt] logic.Commands.get_yt_date'
        if not date:
            self.rep_empty(f)
            return
        pattern = '%Y-%m-%dT%H:%M:%S'
        itime = Time(pattern=pattern)
        # Prevent errors caused by 'datetime' parsing microseconds
        tmp = date.split('.')
        if date != tmp[0]:
            index_ = date.index('.'+tmp[-1])
            date = date[0:index_]
        ''' Sometimes Youtube returns excessive data that are not converted
            properly by 'datetime'.
        '''
        try:
            index_ = date.index('Z')
            date = date[:index_]
        except ValueError:
            pass
        try:
            itime.inst = datetime.datetime.strptime(date, pattern)
        except ValueError:
            mes = _('Wrong input data: "{}"!').format(date)
            ms.Message(f, mes, True).show_warning()
        return itime.get_timestamp()
    
    def get_yt_length(self, length):
        ''' Convert a length of a video provided by Youtube API (string)
            to seconds.
            Possible variants: PT%dM%dS, PT%dH%dM%dS, P%dDT%dH%dM%dS.
        '''
        f = '[SharedQt] logic.Commands.get_yt_length'
        if not length:
            self.rep_empty(f)
            return 0
        if not isinstance(length, str) or length[0] != 'P':
            mes = _('Wrong input data: "{}"!').format(length)
            ms.Message(f, mes, True).show_warning()
            return 0
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        match = re.search(r'(\d+)D', length)
        if match:
            days = int(match.group(1))
        match = re.search(r'(\d+)H', length)
        if match:
            hours = int(match.group(1))
        match = re.search(r'(\d+)M', length)
        if match:
            minutes = int(match.group(1))
        match = re.search(r'(\d+)S', length)
        if match:
            seconds = int(match.group(1))
        result = days * 86400 + hours * 3600 + minutes * 60 + seconds
        return result
    
    def rewrite(self, file, Rewrite=False):
        ''' - We do not put this into File class because we do not need
              to check existence.
            - We use 'Rewrite' just to shorten other procedures (to be
              able to use 'self.rewrite' silently in the code without
              ifs).
        '''
        f = '[SharedQt] logic.Commands.rewrite'
        if not Rewrite and os.path.isfile(file):
            ''' We don't actually need to force rewriting or delete
                the file before rewriting.
            '''
            mes = _('ATTENTION: Do yo really want to rewrite file "{}"?')
            mes = mes.format(file)
            return ms.Message(f, mes, True).show_question()
        else:
            ''' We return True so we may proceed with writing
                if the file has not been found.
            '''
            return True
    
    def set_lang(self):
        f = '[SharedQt] logic.Commands.set_lang'
        result = locale.getlocale()
        if result and result[0]:
            result = result[0]
            if 'ru' in result:
                self.lang = 'ru'
                self.license_url = gpl3_url_ru
            elif 'de' in result:
                self.lang = 'de'
            elif 'es' in result:
                self.lang = 'es'
            elif 'uk' in result:
                self.lang = 'uk'
            elif 'pl' in result:
                self.lang = 'pl'
            elif 'zh' in result:
                self.lang = 'zh'
        ms.Message(f, f'{result} -> {self.lang}').show_debug()
    
    def get_tmpfile(self, suffix='.htm', Delete=0):
        return tempfile.NamedTemporaryFile (mode = 'w'
                                           ,encoding = 'UTF-8'
                                           ,suffix = suffix
                                           ,delete = Delete
                                           ).name
    
    def get_human_time(self, delta):
        f = '[SharedQt] logic.Commands.get_human_time'
        result = '%d %s' % (0, _('sec'))
        # Allows to use 'None'
        if not delta:
            self.rep_empty(f)
            return result
        if not isinstance(delta, int) and not isinstance(delta, float):
            mes = _('Wrong input data: "{}"!').format(delta)
            ms.Message(f, mes).show_warning()
            return result
        # 'datetime' will output years even for small integers
        # https://kalkulator.pro/year-to-second.html
        years = delta // 31536000.00042889
        all_sec = years * 31536000.00042889
        months = (delta - all_sec) // 2592000.0000000005
        all_sec += months * 2592000.0000000005
        weeks = (delta - all_sec) // 604800
        all_sec += weeks * 604800
        days = (delta - all_sec) // 86400
        all_sec += days * 86400
        hours = (delta - all_sec) // 3600
        all_sec += hours * 3600
        minutes = (delta - all_sec) // 60
        all_sec += minutes * 60
        seconds = delta - all_sec
        mes = []
        if years:
            mes.append('%d %s' % (years, _('yrs')))
        if months:
            mes.append('%d %s' % (months, _('mths')))
        if weeks:
            mes.append('%d %s' % (weeks, _('wks')))
        if days:
            mes.append('%d %s' % (days, _('days')))
        if hours:
            mes.append('%d %s' % (hours, _('hrs')))
        if minutes:
            mes.append('%d %s' % (minutes, _('min')))
        if seconds:
            mes.append('%d %s' % (seconds, _('sec')))
        if mes:
            result = ' '.join(mes)
        return result
    
    def cancel(self, func=_('Logic error!')):
        ms.Message(func, _('Operation has been canceled.')).show_warning()
    
    def rep_input(self, func=_('Logic error!')):
        ms.Message(func, _('Wrong input data!')).show_warning()
    
    def rep_empty(self, func=_('Logic error!')):
        ms.Message(func, _('Empty input is not allowed!')).show_warning()
    
    def rep_not_ready(self, func=_('Logic error!')):
        ms.Message(func, _('Not implemented yet!')).show_info()
    
    def rep_out(self, func=_('Logic error!')):
        ms.Message(func, _('Empty output is not allowed!')).show_warning()
    
    def rep_deleted(self, func=_('Logic error!'), count=0):
        if count:
            message = _('{} blocks have been deleted').format(count)
            ms.Message(func, message).show_debug()
    
    def rep_matches(self, func=_('Logic error!'), count=0):
        if count:
            message = _('{} matches').format(count)
            ms.Message(func, message).show_debug()
    
    def rep_third_party(self, func=_('Logic error!'), message=_('Logic error!')):
        mes = _('Third-party module has failed!\n\nDetails: {}').format(message)
        ms.Message(func, mes, False).show_error()
    
    def rep_condition(self, func=_('Logic error!'), message=_('Logic error!')):
        message = _('The condition "{}" is not observed!').format(message)
        ms.Message(func, message, False).show_warning()


objs = Objects()
com = Commands()


if __name__ == '__main__':
    f = '[SharedQt] logic.__main__'
    ReadTextFile('/tmp/aaa').get()
