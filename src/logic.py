#!/usr/bin/python3
# -*- coding: UTF-8 -*-

copyright = 'Copyright 2015-2019, Peter Sklyar'
license   = 'GPL v.3'
email     = 'skl.progs@gmail.com'

import re
import io
import os
import sys
import configparser
import calendar
import datetime
import pickle
import shlex
import shutil
import ssl
import subprocess
import tempfile
import time
import termcolor
import webbrowser
''' 'import urllib' does not work in Python 3, importing must be as
    follows:
'''
import urllib.request, urllib.parse
import difflib
import locale
from skl_shared2.localize import _


gpl3_url_en = 'http://www.gnu.org/licenses/gpl.html'
gpl3_url_ru = 'http://antirao.ru/gpltrans/gplru.pdf'

globs = {'int':{},'bool':{},'var':{}}

nbspace = ' '

ru_alphabet        = '№АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'
# Some vowels are put at the start for the faster search
ru_alphabet_low    = 'аеиоубявгдёжзйклмнпрстфхцчшщыъьэю№'
lat_alphabet       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
lat_alphabet_low   = 'abcdefghijklmnopqrstuvwxyz'
greek_alphabet     = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
greek_alphabet_low = 'αβγδεζηθικλμνξοπρστυφχψω'
other_alphabet     = 'ÀÁÂÆÇÈÉÊÑÒÓÔÖŒÙÚÛÜàáâæßçèéêñòóôöœùúûü'
other_alphabet_low = 'àáâæßçèéêñòóôöœùúûü'
digits             = '0123456789'

SectionBooleans        = 'Boolean'
SectionBooleans_abbr   = 'bool'
SectionFloatings       = 'Floating Values'
SectionFloatings_abbr  = 'float'
SectionIntegers        = 'Integer Values'
SectionIntegers_abbr   = 'int'
SectionLinuxSettings   = 'Linux settings'
SectionMacSettings     = 'Mac settings'
SectionVariables       = 'Variables'
SectionVariables_abbr  = 'var'
SectionWindowsSettings = 'Windows settings'

punc_array      = ['.',',','!','?',':',';']
#TODO: why there were no opening brackets?
#punc_ext_array = ['"','”','»',']','}',')']
punc_ext_array  = ['"','“','”','','«','»','[',']'
                  ,'{','}','(',')','’',"'",'*'
                  ]

forbidden_win = '/\?%*:|"<>'
forbidden_lin = '/'
forbidden_mac = '/\?*:|"<>'
reserved_win  = ['CON','PRN','AUX','NUL','COM1','COM2','COM3','COM4'
                ,'COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3'
                ,'LPT4','LPT5','LPT6','LPT7','LPT8','LPT9'
                ]
config_parser = configparser.ConfigParser()



class FastTable:
    
    def __init__ (self,iterable=[]
                 ,headers=[],sep=' '
                 ,Transpose=False
                 ,maxrow=0,FromEnd=False
                 ,maxrows=0
                 ):
        ''' #NOTE: In case of tuple, do not forget to add commas,
            e.g.: ((1,),).
        '''
        self.Success   = True
        self.lens      = []
        self.lst       = iterable
        self.sep       = sep
        self.headers   = headers
        self.Transpose = Transpose
        self.FromEnd   = FromEnd
        self.maxrow    = maxrow
        self.maxrows   = maxrows
    
    def set_max_rows(self):
        f = '[shared] logic.FastTable.set_max_rows'
        if self.Success:
            if self.maxrows > 0:
                mes = _('Set the max number of rows to {}')
                mes = mes.format(self.maxrows)
                objs.get_mes(f,mes,True).show_debug()
                for i in range(len(self.lst)):
                    # +1 for a header
                    self.lst[i] = self.lst[i][0:self.maxrows+1]
        else:
            com.cancel(f)
    
    def set_max_width(self):
        f = '[shared] logic.FastTable.set_max_width'
        if self.Success:
            if self.maxrow > 0:
                mes = _('Set the max column width to {} symbols')
                mes = mes.format(self.maxrow)
                objs.get_mes(f,mes,True).show_debug()
                for i in range(len(self.lst)):
                    for j in range(len(self.lst[i])):
                        self.lst[i][j] = Text(str(self.lst[i][j])).shorten (max_len = self.maxrow
                                                                           ,FromEnd = self.FromEnd
                                                                           )
        else:
            com.cancel(f)
    
    def transpose(self):
        f = '[shared] logic.FastTable.transpose'
        if self.Success:
            if self.Transpose:
                try:
                    ''' Works only in Python >=3.5. 
                        'eval' is needed since we cannot catch
                        'SyntaxError' in runtime.
                    '''
                    self.lst = eval('[*zip(*self.lst)]')
                except SyntaxError:
                    # 10x slower (with already imported numpy)
                    try:
                        import numpy
                        self.lst = numpy.array(lst).transpose()
                    except ImportError:
                        mes = _('You need to install "{}"!')
                        mes = mes.format('numpy')
                        objs.get_mes(f,mes).show_error()
                # 'zip' produces tuples
                self.lst = [list(item) for item in self.lst]
        else:
            com.cancel(f)
    
    def set_headers(self):
        f = '[shared] logic.FastTable.set_headers'
        if self.Success:
            if self.headers:
                ''' If there is a condition mismatch when everything is
                    seemingly correct, check that headers are provided
                    in the form of ('NO1','NO2') instead of ('NO1,NO2').
                '''
                if len(self.headers) == len(self.lst):
                    for i in range(len(self.lst)):
                        self.lst[i].insert(0,self.headers[i])
                else:
                    sub = '{} == {}'.format (len(self.headers)
                                            ,len(self.lst)
                                            )
                    mes = _('The condition "{}" is not observed!')
                    mes = mes.format(sub)
                    objs.get_mes(f,mes).show_warning()
            else:
                com.rep_lazy(f)
        else:
            com.cancel(f)
    
    def report(self):
        f = '[shared] logic.FastTable.report'
        result = ''
        if self.Success:
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
        else:
            com.cancel(f)
        return result
    
    def add_gap(self):
        f = '[shared] logic.FastTable.add_gap'
        if self.Success:
            lst = [len(item) for item in self.lst]
            if lst:
                maxl = max(lst)
                for i in range(len(self.lst)):
                    delta = maxl - len(self.lst[i])
                    for j in range(delta):
                        self.lst[i].append('')
            else:
                self.Success = False
                com.rep_empty(f)
        else:
            com.cancel(f)
    
    def get_lens(self):
        f = '[shared] logic.FastTable.get_lens'
        if self.Success:
            for item in self.lst:
                tmp = sorted(item,key=len,reverse=True)
                self.lens.append(len(tmp[0]))
        else:
            com.cancel(f)
    
    def make_list(self):
        f = '[shared] logic.FastTable.make_list'
        if self.Success:
            if self.lst:
                try:
                    self.lst = list(self.lst)
                    for i in range(len(self.lst)):
                        self.lst[i] = [str(item) \
                                       for item in self.lst[i]
                                      ]
                except TypeError:
                    self.Success = False
                    mes = _('Only iterable objects are supported!')
                    objs.get_mes(f,mes).show_warning()
            else:
                self.Success = False
                com.rep_empty(f)
        else:
            com.cancel(f)
    
    def run(self):
        self.make_list()
        self.transpose()
        self.set_headers()
        self.set_max_rows()
        self.set_max_width()
        self.add_gap()
        self.get_lens()
        return self.report()



class MessageBuilder:
    
    def __init__(self,level):
        self.set_values()
        self.level = level
        self.set_icon()
    
    def set_icon(self):
        f = '[shared] logic.MessageBuilder.set_icon'
        if not self.icon:
            if self.level in (_('INFO'),_('DEBUG')):
                prefix = 'info'
            elif self.level == _('WARNING'):
                prefix = 'warning'
            elif self.level == _('QUESTION'):
                prefix = 'question'
            else:
                prefix = 'error'
            self.icon = objs.get_pdir().add('..','resources',prefix+'.gif')
        if not os.path.exists(self.icon):
            self.icon = ''
            message = _('File "{}" was not found!').format(self.icon)
            Message (func    = f
                    ,message = message
                    ).show_error()
    
    def reset(self,text='',title=''):
        self.text  = text
        self.title = title
        self.sanitize()
    
    def set_values(self):
        self.text  = ''
        self.title = ''
        self.icon  = ''
        self.level = _('INFO')
    
    def sanitize(self):
        self.title = com.sanitize(self.title) + ':'
        self.text  = com.sanitize(self.text)



class Message:

    def __init__(self,func,message,Silent=True):
        self.func    = func
        self.message = message

    def show_error(self):
        log.append (self.func
                   ,_('ERROR')
                   ,self.message
                   )
    
    def show_warning(self):
        log.append (self.func
                   ,_('WARNING')
                   ,self.message
                   )
    
    def show_info(self):
        log.append (self.func
                   ,_('INFO')
                   ,self.message
                   )
    
    def show_debug(self):
        log.append (self.func
                   ,_('DEBUG')
                   ,self.message
                   )
    
    def show_question(self):
        log.append (self.func
                   ,_('QUESTION')
                   ,self.message
                   )
        try:
            answer = input()
        except (EOFError, KeyboardInterrupt):
            # The user pressed 'Ctrl-c' or 'Ctrl-d'
            answer = ''
        answer = answer.lower().strip()
        if answer in ('y',''):
            return True
        elif answer == 'n':
            return False
        else:
            self.show_question()



class Font:
    
    def __init__(self,name,xborder=0,yborder=0):
        self.set_values()
        if name:
            self.reset (name    = name
                       ,xborder = xborder
                       ,yborder = yborder
                       )
    
    def set_text(self,text):
        f = '[shared] logic.Font.set_text'
        if text:
            self.text = text
        else:
            com.rep_empty(f)
    
    def set_values(self):
        self.font    = None
        self.family  = ''
        self.name    = ''
        self.text    = ''
        self.size    = 0
        self.height  = 0
        self.width   = 0
        self.xborder = 0
        self.yborder = 0
    
    def set_width(self):
        f = '[shared] logic.Font.set_width'
        if self.width:
            self.width += self.xborder
            '''
            Message (func    = f
                    ,message = '%d' % self.width
                    ).show_debug()
            '''
    
    def set_height(self):
        f = '[shared] logic.Font.set_height'
        if self.set_height:
            lines = len(self.text.splitlines())
            if lines:
                self.height = self.height * lines
            self.height += self.yborder
            '''
            Message (func    = f
                    ,message = '%d' % self.height
                    ).show_debug()
            '''
        else:
            com.rep_empty(f)
    
    def reset(self,name,xborder=0,yborder=0):
        self.set_values()
        self.name    = name
        self.xborder = xborder
        self.yborder = yborder
        self.set_attr()
    
    def set_attr(self):
        f = '[shared] logic.Font.set_attr'
        if self.name:
            match = re.match('([aA-zZ].*) (\d+)',self.name)
            if match:
                self.family = match.group(1)
                self.size   = int(match.group(2))
            else:
                message = _('Wrong input data: "{}"!').format(self.name)
                Message (func    = f
                        ,message = message
                        ).show_error()
        else:
            com.rep_empty(f)



class Hotkeys:
    ''' Transform tkinter bindings to a human readable form
        Use the following key names:
        http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
        #TODO: add remaining keypad key
    '''
    def __init__(self,hotkeys,sep='; '):
        self.Success = True
        self.hotkeys = hotkeys
        self.sep     = sep
        self.check()
    
    def check(self):
        f = '[shared] logic.Hotkeys.check'
        if self.hotkeys and self.sep:
            if not isinstance(self.hotkeys,str) \
            and not isinstance(self.hotkeys,tuple) \
            and not isinstance(self.hotkeys,list):
                self.Success = False
                mes = _('Wrong input data: "{}"!').format(self.hotkeys)
                objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            #TODO: do we need this warning?
            com.rep_empty(f)
    
    def _loop(self,pattern):
        self.hotkeys = [hotkey for hotkey in self.hotkeys \
                        if not pattern in hotkey
                       ]
    
    def set_keypad(self):
        ''' Both 'Return' (main key) and 'KP_Enter' (numeric keypad)
            usually do the same thing, so we just remove KP_Enter.
            The same relates to other keypad key.
        '''
        f = '[shared] logic.Hotkeys.set_keypad'
        if self.Success:
            if not isinstance(self.hotkeys,str):
                for hotkey in self.hotkeys:
                    ''' Do not use '<' and '>' signs here since
                        the combination can actually be
                        '<Control-KP_Enter>'.
                    '''
                    if 'Return' in hotkey:
                        self._loop('KP_Enter')
                    if 'Home' in hotkey:
                        self._loop('KP_Home')
                    if 'End' in hotkey:
                        self._loop('KP_End')
                    if 'Delete' in hotkey:
                        self._loop('KP_Delete')
                    if 'Insert' in hotkey:
                        self._loop('KP_Insert')
        else:
            com.cancel(f)
    
    def set_hotkeys(self):
        f = '[shared] logic.Hotkeys.set_hotkeys'
        if self.Success:
            self.hotkeys = [self.replace(hotkey) \
                            for hotkey in self.hotkeys
                           ]
            self.hotkeys = [hotkey for hotkey in self.hotkeys \
                            if hotkey
                           ]
        else:
            com.cancel(f)
    
    def run(self):
        f = '[shared] logic.Hotkeys.run'
        result = ''
        if self.Success:
            if isinstance(self.hotkeys,str):
                result = self.replace(self.hotkeys)
            else:
                self.set_keypad()
                self.set_hotkeys()
                result = self.sep.join(self.hotkeys)
        else:
            com.cancel(f)
        return result
    
    def replace(self,key):
        f = '[shared] logic.Hotkeys.replace'
        if key:
            key = key.replace('<','').replace('>','')
            key = key.replace('Left','←').replace('Right','→')
            key = key.replace ('Button-1'
                              ,_('Left mouse button')
                              )
            key = key.replace ('ButtonRelease-1'
                              ,_('Left mouse button')
                              )
            key = key.replace ('Button-2'
                              ,_('Middle mouse button')
                              )
            key = key.replace ('ButtonRelease-2'
                              ,_('Middle mouse button')
                              )
            key = key.replace ('Button-3'
                              ,_('Right mouse button')
                              )
            key = key.replace ('ButtonRelease-3'
                              ,_('Right mouse button')
                              )
            key = key.replace ('space'
                              ,_('Space')
                              )
            key = key.replace('grave','~')
            # Left and right Alt and Shift are usually interchangeable
            key = key.replace('Alt_R','Alt_L')
            key = key.replace('Alt_L','Alt')
            key = key.replace('Control_L','Control')
            key = key.replace('Control_R','Control')
            key = key.replace('Control','Ctrl')
            key = key.replace('Shift_R','Shift_L')
            key = key.replace('Shift_L','Shift')
            key = key.replace('-Key-','')
            key = key.replace('Delete','Del')
            key = key.replace('Insert','Ins')
            key = key.replace('Scroll_Lock','ScrollLock')
            key = key.replace('Print','PrintScrn')
            key = key.replace('Up','↑').replace('Down','↓')
            key = key.replace('Execute','SysReq')
            key = key.replace('Num_Lock','NumLock')
            key = key.replace('Prior','PgUp')
            key = key.replace('Next','PgDn')
            key = key.replace('Escape','Esc')
            ''' We should leave only 1 key if there are key
                both for keyboard and keypad. Thus, we generally should
                not have to use keypad key without keyboard
                analogs. If we do, we should excplicitly indicate that
                it is keypad.
            '''
            key = key.replace('KP_Delete','Del (keypad)')
            key = key.replace('KP_Divide','/ (keypad)')
            key = key.replace('KP_Down','↓ (keypad)')
            ''' '<Control-S>' actually means 'Ctrl-Shift-s' in tkinter.
                Insert 'Shift' before making key upper-case.
            '''
            match = re.match('.*-([A-Z])$',key)
            if match:
                group = match.group(1)
                key = key.replace ('-'       + group
                                  ,'-Shift-' + group
                                  )
            ''' We make letters upper-case in order to avoid confusion,
                e.g., when using 'i', 'l' and '1'.
            '''
            match = re.match('.*-([a-z])$',key)
            if match:
                group = match.group(1)
                key = key.replace ('-' + group
                                  ,'-' + group.upper()
                                  )
            #key = key.replace('-','+')
        else:
            #TODO: do we need this warning?
            self.rep_empty(f)
        return key



