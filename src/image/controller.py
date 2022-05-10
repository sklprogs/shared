#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import io
import skl_shared.shared as sh
from skl_shared.localize import _
from . import gui


class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
    '''
    def __init__(self):
        self.image = self.bytes_ = self.loader = None
        self.Success = True
        self.gui = gui.Image()
        
    def convert2rgb(self):
        # This is sometimes required in order to produce a JPEG file
        f = '[shared] image.controller.Image.convert2rgb'
        if self.Success:
            if self.loader:
                try:
                    self.loader = self.loader.convert('RGB')
                except Exception as e:
                    self.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def show_error(self,f,e):
        self.Success = False
        mes = _('Third-party module has failed!\n\nDetails: {}')
        mes = mes.format(e)
        sh.objs.get_mes(f,mes).show_error()
    
    def save(self,path,ext='PNG'):
        f = '[shared] image.controller.Image.save'
        if self.Success:
            if self.loader:
                if sh.com.rewrite(path):
                    try:
                        self.loader.save(path,ext)
                    except Exception as e:
                        self.show_error(f,e)
                else:
                    mes = _('Operation has been canceled by the user.')
                    sh.objs.get_mes(f,mes,True).show_info()
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def open(self,path):
        f = '[shared] image.controller.Image.open'
        if self.Success:
            if path:
                if sh.File(path).Success:
                    try:
                        self.loader = self.gui.get_loader(path)
                        self.image = self.gui.get_image(self.loader)
                        return self.image
                    except Exception as e:
                        self.show_error(f,e)
                else:
                    # No need to warn, the error is already GUI-based
                    self.Success = False
            else:
                self.Success = False
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
            
    def get_loader(self):
        f = '[shared] image.controller.Image.get_loader'
        if self.Success:
            if self.bytes_:
                try:
                    self.loader = self.gui.get_loader(io.BytesIO(self.bytes_))
                    return self.loader
                except Exception as e:
                    self.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        
    def get_thumbnail(self,x,y):
        ''' Resize an image to x,y limits. PIL will keep an original
            aspect ratio.
        '''
        f = '[shared] image.controller.Image.get_thumbnail'
        if self.Success:
            if self.loader:
                try:
                    self.loader.thumbnail([x,y])
                    return self.loader
                except Exception as e:
                    self.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
    
    def get_image(self):
        f = '[shared] image.controller.Image.get_image'
        if self.Success:
            if self.loader:
                try:
                    self.image = self.gui.get_image(self.loader)
                    return self.image
                except Exception as e:
                    self.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
        
    def get_bytes(self,ext='PNG'):
        f = '[shared] image.controller.Image.get_bytes'
        if self.Success:
            if self.loader:
                bytes_ = io.BytesIO()
                try:
                    self.loader.save(bytes_,format=ext)
                    self.bytes_ = bytes_.getvalue()
                    return self.bytes_
                except Exception as e:
                    self.show_error(f,e)
            else:
                sh.com.rep_empty(f)
        else:
            sh.com.cancel(f)
