#!/bin/bash

# Do not use "verbose" in order to spot errors easily

mkdir -p ./{resources/locale/ru/LC_MESSAGES,src}

# Copy shared resources
cp -u /usr/local/bin/shared/resources/{error,info,question,warning}.gif ./resources/

# Copy other shared resources
cp -u /usr/local/bin/shared/resources/locale/ru/LC_MESSAGES/shared.mo ./resources/locale/ru/LC_MESSAGES/

# Copy shared Python files
cp -u /usr/local/bin/shared/src/{gettext_windows,regexp,shared,sharedGUI}.py ./src/

rm ./update_structure.sh

ls --color=always .
