#!/usr/bin/python3

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ["re"]
                    ,excludes = []
                    )

executables = [Executable ('shared.py'
                          ,base       = 'Console'
                          ,targetName = 'shared'
                          )
              ]

setup (name        = 'shared'
      ,version     = '1'
      ,description = 'Shared files for all my Python projects'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