class OSSpecific:

    def __init__(self):
        self.name = ''
        self.import_win()

    def get_shift_tab(self):
        if self.is_lin():
            return '<Shift-ISO_Left_Tab>'
        else:
            return '<Shift-KeyPress-Tab>'

    def is_win(self):
        return 'win' in sys.platform

    def is_lin(self):
        return 'lin' in sys.platform

    def is_mac(self):
        return 'mac' in sys.platform

    def get_name(self):
        if not self.name:
            if self.is_win():
                self.name = 'win'
            elif self.is_lin():
                self.name = 'lin'
            elif self.is_mac():
                self.name = 'mac'
            else:
                self.name = 'unknown'
        return self.name

    def import_win(self):
        if self.is_win():
            #http://mail.python.org/pipermail/python-win32/2012-July/012493.html
            _tz = os.getenv('TZ')
            if _tz is not None and '/' in _tz:
                os.unsetenv('TZ')
            import pythoncom, win32com, win32com.client, win32api
            # Required by 'Geometry'
            import win32gui, win32con, ctypes
            if win32com.client.gencache.is_readonly:
                win32com.client.gencache.is_readonly = False
                ''' Under p2exe/cx_freeze the call in gencache to
                    __init__() does not happen so we use Rebuild() to
                    force the creation of the gen_py folder.
                    The contents of library.zip\win32com shall be
                    unpacked to exe.win32 - 3.3\win32com.
                    See also the section where EnsureDispatch is called.
                '''
                win32com.client.gencache.Rebuild()
            ''' 'datetime' may have to be imported last due to
                the problems with TZ.
            '''



class Launch:
    #NOTE: 'Block' works only when a 'custom_app' is set
    def __init__(self,target='',Block=False):
        self.set_values()
        self.target = target
        self.Block  = Block
        # Do not shorten, Path is used further
        self.ipath  = Path(self.target)
        self.ext    = self.ipath.get_ext().lower()
        ''' We do not use the File class because the target can be a
            directory.
        '''
        if self.target and os.path.exists(self.target):
            self.TargetExists = True
        else:
            self.TargetExists = False

    def set_values(self):
        self.custom_app  = ''
        self.custom_args = []
    
    def _launch(self):
        f = '[shared] logic.Launch._launch'
        if self.custom_args:
            mes = _('Custom arguments: "{}"').format(self.custom_args)
            objs.get_mes(f,mes,True).show_debug()
            try:
                # Block the script till the called program is closed
                if self.Block:
                    subprocess.call(self.custom_args)
                else:
                    subprocess.Popen(self.custom_args)
            except:
                mes = _('Failed to run "{}"!').format(self.custom_args)
                objs.get_mes(f,mes).show_error()
        else:
            com.rep_empty(f)

    def _launch_lin(self):
        f = '[shared] logic.Launch._launch_lin'
        try:
            os.system("xdg-open " + self.ipath.escape() + "&")
        except OSError:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.get_mes(f,mes).show_error()

    def _launch_mac(self):
        f = '[shared] logic.Launch._launch_mac'
        try:
            os.system("open " + self.target)
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.get_mes(f,mes).show_error()

    def _launch_win(self):
        f = '[shared] logic.Launch._launch_win'
        try:
            os.startfile(self.target)
        except:
            mes = _('Unable to open the file in an external program. You should probably check the file associations.')
            objs.get_mes(f,mes).show_error()

    def launch_app(self,custom_app='',custom_args=[]):
        self.custom_app  = custom_app
        self.custom_args = custom_args
        if self.custom_app:
            if self.custom_args and len(self.custom_args) > 0:
                self.custom_args.insert(0,self.custom_app)
                if self.TargetExists \
                and not self.target in self.custom_args:
                    self.custom_args.append(self.target)
            else:
                self.custom_args = [self.custom_app]
        self._launch()

    def auto(self):
        ''' Starting third-party apps instead of default ones is no
            longer supported - it introduces an excessive complexity
            and is a potential security breach (programs run by default
            are usually installed with admin rights and cannot be
            compromised).
        '''
        self.launch_default()

    def launch_custom(self):
        f = '[shared] logic.Launch.launch_custom'
        if self.TargetExists:
            self.custom_args = [self.custom_app,self.target]
            self._launch()
        else:
            com.cancel(f)

    def launch_default(self):
        f = '[shared] logic.Launch.launch_default'
        if self.TargetExists:
            if objs.get_os().is_lin():
                self._launch_lin()
            elif objs.os.is_mac():
                self._launch_mac()
            elif objs.os.is_win():
                self._launch_win()
        else:
            com.cancel(f)



class WriteTextFile:

    def __init__(self,file,Rewrite=False):
        f = '[shared] logic.WriteTextFile.__init__'
        self.file    = file
        self.text    = ''
        self.Rewrite = Rewrite
        self.Success = True
        if not self.file:
            self.Success = False
            mes = _('Not enough input data!')
            objs.get_mes(f,mes).show_warning()

    def _write(self,mode='w'):
        f = '[shared] logic.WriteTextFile._write'
        if mode == 'w' or mode == 'a':
            mes = _('Write file "{}"').format(self.file)
            objs.get_mes(f,mes,True).show_info()
            try:
                with open(self.file,mode,encoding='UTF-8') as fl:
                    fl.write(self.text)
            except:
                self.Success = False
                mes = _('Unable to write file "{}"!').format(self.file)
                objs.get_mes(f,mes).show_error()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode,'a, w')
            objs.get_mes(f,mes).show_error()

    def append(self,text=''):
        f = '[shared] logic.WriteTextFile.append'
        if self.Success:
            self.text = text
            if self.text:
                ''' #TODO: In the append mode the file is created if it
                    does not exist, but should we warn the user that we
                    create it from scratch?
                '''
                self._write('a')
            else:
                mes = _('Not enough input data!')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    def write(self,text=''):
        f = '[shared] logic.WriteTextFile.write'
        if self.Success:
            self.text = text
            if self.text:
                if com.rewrite (file    = self.file
                               ,Rewrite = self.Rewrite
                               ):
                    self._write('w')
            else:
                mes = _('Not enough input data!')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)



class Log:

    def __init__ (self,Use=True,Short=False
                 ):
        self.func    = 'shared.Log.__init__'
        self.Success = True
        self.level   = _('INFO')
        self.message = 'Test'
        self.count   = 1
        self.Short   = Short
        if not Use:
            self.Success = False

    def _warn(self,mes):
        return termcolor.colored(mes,'red')
    
    def _debug(self,mes):
        return termcolor.colored(mes,'yellow')
    
    def _generate(self):
        return '{}:{}:{}:{}'.format (self.count,self.func
                                    ,self.level,self.message
                                    )
    
    def print(self):
        f = '[shared] logic.Log.print'
        if self.Success:
            try:
                if self.level in (_('WARNING'),_('ERROR')):
                    print(self._warn(self._generate()))
                elif self.Short:
                    pass
                elif self.level == _('DEBUG'):
                    print(self._debug(self._generate()))
                else:
                    print(self._generate())
            except Exception as e:
                ''' Rarely somehing like "UnicodeEncodeError:
                    'utf-8' codec can't encode character '\udce9' in
                    position 175: surrogates not allowed" occurs.
                    Since there are to many Unicode exceptions to
                    except, we do not specify an exception type.
                '''
                sub = 'Cannot print the message! ({})'.format(e)
                mes = '{}:{}:{}'.format (f,'WARNING'
                                        ,sub
                                        )
                print(mes)

    def append (self,func='shared.Log.append'
               ,level=_('INFO'),message='Test'
               ):
        if self.Success:
            if func and level and message:
                self.func    = func
                self.level   = level
                self.message = str(message)
                self.print()
                self.count += 1



class TextDic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.iread    = ReadTextFile(self.file)
        self.reset()

    ''' This is might be needed only for those dictionaries that
        already may contain duplicates (dictionaries with newly added
        entries do not have duplicates due to new algorithms)
    '''
    def _delete_duplicates(self):
        f = '[shared] logic.TextDic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.lines()
                self.lst = list(set(self.get_list()))
                new = self.lines = len(self.lst)
                mes = _('Entries deleted: {} ({}-{})')
                mes = mes.format(old-new,old,new)
                objs.get_mes(f,mes,True).show_info()
                self.text = '\n'.join(self.lst)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] logic.TextDic._join'
        if len(self.orig) == len(self.transl):
            self.lines = len(self.orig)
            self.lst   = []
            for i in range(self.lines):
                self.lst.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self.lst)
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f,mes).show_warning()

    def _split(self):
        ''' We can use this to check integrity and/or update original
            and translation lists.
        '''
        f = '[shared] logic.TextDic._split'
        if self.get():
            self.Success = True
            self.orig    = []
            self.transl  = []
            ''' Building lists takes ~0.1 longer without temporary
                variables (now self._split() takes ~0.256)
            '''
            for i in range(self.lines):
                tmp_lst = self.lst[i].split('\t')
                if len(tmp_lst) == 2:
                    self.orig.append(tmp_lst[0])
                    self.transl.append(tmp_lst[1])
                else:
                    self.Success = False
                    # i+1: Count from 1
                    mes = _('Dictionary "{}": Incorrect line #{}: "{}"!')
                    mes = mes.format(self.file,i+1,self.lst[i])
                    objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False

    def append(self,original,translation):
        ''' #TODO: skip repetitions
            #TODO: write a dictionary in an append mode after appending
            to memory.
        '''
        f = '[shared] logic.TextDic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                com.rep_empty(f)
        else:
            com.cancel(f)

    def delete_entry(self,entry_no): # Count from 1
        ''' #TODO: #FIX: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] logic.TextDic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.get_lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.get_lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def edit_entry(self,entry_no,orig,transl): # Count from 1
        ''' #TODO: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] logic.TextDic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.get_lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.get_lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def get(self):
        if not self.text:
            self.text = self.iread.load()
        return self.text

    def get_lines(self):
        if self.lines == 0:
            self.lines = len(self.get_list())
        return self.lines

    def get_list(self):
        if not self.lst:
            self.lst = self.get().splitlines()
        return self.lst

    def reset(self):
        self.text   = self.iread.load()
        self.orig   = []
        self.transl = []
        self.lst    = self.get().splitlines()
        self.lines  = len(self.lst)
        self._split()

    # Sort a dictionary with the longest lines going first
    def sort(self):
        f = '[shared] logic.TextDic.sort'
        if self.Success:
            if self.Sortable:
                tmp_list = []
                for i in range(len(self.lst)):
                    tmp_list += [[len(self.orig[i])
                                 ,self.orig[i]
                                 ,self.transl[i]
                                 ]
                                ]
                tmp_list.sort(key=lambda x: x[0],reverse=True)
                for i in range(len(self.lst)):
                    self.orig[i]   = tmp_list[i][1]
                    self.transl[i] = tmp_list[i][2]
                    self.lst[i]    = self.orig[i] + '\t' \
                                                  + self.transl[i]
                self.text = '\n'.join(self.lst)
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    def tail(self):
        f = '[shared] logic.TextDic.tail'
        tail_text = ''
        if self.Success:
            tail_len = globs['int']['tail_len']
            if tail_len > self.get_lines():
                tail_len = self.get_lines()
            i = self.get_lines() - tail_len
            # We count from 1, therefore it is < and not <=
            while i < self.lines():
                # i+1 by the same reason
                tail_text += str(i+1) + ':' + '"' + self.get_list()[i] \
                                      + '"\n'
                i += 1
        else:
            com.cancel(f)
        return tail_text

    def write(self):
        f = '[shared] logic.TextDic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            com.cancel(f)



class ReadTextFile:

    def __init__(self,file):
        f = '[shared] logic.ReadTextFile.__init__'
        self.file    = file
        self.text    = ''
        self.lst     = []
        self.Success = True
        if self.file and os.path.isfile(self.file):
            pass
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            objs.get_mes(f,mes).show_warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            mes = _('Wrong input data!')
            objs.get_mes(f,mes).show_warning()

    def _read(self,encoding):
        try:
            with open(self.file,'r',encoding=encoding) as fl:
                self.text = fl.read()
        except:
            # Avoid UnicodeDecodeError, access errors, etc.
            pass

    def delete_bom(self):
        f = '[shared] logic.ReadTextFile.delete_bom'
        if self.Success:
            self.text = self.text.replace('\N{ZERO WIDTH NO-BREAK SPACE}','')
        else:
            com.cancel(f)

    # Return the text from memory (or load the file first)
    def get(self):
        f = '[shared] logic.ReadTextFile.get'
        if self.Success:
            if not self.text:
                self.load()
        else:
            com.cancel(f)
        return self.text

    # Return a number of lines in the file. Returns 0 for an empty file.
    def get_lines(self):
        f = '[shared] logic.ReadTextFile.get_lines'
        if self.Success:
            return len(self.get_list())
        else:
            com.cancel(f)

    def get_list(self):
        f = '[shared] logic.ReadTextFile.get_list'
        if self.Success:
            if not self.lst:
                self.lst = self.get().splitlines()
        else:
            com.cancel(f)
        # len(None) causes an error
        return self.lst

    def load(self):
        f = '[shared] logic.ReadTextFile.load'
        if self.Success:
            mes = _('Load file "{}"').format(self.file)
            Message(f,mes).show_info()
            ''' We can try to define an encoding automatically, however,
                this often spoils some symbols, so we just proceed with
                try-except and the most popular encodings.
            '''
            self._read('UTF-8')
            if not self.text:
                self._read('windows-1251')
            if not self.text:
                self._read('windows-1252')
            if not self.text:
                ''' The file cannot be read OR the file is empty (we
                    don't need empty files)
                    #TODO: Update the message
                '''
                self.Success = False
                mes = _('Unable to read file "{}"!').format(self.file)
                objs.get_mes(f,mes).show_warning()
            self.delete_bom()
        else:
            com.cancel(f)
        return self.text



class Input:

    def __init__(self,title='Input',value=''):
        self.title = title
        self.value = value

    def check_float(self):
        if isinstance(self.value,float):
            return self.value
        else:
            mes = _('Float is required at input, but found "{}"! Return 0.0')
            mes = mes.format(self.value)
            objs.get_mes(self.title,mes).show_warning()
            self.value = 0.0
        return self.value
    
    def get_list(self):
        if isinstance(self.value,list):
            return self.value
        else:
            mes = _('Wrong input data!')
            objs.get_mes(self.title,mes,True).show_warning()
            return []
    
    def get_integer(self,Negative=False):
        if isinstance(self.value,int):
            return self.value
        else:
            # Avoid exceptions if the input is not an integer or string
            self.value = str(self.value)
            if self.value.isdigit():
                self.value = int(self.value)
                # Too frequent, almost useless
                #mes = _('Convert "{}" to an integer').format(self.value)
                #objs.get_mes(self.title,mes,True).show_debug()
            elif Negative and re.match('-\d+$',self.value):
                ''' 'isinstance' will detect negative integers too,
                    however, we can also have a string at input.
                '''
                old = self.value
                self.value = int(self.value.replace('-','',1))
                self.value -= self.value * 2
                mes = _('Convert "{}" to an integer').format(old)
                objs.get_mes(self.title,mes,True).show_debug()
            else:
                mes = _('Integer is required at input, but found "{}"! Return 0')
                mes = mes.format(self.value)
                objs.get_mes(self.title,mes).show_warning()
                self.value = 0
        return self.value

    # Insert '' instead of 'None' into text widgets
    def get_not_none(self):
        if not self.value:
            self.value = ''
        return self.value



