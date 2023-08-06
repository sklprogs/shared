#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import jsonschema

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


class Json:
    
    def __init__(self, file, schema={}, invalid_mes=''):
        self.Success = True
        self.code = ''
        self.json = {}
        self.file = file
        self.schema = schema
        self.invalid_mes = invalid_mes
    
    def validate(self):
        f = '[SharedQt] config.Json.validate'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Setting empty schema passes validation
        try:
            jsonschema.validate(self.json, self.schema)
        except jsonschema.exceptions.ValidationError as e:
            self.Success = False
            if self.invalid_mes:
                mes = self.invalid_mes + '\n\n' + _('Details:\n{}').format(e)
            else:
                mes = _('Configuration file "{}" is invalid!\n\nDetails:\n{}')
                mes = mes.format(self.file, e)
            sh.objs.get_mes(f, mes).show_error()
    
    def load(self):
        f = '[SharedQt] config.Json.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        if not self.file:
            self.Success = False
            sh.com.rep_empty(f)
            return
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        self.file = sh.Path(self.file).get_absolute()
        self.code = sh.ReadTextFile(self.file).get()
        if not self.code:
            self.Success = False
            sh.com.rep_out(f)
            return
    
    def set(self):
        f = '[SharedQt] config.Json.set'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            self.json = json.loads(self.code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
    
    def save(self, body):
        f = '[SharedQt] config.Json.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        try:
            code = json.dumps(body, ensure_ascii=False, indent=4)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
            return
        self.Success = sh.WriteTextFile(self.file, True).write(code)
    
    def run(self):
        self.load()
        self.set()
        self.validate()
        return self.json



class Config:
    
    def __init__(self, file, pschema, invalid_mes=''):
        self.Success = True
        self.ischema = None
        self.iconfig = None
        self.file = file
        self.pschema = pschema
        self.invalid_mes = invalid_mes
    
    def load_schema(self):
        f = '[SharedQt] config.Config.load_schema'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.ischema = Json(self.pschema)
        # Empty schema is considered valid in 'Json', but not here
        if not self.ischema.run():
            self.Success = False
    
    def load_config(self):
        f = '[SharedQt] config.Config.load_config'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.iconfig = Json(self.file, self.ischema.schema, self.invalid_mes)
        return self.iconfig.run()
    
    def load(self):
        self.load_schema()
        return self.load_config()
    
    def save(self, body):
        f = '[SharedQt] config.Config.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' 'Config' is designed to be a higher level than 'Json', so we allow
            empty contents in 'Json' but not here.
        '''
        if not body:
            self.Success = False
            sh.com.rep_empty(f)
            return
        self.iconfig.save()
        self.Success = self.iconfig.Success
