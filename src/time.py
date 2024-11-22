#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import time
import calendar
import datetime

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.logic import Text


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
    # We constantly recalculate each value because they depend on each other
    def __init__(self, tstamp=None, pattern='%Y-%m-%d'):
        self.reset(tstamp, pattern)
    
    def fail(self, f, e):
        self.Success = False
        mes = _('Set time parameters are incorrect or not supported.\n\nDetails: {}')
        mes = mes.format(e)
        Message(f, mes, True).show_error()

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
        f = '[SharedQt] time.Time.add_days'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.inst = self.get_instance() \
                      + datetime.timedelta(days=days_delta)
        except Exception as e:
            self.fail(f, e)

    def get_date(self):
        f = '[SharedQt] time.Time.get_date'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.date = self.get_instance().strftime(self.pattern)
        except Exception as e:
            self.fail(f, e)
        return self.date

    def get_instance(self):
        f = '[SharedQt] time.Time.get_instance'
        if not self.Success:
            rep.cancel(f)
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
        f = '[SharedQt] time.Time.get_timestamp'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.date:
            self.get_date()
        try:
            self.tstamp = time.mktime(datetime.datetime.strptime(self.date, self.pattern).timetuple())
        except Exception as e:
            self.fail(f, e)
        return self.tstamp

    def is_monday(self):
        f = '[SharedQt] time.Time.is_monday'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        if datetime.datetime.weekday(self.inst) == 0:
            return True

    def get_month_name(self):
        # Month name in English
        f = '[SharedQt] time.Time.get_month_name'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        month_int = Text(self.inst.strftime("%m")).str2int()
        self.month_name = calendar.month_name[month_int]
        return self.month_name
    
    def get_month_abbr(self):
        f = '[SharedQt] time.Time.get_month_abbr'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        month_int = Text(self.inst.strftime("%m")).str2int()
        self.month_abbr = calendar.month_abbr[month_int]
        return self.month_abbr

    def get_todays_date(self):
        self.inst = datetime.datetime.today()

    def get_year(self):
        f = '[SharedQt] time.Time.get_year'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.inst:
            self.get_instance()
        try:
            self.year = self.inst.strftime("%Y")
        except Exception as e:
            self.fail(f, e)
        return self.year


TIME = Time()
