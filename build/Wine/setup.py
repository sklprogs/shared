from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict (packages = []
                    ,includes = ["re"]
                    ,excludes = []
                    )

executables = [Executable ('shared.py'
                          ,base       = 'Win32GUI'
                          ,targetName = 'shared.exe'
                          )
              ]

setup (name        = 'shared'
      ,version     = '1'
      ,description = 'Shared files for all my Python projects'
      ,options     = dict(build_exe=buildOptions)
      ,executables = executables
      )
