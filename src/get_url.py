#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import ssl
import urllib.request

from skl_shared.localize import _
from skl_shared.message.controller import Message, rep
from skl_shared.time import Timer


class Get:
    
    def __init__(self, url, coding='UTF-8', Verbose=True, Verify=False
                ,timeout=6):
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
        f = '[SharedQt] get_url.Get.unverified'
        if self.Verify:
            return
        if not hasattr(ssl, '_create_unverified_context'):
            mes = _('Unable to use unverified certificates!')
            Message(f, mes).show_warning()
            return
        ssl._create_default_https_context = ssl._create_unverified_context
        
    def _get(self):
        ''' Changing UA allows us to avoid a bot protection
            ('Error 403: Forbidden').
        '''
        f = '[SharedQt] get_url.Get._get'
        try:
            req = urllib.request.Request(url = self.url, data = None
                                        ,headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'})
            self.html = urllib.request.urlopen(req, timeout=self.timeout).read()
            if self.Verbose:
                mes = _('[OK]: "{}"').format(self.url)
                Message(f, mes).show_info()
        # Too many possible exceptions
        except Exception as e:
            mes = _('[FAILED]: "{}". Details: {}').format(self.url, e)
            Message(f, mes).show_warning()
    
    def decode(self):
        ''' Set 'coding' to None to cancel decoding. This is useful if we are
            downloading a non-text content.
        '''
        f = '[SharedQt] get_url.Get.decode'
        if not self.coding:
            return self.html
        if not self.html:
            rep.empty(f)
            return
        try:
            self.html = self.html.decode(encoding=self.coding)
        except UnicodeDecodeError:
            self.html = str(self.html)
            mes = _('Unable to decode "{}"!').format(self.url)
            Message(f, mes).show_warning()
    
    def run(self):
        f = '[SharedQt] get_url.Get.run'
        if not self.url:
            rep.empty(f)
            return
        # Safely use URL as a string
        if not isinstance(self.url, str):
            mes = _('Wrong input data: {}!').format(self.url)
            Message(f, mes, True).show_warning()
            return
        if self.Verbose:
            timer = Timer(f)
            timer.start()
        self._get()
        self.decode()
        if self.Verbose:
            timer.end()
        return self.html
