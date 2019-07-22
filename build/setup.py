#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from setuptools import setup, find_packages

setup (name         = 'skl_shared'
      ,packages     = find_packages()
      ,version      = '1.0'
      ,description  = 'These are shared files for all my Python projects'
      ,url          = 'https://github.com/sklprogs/shared'
      ,author       = 'Peter Sklyar'
      ,author_email = 'skl.progs@gmail.com'
      ,package_data = {'skl_shared': ['resources']
                      }
      ,classifiers  = ['Programming Language :: Python :: 3'
                      ,'License :: OSI Approved :: GPLv3+'
                      ,'Operating System :: OS Independent'
                      ]
      )