class Text:

    def __init__(self,text,Auto=False):
        self.text = text
        self.text = Input('Text.__init__',self.text).get_not_none()
        # This can be useful in many cases, e.g. after OCR
        if Auto:
            ''' This will remove symbols that cannot be shown in Tcl/Tk.
                Since in many cases we build 'Words' from the text, we
                need to synchronize this.
            '''
            self.delete_unsupported()
            self.convert_line_breaks()
            self.strip_lines()
            self.delete_duplicate_line_breaks()
            self.tabs2spaces()
            self.delete_trash()
            self.replace_x()
            self.delete_duplicate_spaces()
            self.replace_yo()
            self.text = OCR(text=self.text).run_common()
            self.delete_space_with_punctuation()
            ''' This is necessary even if we do strip for each line (we
                need to strip '\n' at the beginning/end).
            '''
            self.text = self.text.strip()

    def delete_embraced_figs(self):
        self.text = re.sub('\s\(\d+\)','',self.text)
        self.text = re.sub('\s\[\d+\]','',self.text)
        self.text = re.sub('\s\{\d+\}','',self.text)
        return self.text
    
    def replace_sim_syms(self):
        ''' Replace Cyrillic letters with similar Latin ones. This can
            be useful for English words in mostly Russian text.
        '''
        sim_cyr = ('А','В','Е','К','Н'
                  ,'О','Р','С','Т','Х'
                  ,'а','е','о','р','с'
                  ,'у','х'
                  )
        sim_lat = ('A','B','E','K','H'
                  ,'O','P','C','T','X'
                  ,'a','e','o','p','c'
                  ,'y','x'
                  )
        for i in range(len(sim_cyr)):
            self.text = self.text.replace(sim_cyr[i],sim_lat[i])
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
    
    # Getting rid of some useless symbols
    def delete_trash(self):
        self.text = self.text.replace('· ','').replace('• ','')
        self.text = self.text.replace('¬','')
    
    def toggle_case(self):
        if self.text == self.text.lower():
            self.text = self.text.upper()
        else:
            self.text = self.text.lower()
        return self.text

    def replace_quotes(self):
        self.text = re.sub(r'"([a-zA-Z\d\(\[\{\(])',r'“\1',self.text)
        self.text = re.sub(r'([a-zA-Z\d\.\?\!\)])"',r'\1”',self.text)
        self.text = re.sub(r'"(\.\.\.[a-zA-Z\d])',r'“\1',self.text)
        return self.text

    def delete_space_with_figure(self):
        expr = '[-\s]\d+'
        match = re.search(expr,self.text)
        while match:
            old = self.text
            self.text = self.text.replace(match.group(0),'')
            if old == self.text:
                break
            match = re.search(expr,self.text)
        return self.text

    def get_country(self):
        if len(self.text) > 4:
            if self.text[-4:-2] == ', ':
                if self.text[-1].isalpha() and self.text[-1].isupper() \
                and self.text[-2].isalpha() and self.text[-2].isupper():
                    return self.text[-2:]

    def reset(self,text):
        self.text = text

    def replace_x(self):
        # \xa0 is a non-breaking space in Latin1 (ISO 8859-1)
        self.text = self.text.replace('\xa0',' ').replace('\x07',' ')
        return self.text

    #TODO: check
    def delete_alphabetic_numeration(self):
        my_expr = ' [\(,\[]{0,1}[aA-zZ,аА-яЯ][\.,\),\]]( \D)'
        match = re.search(my_expr,self.text)
        while match:
            self.text = self.text.replace(match.group(0),match.group(1))
            match = re.search(my_expr,self.text)
        return self.text

    def delete_embraced_text(self,opening_sym='(',closing_sym=')'):
        ''' If there are some brackets left after performing this
            operation, ensure that all of them are in the right place
            (even when the number of opening and closing brackets is
            the same).
        '''
        f = '[shared] logic.Text.delete_embraced_text'
        if self.text.count(opening_sym) == self.text.count(closing_sym):
            opening_parentheses = []
            closing_parentheses = []
            for i in range(len(self.text)):
                if self.text[i] == opening_sym:
                    opening_parentheses.append(i)
                elif self.text[i] == closing_sym:
                    closing_parentheses.append(i)

            min_val = min (len(opening_parentheses)
                          ,len(closing_parentheses)
                          )

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
            ''' Further steps: self.delete_duplicate_spaces(),
                self.text.strip()
            '''
        else:
            mes = _('Different number of opening and closing brackets: "{}": {}; "{}": {}!')
            mes = mes.format (opening_sym
                             ,self.text.count(opening_sym)
                             ,closing_sym
                             ,self.text.count(closing_sym)
                             )
            objs.get_mes(f,mes).show_warning()
        return self.text

    def convert_line_breaks(self):
        self.text = self.text.replace('\r\n','\n').replace('\r','\n')
        return self.text

    # Apply 'convert_line_breaks' first
    def delete_line_breaks(self):
        self.text = self.text.replace('\n',' ')
        return self.text

    def delete_duplicate_line_breaks(self):
        while '\n\n' in self.text:
            self.text = self.text.replace('\n\n','\n')
        return self.text

    def delete_duplicate_spaces(self):
        while '  ' in self.text:
            self.text = self.text.replace('  ',' ')
        return self.text

    def delete_end_punc(self,Extended=False):
        ''' Delete a space and punctuation marks in the end of a line
            (useful when extracting features with CompareField).
        '''
        f = '[shared] logic.Text.delete_end_punc'
        if len(self.text) > 0:
            if Extended:
                while self.text[-1] == ' ' or self.text[-1] \
                in punc_array or self.text[-1] in punc_ext_array:
                    self.text = self.text[:-1]
            else:
                while self.text[-1] == ' ' or self.text[-1] \
                in punc_array:
                    self.text = self.text[:-1]
        else:
            com.rep_empty(f)
        return self.text

    def delete_figures(self):
        self.text = re.sub('\d+','',self.text)
        return self.text

    def delete_cyrillic(self):
        self.text = ''.join ([sym for sym in self.text if sym not \
                              in ru_alphabet
                             ]
                            )
        return self.text

    def delete_punctuation(self):
        for i in range(len(punc_array)):
            self.text = self.text.replace(punc_array[i],'')
        for i in range(len(punc_ext_array)):
            self.text = self.text.replace(punc_ext_array[i],'')
        return self.text

    def delete_space_with_punctuation(self):
        # Delete duplicate spaces first
        for i in range(len(punc_array)):
            self.text = self.text.replace (' ' + punc_array[i]
                                          ,punc_array[i]
                                          )
        self.text = self.text.replace('“ ','“').replace(' ”','”')
        self.text = self.text.replace('( ','(').replace(' )',')')
        self.text = self.text.replace('[ ','[').replace(' ]',']')
        self.text = self.text.replace('{ ','{').replace(' }','}')
        return self.text

    # Only for pattern '(YYYY-MM-DD)'
    def extract_date(self):
        expr = '\((\d\d\d\d-\d\d-\d\d)\)'
        if self.text:
            match = re.search(expr,self.text)
            if match:
                return match.group(1)

    def enclose(self,sym='"'):
        open_sym = close_sym = sym
        if sym == '(':
            close_sym = ')'
        elif sym == '[':
            close_sym = ']'
        elif sym == '{':
            close_sym = '}'
        elif sym == '“':
            close_sym = '”'
        elif sym == '«':
            close_sym = '»'
        self.text = open_sym + self.text + close_sym
        return self.text
    
    # Shorten a string up to a max length
    def shorten (self,max_len=10,Enclose=False
                ,FromEnd=False,ShowGap=True,sym='"'
                ):
        if len(self.text) > max_len:
            if Enclose:
                enc_len = 2 * len(sym)
                if max_len > enc_len:
                    max_len -= enc_len
            if ShowGap:
                if max_len > 3:
                    gap = '...'
                    max_len -= 3
                else:
                    gap = ''
            else:
                gap = ''
            if FromEnd:
                self.text = gap + self.text[len(self.text)-max_len:]
            else:
                self.text = self.text[0:max_len] + gap
        if Enclose:
            self.enclose(sym=sym)
        return self.text
        
    def grow(self,max_len=20,FromEnd=False,sym=' '):
        delta = max_len - len(self.text)
        if delta > 0:
            if FromEnd:
                self.text += delta * sym
            else:
                self.text = delta * sym + self.text
        return self.text
        
    def fit(self,max_len=20,FromEnd=False,sym=' '):
        self.shorten (max_len = max_len
                     ,FromEnd = FromEnd
                     ,ShowGap = False
                     )
        self.grow (max_len = max_len
                  ,FromEnd = FromEnd
                  ,sym     = sym
                  )
        return self.text

    def split_by_comma(self):
        ''' Replace commas or semicolons with line breaks or line breaks
            with commas.
        '''
        f = '[shared] logic.Text.split_by_comma'
        if (';' in self.text or ',' in self.text) and '\n' in self.text:
            mes = _('Commas and/or semicolons or line breaks can be used, but not altogether!')
            objs.get_mes(f,mes).show_warning()
        elif ';' in self.text or ',' in self.text:
            self.text = self.text.replace(',','\n')
            self.text = self.text.replace(';','\n')
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
        f = '[shared] logic.Text.str2int'
        par = 0
        try:
            par = int(self.text)
        except(ValueError,TypeError):
            mes = _('Failed to convert "{}" to an integer!')
            mes = mes.format(self.text)
            objs.get_mes(f,mes,True).show_warning()
        return par

    def str2float(self):
        f = '[shared] logic.Text.str2float'
        par = 0.0
        try:
            par = float(self.text)
        except(ValueError,TypeError):
            mes = _('Failed to convert "{}" to a floating-point number!')
            mes = mes.format(self.text)
            objs.get_mes(f,mes,True).show_warning()
        return par

    def strip_lines(self):
        self.text = self.text.splitlines()
        for i in range(len(self.text)):
            self.text[i] = self.text[i].strip()
        self.text = '\n'.join(self.text)
        return self.text

    def tabs2spaces(self):
        self.text = self.text.replace('\t',' ')
        return self.text

    # This allows to shorten dictionaries
    def replace_yo(self):
        self.text = self.text.replace('Ё','Е')
        self.text = self.text.replace('ё','е')
        return self.text

    # Delete everything but alphas and digits
    def get_alphanum(self):
        self.text = ''.join([x for x in self.text if x.isalnum()])
        return self.text
        
    def has_latin(self):
        for sym in self.text:
            if sym in lat_alphabet:
                return True
                
    def has_cyrillic(self):
        for sym in self.text:
            if sym in ru_alphabet:
                return True
                
    def delete_unsupported(self):
        ''' Remove characters from a range not supported by Tcl 
            (and causing a Tkinter error).
        '''
        self.text = ''.join ([char for char in self.text if ord(char) \
                              in range(65536)
                             ]
                            )
        return self.text



