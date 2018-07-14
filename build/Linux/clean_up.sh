#!/bin/sh

# Do not use "verbose" in order to spot errors easily

# Remove shared resources
rm ./resources/{error,info,question,warning}.gif

# Remove other shared resources
rm ./resources/locale/ru/LC_MESSAGES/shared.mo

# Remove shared Python files
rm ./{gettext_windows,regexp,shared,sharedGUI}.py

# (Linux-only) Remove build scripts
rm ./{build.sh,clean_up.sh,setup.py,update_here.sh}

rmdir -p resources/locale/ru/LC_MESSAGES

ls .
