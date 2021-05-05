#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from skl_shared.localize import _
import skl_shared.shared as sh
# Load PIL only after loading tkinter
from PIL import Image as pilimage
from PIL import ImageTk as piltk


class Image:
    ''' Load an image from a file, convert this image to bytes and
        convert bytes back to the image.
    '''
    # Accepts both path and 'io.BytesIO(image_bytes)'
    def get_loader(self,path):
        return pilimage.open(path)
    
    def get_image(self,loader):
        return piltk.PhotoImage(loader)