class List:

    def __init__(self,lst1=[],lst2=[]):
        if lst1 is None:
            self.lst1 = []
        else:
            self.lst1 = list(lst1)
        if lst2 is None:
            self.lst2 = []
        else:
            self.lst2 = list(lst2)

    def get_shared(self):
        return [item for item in self.lst2 if item in self.lst1]
    
    # Check if 'lst1' fully comprises 'lst2'
    def eats(self):
        for item in self.lst2:
            if not item in self.lst1:
                return False
        return True
    
    def get_duplicates_low(self):
        ''' Remove (case-insensitively) duplicate items (positioned
            after original items). Both lists must consist of strings.
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
    
    # Remove duplicate items (positioned after original items)
    def delete_duplicates(self):
        i = len(self.lst1) - 1
        while i >= 0:
            ind = self.lst1.index(self.lst1[i])
            if ind < i:
                del self.lst1[i]
            i -= 1
        return self.lst1
    
    # Add a space where necessary and convert to a string
    def space_items(self,MultSpaces=False):
        text = ''
        for i in range(len(self.lst1)):
            if not self.lst1[i] == '':
                if text == '':
                    text += self.lst1[i]
                elif self.lst1[i] and self.lst1[i][0] in punc_array \
                or self.lst1[i][0] in '”»])}':
                    text += self.lst1[i]
                elif len(text) > 1 and text[-2].isspace() \
                and text[-1] == '"':
                    ''' We do not know for sure where quotes should be
                        placed, but we cannot leave out cases like ' " '
                    '''
                    text += self.lst1[i]
                elif len(text) > 1 and text[-2].isspace() \
                and text[-1] == "'":
                    text += self.lst1[i]
                # Only after "text == ''"
                elif text[-1] in '“«[{(':
                    text += self.lst1[i]
                elif text[-1].isspace() and self.lst1[i] \
                and self.lst1[i][0].isspace() and not MultSpaces:
                    tmp = self.lst1[i].lstrip()
                    if tmp:
                        text += tmp
                elif text[-1].isspace():
                    text += self.lst1[i]
                elif i == len(self.lst1) - 1 and self.lst1[i] \
                in punc_array:
                    text += self.lst1[i]
                # Do not allow ' "' in the end
                elif i == len(self.lst1) - 1 and self.lst1[i] \
                in ('”','»',']',')','}','"',"'"):
                    text += self.lst1[i]
                else:
                    text += ' ' + self.lst1[i]
        return text

    # Adjust the lists at input to have the same length
    def equalize(self):
        max_range = max(len(self.lst1),len(self.lst2))
        if max_range == len(self.lst1):
            for i in range(len(self.lst1)-len(self.lst2)):
                self.lst2.append('')
        else:
            for i in range(len(self.lst2)-len(self.lst1)):
                self.lst1.append('')
        return(self.lst1,self.lst2)

    # Find different elements (strict order)
    # Based on http://stackoverflow.com/a/788780
    def get_diff(self):
        seqm = difflib.SequenceMatcher(a=self.lst1,b=self.lst2)
        output = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            if opcode != 'equal':
                output += seqm.a[a0:a1]
        return output



class Time:
    ''' We constantly recalculate each value because they depend on each
        other.
    '''
    def __init__ (self,tstamp=None,pattern='%Y-%m-%d'):
        self.reset (tstamp  = tstamp
                   ,pattern = pattern
                   )

    def set_values(self):
        self.Success = True
        self.date = self.year = self.month_abbr = self.month_name = ''
        self.inst = None
    
    def reset(self,tstamp=None,pattern='%Y-%m-%d'):
        self.set_values()
        self.pattern = pattern
        self.tstamp  = tstamp
        # Prevent recursion
        if self.tstamp is None:
            self.get_todays_date()
        else:
            self.get_instance()

    def add_days(self,days_delta):
        f = '[shared] logic.Time.add_days'
        if self.Success:
            try:
                self.inst = self.get_instance() \
                          + datetime.timedelta(days=days_delta)
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    def get_date(self):
        f = '[shared] logic.Time.get_date'
        if self.Success:
            try:
                self.date = self.get_instance().strftime(self.pattern)
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)
        return self.date

    def get_instance(self):
        f = '[shared] logic.Time.get_instance'
        if self.Success:
            if self.inst is None:
                if self.tstamp is None:
                    self.get_timestamp()
                try:
                    self.inst = datetime.datetime.fromtimestamp(self.tstamp)
                except Exception as e:
                    self.Success = False
                    mes = _('Set time parameters are incorrect or not supported.\n\nDetails: {}')
                    mes = mes.format(e)
                    objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)
        return self.inst

    def get_timestamp(self):
        f = '[shared] logic.Time.get_timestamp'
        if self.Success:
            if not self.date:
                self.get_date()
            try:
                self.tstamp = time.mktime(datetime.datetime.strptime(self.date,self.pattern).timetuple())
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)
        return self.tstamp

    def is_monday(self):
        f = '[shared] logic.Time.is_monday'
        if self.Success:
            if not self.inst:
                self.get_instance()
            if datetime.datetime.weekday(self.inst) == 0:
                return True
        else:
            com.cancel(f)

    def get_month_name(self):
        f = '[shared] logic.Time.get_month_name'
        if self.Success:
            if not self.inst:
                self.get_instance()
            self.month_name = calendar.month_name \
                              [Text (text = self.inst.strftime("%m")
                                    ,Auto = False
                                    ).str2int()
                              ]
        else:
            com.cancel(f)
        return self.month_name

    def localize_month_abbr(self):
        f = '[shared] logic.Time.localize_month_abbr'
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
            objs.get_mes(f,mes,True).show_warning()
        return self.month_abbr
    
    def get_month_abbr(self):
        f = '[shared] logic.Time.get_month_abbr'
        if self.Success:
            if not self.inst:
                self.get_instance()
            self.month_abbr = calendar.month_abbr \
                              [Text (text = self.inst.strftime("%m")
                                    ,Auto = False
                                    ).str2int()
                              ]
        else:
            com.cancel(f)
        return self.month_abbr

    def get_todays_date(self):
        self.inst = datetime.datetime.today()

    def get_year(self):
        f = '[shared] logic.Time.get_year'
        if self.Success:
            if not self.inst:
                self.get_instance()
            try:
                self.year = self.inst.strftime("%Y")
            except:
                self.Success = False
                mes = _('Set time parameters are incorrect or not supported.')
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)
        return self.year



class File:

    def __init__(self,file,dest=None,Rewrite=False):
        f = '[shared] logic.File.__init__'
        self.Success = True
        self.Rewrite = Rewrite
        self.file    = file
        self.dest    = dest
        # This will allow to skip some checks for destination
        if not self.dest:
            self.dest = self.file
        self.atime = ''
        self.mtime = ''
        # This already checks existence
        if self.file and os.path.isfile(self.file):
            ''' If the destination directory does not exist, this will
                be caught in try-except while copying/moving
            '''
            if os.path.isdir(self.dest):
                self.dest = os.path.join (self.dest
                                         ,Path(self.file).basename()
                                         )
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            objs.get_mes(f,mes).show_warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            objs.get_mes(f,mes).show_warning()
        else:
            self.Success = False
            mes = _('The object "{}" is not a file!').format(self.file)
            objs.get_mes(f,mes).show_warning()

    def get_size(self,Follow=True):
        f = '[shared] logic.File.get_size'
        result = 0
        if self.Success:
            try:
                if Follow:
                    cond = not os.path.islink(self.file)
                else:
                    cond = True
                if cond:
                    result = os.path.getsize(self.file)
            except Exception as e:
                ''' Along with other errors, 'No such file or directory'
                    error will be raised if Follow=False and this is
                    a broken symbolic link.
                '''
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)
        return result
    
    def _copy(self):
        f = '[shared] logic.File._copy'
        Success = True
        mes = _('Copy "{}" to "{}"').format(self.file,self.dest)
        objs.get_mes(f,mes,True).show_info()
        try:
            shutil.copyfile(self.file,self.dest)
        except:
            Success = False
            mes = _('Failed to copy file "{}" to "{}"!')
            mes = mes.format(self.file,self.dest)
            objs.get_mes(f,mes).show_error()
        return Success

    def _move(self):
        f = '[shared] logic.File._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.file,self.dest)
        objs.get_mes(f,mes,True).show_info()
        try:
            shutil.move(self.file,self.dest)
        except:
            Success = False
            mes = _('Failed to move "{}" to "{}"!')
            mes = mes.format(self.file,self.dest)
            objs.get_mes(f,mes).show_error()
        return Success

    def get_access_time(self):
        f = '[shared] logic.File.get_access_time'
        if self.Success:
            try:
                self.atime = os.path.getatime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
                return self.atime
            except:
                mes = _('Failed to get the date of the file "{}"!')
                mes = mes.format(self.file)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def copy(self):
        f = '[shared] logic.File.copy'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                mes = _('Unable to copy the file "{}" to iself!')
                mes = mes.format(self.file)
                objs.get_mes(f,mes).show_error()
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._copy()
            else:
                mes = _('Operation has been canceled by the user.')
                objs.get_mes(f,mes,True).show_info()
        else:
            com.cancel(f)
        return Success

    def delete(self):
        f = '[shared] logic.File.delete'
        if self.Success:
            mes = _('Delete "{}"').format(self.file)
            objs.get_mes(f,mes,True).show_info()
            try:
                os.remove(self.file)
                return True
            except:
                mes = _('Failed to delete file "{}"!').format(self.file)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def get_modification_time(self):
        f = '[shared] logic.File.get_modification_time'
        if self.Success:
            try:
                self.mtime = os.path.getmtime(self.file)
                # Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
                return self.mtime
            except:
                mes = _('Failed to get the date of the file "{}"!')
                mes = mes.format(self.file)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def move(self):
        f = '[shared] logic.File.move'
        Success = True
        if self.Success:
            if self.file.lower() == self.dest.lower():
                mes = _('Moving is not necessary, because the source and destination are identical ({}).')
                mes = mes.format(self.file)
                objs.get_mes(f,mes).show_warning()
            elif com.rewrite (file    = self.dest
                             ,Rewrite = self.Rewrite
                             ):
                Success = self._move()
            else:
                mes = _('Operation has been canceled by the user.')
                objs.get_mes(f,mes,True).show_info()
        else:
            com.cancel(f)
        return Success

    def set_time(self):
        f = '[shared] logic.File.set_time'
        if self.Success:
            if self.atime and self.mtime:
                mes = _('Change the time of the file "{}" to {}')
                mes = mes.format(self.file,(self.atime,self.mtime))
                objs.get_mes(f,mes,True).show_info()
                try:
                    os.utime(self.file,(self.atime,self.mtime))
                except:
                    mes = _('Failed to change the time of the file "{}" to "{}"!')
                    mes = mes.format(self.file,(self.atime,self.mtime))
                    objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)



class Path:

    def __init__(self,path):
        self.reset(path)

    def get_free_space(self):
        f = '[shared] logic.Path.get_free_space'
        result = 0
        if self.path:
            if os.path.exists(self.path):
                try:
                    istat  = os.statvfs(self.path)
                    result = istat.f_bavail * istat.f_bsize
                except Exception as e:
                    mes = _('Operation has failed!\nDetails: {}')
                    mes = mes.format(e)
                    objs.get_mes(f,mes).show_error()
            else:
                mes = _('Wrong input data: "{}"!').format(self.path)
                objs.get_mes(f,mes).show_warning()
        else:
            com.rep_empty(f)
        return result
    
    def _split_path(self):
        if not self.split:
            self.split = os.path.splitext(self.get_basename())
        return self.split

    def get_basename(self):
        if not self.basename:
            self.basename = os.path.basename(self.path)
        return self.basename

    # This will recursively (by design) create self.path
    def create(self):
        f = '[shared] logic.Path.create'
        # We actually don't need to fail the class globally
        Success = True
        if self.path:
            if os.path.exists(self.path):
                if os.path.isdir(self.path):
                    mes = _('Directory "{}" already exists.')
                    mes = mes.format(self.path)
                    objs.get_mes(f,mes,True).show_info()
                else:
                    Success = False
                    mes = _('The path "{}" is invalid!')
                    mes = mes.format(self.path)
                    objs.get_mes(f,mes).show_warning()
            else:
                mes = _('Create directory "{}"').format(self.path)
                objs.get_mes(f,mes,True).show_info()
                try:
                    #TODO: consider os.mkdir
                    os.makedirs(self.path)
                except:
                    Success = False
                    mes = _('Failed to create directory "{}"!')
                    mes = mes.format(self.path)
                    objs.get_mes(f,mes).show_error()
        else:
            Success = False
            com.rep_empty(f)
        return Success

    def delete_inappropriate_symbols(self):
        ''' These symbols may pose a problem while opening files
            #TODO: check whether this is really necessary
        '''
        return self.get_filename().replace("'",'').replace("&",'')

    def get_dirname(self):
        if not self.dirname:
            self.dirname = os.path.dirname(self.path)
        return self.dirname

    # In order to use xdg-open, we need to escape some characters first
    def escape(self):
        self.path = shlex.quote(self.path)
        return self.path

    # An extension with a dot
    def get_ext(self):
        if not self.extension:
            if len(self._split_path()) > 1:
                self.extension = self._split_path()[1]
        return self.extension

    def get_filename(self):
        if not self.filename:
            if len(self._split_path()) >= 1:
                self.filename = self._split_path()[0]
        return self.filename

    def reset(self,path):
        # Prevent 'NoneType'
        if path:
            self.path = path
        else:
            self.path = ''
        ''' Building paths in Windows:
            - Use raw strings (e.g., set path as r'C:\1.txt')
            - Use os.path.join(mydir,myfile) or os.path.normpath(path)
              instead of os.path.sep
            - As an alternative, import ntpath, posixpath
        '''
        ''' We remove a separator from the end, because basename and
            dirname work differently in this case ('' and the last
            directory, correspondingly)
        '''
        if self.path != '/':
            self.path = self.path.rstrip('//')
        self.basename = self.dirname = self.extension \
                      = self.filename = self.split = self.date = ''
        self.parts = []

    def split(self):
        if not self.parts:
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



class WriteBinary:

    def __init__(self,file,obj,Rewrite=True):
        f = '[shared] logic.WriteBinary.__init__'
        self.Success = True
        self.file    = file
        self.obj     = obj
        if self.file and self.obj:
            self.Rewrite = Rewrite
            self.fragm   = None
        else:
            self.Success = False
            com.rep_empty(f)

    def _write(self,mode='w+b'):
        f = '[shared] logic.WriteBinary._write'
        mes = _('Write file "{}"').format(self.file)
        objs.get_mes(f,mes,True).show_info()
        if mode == 'w+b' or mode == 'a+b':
            try:
                with open(self.file,mode) as fl:
                    if mode == 'w+b':
                        pickle.dump(self.obj,fl)
                    elif mode == 'a+b':
                        pickle.dump(self.fragm,fl)
            except Exception as e:
                self.Success = False
                mes = _('Unable to write file "{}"!\n\nDetails: {}')
                mes = mes.format(self.file,e)
                objs.get_mes(f,mes).show_error()
        else:
            mes = _('An unknown mode "{}"!\n\nThe following modes are supported: "{}".')
            mes = mes.format(mode,'w+b, a+b')
            objs.get_mes(f,mes).show_error()

    def append(self,fragm):
        f = '[shared] logic.WriteBinary.append'
        if self.Success:
            self.fragm = fragm
            if self.fragm:
                self._write(mode='a+b')
            else:
                com.rep_empty(f)
        else:
            com.cancel(f)

    def write(self):
        f = '[shared] logic.WriteBinary.write'
        if self.Success:
            if com.rewrite (file    = self.file
                           ,Rewrite = self.Rewrite
                           ):
                self._write(mode='w+b')
            else:
                mes = _('Operation has been canceled by the user.')
                Message(f,mes).show_info()
        else:
            com.cancel(f)



class Dic:

    def __init__(self,file,Sortable=False):
        self.file     = file
        self.Sortable = Sortable
        self.errors   = []
        self.iread    = ReadTextFile(self.file)
        self.reset()

    def _delete_duplicates(self):
        ''' This is might be needed only for those dictionaries that
            already may contain duplicates (dictionaries with newly
            added entries do not have duplicates due to new algorithms).
        '''
        f = '[shared] logic.Dic._delete_duplicates'
        if self.Success:
            if self.Sortable:
                old = self.get_lines()
                self.lst = list(set(self.get_list()))
                new = self.lines = len(self.lst)
                mes = _('Entries deleted: {} ({}-{})')
                mes = mes.format(old-new,old,new)
                objs.get_mes(f,mes,True).show_info()
                self.text = '\n'.join(self.lst)
                # Update original and translation
                self._split()
                # After using set(), the original order was lost
                self.sort()
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    # We can use this as an updater, even without relying on Success
    def _join(self):
        f = '[shared] logic.Dic._join'
        if len(self.orig) == len(self.transl):
            self.lines = len(self.orig)
            self.lst   = []
            for i in range(self.lines):
                self.lst.append(self.orig[i]+'\t'+self.transl[i])
            self.text = '\n'.join(self.lst)
        else:
            mes = _('Wrong input data!')
            objs.get_mes(f,mes).show_warning()

    def _split(self):
        ''' We can use this to check integrity and/or update original
            and translation lists.
        '''
        if self.get():
            self.Success = True
            self.orig    = []
            self.transl  = []
            ''' Building lists takes ~0.1 longer without temporary
                variables (now self._split() takes ~0.256)
            '''
            for i in range(self.lines):
                tmp_lst = self.lst[i].split('\t')
                if len(tmp_lst) == 2:
                    self.orig.append(tmp_lst[0])
                    self.transl.append(tmp_lst[1])
                else:
                    ''' Lines that were successfully parsed can be
                        further processed upon correcting 'self.lines'
                    '''
                    self.Success = False
                    self.errors.append(str(i))
            self.warn()
            if not self.orig or not self.transl:
                self.Success = False
        else:
            self.Success = False
            
    def warn(self):
        f = '[shared] logic.Dic.warn'
        if self.errors:
            message = ', '.join(self.errors)
            mes = _('The following lines cannot be parsed:')
            mes += '\n' + message
            objs.get_mes(f,mes).show_warning()

    def append(self,original,translation):
        ''' #TODO: write a dictionary in an append mode after appending
                   to memory.
            #TODO: skip repetitions
        '''
        f = '[shared] logic.Dic.append'
        if self.Success:
            if original and translation:
                self.orig.append(original)
                self.transl.append(translation)
                self._join()
            else:
                com.rep_empty(f)
        else:
            com.cancel(f)

    # Count from 1
    def delete_entry(self,entry_no):
        ''' #TODO: fix: an entry which is only one in a dictionary is
            not deleted.
        '''
        f = '[shared] logic.Dic.delete_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.get_lines():
                del self.orig[entry_no]
                del self.transl[entry_no]
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.get_lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    # Count from 1
    def edit_entry(self,entry_no,orig,transl):
        ''' #TODO: Add checking orig and transl (where needed) for
            a wrapper function.
        '''
        f = '[shared] logic.Dic.edit_entry'
        if self.Success:
            entry_no -= 1
            if entry_no >= 0 and entry_no < self.get_lines():
                self.orig[entry_no] = orig
                self.transl[entry_no] = transl
                self._join()
            else:
                sub = '0 <= {} < {}'.format(entry_no,self.get_lines())
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    def get(self):
        if not self.text:
            self.text = self.iread.load()
        return self.text

    def get_lines(self):
        if self.lines == 0:
            self.lines = len(self.get_list())
        return self.lines

    def get_list(self):
        if not self.lst:
            self.lst = self.get().splitlines()
        return self.lst

    def reset(self):
        self.text   = self.iread.load()
        self.orig   = []
        self.transl = []
        self.lst    = self.get().splitlines()
        # Delete empty and commented lines
        self.lst = [line for line in self.lst if line \
                    and not line.startswith('#')
                   ]
        self.text  = '\n'.join(self.lst)
        self.lines = len(self.lst)
        self._split()

    # Sort a dictionary with the longest lines going first
    def sort(self):
        f = '[shared] logic.Dic.sort'
        if self.Success:
            if self.Sortable:
                tmp_list = []
                for i in range(len(self.lst)):
                    tmp_list += [[len(self.orig[i])
                                 ,self.orig[i]
                                 ,self.transl[i]
                                 ]
                                ]
                tmp_list.sort(key=lambda x: x[0],reverse=True)
                for i in range(len(self.lst)):
                    self.orig[i] = tmp_list[i][1]
                    self.transl[i] = tmp_list[i][2]
                    self.lst[i] = self.orig[i] + '\t' + self.transl[i]
                self.text = '\n'.join(self.lst)
            else:
                mes = _('File "{}" is not sortable!').format(self.file)
                objs.get_mes(f,mes).show_warning()
        else:
            com.cancel(f)

    def tail(self):
        f = '[shared] logic.Dic.tail'
        tail_text = ''
        if self.Success:
            tail_len = globs['int']['tail_len']
            if tail_len > self.get_lines():
                tail_len = self.get_lines()
            i = self.get_lines() - tail_len
            # We count from 1, therefore it is < and not <=
            while i < self.get_lines():
                # i+1 by the same reason
                tail_text += str(i+1) + ':' + '"' + self.get_list()[i] \
                             + '"\n'
                i += 1
        else:
            com.cancel(f)
        return tail_text

    def write(self):
        f = '[shared] logic.Dic.write'
        if self.Success:
            WriteTextFile (file    = self.file
                          ,Rewrite = True
                          ).write(self.get())
        else:
            com.cancel(f)



class ReadBinary:

    def __init__(self,file):
        self.file    = file
        self.obj     = None
        h_file       = File(self.file)
        self.Success = h_file.Success

    def _load(self):
        f = '[shared] logic.ReadBinary._load'
        mes = _('Load file "{}"').format(self.file)
        objs.get_mes(f,mes,True).show_info()
        try:
            ''' AttributeError means that a module using _load does not
                have a class that was defined while creating the binary
            '''
            with open(self.file,'r+b') as fl:
                self.obj = pickle.load(fl)
        except Exception as e:
            self.Success = False
            mes = _('Unable to read file "{}"!\n\nDetails: {}')
            mes = mes.format(self.file,e)
            objs.get_mes(f,mes).show_error()

    #TODO: load fragments appended to a binary
    def load(self):
        f = '[shared] logic.ReadBinary.load'
        if self.Success:
            self._load()
        else:
            com.cancel(f)
        return self.obj

    def get(self):
        if not self.obj:
            self.load()
        return self.obj



# Do not forget to import this class if it was used to pickle an object
class CreateInstance:
    pass



#TODO: fix: does not work with a root dir ('/')
class Directory:

    def __init__(self,path,dest=''):
        f = '[shared] logic.Directory.__init__'
        self.set_values()
        if path:
            ''' Remove trailing slashes and follow symlinks. No error is
                thrown for broken symlinks, but further checks will fail
                for them. Failing a real path (e.g., pointing to
                the volume that is not mounted yet) is more
                apprehensible than failing a symlink.
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
            objs.get_mes(f,mes).show_warning()

    def get_subfiles(self,Follow=True):
        # Include files in subfolders
        f = '[shared] logic.Directory.get_subfiles'
        if self.Success:
            if not self.subfiles:
                try:
                    for dirpath, dirnames, fnames \
                    in os.walk(self.dir,followlinks=Follow):
                        for name in fnames:
                            obj = os.path.join(dirpath,name)
                            if os.path.isfile(obj):
                                self.subfiles.append(obj)
                    self.subfiles.sort(key=lambda x: x.lower())
                except Exception as e:
                    mes = _('Operation has failed!\nDetails: {}')
                    mes = mes.format(e)
                    objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
        return self.subfiles
    
    def get_size(self,Follow=True):
        f = '[shared] logic.Directory.get_size'
        result = 0
        if self.Success:
            try:
                for dirpath, dirnames, filenames in os.walk(self.dir):
                    for name in filenames:
                        obj = os.path.join(dirpath,name)
                        if Follow:
                            cond = not os.path.islink(obj)
                        else:
                            cond = True
                        if cond:
                            result += os.path.getsize(obj)
            except Exception as e:
                ''' Along with other errors, 'No such file or directory'
                    error will be raised if Follow=False and there are
                    broken symbolic links.
                '''
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
        return result
    
    def set_values(self):
        self.Success = True
        # Assigning lists must be one per line
        self.lst      = []
        self.rellist  = []
        self.files    = []
        self.relfiles = []
        self.dirs     = []
        self.reldirs  = []
        self.exts     = []
        self.extslow  = []
        self.subfiles = []
    
    def get_ext(self): # with a dot
        f = '[shared] logic.Directory.get_ext'
        if self.Success:
            if not self.exts:
                for file in self.relfiles():
                    ext = Path(path=file).get_ext()
                    self.exts.append(ext)
                    self.extslow.append(ext.lower())
        else:
            com.cancel(f)
        return self.exts

    def get_ext_low(self): # with a dot
        f = '[shared] logic.Directory.get_ext_low'
        if self.Success:
            if not self.extslow:
                self.get_ext()
        else:
            com.cancel(f)
        return self.extslow

    def delete_empty(self):
        f = '[shared] logic.Directory.delete_empty'
        if self.Success:
            # Do not delete nested folders
            if not os.listdir(self.dir):
                self.delete()
        else:
            com.cancel(f)
    
    def delete(self):
        f = '[shared] logic.Directory.delete'
        if self.Success:
            mes = _('Delete "{}"').format(self.dir)
            objs.get_mes(f,mes,True).show_info()
            try:
                shutil.rmtree(self.dir)
                return True
            except:
                mes = _('Failed to delete directory "{}"! Delete it manually.')
                mes = mes.format(self.dir)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)

    # Create a list of objects with a relative path
    def get_rel_list(self):
        f = '[shared] logic.Directory.get_rel_list'
        if self.Success:
            if not self.rellist:
                self.get_list()
        else:
            com.cancel(f)
        return self.rellist

    # Create a list of objects with an absolute path
    def get_list(self):
        f = '[shared] logic.Directory.get_list'
        if self.Success:
            if not self.lst:
                self.lst = os.listdir(self.dir)
                self.lst.sort(key=lambda x: x.lower())
                self.rellist = list(self.lst)
                for i in range(len(self.lst)):
                    self.lst[i] = os.path.join(self.dir,self.lst[i])
        else:
            com.cancel(f)
        return self.lst

    def get_rel_dirs(self):
        f = '[shared] logic.Directory.get_rel_dirs'
        if self.Success:
            if not self.reldirs:
                self.dirs()
        else:
            com.cancel(f)
        return self.reldirs

    def get_rel_files(self):
        f = '[shared] logic.Directory.get_rel_files'
        if self.Success:
            if not self.relfiles:
                self.files()
        else:
            com.cancel(f)
        return self.relfiles

    # Needs absolute path
    def get_dirs(self):
        f = '[shared] logic.Directory.get_dirs'
        if self.Success:
            if not self.dirs:
                for i in range(len(self.get_list())):
                    if os.path.isdir(self.lst[i]):
                        self.dirs.append(self.lst[i])
                        self.reldirs.append(self.rellist[i])
        else:
            com.cancel(f)
        return self.dirs

    # Needs absolute path
    def get_files(self):
        f = '[shared] logic.Directory.get_files'
        if self.Success:
            if not self.files:
                for i in range(len(self.get_list())):
                    if os.path.isfile(self.lst[i]):
                        self.files.append(self.lst[i])
                        self.relfiles.append(self.rellist[i])
        else:
            com.cancel(f)
        return self.files

    def copy(self):
        f = '[shared] logic.Directory.copy'
        if self.Success:
            if self.dir.lower() == self.dest.lower():
                mes = _('Unable to copy "{}" to iself!')
                mes = mes.format(self.dir)
                objs.get_mes(f,mes).show_error()
            elif os.path.isdir(self.dest):
                mes = _('Directory "{}" already exists.')
                mes = mes.format(self.dest)
                objs.get_mes(f,mes).show_info()
            else:
                self._copy()
        else:
            com.cancel(f)

    def _copy(self):
        f = '[shared] logic.Directory._copy'
        mes = _('Copy "{}" to "{}"').format(self.dir,self.dest)
        objs.get_mes(f,mes,True).show_info()
        try:
            shutil.copytree(self.dir,self.dest)
        except:
            self.Success = False
            mes = _('Failed to copy "{}" to "{}"!')
            mes = mes.format(self.dir,self.dest)
            objs.get_mes(f,mes).show_error()



