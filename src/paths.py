#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import os
import sys
import shlex
import shutil

from skl_shared_qt.localize import _
from skl_shared_qt.message.controller import Message, rep
from skl_shared_qt.logic import OS


class Path:

    def __init__(self, path):
        self.reset(path)

    def get_free_space(self):
        f = '[SharedQt] paths.Path.get_free_space'
        result = 0
        if not self.path:
            rep.empty(f)
            return result
        if not os.path.exists(self.path):
            mes = _('Wrong input data: "{}"!').format(self.path)
            Message(f, mes, True).show_warning()
            return result
        try:
            istat = os.statvfs(self.path)
            result = istat.f_bavail * istat.f_bsize
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_error()
        return result
    
    def _split_path(self):
        if not self.split:
            self.split = os.path.splitext(self.get_basename())
        return self.split

    def get_basename(self):
        if not self.basename:
            self.basename = os.path.basename(self.path)
        return self.basename
    
    def get_basename_low(self):
        return self.get_basename().lower()

    def create(self):
        # This will recursively (by design) create self.path
        # We actually don't need to fail the class globally
        f = '[SharedQt] paths.Path.create'
        Success = True
        if not self.path:
            Success = False
            rep.empty(f)
            return Success
        if os.path.exists(self.path):
            if os.path.isdir(self.path):
                mes = _('Directory "{}" already exists.').format(self.path)
                Message(f, mes).show_info()
            else:
                Success = False
                mes = _('The path "{}" is invalid!').format(self.path)
                Message(f, mes, True).show_warning()
        else:
            mes = _('Create directory "{}"').format(self.path)
            Message(f, mes).show_info()
            try:
                #TODO: consider os.mkdir
                os.makedirs(self.path)
            except:
                Success = False
                mes = _('Failed to create directory "{}"!').format(self.path)
                Message(f, mes, True).show_error()
        return Success

    def delete_inappropriate_symbols(self):
        ''' These symbols may pose a problem while opening files
            #TODO: check whether this is really necessary
        '''
        return self.get_filename().replace("'", '').replace("&", '')

    def get_dirname(self):
        if not self.dirname:
            self.dirname = os.path.dirname(self.path)
        return self.dirname

    def escape(self):
        # In order to use xdg-open, we need to escape some characters first
        self.path = shlex.quote(self.path)
        return self.path

    def get_ext(self):
        # An extension with a dot
        if not self.extension:
            if len(self._split_path()) > 1:
                self.extension = self._split_path()[1]
        return self.extension
    
    def get_ext_low(self):
        return self.get_ext().lower()

    def get_filename(self):
        if not self.filename:
            if len(self._split_path()) >= 1:
                self.filename = self._split_path()[0]
        return self.filename

    def reset(self, path):
        # Prevent 'NoneType'
        if path:
            self.path = path
        else:
            self.path = ''
        ''' Building paths in Windows:
            - Use raw strings (e.g., set path as r'C:\1.txt')
            - Use os.path.join(mydir, myfile) or os.path.normpath(path)
              instead of os.path.sep
            - As an alternative, import ntpath, posixpath
        '''
        ''' We remove a separator from the end, because basename and dirname
            work differently in this case ('' and the last directory,
            correspondingly).
        '''
        if self.path != '/':
            self.path = self.path.rstrip('//')
        self.basename = self.dirname = self.extension = self.filename \
                      = self.split = self.date = ''
        self.parts = []

    def split(self):
        if self.parts:
            return self.parts
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
    
    def get_absolute(self):
        return os.path.abspath(self.path)



class ProgramDir:

    def __init__(self):
        self.dir = sys.path[0]
        # We run app, not interpreter
        if os.path.isfile(self.dir):
            self.dir = Path(self.dir).get_dirname()

    def add(self, *args):
        return os.path.join(self.dir, *args)



class Home:

    def __init__(self, app_name='myapp'):
        self.appname = app_name
        self.confdir = self.sharedir = ''
        
    def add_share(self, *args):
        return os.path.join(self.get_share_dir(), *args)
    
    def create_share(self):
        return Path(self.get_share_dir()).create()
    
    def get_share_dir(self):
        if not self.sharedir:
            if OS.is_win():
                os_folder = 'Application Data'
            else:
                os_folder = os.path.join('.local', 'share')
            self.sharedir = os.path.join(self.get_home(), os_folder
                                        ,self.appname)
        return self.sharedir
    
    def create_conf(self):
        return Path(self.get_conf_dir()).create()
    
    def get_home(self):
        return os.path.expanduser('~')
        
    def get_conf_dir(self):
        if not self.confdir:
            if OS.is_win():
                os_folder = 'Application Data'
            else:
                os_folder = '.config'
            self.confdir = os.path.join(self.get_home(), os_folder
                                       ,self.appname)
        return self.confdir
    
    def add(self, *args):
        return os.path.join(self.get_home(), *args)
    
    def add_config(self, *args):
        return os.path.join(self.get_conf_dir(), *args)



