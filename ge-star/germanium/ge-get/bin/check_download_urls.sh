#!/usr/bin/env bash

PROJECT_FOLDER=$(readlink -f $(dirname $(readlink -f "$0"))/..)

cd $PROJECT_FOLDER

# simple function to check http response code before downloading a remote file
# example usage:
# if `validate_url $url >/dev/null`; then dosomething; else echo "does not exist"; fi

function validate_url(){
  if [[ `wget --header="Cookie: oraclelicense=accept-securebackup-cookie" -S --spider $1  2>&1 | grep 'HTTP/1.1 200 OK'` ]]; then echo "true"; fi
}

for url in `cat germaniumget/download_urls.py | grep -v mozilla | cut -f2 -d\"`; do
  RESULT="$(validate_url $url)"

  if [[ "$RESULT" == "true" ]]; then
    echo "    OK: $url"
  else
    echo "not OK: $url -> $RESULT"
    exit 1
  fi
done