class Config:

    def __init__(self):
        self.set_values()
        
    def set_values(self):
        self.Success          = True
        self.sections         = [SectionVariables]
        self.sections_abbr    = [SectionVariables_abbr]
        self.sections_func    = [config_parser.get]
        self.message          = _('The following sections and/or keys are missing:') + '\n'
        self.total_keys       = 0
        self.changed_keys     = 0
        self.missing_keys     = 0
        self.missing_sections = 0

    def load(self):
        f = '[shared] logic.Config.load'
        if self.Success:
            for i in range(len(self.sections)):
                for option in globs[self.sections_abbr[i]]:
                    new_val = self.sections_func[i](self.sections[i],option)
                    if globs[self.sections_abbr[i]][option] != new_val:
                        mes = _('New value of the key "{}" has been loaded.')
                        mes = mes.format(option)
                        Message(f,mes).show_info()
                        self.changed_keys += 1
                        globs[self.sections_abbr[i]][option] = new_val
            mes = _('Keys loaded in total: {}, whereas {} are modified.')
            mes = mes.format(self.total_keys,self.changed_keys)
            Message(f,mes).show_info()
        else:
            com.cancel(f)

    def check(self):
        f = '[shared] logic.Config.check'
        if self.Success:
            for i in range(len(self.sections)):
                if config_parser.has_section(self.sections[i]):
                    for option in globs[self.sections_abbr[i]]:
                        self.total_keys += 1
                        if not config_parser.has_option(self.sections[i]
                                                       ,option
                                                       ):
                            self.Success = False
                            self.missing_keys += 1
                            self.message += option + '; '
                else:
                    self.Success = False
                    self.missing_sections += 1
                    self.message += self.sections[i] + '; '
            if not self.Success:
                self.message += '\n'
                sub = _('Missing sections: {}')
                sub = sub.format(self.missing_sections)
                self.message += sub
                self.message += '\n'
                sub = _('Missing keys: {}').format(self.missing_keys)
                self.message += sub
                self.message += '\n'
                self.message += _('The default configuration has been loaded.')
                objs.get_mes(f,self.message).show_warning()
                self.load_default()
        else:
            com.cancel(f)

    def open(self):
        f = '[shared] logic.Config.open'
        if self.Success:
            try:
                config_parser.read(self.path,'utf-8')
            except:
                Success = False
                mes = _('Failed to read the configuration file "{}". This file must share the same directory with the program and have UTF-8 encoding (no BOM) and UNIX line break type.')
                mes = mes.format(self.path)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)



class Online:
    ''' If you get 'TypeError("quote_from_bytes() expected bytes")',
        then you probably forgot to call 'self.reset' here or
        in children classes.
    '''
    def __init__ (self,base='%s',pattern=''
                 ,coding='UTF-8'
                 ):
        self.reset (base    = base
                   ,pattern = pattern
                   ,coding  = coding
                   )

    def get_bytes(self):
        if not self.bytes:
            self.bytes = bytes (self.pattern
                               ,encoding = self.coding
                               )
        return self.bytes

    # Open a URL in a default browser
    def browse(self):
        f = '[shared] logic.Online.browse'
        try:
            webbrowser.open (url       = self.get_url()
                            ,new       = 2
                            ,autoraise = True
                            )
        except Exception as e:
            mes = _('Failed to open URL "{}" in a default browser!\n\nDetails: {}')
            mes = mes.format(self.url,e)
            objs.get_mes(f,mes).show_error()

    # Create a correct online link (URI => URL)
    def get_url(self):
        f = '[shared] logic.Online.get_url'
        if not self.url:
            self.url = self.base % urllib.parse.quote(self.get_bytes())
            mes = str(self.url)
            objs.get_mes(f,mes,True).show_debug()
        return self.url

    def reset (self,base='',pattern=''
              ,coding='UTF-8'
              ):
        self.bytes   = None
        self.url     = None
        self.coding  = coding
        self.base    = base
        self.pattern = pattern



class Diff:

    def __init__(self,text1='',text2='',file=None):
        self.Custom     = False
        ''' Some browsers update web-page as soon as we rewrite it, and
            some even do not open the same file again. So, we have to
            create a new temporary file each time.
        '''
        self.wda_html   = com.get_tmpfile(suffix='.htm',Delete=0)
        self.iwda_write = WriteTextFile (file    = self.wda_html
                                        ,Rewrite = True
                                        )
        if text1 or text2:
            self.reset (text1 = text1
                       ,text2 = text2
                       ,file  = file
                       )

    def reset(self,text1,text2,file=None):
        self.diff = ''
        self.text1 = text1
        self.text2 = text2
        if file:
            self.Custom  = True
            self.file    = file
            self.header  = ''
            self.iwrite  = WriteTextFile (file    = self.file
                                         ,Rewrite = False
                                         )
            self.ipath   = Path(self.file)
        else:
            self.Custom  = False
            self.file    = self.wda_html
            self.header  = '<title>%s</title>' % _('Differences:')
            self.iwrite  = self.iwda_write
        return self

    def set_diff(self):
        self.text1 = self.text1.split(' ')
        self.text2 = self.text2.split(' ')
        self.diff  = difflib.HtmlDiff().make_file(self.text1,self.text2)
        # Avoid a bug in HtmlDiff()
        self.diff  = self.diff.replace ('charset=ISO-8859-1'
                                       ,'charset=UTF-8'
                                       )

    def set_header(self):
        if self.Custom:
            self.header = self.ipath.basename()
            self.header = self.header.replace(self.ipath.get_ext(),'')
            self.header = '<title>' + self.header + '</title>'
        self.diff = self.diff.replace('<title></title>',self.header)
        self.diff += '\n'

    def compare(self):
        f = '[shared] logic.Diff.compare'
        if self.text1 and self.text2:
            if self.text1 == self.text2:
                mes = _('Texts are identical!')
                objs.get_mes(f,mes).show_info()
            else:
                self.set_diff()
                self.set_header()
                self.iwrite.write(self.diff)
                if self.iwrite.Success:
                    ''' Cannot reuse the class instance because the
                        temporary file might be missing
                    '''
                    Launch(target=self.file).launch_default()
        else:
            com.rep_empty(f)