class File:

    def __init__(self, file, dest=None, Rewrite=False):
        f = '[SharedQt] paths.File.__init__'
        self.Success = True
        self.Rewrite = Rewrite
        self.file = file
        self.dest = dest
        # This will allow to skip some checks for destination
        if not self.dest:
            self.dest = self.file
        self.atime = ''
        self.mtime = ''
        # This already checks existence
        if self.file and os.path.isfile(self.file):
            ''' If the destination directory does not exist, this will be
                caught in try-except while copying/moving.
            '''
            if os.path.isdir(self.dest):
                self.dest = os.path.join (self.dest
                                         ,Path(self.file).basename()
                                         )
        elif not self.file:
            self.Success = False
            mes = _('Empty input is not allowed!')
            Message(f, mes, True).show_warning()
        elif not os.path.exists(self.file):
            self.Success = False
            mes = _('File "{}" has not been found!').format(self.file)
            Message(f, mes, True).show_warning()
        else:
            self.Success = False
            mes = _('The object "{}" is not a file!').format(self.file)
            Message(f, mes, True).show_warning()

    def get_size(self, Follow=True):
        f = '[SharedQt] paths.File.get_size'
        result = 0
        if not self.Success:
            rep.cancel(f)
            return
        try:
            if Follow:
                cond = not os.path.islink(self.file)
            else:
                cond = True
            if cond:
                result = os.path.getsize(self.file)
        except Exception as e:
            ''' Along with other errors, 'No such file or directory' error will
                be raised if Follow=False and this is a broken symbolic link.
            '''
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_warning()
        return result
    
    def _copy(self):
        f = '[SharedQt] paths.File._copy'
        Success = True
        mes = _('Copy "{}" to "{}"').format(self.file, self.dest)
        Message(f, mes).show_info()
        try:
            shutil.copyfile(self.file, self.dest)
        except:
            Success = False
            mes = _('Failed to copy file "{}" to "{}"!')
            mes = mes.format(self.file, self.dest)
            Message(f, mes, True).show_error()
        return Success

    def _move(self):
        f = '[SharedQt] paths.File._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.file, self.dest)
        Message(f, mes).show_info()
        try:
            shutil.move(self.file, self.dest)
        except Exception as e:
            Success = False
            mes = _('Failed to move "{}" to "{}"!\n\nDetails: {}')
            mes = mes.format(self.file, self.dest, e)
            Message(f, mes, True).show_error()
        return Success

    def get_access_time(self):
        f = '[SharedQt] paths.File.get_access_time'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.atime = os.path.getatime(self.file)
            # Further steps: datetime.date.fromtimestamp(self.atime).strftime(self.pattern)
            return self.atime
        except:
            mes = _('Failed to get the date of the file "{}"!')
            mes = mes.format(self.file)
            Message(f, mes, True).show_error()

    def copy(self):
        f = '[SharedQt] paths.File.copy'
        Success = True
        if not self.Success:
            rep.cancel(f)
            return
        if self.file.lower() == self.dest.lower():
            mes = _('Unable to copy the file "{}" to iself!').format(self.file)
            Message(f, mes, True).show_error()
        elif com.rewrite (file = self.dest
                         ,Rewrite = self.Rewrite
                         ):
            Success = self._copy()
        else:
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
        return Success

    def delete(self):
        f = '[SharedQt] paths.File.delete'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Delete "{}"').format(self.file)
        Message(f, mes).show_info()
        try:
            os.remove(self.file)
            return True
        except:
            mes = _('Failed to delete file "{}"!').format(self.file)
            Message(f, mes, True).show_error()

    def get_modification_time(self):
        f = '[SharedQt] paths.File.get_modification_time'
        if not self.Success:
            rep.cancel(f)
            return
        try:
            self.mtime = os.path.getmtime(self.file)
            # Further steps: datetime.date.fromtimestamp(self.mtime).strftime(self.pattern)
            return self.mtime
        except:
            mes = _('Failed to get the date of the file "{}"!')
            mes = mes.format(self.file)
            Message(f, mes, True).show_error()

    def move(self):
        f = '[SharedQt] paths.File.move'
        Success = True
        if not self.Success:
            rep.cancel(f)
            return
        if self.file.lower() == self.dest.lower():
            mes = _('Moving is not necessary, because the source and destination are identical ({}).')
            mes = mes.format(self.file)
            Message(f, mes, True).show_warning()
        elif com.rewrite (file = self.dest
                         ,Rewrite = self.Rewrite
                         ):
            Success = self._move()
        else:
            mes = _('Operation has been canceled by the user.')
            Message(f, mes).show_info()
        return self.Success and Success

    def set_time(self):
        f = '[SharedQt] paths.File.set_time'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.atime or not self.mtime:
            return
        mes = _('Change the time of the file "{}" to {}')
        mes = mes.format(self.file, (self.atime, self.mtime))
        Message(f, mes).show_info()
        try:
            os.utime(self.file, (self.atime, self.mtime))
        except:
            mes = _('Failed to change the time of the file "{}" to "{}"!')
            mes = mes.format(self.file, (self.atime, self.mtime))
            Message(f, mes, True).show_error()



