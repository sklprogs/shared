#!/usr/bin/python3
# -*- coding: UTF-8 -*-

copyright = 'Copyright 2015-2024, Peter Sklyar'
license = 'GPL v.3'
email = 'skl.progs@gmail.com'

import re
import sys
import locale
from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep


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
                 ,'’', "'", '*']

forbidden_win = '/\?%*:|"<>'
forbidden_lin = '/'
forbidden_mac = '/\?*:|"<>'
reserved_win = ['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4'
               ,'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3'
               ,'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']


class GetOs:

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
            Message(self.title, mes, False).show_warning()
            self.value = 0.0
        return self.value
    
    def get_list(self):
        if not isinstance(self.value, list):
            rep.wrong_input(self.title)
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
            #Message(self.title, mes).show_debug()
        elif Negative and re.match('-\d+$', self.value):
            ''' 'isinstance' will detect negative integers too, however, we can
                also have a string at input.
            '''
            old = self.value
            self.value = int(self.value.replace('-', '', 1))
            self.value -= self.value * 2
            mes = _('Convert "{}" to an integer').format(old)
            Message(self.title, mes).show_debug()
        else:
            mes = _('Integer is required at input, but found "{}"! Return 0')
            mes = mes.format(self.value)
            Message(self.title, mes).show_warning()
            self.value = 0
        return self.value

    def get_not_none(self):
        # Insert '' instead of 'None' into text widgets
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
            rep.condition(f, mes)
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
            mes = mes.format(opening_sym, self.text.count(opening_sym)
                            ,closing_sym, self.text.count(closing_sym))
            Message(f, mes, True).show_warning()
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
            rep.empty(f)
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
            Message(f, mes, True).show_warning()
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
            Message(f, mes).show_warning()
        return par

    def str2float(self):
        f = '[SharedQt] logic.Text.str2float'
        par = 0.0
        try:
            par = float(self.text)
        except(ValueError, TypeError):
            mes = _('Failed to convert "{}" to a floating-point number!')
            mes = mes.format(self.text)
            Message(f, mes).show_warning()
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
            Message(f, mes, True).show_warning()
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
            rep.empty(f)
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
    
    def set_lang(self):
        f = '[SharedQt] logic.Commands.set_lang'
        result = locale.getlocale()
        if result and result[0]:
            result = result[0].lower()
            # Possible input: None, ru_RU, Russian_Russia
            if 'ru' in result:
                self.lang = 'ru'
                self.license_url = gpl3_url_ru
            elif 'de' in result or 'ger' in result:
                self.lang = 'de'
            elif 'es' in result:
                self.lang = 'es'
            elif 'uk' in result:
                self.lang = 'uk'
            elif 'pl' in result or 'pol' in result:
                self.lang = 'pl'
            elif 'zh' in result:
                self.lang = 'zh'
        Message(f, f'{result} -> {self.lang}').show_debug()
    
    def get_human_time(self, delta):
        f = '[SharedQt] logic.Commands.get_human_time'
        result = '%d %s' % (0, _('sec'))
        # Allows to use 'None'
        if not delta:
            self.rep_empty(f)
            return result
        if not isinstance(delta, int) and not isinstance(delta, float):
            mes = _('Wrong input data: "{}"!').format(delta)
            Message(f, mes).show_warning()
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


com = Commands()
OS = GetOs()