class Shortcut:

    def __init__(self,symlink='',path=''):
        f = '[shared] logic.Shortcut.__init__'
        self.Success = True
        self.path    = path
        self.symlink = symlink
        if not self.path and not self.symlink:
            self.Success = False
            mes = _('Wrong input data!')
            objs.get_mes(f,mes).show_warning()

    # http://timgolden.me.uk/python/win32_how_do_i/read-a-shortcut.html
    def _get_win(self):
        link = pythoncom.CoCreateInstance (win32com.shell.shell.CLSID_ShellLink
                                          ,None
                                          ,pythoncom.CLSCTX_INPROC_SERVER
                                          ,win32com.shell.shell.IID_IShellLink
                                          )
        link.QueryInterface(pythoncom.IID_IPersistFile).Load(self.symlink)
        ''' GetPath returns the name and a WIN32_FIND_DATA structure
            which we're ignoring. The parameter indicates whether
            shortname, UNC or the "raw path" are to be returned.
            Bizarrely, the docs indicate that the flags can be combined.
        '''
        self.path,_=link.GetPath(win32com.shell.shell.SLGP_UNCPRIORITY)

    def _get_unix(self):
        self.path = os.path.realpath(self.symlink)

    def get(self):
        if self.Success and not self.path:
            if objs.get_os().is_win():
                self._get_win()
            else:
                self._get_unix()
        return self.path

    def _delete(self):
        f = '[shared] logic.Shortcut._delete'
        mes = _('Delete the symbolic link "{}"').format(self.symlink)
        objs.get_mes(f,mes,True).show_info()
        try:
            os.unlink(self.symlink)
        except:
            mes = _('Failed to remove shortcut "{}". Remove it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.get_mes(f,mes).show_error()

    def delete(self):
        f = '[shared] logic.Shortcut.delete'
        if self.Success:
            if os.path.islink(self.symlink):
                self._delete()
        else:
            com.cancel(f)

    def _create_unix(self):
        f = '[shared] logic.Shortcut._create_unix'
        mes = _('Create a symbolic link "{}"').format(self.symlink)
        objs.get_mes(f,mes,True).show_info()
        try:
            os.symlink(self.path,self.symlink)
        except:
            mes = _('Failed to create shortcut "{}". Create it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.get_mes(f,mes).show_error()

    def create_unix(self):
        f = '[shared] logic.Shortcut.create_unix'
        self.delete()
        if os.path.exists(self.symlink):
            if os.path.islink(self.symlink):
                com.rep_lazy(f)
            else:
                self.Success = False
                mes = _('Wrong input data!')
                objs.get_mes(f,mes).show_warning()
        else:
            self._create_unix()

    def _create_win(self):
        f = '[shared] logic.Shortcut._create_win'
        mes = _('Create a symbolic link "{}"').format(self.symlink)
        objs.get_mes(f,mes,True).show_info()
        try:
            # The code will automatically add '.lnk' if necessary
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(self.symlink)
            shortcut.Targetpath = self.path
            shortcut.save()
        except:
            mes = _('Failed to create shortcut "{}". Create it manually and press OK.')
            mes = mes.format(self.symlink)
            objs.get_mes(f,mes).show_error()

    def create_win(self):
        ''' Using python 3 and windows (since 2009) it is possible to
            create a symbolic link, however, this will not be the same
            as a shortcut (.lnk). Therefore, in case the shortcut is
            used, os.path.islink() will always return False (not
            supported) (must use os.path.exists()), however, os.unlink()
            will work as expected.
        '''
        #NOTE: windows paths must have a double backslash!
        f = '[shared] logic.Shortcut.create_win'
        if self.Success:
            if not Path(self.symlink).get_ext().lower() == '.lnk':
                self.symlink += '.lnk'
            self.delete()
            if os.path.exists(self.symlink):
                com.rep_lazy(f)
            else:
                self._create_win()
        else:
            com.cancel(f)

    def create(self):
        f = '[shared] logic.Shortcut.create'
        if self.Success:
            if objs.get_os().is_win():
                self.create_win()
            else:
                self.create_unix()
        else:
            com.cancel(f)



class Email:
    ''' Invoke a default email client with the required input.
        Since there is no conventional way to programatically add
        an attachment in the default email client, we attempt to call
        Thunderbird, then Outlook, and finally mailto.
        Using 'webbrowser.open' has the following shortcomings:
        - A web browser is used to parse 'mailto' (we need to launch it
          first)
        - Instead of passing arguments to a mail agent, the web browser
          can search all input online which is a security breach
        - (AFAIK) Using this method, there is no standard way to add
          an attachment. Currently, I managed to add attachments only
          using CentOS6 + Palemoon + Thunderbird.
    '''
    def __init__ (self,email='',subject=''
                 ,message='',attach=''
                 ):
        if email:
            self.reset (email   = email
                       ,subject = subject
                       ,message = message
                       ,attach  = attach
                       )
    
    def reset (self,email,subject=''
              ,message='',attach=''
              ):
        f = '[shared] logic.Email.reset'
        self.Success = True
        ''' A single address or multiple comma-separated addresses (not
            all mail agents support ';'). #note that, however, Outlook
            supports ONLY ';' and Evolution - only ','!
        '''
        self.email   = email
        self.subject = Input(f,subject).get_not_none()
        self.message = Input(f,message).get_not_none()
        self.attach  = attach
        if not self.email:
            self.Success = False
            com.rep_empty(f)
        if self.attach:
            self.Success = File(file=self.attach).Success
            if not self.Success:
                com.cancel(f)

    # Screen symbols that may cause problems when composing 'mailto'
    def sanitize(self,value):
        f = '[shared] logic.Email.sanitize'
        if self.Success:
            return str(Online(pattern=value).get_url())
        else:
            com.cancel(f)
    
    def browser(self):
        f = '[shared] logic.Email.browser'
        if self.Success:
            try:
                if self.attach:
                    ''' - This is the last resort. Attaching a file
                          worked for me only with CentOS6 + Palemoon +
                          Thunderbird. Using another OS/browser/email
                          client will probably call a default email
                          client without the attachment.
                        - Quotes are necessary for attachments only,
                          they will stay visible otherwise.
                    '''
                    webbrowser.open ('mailto:%s?subject=%s&body=%s&attach="%s"'\
                                    % (self.email
                                      ,self.subject
                                      ,self.message
                                      ,self.attach
                                      )
                                    )
                else:
                    webbrowser.open ('mailto:%s?subject=%s&body=%s' \
                                    % (self.email
                                      ,self.subject
                                      ,self.message
                                      )
                                    )
            except:
                mes = _('Failed to load an e-mail client.')
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
    
    def create(self):
        f = '[shared] logic.Email.create'
        if self.Success:
            if not self.run_evolution() and not self.run_thunderbird() \
            and not self.run_outlook():
                self.subject = self.sanitize(self.subject)
                self.message = self.sanitize(self.message)
                self.attach  = self.sanitize(self.attach)
                self.browser()
        else:
            com.cancel(f)
                       
    #NOTE: this does not work in wine!
    def run_outlook(self):
        f = '[shared] logic.Email.run_outlook'
        if objs.get_os().is_win():
            try:
                import win32com.client
                #https://stackoverflow.com/a/51993450
                outlook       = win32com.client.dynamic.Dispatch('outlook.application')
                mail          = outlook.CreateItem(0)
                mail.To       = self.email.replace(',',';')
                mail.Subject  = self.subject
                mail.HtmlBody = '<html><body><meta http-equiv="Content-Type" content="text/html;charset=UTF-8">%s</body></html>'\
                                % self.message
                if self.attach:
                    mail.Attachments.Add(self.attach)
                mail.Display(True)
                return True
            except Exception as e:
                mes = _('Operation has failed!\nDetails: {}').format(e)
                objs.get_mes(f,mes).show_error()
        else:
            mes = _('This operation cannot be executed on your operating system.')
            objs.get_mes(f,mes).show_info()
    
    def run_thunderbird(self):
        f = '[shared] logic.Email.run_thunderbird'
        if self.Success:
            app = '/usr/bin/thunderbird'
            if os.path.isfile(app):
                if self.attach:
                    self.custom_args = [app,'-compose'
                                       ,"to='%s',subject='%s',body='%s',attachment='%s'"\
                                       % (self.email,self.subject
                                         ,self.message,self.attach
                                         )
                                       ]
                else:
                    self.custom_args = [app,'-compose'
                                       ,"to='%s',subject='%s',body='%s'"\
                                       % (self.email,self.subject
                                         ,self.message
                                         )
                                       ]
                try:
                    subprocess.Popen(self.custom_args)
                    return True
                except:
                    mes = _('Failed to run "{}"!')
                    mes = mes.format(self.custom_args)
                    objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
    
    def run_evolution(self):
        f = '[shared] logic.Email.run_evolution'
        if self.Success:
            app = '/usr/bin/evolution'
            if os.path.isfile(app):
                if self.attach:
                    self.custom_args = [app,'mailto:%s?subject=%s&body=%s&attach=%s'\
                                       % (self.email.replace(';',',')
                                         ,self.subject,self.message
                                         ,self.attach
                                         )
                                       ]
                else:
                    self.custom_args = [app,'mailto:%s?subject=%s&body=%s'\
                                       % (self.email.replace(';',',')
                                         ,self.subject,self.message
                                         )
                                       ]
                try:
                    subprocess.Popen(self.custom_args)
                    return True
                except:
                    mes = _('Failed to run "{}"!')
                    mes = mes.format(self.custom_args)
                    objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)



class Grep:

    def __init__ (self,lst,start=[]
                 ,middle=[],end=[]
                 ):
        self.lst    = lst
        self.start  = start
        self.middle = middle
        self.end    = end
        self.found  = []
        self.i      = 0
        self.sanitize()

    def sanitize(self):
        ''' Get rid of constructs like [None] instead of checking
            arguments when parameterizing.
        '''
        if len(self.lst) == 1:
            if not self.lst[0]:
                self.lst = []
        if len(self.start) == 1:
            if not self.start[0]:
                self.start = []
        if len(self.middle) == 1:
            if not self.middle[0]:
                self.middle = []
        if len(self.end) == 1:
            if not self.end[0]:
                self.end = []

    def match_start(self):
        if not self.start:
            return True
        found = False
        for i in range(len(self.start)):
            if self.start[i] \
            and self.lst[self.i].startswith(self.start[i]):
                found = True
        return found

    def match_middle(self):
        if not self.middle:
            return True
        found = False
        for i in range(len(self.middle)):
            if self.middle[i] and self.middle[i] in self.lst[self.i]:
                found = True
        return found

    def match_end(self):
        if not self.end:
            return True
        found = False
        for i in range(len(self.end)):
            if self.end[i] and self.lst[self.i].endswith(self.end[i]):
                found = True
        return found

    # Return all matches as a list
    def get(self):
        if not self.found:
            for i in range(len(self.lst)):
                self.i = i
                if self.match_start() and self.match_middle() \
                and self.match_end():
                    self.found.append(self.lst[i])
        return self.found

    # Return the 1st match as a string
    def get_first(self):
        self.get()
        if self.found:
            return self.found[0]



class Word:

    def __init__(self):
        ''' 'p': word with punctuation
            'n': 'p' without punctuation, lower case
            'nm': normal form of 'n'
            'pf': position of the 1st symbol of 'p'
            'pl': position of the last symbol of 'p'
            'nf': position of the 1st symbol of 'n'
            'nl': position of the last symbol of 'n'
            'nmf': position of the 1st symbol of 'nm'  # 'matches'
            'nml': position of the last symbol of 'nm' # 'matches'
        '''
        self.nm = self.nmf = self.nml = self.pf = self.pl = self.nf \
                = self.nl = self.cyr = self.lat = self.greek \
                = self.digit = self.empty = self.ref = self.sentno \
                = self.spell = self.sentslen = self.tf = self.tl = None

    def is_empty(self):
        if self.empty is None:
            self.empty = True
            for sym in self.p:
                if sym.isalpha():
                    self.empty = False
                    break
        return self.empty

    def has_digit(self):
        if self.digit is None:
            self.digit = False
            for sym in self.p:
                if sym.isdigit():
                    self.digit = True
                    break
        return self.digit

    def has_cyr(self):
        if self.cyr is None:
            self.cyr = False
            for sym in ru_alphabet_low:
                if sym in self.n:
                    self.cyr = True
                    break
        return self.cyr

    def has_lat(self):
        if self.lat is None:
            self.lat = False
            for sym in lat_alphabet_low:
                if sym in self.n:
                    self._lat = True
                    break
        return self.lat

    def has_greek(self):
        if self.greek is None:
            self.greek = False
            for sym in greek_alphabet_low:
                if sym in self.n:
                    self.greek = True
                    break
        return self.greek

    # Do only after Words.sent_nos
    def print(self,no=0):
        f = '[shared] logic.Word.print'
        mes = 'no: {}; p: {}; n: {}; nm: {}; pf: {}; pl: {}; nf: {}; nl: {}; cyr: {}; lat: {}; greek: {}; digit: {}; empty: {}; ref: {}; sentno: {}; sentslen: {}; spell: {}; nmf: {}; nml: {}'
        mes = mes.format (no,self.p,self.n,self.nm,self.pf,self.pl
                         ,self.nf,self.nl,self.cyr,self.lat
                         ,self.greek,self.digit,self.empty,self.ref
                         ,self.sentno,self.sentslen,self.spell
                         ,self.nmf,self.nml)
        objs.get_mes(f,mes,True).show_debug()

    def get_nm(self):
        if self.nm is None:
            if self.has_ref():
                ''' #NOTE: Setting 'nm' to '' allows to find longer
                    matches (without references), but requires replacing
                    duplicate spaces in 'text_nm' with ordinary ones and
                    using another word numbering for 'nm'.
                '''
                #self.nm = ''
                self.nm = self.n
            else:
                result = Decline (text = self.n
                                 ,Auto = False
                                 ).normal().get()
                if result:
                    self.nm = result.replace('ё','е')
                else:
                    self.nm = self.n
        return self.nm

    def has_ref(self):
        ''' Criteria for setting the 'reference' mark:
            - The word has digits
            - The word has Greek characters (that are treated as
              variables. Greek should NOT be a predominant language)
            - The word has Latin characters in the predominantly Russian
              text (inexact)
            - The word has '-' (inexact) (#NOTE: when finding matches,
              set the condition of ''.join(set(ref)) != '-')
        '''
        if self.ref is None:
            if self.has_lat() or self.has_digit() or self.has_greek():
                self.ref = True
            else:
                self.ref = False
        return self.ref

    def check_spell_ru(self):
        return objs.get_enchant(lang='ru').check(self.n)
    
    def check_spell_yo(self):
        words = []
        for i in range(len(self.n)):
            if self.n[i] == 'е':
                word    = list(self.n)
                word[i] = 'ё'
                word    = ''.join(word)
                words.append(word)
        for word in words:
            if objs.get_enchant(lang='ru').check(word):
                return True
    
    def check_spell_us(self):
        return objs.get_enchant(lang='us').check(self.n)
    
    def check_spell_gb(self):
        return objs.get_enchant(lang='gb').check(self.n)
    
    def check_spell(self):
        ''' Enchant:
            1) Lower-case, upper-case and words where the first letter
               is capital, are all accepted. Mixed case is not accepted;
            2) Punctuation is not accepted;
            3) Empty input raises an exception;
            4) 'е' instead of 'ё' returns False, however, 'ё' in
               a wrong place returns True.
        '''
        if self.spell is None:
            self.spell = False
            if self.n:
                if Text(self.n).has_digits():
                    self.spell = True
                elif Text(self.n).has_cyrillic():
                    if self.check_spell_ru() or self.check_spell_yo():
                        self.spell = True
                elif Text(self.n).has_latin():
                    if self.check_spell_us() or self.check_spell_gb():
                        self.spell = True
                else:
                    self.spell = True
            else:
                self.spell = True
        return self.spell

    # Wrong selection upon search: see an annotation to SearchBox
    def get_tf(self):
        f = '[shared] logic.Word.get_tf'
        if self.tf is None:
            self.tf = '1.0'
            # This could happen if double line breaks were not deleted
            if self.sentno is None:
                com.rep_empty(f)
            else:
                # This is easier, but assigning a tag throws an error
                #self.tf = '1.0+%dc' % (self.pf - self.sentno)
                result = self.pf - self.sentslen
                if self.sentno > 0 and result > 0:
                    result -= 1
                self.tf = '%d.%d' % (self.sentno + 1,result)
                #objs.get_mes(f,str(self.tf),True).show_debug()
        return self.tf

    def get_tl(self):
        f = '[shared] logic.Word.get_tl'
        if self.tl is None:
            self.tl = '1.1'
            # This could happen if double line breaks were not deleted
            if self.sentno is None:
                com.rep_empty(f)
            else:
                # This is easier, but assigning a tag throws an error
                #self.tl = '1.0+%dc' % (self.pl - self.sentno + 1)
                result = self.pl - self.sentslen
                if self.sentno > 0 and result > 0:
                    result -= 1
                self.tl = '%d.%d' % (self.sentno + 1,result + 1)
                #objs.get_mes(f,str(self.tl),True).show_debug()
        return self.tl



# Use cases: case-insensitive search; spellchecking; text comparison
# Requires Search, Text
class Words:

    def __init__(self,text,Auto=False):
        f = '[shared] logic.Words.__init__'
        self.Success = True
        self.Auto    = Auto
        self.set_values()
        if text:
            mes = _('Analyze the text')
            objs.get_mes(f,mes,True).show_info()
            ''' This is MUCH faster than using old symbol-per-symbol
                algorithm for finding words. We must, however, drop
                double space cases.
            '''
            self.textorig = Text(text=text,Auto=self.Auto).text
            self.linebr   = Search(self.textorig,'\n').get_next_loop()
            self.textp    = Text(text=self.textorig).delete_line_breaks()
            self.textn    = Text(text=self.textp).delete_punctuation().lower()
            self.split()
        else:
            self.Success = False
            com.cancel(f)
                       
    def set_values(self):
        self.no       = 0
        self.words    = []
        self.linebr   = []
        self.listnm   = []
        self.textnm   = None
        self.textorig = ''
        self.textp    = ''
        self.textn    = ''

    def split(self):
        f = '[shared] logic.Words.split'
        if self.Success:
            if not self.get_len():
                lst_p = self.textp.split(' ')
                lst_n = self.textn.split(' ')
                assert len(lst_p) == len(lst_n)
                cur_len_p = cur_len_n = 0
                for i in range(len(lst_p)):
                    if i > 0:
                        cur_len_p += 2
                        cur_len_n += 2
                    cur_word = Word()
                    cur_word.p = lst_p[i]
                    cur_word.n = lst_n[i]
                    cur_word.pf = cur_len_p
                    cur_word.nf = cur_len_n
                    cur_len_p = cur_word.pl = cur_word.pf \
                                            + len(cur_word.p) - 1
                    cur_len_n = cur_word.nl = cur_word.nf \
                                            + len(cur_word.n) - 1
                    self.words.append(cur_word)
        else:
            com.cancel(f)

    def print(self):
        f = '[shared] logic.Words.print'
        if self.Success:
            for i in range(self.get_len()):
                self.words[i].print(no=i)
        else:
            com.cancel(f)

    # Running 'range(self.get_len())' does not re-run 'get_len'
    def get_len(self):
        return len(self.words)

    def _get_sent_nos(self):
        no = sents_len = 0
        for i in range(self.get_len()):
            condition1 = self.words[i].pf - 1 in self.linebr
            if self.Auto:
                condition = condition1
            else:
                # In case duplicate spaces/line breaks were not deleted
                condition2 = self.words[i].p == '\n' \
                             or self.words[i].p == '\r' \
                             or self.words[i].p == '\r\n'
                condition = condition1 or condition2
            if condition:
                no += 1
                sents_len = self.words[i].pf - 1
            self.words[i].sentno = no
            self.words[i].sentslen = sents_len

    def get_sent_nos(self):
        f = '[shared] logic.Words.get_sent_nos'
        if self.Success:
            if self.get_len() > 0:
                if self.words[self.no].sentno is None:
                    self._get_sent_nos()
        else:
            com.cancel(f)

    def get_sent_p(self):
        f = '[shared] logic.Words.get_sent_p'
        if self.Success:
            sent_no = self.get_sent_no()
            sent_no = Input(f,sent_no).get_integer()
            old     = self.no
            result = []
            for self.no in range(self.get_len()):
                if self.words[self.no].sentno == sent_no:
                    result.append(self.words[self.no].p)
            self.no = old
            return ' '.join(result)
        else:
            com.cancel(f)

    def get_sent_no(self):
        f = '[shared] logic.Words.get_sent_no'
        if self.Success:
            self.get_sent_nos()
            return self.words[self.no].sentno
        else:
            com.cancel(f)

    def get_next_ref(self):
        f = '[shared] logic.Words.get_next_ref'
        if self.Success:
            old = self.no
            Found = False
            while self.no < self.get_len():
                if self.words[self.no].has_ref():
                    Found = True
                    break
                else:
                    self.no += 1
            if not Found:
                self.no = old
            return self.no
        else:
            com.cancel(f)

    def get_prev_ref(self):
        f = '[shared] logic.Words.get_prev_ref'
        if self.Success:
            old = self.no
            Found = False
            while self.no >= 0:
                if self.words[self.no].ref():
                    Found = True
                    break
                else:
                    self.no -= 1
            if not Found:
                self.no = old
            return self.no
        else:
            com.cancel(f)

    def check_spell(self):
        f = '[shared] logic.Words.check_spell'
        if self.Success:
            if self.get_len() > 0:
                if self.words[0].spell is None:
                    for i in range(self.get_len()):
                        self.words[i].check_spell()
        else:
            com.cancel(f)

    def _get_refs(self):
        for i in range(self.get_len()):
            self.words[i].has_ref()

    def get_refs(self):
        f = '[shared] logic.Words.get_refs'
        if self.Success:
            if self.get_len() > 0:
                if self.words[0].ref is None:
                    self._get_refs()
        else:
            com.cancel(f)

    # Needed for text comparison
    def get_list_nm(self):
        f = '[shared] logic.Words.get_list_nm'
        if self.Success:
            if not self.listnm:
                cur_len_nm = 0
                for i in range(self.get_len()):
                    self.listnm.append(self.words[i].get_nm())
                    if i > 0:
                        cur_len_nm += 2
                    cur_word     = self.words[i]
                    cur_word.nmf = cur_len_nm
                    cur_len_nm   = cur_word.nml = cur_word.nmf \
                                                + len(cur_word.nm) - 1
            return self.listnm
        else:
            com.cancel(f)

    # Needed for text comparison
    def get_text_nm(self):
        f = '[shared] logic.Words.get_text_nm'
        if self.Success:
            if not self.textnm:
                self.textnm = ' '.join(self.get_list_nm())
            return self.textnm
        else:
            com.cancel(f)

    def get_no_by_pos_p(self,pos):
        f = '[shared] logic.Words.get_no_by_pos_p'
        if self.Success:
            result = self.no
            for i in range(self.get_len()):
                if self.words[i].pf - 1 <= pos <= self.words[i].pl + 1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    def get_no_by_pos_n(self,pos):
        f = '[shared] logic.Words.get_no_by_pos_n'
        if self.Success:
            result = self.no
            for i in range(self.get_len()):
                if self.words[i].nf - 1 <= pos <= self.words[i].nl + 1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    # Call 'get_list_nm()' first
    def get_no_by_pos_nm(self,pos):
        f = '[shared] logic.Words.get_no_by_pos_nm'
        if self.Success:
            result = self.no
            for i in range(self.get_len()):
                if self.words[i].nmf - 1 <= pos <= self.words[i].nml+1:
                    result = i
                    break
            return result
        else:
            com.cancel(f)

    def get_no_by_tk(self,tkpos):
        f = '[shared] logic.Words.get_no_by_tk'
        if self.Success:
            if tkpos:
                lst = tkpos.split('.')
                if len(lst) == 2:
                    lst[0] = Text(text=lst[0]).str2int()
                    if lst[0] > 0:
                        lst[0] -= 1
                    lst[1] = Text(text=lst[1]).str2int()
                    result = None
                    for i in range(self.len()):
                        if self.words[i].sentno == lst[0]:
                            result = self.words[i].sentslen
                            break
                    if result is not None:
                        if lst[1] == 0:
                            result += 1
                        elif lst[0] == 0:
                            result += lst[1]
                        else:
                            result += lst[1] + 1
                        mes = '{} -> {}'.format(tkpos,result)
                        objs.get_mes(f,mes,True).show_debug()
                        return self.get_no_by_pos_p(pos=result)
                else:
                    mes = _('Wrong input data: "{}"!').format(lst)
                    objs.get_mes(f,mes).show_warning()
            else:
                com.rep_empty(f)
        else:
            com.cancel(f)

    def get_nos_by_sent_no(self,sent_no=0):
        f = '[shared] logic.Words.get_nos_by_sent_no'
        result = (0,0)
        if self.Success:
            sent_no = Input(f,sent_no).get_integer()
            old = self.no
            nos = []
            for self.no in range(self.get_len()):
                if sent_no == self.get_sent_no():
                    nos.append(self.no)
            self.no = old
            if nos:
                # Valid for one-word paragraph
                result = (min(nos),max(nos))
            else:
                mes = _('Failed to find words of paragraph #{}!')
                mes = mes.format(sent_no)
                objs.get_mes(f,mes,True).show_warning()
        else:
            com.cancel(f)
        return result

    def complete(self):
        f = '[shared] logic.Words.complete'
        if self.Success:
            self.get_sent_nos()
            for i in range(self.get_len()):
                self.words[i].is_empty()
                self.words[i].has_ref()
                self.words[i].get_nm()
                self.words[i].check_spell()
                self.words[i].get_tf()
                self.words[i].get_tl()
            self.get_text_nm()
        else:
            com.cancel(f)



class Search:

    def __init__(self,text=None,pattern=None):
        self.Success  = False
        self.i        = 0
        self.nextloop = []
        self.prevloop = []
        if text and pattern:
            self.reset (text    = text
                       ,pattern = pattern
                       )

    def reset(self,text,pattern):
        f = '[shared] logic.Search.reset'
        self.Success  = True
        self.i        = 0
        self.nextloop = []
        self.prevloop = []
        self.text     = text
        self.pattern  = pattern
        if not self.pattern or not self.text:
            self.Success = False
            mes = _('Wrong input data!')
            objs.get_mes(f,mes,True).show_warning()

    def add(self):
        f = '[shared] logic.Search.add'
        if self.Success:
            if len(self.text) > self.i + len(self.pattern) - 1:
                self.i += len(self.pattern)
        else:
            com.cancel(f)

    def get_next(self):
        f = '[shared] logic.Search.get_next'
        if self.Success:
            result = self.text.find(self.pattern,self.i)
            if result != -1:
                self.i = result
                self.add()
            return result
        else:
            com.cancel(f)

    def get_prev(self):
        f = '[shared] logic.Search.get_prev'
        if self.Success:
            ''' rfind, unlike find, does not include limits, so we can
                use it to search backwards
            '''
            result = self.text.rfind(self.pattern,0,self.i)
            if result != -1:
                self.i = result
            return result
        else:
            com.cancel(f)

    def get_next_loop(self):
        f = '[shared] logic.Search.get_next_loop'
        if self.Success:
            if not self.nextloop:
                self.i = 0
                while True:
                    result = self.get_next()
                    if result == -1:
                        break
                    else:
                        self.nextloop.append(result)
        else:
            com.cancel(f)
        return self.nextloop

    def get_prev_loop(self):
        f = '[shared] logic.Search.get_prev_loop'
        if self.Success:
            if not self.prevloop:
                self.i = len(self.text)
                while True:
                    result = self.get_prev()
                    if result == -1:
                        break
                    else:
                        self.prevloop.append(result)
        else:
            com.cancel(f)
        return self.prevloop



class OCR:

    def __init__(self,text):
        self.text = text

    # Texts in Latin characters only
    def cyr2lat(self):
        ''' 'У' -> 'Y' is not actually an OCR error, but rather a human
            one.
        '''
        cyr = ['А','В','Е','К','М','Н','О','Р','С','Т','У','Х','Ь','а'
              ,'е','о','р','с','у'
              ]
        lat = ['A','B','E','K','M','H','O','P','C','T','Y','X','b','a'
              ,'e','o','p','c','y'
              ]
        for i in range(len(cyr)):
            self.text = self.text.replace(cyr[i],lat[i])
        return self.text

    # Digits only
    def letter2digit(self):
        self.text = self.text.replace('З','3').replace('з','3')
        self.text = self.text.replace('O','0').replace('О','0')
        self.text = self.text.replace('б','6')
        return self.text

    def run_common(self):
        # 100o => 100°
        self.text = re.sub(r'(\d+)[oо]',r'\1°',self.text)
        # 106а => 106a (Cyrillic)
        self.text = re.sub(r'(\d+)а',r'\1a',self.text)
        # 106е => 106e (Cyrillic)
        self.text = re.sub(r'(\d+)е',r'\1e',self.text)
        # 106Ь => 106b
        self.text = re.sub(r'(\d+)Ь',r'\1b',self.text)
        # А1 => A1 (Cyrillic)
        self.text = re.sub(r'А(\d+)',r'A\1',self.text)
        # 1А => 1A (Cyrillic)
        self.text = re.sub(r'(\d+)А',r'\1A',self.text)
        # В1 => B1 (Cyrillic)
        self.text = re.sub(r'В(\d+)',r'B\1',self.text)
        # 1В => 1B (Cyrillic)
        self.text = re.sub(r'(\d+)В',r'\1B',self.text)
        # С1 => C1 (Cyrillic)
        self.text = re.sub(r'С(\d+)',r'C\1',self.text)
        # 1С => 1C (Cyrillic)
        self.text = re.sub(r'(\d+)С',r'\1C',self.text)
        # Fix a degree sign
        self.text = re.sub (r'[\s]{0,1}[°o][\s]{0,1}[CС](\W)'
                           ,r'°C',self.text
                           )
        return self.text



class Decline:
    ''' #note ABOUT PYMORPHY2:
        1) Input must be stripped of punctuation, otherwise, the program
           fails.
        2) Output keeps unstripped spaces to the left, however, spaces
           to the right fail the program.
        3) Input can have any register. The output is lower-case.
        4) Output can have 'ё' irrespectively of input.
    '''
    def __init__ (self,text='',number=''
                 ,case='',Auto=True):
        if text:
            self.reset (text   = text
                       ,number = number
                       ,case   = case
                       ,Auto   = Auto
                       )
        else:
            self.Auto   = Auto
            self.orig   = ''
            self.number = 'sing'
            self.case   = 'nomn'
            self.lst    = []

    def reset(self,text,number='',case='',Auto=True):
        ''' #TODO:
            1) Restore punctuation
            2) Optional leading/trailing spaces
        '''
        self.orig = text
        self.number = number
        # 'nomn', 'gent', 'datv', 'accs', 'ablt', 'loct'
        self.case = case
        self.Auto = Auto
        if self.Auto:
            result = Text(text=self.orig).delete_punctuation()
        else:
            result = self.orig
        self.lst = result.split(' ')
        ''' Returning 'self' allows to call 'get' in the same line, e.g.
            Decline(text='текст').normal().get()
        '''
        return self

    def get(self):
        result = ' '.join(self.lst)
        if self.Auto:
            result = result.replace('ё','е')
        return result

    def decline(self):
        f = '[shared] logic.Decline.decline'
        for i in range(len(self.lst)):
            # Inflecting '', None, digits and Latin words *only* fails
            ''' mes = _('Decline "{}" in "{}" number and "{}" case')
                mes = mes.format (self.lst[i]
                                 ,self.number()
                                 ,self.case()
                                 )
                objs.get_mes(f,mes,True).show_debug()
            '''
            try:
                form = objs.get_morph().parse(self.lst[i])[0]
                form = form.inflect({self.get_number(),self.get_case()})
                form = form.word
                self.lst[i] = form
            except AttributeError:
                pass
        return self

    # If input is a phrase, 'normal' each word of it
    def get_normal(self):
        for i in range(len(self.lst)):
            form = objs.get_morph().parse(self._list[i])[0]
            self.lst[i] = form.normal_form
        return self

    def get_number(self):
        f = '[shared] logic.Decline.get_number'
        if not self.number:
            self.number = 'sing'
            # Needed by 'max'
            if self.lst:
                tmp = []
                for i in range(len(self.lst)):
                    if self.lst[i]:
                        # Returns 'sing', 'plur' or None
                        number = self.lst[i][0].tag.number
                        tmp.append(objs.get_morph().parse(number))
                if tmp and max(tmp,key=tmp.count) == 'plur':
                    self.number = 'plur'
            ''' mes = str(self.number)
                objs.get_mes(f,mes,True).show_debug()
            '''
        return self.number

    def get_case(self):
        f = '[shared] logic.Decline.get_case'
        if not self.case:
            self.case = 'nomn'
            # Needed by 'max'
            if self.lst:
                tmp = []
                for i in range(len(self.lst)):
                    if self.lst[i]:
                        form = objs.get_morph().parse(self.lst[i])[0]
                        tmp.append(form.tag.case)
                result = max(tmp,key=tmp.count)
                if result:
                    self.case = result
            mes = str(self.case)
            objs.get_mes(f,mes,True).show_debug()
        return self.case



class Objects:
    ''' Values here will be kept through different modules (but not
        through different programs both using 'shared.py').
    '''
    def __init__(self):
        self.enchant_ru = self.morph = self.pretty_table \
                         = self.pdir = self.online = self.tmpfile \
                         = self.os = self.mes = None
        self.icon = ''

    def get_mes (self,func=_('Logic error!')
                ,message=_('Logic error!')
                ,Silent=False
                ):
        if self.mes is None:
            self.mes = Message
        return self.mes(func,message,Silent)
    
    def get_os(self):
        if self.os is None:
            self.os = OSSpecific()
        return self.os
    
    def get_tmpfile(self,suffix='.htm',Delete=0):
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

    def get_enchant(self,lang='ru'):
        import enchant
        if not self.enchant_ru:
            self.enchant_ru = enchant.Dict('ru_RU')
            self.enchant_gb = enchant.Dict('en_GB')
            self.enchant_us = enchant.Dict('en_US')
        if lang == 'ru':
            return self.enchant_ru
        elif lang == 'gb':
            return self.enchant_gb
        elif lang == 'us':
            return self.enchant_us
        else:
            mes = 'An unknown mode "{}"!\n\nThe following modes are supported: "{}".'
            mes = mes.format(lang,'ru; gb; us')
            objs.get_mes(f,mes).show_error()
            return self.enchant_ru

    def get_morph(self):
        if not self.morph:
            import pymorphy2
            self.morph = pymorphy2.MorphAnalyzer()
        return self.morph

    def get_pretty_table(self):
        if not self.pretty_table:
            from prettytable import PrettyTable
            self.pretty_table = PrettyTable
        return self.pretty_table



class MessagePool:

    def __init__(self,max_size=5):
        self.max_size = max_size
        self.pool = []

    def free(self):
        if len(self.pool) == self.max_size:
            self.delete_first()

    def add(self,message):
        f = '[shared] logic.MessagePool.add'
        if message:
            self.free()
            self.pool.append(message)
        else:
            com.rep_empty(f)

    def delete_first(self):
        f = '[shared] logic.MessagePool.delete_first'
        if len(self.pool) > 0:
            del self.pool[0]
        else:
            mes = _('The pool is empty!')
            objs.get_mes(f,mes,True).show_warning()

    def delete_last(self):
        f = '[shared] logic.MessagePool.delete_last'
        if len(self.pool) > 0:
            del self.pool[-1]
        else:
            mes = _('The pool is empty!')
            objs.get_mes(f,mes,True).show_warning()

    def clear(self):
        self.pool = []

    def get(self):
        return List(lst1=self.pool).space_items()



class ProgramDir:

    def __init__(self):
        self.dir = sys.path[0]
        # We run app, not interpreter
        if os.path.isfile(self.dir):
            self.dir = Path(path=self.dir).get_dirname()

    def add(self,*args):
        return os.path.join(self.dir,*args)



class Timer:

    def __init__(self,func_title='__main__'):
        self.startv = 0
        self.func_title = func_title

    def start(self):
        self.startv = time.time()

    def end(self):
        delta = float(time.time()-self.startv)
        mes = _('The operation has taken {} s.').format(delta)
        objs.get_mes(self.func_title,mes,True).show_debug()
        return delta



class Table:

    def __init__ (self,headers,rows
                 ,Shorten=True,MaxRow=18
                 ,MaxRows=20
                 ):
        f = '[shared] logic.Table.__init__'
        self.headers = headers
        self.rows    = rows
        self.Shorten = Shorten
        self.MaxRow  = MaxRow
        self.MaxRows = MaxRows
        if self.headers and self.rows:
            self.Success = True
        else:
            self.Success = False
            com.rep_empty(f)

    def _shorten_headers(self):
        self._headers = [Text(text=header).shorten(max_len=self.MaxRow)\
                         for header in self.headers
                        ]
        # prettytable.py, 302: Exception: Field names must be unique!
        headers = list(set(self.headers))
        ''' prettytable.py, 818: Exception: Row has incorrect number of
            values
        '''
        if len(headers) != len(self.headers):
            result = List (lst1 = headers
                          ,lst2 = self.headers
                          ).equalize()
            if result:
                self.headers = result[0]

    def _shorten_rows(self):
        f = '[shared] logic.Table._shorten_rows'
        if self.MaxRows < 2 or self.MaxRows > len(self.rows):
            self.MaxRows = len(self.rows)
            mes = _('Set the max number of rows to {}')
            mes = mes.format(self.MaxRows)
            objs.get_mes(f,mes,True).show_info()
        self.MaxRows = int(self.MaxRows / 2)
        pos3 = len(self.rows)
        pos2 = pos3 - self.MaxRows
        self.rows = self.rows[0:self.MaxRows] + self.rows[pos2:pos3]

    def _shorten_row(self):
        # Will not be assigned without using 'for i in range...'
        for i in range(len(self.rows)):
            if isinstance(self.rows[i],tuple):
                self.rows[i] = list(self.rows[i])
            for j in range(len(self.rows[i])):
                if isinstance(self.rows[i][j],str):
                    if len(self.rows[i][j]) > self.MaxRow:
                        self.rows[i][j] = self.rows[i][j][0:self.MaxRow]

    def shorten(self):
        f = '[shared] logic.Table.shorten'
        if self.Success:
            if self.Shorten:
                self._shorten_headers()
                self._shorten_rows()
                self._shorten_row()
        else:
            com.cancel(f)

    def print(self):
        f = '[shared] logic.Table.print'
        if self.Success:
            self.shorten()
            obj = objs.get_pretty_table()(self.headers)
            for row in self.rows:
                obj.add_row(row)
            print(obj)
        else:
            com.cancel(f)



class FixBaseName:
    ''' Return a path base name that would comply with OS-specific
        rules. We should not use absolute paths at input because we
        cannot tell for sure that the path separator is actually
        a separator and not an illegal character.
    '''
    def __init__(self,basename,AllOS=False,max_len=0):
        self.AllOS   = AllOS
        self.name    = basename
        self.max_len = max_len
        
    def set_length(self):
        if self.max_len:
            self.name = self.name[:self.max_len]
    
    def run_win(self):
        self.name = [char for char in self.name if not char \
                     in forbidden_win
                    ]
        self.name = ''.join(self.name)
        if self.name.endswith('.'):
            self.name = self.name[:-1]
        self.name = self.name.strip()
        if self.name.upper() in reserved_win:
            self.name = ''
        
    def run_lin(self):
        self.name = [char for char in self.name if not char \
                     in forbidden_lin
                    ]
        self.name = ''.join(self.name)
        self.name = self.name.strip()
        
    def run_mac(self):
        self.name = [char for char in self.name if not char \
                     in forbidden_mac
                    ]
        self.name = ''.join(self.name)
        self.name = self.name.strip()
        
    def run(self):
        if self.AllOS:
            self.run_win()
            self.run_lin()
            self.run_mac()
        elif objs.get_os().is_win():
            self.run_win()
        elif objs.os.is_lin():
            self.run_lin()
        elif objs.os.is_mac():
            self.run_mac()
        else:
            self.run_win()
            self.run_lin()
            self.run_mac()
        self.set_length()
        return self.name



class Get:
    
    def __init__ (self,url,coding='UTF-8'
                 ,Verbose=True,Verify=False
                 ,timeout=6
                 ):
        self.html    = ''
        self.timeout = timeout
        self.url     = url
        self.coding  = coding
        self.Verbose = Verbose
        self.Verify  = Verify
        self.use_unverified()
    
    def read(self):
        ''' This is a dummy function to return the final result.
            It is needed merely to use 'json' which calls 'read'
            for input object.
        '''
        return self.html
    
    def use_unverified(self):
        ''' On *some* systems we can get urllib.error.URLError: 
            <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED].
            To get rid of this error, we use this small workaround.
        '''
        f = '[shared] logic.Get.unverified'
        if not self.Verify:
            if hasattr(ssl,'_create_unverified_context'):
                ssl._create_default_https_context = ssl._create_unverified_context
            else:
                mes = _('Unable to use unverified certificates!')
                objs.get_mes(f,mes,True).show_warning()
        
    def _get(self):
        ''' Changing UA allows us to avoid a bot protection
            ('Error 403: Forbidden').
        '''
        f = '[shared] logic.Get._get'
        try:
            req = urllib.request.Request (url     = self.url
                                         ,data    = None
                                         ,headers = {'User-Agent': \
                                                     'Mozilla'
                                                    }
                                         )
            self.html = \
            urllib.request.urlopen(req,timeout=self.timeout).read()
            if self.Verbose:
                mes = _('[OK]: "{}"').format(self.url)
                objs.get_mes(f,mes,True).show_info()
        # Too many possible exceptions
        except Exception as e:
            mes = _('[FAILED]: "{}". Details: {}')
            mes = mes.format(self.url,e)
            objs.get_mes(f,mes,True).show_warning()
    
    def decode(self):
        ''' Set 'coding' to None to cancel decoding. This is useful
            if we are downloading a non-text content.
        '''
        f = '[shared] logic.Get.decode'
        if self.coding:
            if self.html:
                try:
                    self.html = \
                    self.html.decode(encoding=self.coding)
                except UnicodeDecodeError:
                    self.html = str(self.html)
                    mes = _('Unable to decode "{}"!').format(self.url)
                    objs.get_mes(f,mes,True).show_warning()
            else:
                com.rep_empty(f)
    
    def run(self):
        f = '[shared] logic.Get.run'
        if self.url:
            # Safely use URL as a string
            if isinstance(self.url,str):
                if self.Verbose:
                    timer = Timer(func_title=f)
                    timer.start()
                self._get()
                self.decode()
                if self.Verbose:
                    timer.end()
                return self.html
            else:
                mes = _('Wrong input data: {}!').format(self.url)
                objs.get_mes(f,mes).show_warning()
        else:
            com.rep_empty(f)



class References:
    
    def __init__(self,words1,words2):
        f = '[shared] logic.References.__init__'
        self.words1 = words1
        self.words2 = words2
        if self.words1 and self.words2 and len(self.words1.words) \
        and len(self.words2.words):
            self.Success = True
            self.words1.get_sent_nos()
            self.words2.get_sent_nos()
            self.words1.get_refs()
        else:
            self.Success = False
            com.rep_empty(f)
        
    def get_ref_before(self,word_no):
        f = '[shared] logic.References.get_ref_before'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no >= 0:
                    if self.words1.words[word_no].ref:
                        break
                    else:
                        word_no -= 1
                return word_no
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
        
    def get_ref_after(self,word_no):
        f = '[shared] logic.References.get_ref_after'
        if self.Success:
            if word_no < len(self.words1.words):
                while word_no < len(self.words1.words):
                    if self.words1.words[word_no].ref:
                        return word_no
                    else:
                        word_no += 1
                return -1
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
    
    def get_nearest_ref(self,word_no):
        f = '[shared] logic.References.get_nearest_ref'
        if self.Success:
            word_no1 = self.get_ref_before(word_no)
            word_no2 = self.get_ref_after(word_no)
            if word_no1 == -1 and word_no2 == -1:
                mes = _('No references have been found!')
                objs.get_mes(f,mes,True).show_info()
                return word_no
            elif word_no1 >= 0 and word_no2 == -1:
                mes = _('No references to the right!')
                objs.get_mes(f,mes,True).show_info()
                return word_no1
            elif word_no2 >= 0 and word_no1 == -1:
                mes = _('No references to the left!')
                objs.get_mes(f,mes,True).show_info()
                return word_no2
            else:
                delta_before = word_no - word_no1
                delta_after  = word_no2 - word_no
                if min(delta_before,delta_after) == delta_before:
                    return word_no1
                else:
                    return word_no2
        else:
            com.cancel(f)
                
    def get_repeated(self,word_no):
        f = '[shared] logic.References.get_repeated'
        if self.Success:
            if word_no < len(self.words1.words):
                count = 0
                for i in range(word_no+1):
                    if self.words1.words[i].n == self.words1.words[word_no].n:
                        count += 1
                return count
            else:
                sub = '{} < {}'.format(word_no,len(self.words1.words))
                mes = _('The condition "{}" is not observed!')
                mes = mes.format(sub)
                objs.get_mes(f,mes).show_error()
        else:
            com.cancel(f)
        
    def get_repeated2(self,word_n,count):
        f = '[shared] logic.References.get_repeated2'
        if self.Success:
            tmp = 0
            for i in range(len(self.words2.words)):
                if self.words2.words[i].n == word_n:
                   tmp += 1
                   if tmp == count:
                       return i
        else:
            com.cancel(f)



class Links:
    
    def __init__(self,text,root='href="'):
        self.set_values()
        self.text = text
        # Some sites omit 'http(s):' for their links
        self.text = self.text.replace('"//www.','"http://www.')
        self.root = root
        
    def redirect(self):
        for i in range(len(self.links)):
            if '?url' in self.links[i]:
                self.links[i] = re.sub('.*\?url=','',self.links[i])
                # Replace '%3A%2F%2F' with '://' and so on
                self.links[i] = urllib.parse.unquote(self.links[i])
    
    def set_values(self):
        self.pos   = 0
        self.links = []
    
    def get_poses(self):
        search = Search (text    = self.text
                        ,pattern = self.root
                        )
        loop = search.get_next_loop()
        for self.pos in loop:
            self.get_link()
            
    def get_link(self):
        f = '[shared] logic.Links.get_link'
        pos = self.pos + len(self.root)
        if pos >= len(self.text):
            mes = _('Unexpected end of text!')
            objs.get_mes(f,mes,True).show_warning()
        else:
            text = self.text[pos:]
            try:
                pos = text.index('"')
                self.links.append(text[:pos])
            except ValueError:
                mes = _('Wrong input data!')
                objs.get_mes(f,mes,True).show_warning()
                              
    def delete_duplicates(self):
        ''' Sometimes there are duplicate URLs on a page - we delete
            them there. We may need to preserve an original sorting so
            do not use 'set'.
        '''
        i = len(self.links) - 1
        while i >= 0:
            ind = self.links.index(self.links[i])
            if ind < i:
                del self.links[i]
            i -= 1
        return self.links
    
    def add_root(self,root):
        for i in range(len(self.links)):
            if self.links[i].startswith('/'):
                self.links[i] = root + self.links[i]
        return self.links
        
    def get_valid(self):
        self.links = [link for link in self.links \
                      if link.startswith('http')
                     ]
        return self.links



class FilterList:
    ''' Filter base names (case-ignorant) of files & folders in a path.
        Blacklist is a list of patterns, not obligatory full names.
    '''
    def __init__(self,path,blacklist=[]):
        self.lst     = []
        self.path    = path
        self.block   = blacklist
        self.Success = Directory(self.path).Success \
                       and isinstance(self.block,list)
    
    def set_block(self):
        f = '[shared] logic.FilterList.set_block'
        if self.Success:
            # Actually, there is no reason to use 'strip' here
            self.block = [item.lower() for item in self.block if item]
        else:
            com.cancel(f)
    
    def get_list(self):
        f = '[shared] logic.FilterList.get_list'
        if self.Success:
            if not self.lst:
                # Those are base names
                self.lst = os.listdir(self.path)
            return self.lst
        else:
            com.cancel(f)
    
    def filter(self):
        f = '[shared] logic.FilterList.filter'
        if self.Success:
            match = []
            for item in self.lst:
                for pattern in self.block:
                    if pattern in item.lower():
                        match.append(item)
                        break
            # This allows us to return matches as well if necessary
            mismatch = list(set(self.lst) - set(match))
            mismatch.sort()
            return [os.path.join(self.path,item) for item in mismatch]
        else:
            com.cancel(f)
        
    def run(self):
        self.set_block()
        self.get_list()
        return self.filter()



class Home:

    def __init__(self,app_name='myapp'):
        self.appname = app_name
        self.confdir = self.sharedir = ''
        
    def add_share(self,*args):
        return os.path.join(self.get_share_dir(),*args)
    
    def create_share(self):
        return Path(path=self.get_share_dir()).create()
    
    def get_share_dir(self):
        if not self.sharedir:
            if objs.get_os().is_win():
                os_folder = 'Application Data'
            else:
                os_folder = os.path.join('.local','share')
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
    
    def add(self,*args):
        return os.path.join(self.get_home(),*args)
    
    def add_config(self,*args):
        return os.path.join(self.get_conf_dir(),*args)



class Commands:

    def __init__(self):
        self.set_lang()
    
    def get_additives(self,number):
        f = '[shared] logic.Commands.get_additives'
        ''' Return integers by which a set integer is divisible (except
            for 1 and itself).
        '''
        result = []
        if str(number).isdigit():
            i = 2
            while i < number:
                if number % i == 0:
                    result.append(i)
                i += 1
        else:
            mes = _('Wrong input data: "{}"!').format(number)
            objs.get_mes(f,mes).show_warning()
        return result
    
    def set_figure_commas(self,figure):
        f = '[shared] logic.Commands.set_figure_commas'
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
                    figure.insert(i,_(','))
                i += 1
            figure = figure[::-1]
            figure = ''.join(figure)
        if Minus:
            figure = '-' + figure
        return figure
    
    def rep_failed (self,f='Logic error'
                   ,e='Logic error'
                   ,Silent=False
                   ):
        mes = _('Operation has failed!\n\nDetails: {}').format(e)
        objs.get_mes(f,mes,Silent).show_error()
    
    def sanitize(self,text):
        if text is None:
            text = ''
        else:
            text = Text(str(text)).delete_unsupported()
        return text
    
    def get_mod_color(self,rgb,delta):
        rgb = list(max(min(255,x/256+delta),0) for x in rgb)
        # We need to have integers here. I had a float once.
        rgb = tuple(int(item) for item in rgb)
        return '#%02x%02x%02x' % rgb
    
    def show_save_dialog(self,types=()):
        if not types:
            types = ((_('Plain text (UTF-8)'),'.txt' )
                    ,( _('Web-page')         ,'.htm' )
                    ,( _('Web-page')         ,'.html')
                    ,( _('All files')        ,'*'    )
                    )
        options                = {}
        options['initialfile'] = ''
        options['filetypes']   = types
        options['title']       = _('Save As:')
        return options
    
    def rep_lazy(self,func=_('Logic error!')):
        Message (func    = func
                ,message = _('Nothing to do!')
                ).show_info()
    
    def show_warning (self,func=_('Logic error!')
                     ,message=_('Logic error!')
                     ):
        objs.get_mes (func    = func
                     ,level   = _('WARNING')
                     ,message = message
                     )
    
    def show_info (self,func=_('Logic error!')
                  ,message=_('Logic error!')
                  ):
        objs.get_mes (func    = func
                     ,level   = _('INFO')
                     ,message = message
                     )
        
    # IEC standard
    def get_human_size(self,bsize,LargeOnly=False):
        result = '%d %s' % (0,_('B'))
        if bsize:
            tebibytes = bsize // pow(2,40)
            cursize   = tebibytes * pow(2,40)
            gibibytes = (bsize - cursize) // pow(2,30)
            cursize  += gibibytes * pow(2,30)
            mebibytes = (bsize - cursize) // pow(2,20)
            cursize  += mebibytes * pow(2,20)
            kibibytes = (bsize - cursize) // pow(2,10)
            cursize  += kibibytes * pow(2,10)
            rbytes    = bsize - cursize
            mes = []
            if tebibytes:
                mes.append('%d %s' % (tebibytes,_('TiB')))
            if gibibytes:
                mes.append('%d %s' % (gibibytes,_('GiB')))
            if mebibytes:
                mes.append('%d %s' % (mebibytes,_('MiB')))
            if not (LargeOnly and bsize // pow(2,20)):
                if kibibytes:
                    mes.append('%d %s' % (kibibytes,_('KiB')))
                if rbytes:
                    mes.append('%d %s' % (rbytes,_('B')))
            if mes:
                result = ' '.join(mes)
        return result
    
    def split_time(self,length=0):
        hours   = length // 3600
        all_sec = hours * 3600
        minutes = (length - all_sec) // 60
        all_sec += minutes * 60
        seconds = length - all_sec
        return(hours,minutes,seconds)
    
    def get_easy_time(self,length=0):
        f = '[shared] logic.Commands.get_easy_time'
        result = '00:00:00'
        if length:
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
            result = ':'.join(mes)
        else:
            com.rep_empty(f)
        return result
    
    def get_yt_date(self,date):
        # Convert a date provided by Youtube API to a timestamp
        f = '[shared] logic.Commands.get_yt_date'
        if date:
            pattern = '%Y-%m-%dT%H:%M:%S'
            itime = Time(pattern=pattern)
            # Prevent errors caused by 'datetime' parsing microseconds
            tmp = date.split('.')
            if date != tmp[0]:
                ind  = date.index('.'+tmp[-1])
                date = date[0:ind]
            itime.inst = datetime.datetime.strptime(date,pattern)
            return itime.get_timestamp()
        else:
            self.rep_empty(f)
    
    def get_yt_length(self,length):
        ''' Convert a length of a video provided by Youtube API (string)
            to seconds.
            Possible variants: PT%dM%dS, PT%dH%dM%dS, P%dDT%dH%dM%dS.
        '''
        f = '[shared] logic.Commands.get_yt_length'
        result = 0
        if length:
            if isinstance(length,str) and length[0] == 'P':
                days    = 0
                hours   = 0
                minutes = 0
                seconds = 0
                match = re.search(r'(\d+)D',length)
                if match:
                    days = int(match.group(1))
                match = re.search(r'(\d+)H',length)
                if match:
                    hours = int(match.group(1))
                match = re.search(r'(\d+)M',length)
                if match:
                    minutes = int(match.group(1))
                match = re.search(r'(\d+)S',length)
                if match:
                    seconds = int(match.group(1))
                result = days * 86400 + hours * 3600 + minutes * 60 \
                         + seconds
            else:
                mes = _('Wrong input data: "{}"!').format(length)
                objs.get_mes(f,mes).show_warning()
        else:
            self.rep_empty(f)
        return result
    
    def rewrite(self,file,Rewrite=False):
        ''' - We do not put this into File class because we do not need
              to check existence.
            - We use 'Rewrite' just to shorten other procedures (to be
              able to use 'self.rewrite' silently in the code without
              ifs).
        '''
        f = '[shared] logic.Commands.rewrite'
        if not Rewrite and os.path.isfile(file):
            ''' We don't actually need to force rewriting or delete
                the file before rewriting.
            '''
            mes = _('ATTENTION: Do yo really want to rewrite file "{}"?')
            mes = mes.format(file)
            return objs.get_mes(f,mes).show_question()
        else:
            ''' We return True so we may proceed with writing
                if the file has not been found.
            '''
            return True
    
    def set_lang(self):
        result = locale.getdefaultlocale()
        if result and len(result) > 0 and result[0]:
            if 'ru' in result[0]:
                globs['ui_lang'] = 'ru'
                globs['license_url'] = gpl3_url_ru
            else:
                globs['ui_lang'] = 'en'
                globs['license_url'] = gpl3_url_en
        else:
            globs['ui_lang'] = 'en'
    
    def get_tmpfile(self,suffix='.htm',Delete=0):
        return tempfile.NamedTemporaryFile (mode     = 'w'
                                           ,encoding = 'UTF-8'
                                           ,suffix   = suffix
                                           ,delete   = Delete
                                           ).name
    
    def get_human_time(self,delta):
        f = '[shared] logic.Commands.get_human_time'
        result = '%d %s' % (0,_('sec'))
        # Allows to use 'None'
        if delta:
            if isinstance(delta,int) or isinstance(delta,float):
                # 'datetime' will output years even for small integers
                # https://kalkulator.pro/year-to-second.html
                years   = delta // 31536000.00042889
                all_sec = years * 31536000.00042889
                months  = (delta - all_sec) // 2592000.0000000005
                all_sec += months * 2592000.0000000005
                weeks   = (delta - all_sec) // 604800
                all_sec += weeks * 604800
                days    = (delta - all_sec) // 86400
                all_sec += days * 86400
                hours   = (delta - all_sec) // 3600
                all_sec += hours * 3600
                minutes = (delta - all_sec) // 60
                all_sec += minutes * 60
                seconds = delta - all_sec
                mes = []
                if years:
                    mes.append('%d %s' % (years,_('yrs')))
                if months:
                    mes.append('%d %s' % (months,_('mths')))
                if weeks:
                    mes.append('%d %s' % (weeks,_('wks')))
                if days:
                    mes.append('%d %s' % (days,_('days')))
                if hours:
                    mes.append('%d %s' % (hours,_('hrs')))
                if minutes:
                    mes.append('%d %s' % (minutes,_('min')))
                if seconds:
                    mes.append('%d %s' % (seconds,_('sec')))
                if mes:
                    result = ' '.join(mes)
            else:
                mes = _('Wrong input data: "{}"!').format(delta)
                Message (func    = f
                        ,message = mes
                        ).show_warning()
        else:
            self.rep_empty(f)
        return result
    
    def cancel(self,func):
        Message (func    = func
                ,message = _('Operation has been canceled.')
                ).show_warning()
    
    def rep_empty(self,func):
        Message (func    = func
                ,message = _('Empty input is not allowed!')
                ).show_warning()
    
    def rep_not_ready(self,func):
        Message (func    = func
                ,message = _('Not implemented yet!')
                ).show_info()


''' If there are problems with import or tkinter's wait_variable, put
    this beneath 'if __name__'
'''
com  = Commands()
log  = Log (Use   = True
           ,Short = False
           )
objs = Objects()


if __name__ == '__main__':
    f = '[shared] logic.__main__'
    ReadTextFile('/tmp/aaa').get()
