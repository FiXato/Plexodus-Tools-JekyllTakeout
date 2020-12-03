#!/usr/bin/env sh
input="$1"
filename="$(basename "$input")"
clean_filename="$(printf '%s' "$filename" | sed 's/ /_/g;s/[^a-zA-Z0-9_\.)(-\[\]]*//g')"
mkdir -p "_data/posts"

if hash ditto 2>/dev/null; then
  CP_COMMAND='ditto'
else
  CP_COMMAND='cp -r'
fi

$CP_COMMAND "$input" "_data/posts/$clean_filename"
