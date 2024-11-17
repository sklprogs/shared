#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import subprocess
import urllib.parse
import webbrowser

from skl_shared_qt.localize import _
import skl_shared_qt.message.controller as ms
import skl_shared_qt.logic as lg


class Online:
    ''' If you get 'TypeError("quote_from_bytes() expected bytes")', then you
        probably forgot to call 'self.reset' here or in children classes.
    '''
    def __init__(self, base='%s', pattern='', coding='UTF-8'):
        if pattern:
            self.reset (base = base
                       ,pattern = pattern
                       ,coding = coding
                       )

    def get_bytes(self):
        if not self.bytes:
            self.bytes = bytes(self.pattern, encoding=self.coding)
        return self.bytes

    def browse(self):
        # Open a URL in a default browser
        f = '[SharedQt] browser.Online.browse'
        try:
            webbrowser.open (url = self.get_url()
                            ,new = 2
                            ,autoraise = True
                            )
        except Exception as e:
            mes = _('Failed to open URL "{}" in a default browser!\n\nDetails: {}')
            mes = mes.format(self.url, e)
            ms.Message(f, mes, True).show_error()

    def get_url(self):
        # Create a correct online link (URI => URL)
        f = '[SharedQt] browser.Online.get_url'
        if not self.url:
            self.url = self.base % urllib.parse.quote(self.get_bytes())
            mes = str(self.url)
            ms.Message(f, mes).show_debug()
        return self.url

    def reset(self, base='%s', pattern='', coding='UTF-8'):
        self.bytes = None
        self.url = None
        self.base = base
        self.pattern = pattern
        self.coding = coding



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
        f = '[SharedQt] browser.Email.reset'
        self.Success = True
        ''' A single address or multiple comma-separated addresses (not all
            mail agents support ';'). #NOTE that, however, Outlook supports
            ONLY ';' and Evolution - only ','!
        '''
        self.email = email
        self.subject = lg.Input(f, subject).get_not_none()
        self.message = lg.Input(f, message).get_not_none()
        self.attach = attach
        if not self.email:
            self.Success = False
            ms.rep.empty(f)
        if self.attach:
            self.Success = lg.File(self.attach).Success
            if not self.Success:
                ms.rep.cancel(f)

    def sanitize(self, value):
        # Escape symbols that may cause issues when composing 'mailto'
        f = '[SharedQt] browser.Email.sanitize'
        if not self.Success:
            ms.rep.cancel(f)
            return
        if not value:
            return ''
        return str(Online(pattern=value).get_url())
    
    def call_browser(self):
        f = '[SharedQt] browser.Email.call_browser'
        if not self.Success:
            ms.rep.cancel(f)
            return
        ''' - This is the last resort. Attaching a file worked for me only with
              CentOS6 + Palemoon + Thunderbird. Using another OS/browser/email
              client will probably call a default email client without the
              attachment.
            - Quotes are necessary for attachments only, they will stay visible
              otherwise.
        '''
        mailto = f'mailto:{self.email}?subject={self.subject}&body={self.message}'
        if self.attach:
            mailto += f'&attach="{self.attach}"'
        ms.Message(f, f'"{mailto}"').show_debug()
        try:
            webbrowser.open(mailto)
        except:
            mes = _('Failed to load an e-mail client.')
            ms.Message(f, mes, True).show_error()
    
    def create(self):
        f = '[SharedQt] browser.Email.create'
        if not self.Success:
            ms.rep.cancel(f)
            return
        if not self.run_evolution() and not self.run_thunderbird() \
        and not self.run_outlook():
            self.subject = self.sanitize(self.subject)
            self.message = self.sanitize(self.message)
            self.attach = self.sanitize(self.attach)
            self.call_browser()
                       
    def run_outlook(self):
        #NOTE: this does not work in wine!
        f = '[SharedQt] logic.Email.run_outlook'
        if not lg.objs.get_os().is_win():
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
            ms.rep.cancel(f)
            return
        app = '/usr/bin/thunderbird'
        if not os.path.isfile(app):
            return
        # Thunderbird requires single quotes and ignores body for some reason
        args = f"to='{self.email}',subject='{self.subject}',body='{self.message}'"
        if self.attach:
            args += f",attachment='{self.attach}'"
        self.custom_args = [app, '-compose', args]
        try:
            subprocess.Popen(self.custom_args)
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            ms.Message(f, mes, True).show_error()
    
    def run_evolution(self):
        f = '[SharedQt] browser.Email.run_evolution'
        if not self.Success:
            ms.rep.cancel(f)
            return
        app = '/usr/bin/evolution'
        if not os.path.isfile(app):
            return
        email = self.email.replace(';', ',')
        mailto = f'mailto:{email}?subject={self.subject}&body={self.message}'
        if self.attach:
            mailto += f'&attach={self.attach}'
        self.custom_args = [app, mailto]
        try:
            subprocess.Popen(self.custom_args)
            return True
        except:
            mes = _('Failed to run "{}"!').format(self.custom_args)
            ms.Message(f, mes, True).show_error()


ONLINE = Online()
EMAIL = Email()
