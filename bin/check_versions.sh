#!/usr/bin/env bash

GERMANIUM_FOLDER=$(readlink -f $(dirname $0)/..)

set -e

. $GERMANIUM_FOLDER/_gbs/prepare-build2/driver_versions

#
# Check the Chrome Driver version.
#
echo -n "Checking Chrome Driver $CHROMEDRIVER_VERSION ... "

CHROME_VERSION=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)

if [[ "$CHROME_VERSION" != "$CHROMEDRIVER_VERSION" ]]; then
    echo "NOPE"
    echo "Newer Chrome Version: $CHROME_VERSION is available"
else # not [[ "CHROME_VERSION" != "$CHROMEDRIVER_VERSION" ]]
    echo "OK"
fi   # else [[ "CHROME_VERSION" != "$CHROMEDRIVER_VERSION" ]]


#
# Check the Firefox version itself.
#
echo -n "Checking Firefox version $FIREFOX_VERSION ... "

REMOTE_FIREFOX_VERSION=$(wget -q -O - https://www.mozilla.org/en-US/firefox/notes/ | grep '<div class="version">' -A 1 | grep '<h2>' | cut -f2 -d '>' | cut -f1 -d '<')

if [[ "$REMOTE_FIREFOX_VERSION" != "$FIREFOX_VERSION" ]]; then
    echo "NOPE"
    echo "Newer Firefox Version: $REMOTE_FIREFOX_VERSION"
else # not [[ "$REMOTE_FIREFOX_VERSION" != "$FIREFOX_VERSION" ]]
    echo "OK"
fi   # else [[ "$REMOTE_FIREFOX_VERSION" != "$FIREFOX_VERSION" ]]

#
# Check the Marionette/Firefox Driver Version
#

echo -n "Checking Firefox (Marionette) Driver $FIREFOXDRIVER_VERSION ... "

REMOTE_FIREFOXDRIVER_VERSION=$(wget -q -O - https://github.com/mozilla/geckodriver/releases.atom | grep '<title>v' | perl -pe 's|\s*<title>v(.*?)</title>|$1|' | head -n 1)

if [[ "$REMOTE_FIREFOXDRIVER_VERSION" != "$FIREFOXDRIVER_VERSION" ]]; then
    echo "NOPE"
    echo "Newer Firefox Marionette Version: $REMOTE_FIREFOXDRIVER_VERSION"
else # not [[ "$REMOTE_FIREFOXDRIVER_VERSION" != "$FIREFOXDRIVER_VERSION" ]]
    echo "OK"
fi   # else [[ "$REMOTE_FIREFOXDRIVER_VERSION" != "$FIREFOXDRIVER_VERSION" ]]

#
# Check the IE Driver Version
#
echo -n "Checking IE Driver $IEDRIVER_VERSION ... "

IE_VERSION=$(wget -q -O - http://www.seleniumhq.org/download/ | grep "selenium-release" | grep IEDriver | grep Win32 | perl -pe 's|.*_Win32_(.*?).zip.*|$1|')

if [[ "$IEDRIVER_VERSION" != "$IE_VERSION" ]]; then
    echo "NOPE"
    echo "Newer IE Driver Version: $IE_VERSION"
else # not [[ "$IEDRIVER_VERSION" != "$IE_VERSION" ]]
    echo "OK"
fi   # else [[ "$IEDRIVER_VERSION" != "$IE_VERSION" ]]

#
# Check the EDGE Version
#
echo -n "Checking Edge Driver $EDGEDRIVER_VERSION ... "

EDGE_VERSION=$(wget -q -O - "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/" | html-beautify | grep "driver-download" | grep "WebDriver for release number" | head -n 1 | tr -s " " | cut -f 10 -d\  | cut -f1 -d\")

if [[ "$EDGEDRIVER_VERSION" != "$EDGE_VERSION" ]]; then
    echo "NOPE"
    echo "Newer Edge Driver Version: $EDGE_VERSION"
    echo "URL: $(wget -q -O - "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/" | html-beautify | grep "driver-download" | grep "WebDriver for release number" | head -n1 | perl -pe 's|^.* href="(.*?)".*?$|\1|g')"
else # not [[ "$EDGEDRIVER_VERSION" != "$EDGE_VERSION" ]]
    echo "OK"
fi   # else [[ "$EDGEDRIVER_VERSION" != "$EDGE_VERSION" ]]


#
# Check the EDGE EULA URL if it changed
#
echo -n "Checking Edge EULA Driver Version: $EDGEDRIVER_EULA_VERSION ... "

EDGE_EULA_VERSION=$(wget -q -O - "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/" | html-beautify | grep "License terms" | head -1 | perl -pe 's|^.* href="(.*?)".*?$|\1|g')

if [[ "$EDGEDRIVER_EULA_VERSION" != "$EDGE_EULA_VERSION" ]]; then
    echo "NOPE"
    echo "New EULA Edge Driver Version: $EDGE_EULA_VERSION"
else # not [[ "$EDGEDRIVER_EULA_VERSION" != "$EDGE_EULA_VERSION" ]]
    echo "OK"
fi   # else [[ "$EDGEDRIVER_EULA_VERSION" != "$EDGE_EULA_VERSION" ]]