class Directory:
    #TODO: fix: does not work with a root dir ('/')
    def __init__(self, path, dest=''):
        f = '[SharedQt] paths.Directory.__init__'
        self.set_values()
        if path:
            ''' Remove trailing slashes and follow symlinks. No error is thrown
                for broken symlinks, but further checks will fail for them.
                Failing a real path (e.g., pointing to the volume that is not
                mounted yet) is more apprehensible than failing a symlink.
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
            Message(f, mes, True).show_warning()
    
    def _move(self):
        f = '[SharedQt] paths.Directory._move'
        Success = True
        mes = _('Move "{}" to "{}"').format(self.dir, self.dest)
        Message(f, mes).show_info()
        try:
            shutil.move(self.dir, self.dest)
        except Exception as e:
            Success = False
            mes = _('Failed to move "{}" to "{}"!\n\nDetails: {}')
            mes = mes.format(self.dir, self.dest, e)
            Message(f, mes, True).show_error()
        return Success

    def move(self):
        f = '[SharedQt] paths.Directory.move'
        Success = True
        if not self.Success:
            rep.cancel(f)
            return
        if os.path.exists(self.dest):
            mes = _('Path "{}" already exists!').format(self.dest)
            Message(f, mes).show_warning()
            Success = False
        elif self.dir.lower() == self.dest.lower():
            mes = _('Moving is not necessary, because the source and destination are identical ({}).')
            mes = mes.format(self.dir)
            Message(f, mes, True).show_warning()
        else:
            Success = self._move()
        return self.Success and Success
    
    def get_subfiles(self, Follow=True):
        # Include files in subfolders
        f = '[SharedQt] paths.Directory.get_subfiles'
        if not self.Success:
            rep.cancel(f)
            return []
        if self.subfiles:
            return self.subfiles
        try:
            for dirpath, dirnames, fnames \
            in os.walk(self.dir, followlinks=Follow):
                for name in fnames:
                    obj = os.path.join(dirpath, name)
                    if os.path.isfile(obj):
                        self.subfiles.append(obj)
            self.subfiles.sort(key=lambda x: x.lower())
        except Exception as e:
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_error()
        return self.subfiles
    
    def get_size(self, Follow=True):
        f = '[SharedQt] paths.Directory.get_size'
        result = 0
        if not self.Success:
            return result
        try:
            for dirpath, dirnames, filenames in os.walk(self.dir):
                for name in filenames:
                    obj = os.path.join(dirpath, name)
                    if Follow:
                        cond = not os.path.islink(obj)
                    else:
                        cond = True
                    if cond:
                        result += os.path.getsize(obj)
        except Exception as e:
            ''' Along with other errors, 'No such file or directory' error will
                be raised if Follow=False and there are broken symbolic links.
            '''
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_error()
        return result
    
    def set_values(self):
        self.Success = True
        # Assigning lists must be one per line
        self.lst = []
        self.rellist = []
        self.files = []
        self.relfiles = []
        self.dirs = []
        self.reldirs = []
        self.exts = []
        self.extslow = []
        self.subfiles = []
    
    def get_ext(self): # with a dot
        f = '[SharedQt] paths.Directory.get_ext'
        if not self.Success:
            rep.cancel(f)
            return self.exts
        if not self.exts:
            for file in self.get_rel_files():
                ext = Path(file).get_ext()
                self.exts.append(ext)
                self.extslow.append(ext.lower())
        return self.exts

    def get_ext_low(self): # with a dot
        f = '[SharedQt] paths.Directory.get_ext_low'
        if not self.Success:
            rep.cancel(f)
            return self.extslow
        if not self.extslow:
            self.get_ext()
        return self.extslow

    def delete_empty(self):
        f = '[SharedQt] paths.Directory.delete_empty'
        if not self.Success:
            rep.cancel(f)
            return
        # Do not delete nested folders
        if os.listdir(self.dir):
            mes = _('Unable to delete {}, because it has nested objects!')
            mes = mes.format(self.dir)
            Message(f, mes, True).show_warning()
            return
        self.delete()
    
    def delete(self):
        f = '[SharedQt] paths.Directory.delete'
        if not self.Success:
            rep.cancel(f)
            return
        mes = _('Delete "{}"').format(self.dir)
        Message(f, mes).show_info()
        try:
            shutil.rmtree(self.dir)
            return True
        except:
            mes = _('Failed to delete directory "{}"! Delete it manually.')
            mes = mes.format(self.dir)
            Message(f, mes, True).show_error()

    def get_rel_list(self):
        # Create a list of objects with a relative path
        f = '[SharedQt] paths.Directory.get_rel_list'
        if not self.Success:
            rep.cancel(f)
            return
        if not self.rellist:
            self.get_list()
        return self.rellist

    def get_list(self):
        # Create a list of objects with an absolute path
        f = '[SharedQt] paths.Directory.get_list'
        if not self.Success:
            rep.cancel(f)
            return self.lst
        if self.lst:
            return self.lst
        try:
            self.lst = os.listdir(self.dir)
        except Exception as e:
            # We can encounter, e.g., PermissionError here
            self.Success = False
            mes = _('Operation has failed!\nDetails: {}').format(e)
            Message(f, mes, True).show_error()
        self.lst.sort(key=lambda x: x.lower())
        self.rellist = list(self.lst)
        for i in range(len(self.lst)):
            self.lst[i] = os.path.join(self.dir, self.lst[i])
        return self.lst

    def get_rel_dirs(self):
        f = '[SharedQt] paths.Directory.get_rel_dirs'
        if not self.Success:
            rep.cancel(f)
            return self.reldirs
        if not self.reldirs:
            self.dirs()
        return self.reldirs

    def get_rel_files(self):
        f = '[SharedQt] paths.Directory.get_rel_files'
        if not self.Success:
            rep.cancel(f)
            return self.relfiles
        if not self.relfiles:
            self.get_files()
        return self.relfiles

    def get_dirs(self):
        # Needs absolute path
        f = '[SharedQt] paths.Directory.get_dirs'
        if not self.Success:
            rep.cancel(f)
            return self.dirs
        if self.dirs:
            return self.dirs
        for i in range(len(self.get_list())):
            if os.path.isdir(self.lst[i]):
                self.dirs.append(self.lst[i])
                self.reldirs.append(self.rellist[i])
        return self.dirs

    def get_files(self):
        # Needs absolute path
        f = '[SharedQt] paths.Directory.get_files'
        if not self.Success:
            rep.cancel(f)
            return self.files
        if self.files:
            return self.files
        for i in range(len(self.get_list())):
            if os.path.isfile(self.lst[i]):
                self.files.append(self.lst[i])
                self.relfiles.append(self.rellist[i])
        return self.files

    def copy(self):
        f = '[SharedQt] paths.Directory.copy'
        if not self.Success:
            rep.cancel(f)
            return
        if self.dir.lower() == self.dest.lower():
            mes = _('Unable to copy "{}" to iself!').format(self.dir)
            Message(f, mes, True).show_error()
        elif os.path.isdir(self.dest):
            mes = _('Directory "{}" already exists.').format(self.dest)
            Message(f, mes, True).show_info()
        else:
            self._copy()

    def _copy(self):
        f = '[SharedQt] paths.Directory._copy'
        mes = _('Copy "{}" to "{}"').format(self.dir, self.dest)
        Message(f, mes).show_info()
        try:
            shutil.copytree(self.dir, self.dest)
        except:
            self.Success = False
            mes = _('Failed to copy "{}" to "{}"!').format(self.dir, self.dest)
            Message(f, mes, True).show_error()


PDIR = ProgramDir()
