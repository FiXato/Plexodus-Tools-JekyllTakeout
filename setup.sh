#!/usr/bin/env sh
# encoding: utf-8
find ../extracted/Takeout/Google+\ Stream/Posts -type f -iname '*.json' -exec ./import_json_data_file.sh '{}' \;