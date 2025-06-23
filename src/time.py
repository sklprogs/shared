#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import calendar
import datetime

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.logic import Text


class Timer:

    def __init__(self, func_title='__main__'):
        self.startv = 0
        self.func_title = func_title

    def start(self):
        self.startv = time.time()

    def end(self):
        delta = float(time.time() - self.startv)
        mes = _('The operation has taken {} s.').format(delta)
        Message(self.func_title, mes).show_debug()
        return delta



class Time:
    # Values depend on each other and should be recalculated
    def __init__(self, pattern='%Y-%m-%d', tstamp=None):
        self.Success = True
        self.inst = None
        self.pattern = pattern
        self.tstamp = tstamp
        self.set_instance()
    
    def get_date_gen(self):
        f = '[shared] time.Time.get_date_gen'
        day = self.get_day()
        month = self.get_month_gen()
        year = self.get_year()
        if not self.Success:
            rep.cancel(f)
            return ''
        return f'{day} {month} {year}'
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Set time parameters are incorrect or not supported.\n\nDetails: {}')
        mes = mes.format(e)
        Message(f, mes, True).show_error()

    def add_days(self, days_delta):
        f = '[shared] time.Time.add_days'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.inst += datetime.timedelta(days_delta)
        except Exception as e:
            self.fail(f, e)

    def get_date(self):
        f = '[shared] time.Time.get_date'
        if not self.Success:
            rep.cancel(f)
            return ''
        try:
            return self.inst.strftime(self.pattern)
        except Exception as e:
            self.fail(f, e)
        return ''

    def set_instance(self):
        f = '[shared] time.Time.set_instance'
        if self.tstamp is None:
            self.set_todays_date()
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.inst = datetime.datetime.fromtimestamp(self.tstamp)
        except Exception as e:
            self.fail(f, e)

    def get_month_name(self):
        f = '[shared] time.Time.get_month_name'
        if not self.Success:
            rep.cancel(f)
            return ''
        month_int = Text(self.inst.strftime("%m")).str2int()
        return _(calendar.month_name[month_int])
    
    def get_day(self):
        f = '[shared] time.Time.get_day'
        if not self.Success:
            rep.cancel(f)
            return 0
        return Text(self.inst.strftime("%d")).str2int()
    
    def get_day_name(self):
        f = '[shared] time.Time.get_day_name'
        if not self.Success:
            rep.cancel(f)
            return ''
        try:
            return _(self.inst.strftime('%A'))
        except Exception as e:
            self.fail(f, e)
        return ''
    
    def get_day_abbr(self):
        # Get localized three-letter day abbreviation
        f = '[shared] time.Time.get_day_abbr'
        if not self.Success:
            rep.cancel(f)
            return ''
        try:
            return _(self.inst.strftime('%a'))
        except Exception as e:
            self.fail(f, e)
        return ''
    
    def get_day_abbr2(self):
        # Get localized two-letter day abbreviation
        f = '[shared] time.Time.get_day_abbr2'
        day = self.get_day_abbr()
        if not self.Success:
            rep.cancel(f)
            return ''
        if day == _('Mon'):
            return _('Mo')
        if day == _('Tue'):
            return _('Tu')
        if day == _('Thu'):
            return _('Th')
        if day == _('Fri'):
            return _('Fr')
        if day == _('Sat'):
            return _('Sa')
        if day == _('Sun'):
            return _('Su')
        return ''
    
    def get_month_abbr(self):
        f = '[shared] time.Time.get_month_abbr'
        if not self.Success:
            rep.cancel(f)
            return ''
        month_int = Text(self.inst.strftime("%m")).str2int()
        return _(calendar.month_abbr[month_int])
    
    def get_month_gen(self):
        f = '[shared] time.Time.get_month_gen'
        month = self.get_month_name()
        if not self.Success:
            rep.cancel(f)
            return ''
        match month:
            case 'Январь':
                return 'января'
            case 'Февраль':
                return 'февраля'
            case 'Март':
                return 'марта'
            case 'Апрель':
                return 'апреля'
            case 'Май':
                return 'мая'
            case 'Июнь':
                return 'июня'
            case 'Июль':
                return 'июля'
            case 'Август':
                return 'августа'
            case 'Сентябрь':
                return 'сентября'
            case 'Октябрь':
                return 'октября'
            case 'Ноябрь':
                return 'ноября'
            case 'Декабрь':
                return 'декабря'
            case other:
                return other

    def set_todays_date(self):
        f = '[shared] time.Time.set_todays_date'
        self.inst = datetime.datetime.today()
        date = self.get_date()
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.tstamp = time.mktime(datetime.datetime.strptime(date, self.pattern).timetuple())
        except Exception as e:
            self.fail(f, e)
    
    def set_date(self, date):
        f = '[shared] time.Time.set_date'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.tstamp = time.mktime(datetime.datetime.strptime(date, self.pattern).timetuple())
        except Exception as e:
            self.fail(f, e)
        self.set_instance()

    def get_year(self):
        f = '[shared] time.Time.get_year'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            return self.inst.strftime("%Y")
        except Exception as e:
            self.fail(f, e)
