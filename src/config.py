#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import copy
import json
import jsonschema

from skl_shared_qt.localize import _
import skl_shared_qt.shared as sh


''' We need to load the default config anyway since the local config can be
    outdated and may not comprise new keys. We cannot just check the local
    config against the default schema since the latter checks the presence of
    default keys and the program will force default configuration each time
    new keys are added to the default config instead of just updating the local
    config. Checking the presence of default keys is also necessary since we
    will have to try-except all config values otherwise.
'''


class Json:
    
    def __init__(self, file, Silent=False):
        self.code = ''
        self.json = {}
        self.file = file
        self.Silent = Silent
        ''' Since absent config is allowed, this class fails only in case of
            JSON exceptions. Schema is allowed to fail since local config can
            be outdated.
        '''
        self.Success = True
    
    def validate(self, schema):
        f = '[SharedQt] config.Json.validate'
        if not self.json or not schema:
            sh.com.rep_empty(f)
            return
        # Setting empty schema passes validation
        try:
            jsonschema.validate(self.json, schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            mes = _('Configuration file "{}" is invalid!\n\nDetails:\n{}')
            mes = mes.format(self.file, e)
            sh.objs.get_mes(f, mes, self.Silent).show_error()
    
    def load(self):
        f = '[SharedQt] config.Json.load'
        if not self.file:
            sh.com.rep_empty(f)
            return
        if not os.path.exists(self.file):
            sh.com.rep_lazy(f)
            return
        ''' Show the full path in case of not finding the file to make
            debugging easier.
        '''
        self.file = sh.Path(self.file).get_absolute()
        code = sh.ReadTextFile(self.file).get()
        if not code:
            sh.com.rep_out(f)
            return
        try:
            self.json = json.loads(code)
        except Exception as e:
            self.Success = False
            sh.com.rep_third_party(f, e)
            return
        return True
    
    def dump(self):
        f = '[SharedQt] config.Json.dump'
        if not self.json:
            sh.com.rep_empty(f)
            return
        try:
            return json.dumps(self.json, ensure_ascii=False, indent=4)
        except Exception as e:
            sh.com.rep_third_party(f, e)
    
    def save(self, obj):
        f = '[SharedQt] config.Json.save'
        self.json = obj
        code = self.dump()
        if not code:
            sh.com.rep_empty(f)
            return
        return sh.WriteTextFile(self.file, True).write(code)



class Schema:
    
    def __init__(self, file):
        self.Success = True
        self.file = file
        self.iconfig = Json(self.file)
    
    def get(self):
        f = '[SharedQt] config.Schema.get'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        return self.iconfig.json
    
    def dump(self):
        f = '[SharedQt] config.Schema.dump'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        code = self.iconfig.dump()
        if not code:
            sh.com.rep_empty(f)
            return ''
        return code
    
    def load(self):
        f = '[SharedQt] config.Schema.load'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        self.Success = self.iconfig.load()
    
    def run(self):
        self.load()



class Default:
    
    def __init__(self, file, schema):
        self.Success = True
        self.file = file
        self.iconfig = Json(self.file)
        self.schema = schema
    
    def get(self):
        f = '[SharedQt] config.Default.get'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        return self.iconfig.json
    
    def dump(self):
        f = '[SharedQt] config.Default.dump'
        if not self.Success:
            sh.com.cancel(f)
            return ''
        code = self.iconfig.dump()
        if not code:
            sh.com.rep_empty(f)
            return ''
        return code
    
    def load(self):
        f = '[SharedQt] config.Default.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.Success = self.iconfig.load()
    
    def get_version(self):
        f = '[SharedQt] config.Default.get_version'
        if not self.Success:
            sh.com.cancel(f)
            return 0
        try:
            return self.iconfig.json['config']['min_version']
        except KeyError:
            self.Success = False
            return 0
    
    def validate(self):
        f = '[SharedQt] config.Default.validate'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.Success = self.iconfig.validate(self.schema)
    
    def run(self):
        self.load()
        self.validate()
        self.get_version()



class Local:
    
    def __init__(self, file, min_version):
        self.Success = True
        self.file = file
        self.iconfig = Json(self.file)
        self.min_version = min_version
    
    def get(self):
        f = '[SharedQt] config.Local.get'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        return self.iconfig.json
    
    def dump(self):
        f = '[SharedQt] config.Local.dump'
        if not self.Success:
            sh.com.cancel(f)
            return '{}'
        code = self.iconfig.dump()
        if not code:
            sh.com.rep_empty(f)
            return '{}'
        return code
    
    def load(self):
        f = '[SharedQt] config.Local.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.iconfig.load()
        # Absent file is allowed, but not JSON exceptions
        self.Success = self.iconfig.Success
    
    def get_version(self):
        try:
            return self.iconfig.json['config']['min_version']
        except KeyError:
            self.Success = False
            return 0
    
    def check_version(self):
        f = '[SharedQt] config.Local.check_version'
        if not self.Success:
            sh.com.cancel(f)
            return
        ''' We need to check the existence and validity of the config version
            key. This can also be done by duplicating a schema for the local
            config without checking key existence (but will require more effort
            in maintaining schemas).
        '''
        if not 'config' in self.iconfig.json:
            self.Success = False
            mes = _('Configuration file "{}" does not have key "{}"!')
            mes = mes.format(self.iconfig.file, 'config')
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        if not isinstance(self.iconfig.json['config'], dict):
            self.Success = False
            mes = _('Configuration file "{}": key "{}" has a wrong type!')
            mes = mes.format(self.iconfig.file)
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        if not 'min_version' in self.iconfig.json['config']:
            self.Success = False
            mes = _('Configuration file "{}" does not have key "{}"!')
            mes = mes.format(self.iconfig.file, "['config']['min_version']")
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        if not isinstance(self.iconfig.json['config']['min_version'], int):
            self.Success = False
            mes = _('Configuration file "{}": key "{}" has a wrong type!')
            mes = mes.format(self.iconfig.file, "['config']['min_version']")
            sh.objs.get_mes(f, mes, True).show_warning()
            return
        if self.iconfig.json['config']['min_version'] != self.min_version:
            self.Success = False
            mes = _('Wrong version {}, expected {}!')
            mes = mes.format (self.iconfig.json['config']['min_version']
                             ,self.min_version
                             )
            sh.objs.get_mes(f, mes, True).show_warning()
    
    def save(self, obj):
        # Should run even if Success == False
        return self.iconfig.save(obj)
    
    def run(self):
        self.load()
        self.check_version()



class Config:
    
    def __init__(self, default, schema, local):
        self.set_values()
        self.default = default
        self.schema = schema
        self.local = local
    
    def set_values(self):
        self.Success = True
        self.schema = ''
        self.default = ''
        self.local = ''
        self.new = {}
        self.local_dump = ''
    
    def set_local_dump(self):
        f = '[SharedQt] config.Config.set_local_dump'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.local_dump = copy.deepcopy(self.ilocal.dump())
    
    def _copy(self):
        self.new = copy.deepcopy(self.idefault.get())
    
    def update(self):
        f = '[SharedQt] config.Config.update'
        if not self.Success:
            sh.com.cancel(f)
            return
        if self.ilocal.Success:
            mes = _('Update default configuration')
            self.new = Update(self.idefault.get(), self.ilocal.get()).run()
        else:
            mes = _('Use default configuration')
            self._copy()
        sh.objs.get_mes(f, mes, True).show_info()
    
    def load(self):
        f = '[SharedQt] config.Config.load'
        if not self.Success:
            sh.com.cancel(f)
            return
        self.ischema = Schema(self.schema)
        self.ischema.run()
        self.idefault = Default(self.default, self.ischema.get())
        self.idefault.run()
        self.ilocal = Local(self.local, self.idefault.get_version())
        self.ilocal.run()
        self.Success = self.ischema.Success and self.idefault.Success
    
    def get(self):
        f = '[SharedQt] config.Config.get'
        if not self.Success:
            sh.com.cancel(f)
            return {}
        return self.new
    
    def dump(self):
        f = '[SharedQt] config.Config.dump'
        if not self.Success:
            sh.com.cancel(f)
            return '{}'
        try:
            return json.dumps(self.new, ensure_ascii=False, indent=4)
        except Exception as e:
            sh.com.rep_third_party(f, e)
        return '{}'
    
    def quit(self):
        self.revert_types()
        self.save()
    
    def save(self):
        f = '[SharedQt] config.Config.save'
        if not self.Success:
            sh.com.cancel(f)
            return
        # Do not forget to revert unsupported types back to strings first
        if self.local_dump == self.dump():
            sh.com.rep_lazy(f)
            return
        self.Success = self.ilocal.save(self.new)
    
    def run(self):
        self.load()
        self.update()



class Update:
    
    def __init__(self, d1, d2):
        ''' Merge two dictionaries such that all existing keys are kept
            (including those of embedded dictionaries ('branches')), empty
            branches and diverting non-dictionary items are overwritten.
            'd1 | d2' is not enough since that will delete sections not present
            in d2.
        '''
        self.new_keys = 0
        self.mod_keys = 0
        self.d1 = d1
        self.d2 = d2
        ''' Global dictionaries modified inside this class will inherit
            changes, so we need to create a clone.
        '''
        self.new = copy.deepcopy(self.d1)

    def report(self):
        f = '[SharedQt] config.Update.report'
        mes = _('Modified keys: {}').format(self.mod_keys)
        sh.objs.get_mes(f, mes, True).show_info()
        mes = _('New keys: {}').format(self.new_keys)
        sh.objs.get_mes(f, mes, True).show_info()
    
    def debug(self):
        f = '[SharedQt] config.Update.debug'
        try:
            return json.dumps(self.new, ensure_ascii=False, indent=4)
        except Exception as e:
            sh.com.rep_third_party(f, e)
        return self.new
    
    def iterate(self, section1, section2):
        f = '[SharedQt] config.Update.iterate'
        for key2 in section2:
            if not key2 in section1:
                if isinstance(section2[key2], dict):
                    mes = _('New branch: "{}"').format(key2)
                else:
                    mes = _('New value: "{}"').format(key2)
                self.new_keys += 1
                sh.objs.get_mes(f, mes, True).show_debug()
                section1[key2] = section2[key2]
        for key1 in section1:
            if not key1 in section2:
                continue
            if section1[key1] == section2[key1]:
                continue
            if isinstance(section1[key1], dict) and isinstance(section2[key1], dict):
                if not section1[key1]:
                    self.mod_keys += 1
                    mes = _('Overwrite empty "{}" branch with "{}"')
                    mes = mes.format(key1, section2[key1])
                    sh.objs.get_mes(f, mes, True).show_debug()
                    section1[key1] = section2[key1]
                    continue
                self.iterate(section1[key1], section2[key1])
            elif section1[key1] != section2[key1]:
                self.mod_keys += 1
                mes = _('Update "{}" branch value: {} -> {}')
                mes = mes.format(key1, section1[key1], section2[key1])
                sh.objs.get_mes(f, mes, True).show_debug()
                section1[key1] = section2[key1]
    
    def run(self):
        self.iterate(self.new, self.d2)
        self.report()
        return self.new
