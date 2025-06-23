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
            return
        try:
            return self.inst.strftime(self.pattern)
        except Exception as e:
            self.fail(f, e)

    def set_instance(self):
        f = '[shared] time.Time.set_instance'
        if self.tstamp is None:
            self.set_todays_date()
        if not self.Success:
            rep.cancel(f)
            return
        if self.inst is not None:
            return
        try:
            self.inst = datetime.datetime.fromtimestamp(self.tstamp)
        except Exception as e:
            self.fail(f, e)

    def get_month_name(self):
        # Month name in English
        f = '[shared] time.Time.get_month_name'
        if not self.Success:
            rep.cancel(f)
            return
        month_int = Text(self.inst.strftime("%m")).str2int()
        return calendar.month_name[month_int]
    
    def get_month_abbr(self):
        f = '[shared] time.Time.get_month_abbr'
        if not self.Success:
            rep.cancel(f)
            return
        month_int = Text(self.inst.strftime("%m")).str2int()
        return calendar.month_abbr[month_int]

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

    def get_year(self):
        f = '[shared] time.Time.get_year'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            return self.inst.strftime("%Y")
        except Exception as e:
            self.fail(f, e)
