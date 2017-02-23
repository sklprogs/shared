#!/usr/bin/python3
# -*- coding: UTF-8 -*-

author = 'Peter Sklyar'
copyright = 'Copyright 2015-2017, Peter Sklyar'
license = 'GPL v.3'
version = '1.0'
email = 'skl.progs@gmail.com'

import re
import os, sys
import mes_ru
import mes_en
from configparser import SafeConfigParser



class OSSpecific:
	
	def __init__(self):
		self._sys = ''
		self._sep = ''
		self.sys()
		self.sep()
	
	def sys(self):
		if not self._sys:
			self._sys = 'unknown'
			sys_plat = sys.platform
			if 'win' in sys_plat:
				self._sys = 'win'
			elif 'lin' in sys_plat:
				self._sys = 'lin'
			elif 'mac' in sys_plat:
				self._sys = 'mac'
		return self._sys
	
	def sep(self):
		if not self._sep:
			self._sep = os.path.sep
		return self._sep



config_parser = SafeConfigParser()

gpl3_url_en = 'http://www.gnu.org/licenses/gpl.html'
gpl3_url_ru = 'http://rusgpl.ru/rusgpl.html'

globs = {'int':{},'bool':{},'var':{}}

lev_crit = 'CRITICAL'
lev_debug = 'DEBUG'
lev_debug_err = 'DEBUG-ERROR'
lev_err = 'ERROR'
lev_info = 'INFO'
lev_ques = 'QUESTION'
lev_warn = 'WARNING'

ru_alphabet = '№АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЪЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщыъьэюя'
ru_alphabet_low = 'аеиоубявгдёжзйклмнпрстфхцчшщыъьэю№' # Some vowels are put at the start for the faster search
lat_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
lat_alphabet_low = 'abcdefghijklmnopqrstuvwxyz'
greek_alphabet = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω'
greek_alphabet_low = 'αβγδεζηθικλμνξοπρστυφχψω'
other_alphabet = 'ÀÁÂÆÇÈÉÊÑÒÓÔÖŒÙÚÛÜàáâæßçèéêñòóôöœùúûü'
other_alphabet_low = 'àáâæßçèéêñòóôöœùúûü'
digits = '0123456789'

SectionBooleans = 'Boolean'
SectionBooleans_abbr = 'bool'
SectionFloatings = 'Floating Values'
SectionFloatings_abbr = 'float'
SectionIntegers = 'Integer Values'
SectionIntegers_abbr = 'int'
SectionLinuxSettings = 'Linux settings'
SectionMacSettings = 'Mac settings'
SectionVariables = 'Variables'
SectionVariables_abbr = 'var'
SectionWindowsSettings = 'Windows settings'

punc_array = ['.',',','!','?',':',';']
#punc_ext_array = ['"','”','»',']','}',')'] # todo: why there were no opening brackets?
punc_ext_array = ['"','“','”','','«','»','[',']','{','}','(',')']

# All third-party modules are the intellectual work of their authors.

third_parties = '''
tkinterhtml
https://bitbucket.org/aivarannamaa/tkinterhtml
License: MIT
Copyright (c) <year> aivarannamaa

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

h_os = OSSpecific()
