# TEST_HOST="192.168.0.23"
TEST_HOST = "172.17.0.1"

IE_DRIVER_DOWNLOAD_URL = "http://%s:8000/IEDriverServer_Win32_3.0.0.zip" % TEST_HOST
GECKO_DRIVER_DOWNLOAD_URL = "http://%s:8000/geckodriver-v0.13.0-win64.zip" % TEST_HOST
CHROME_DRIVER_DOWNLOAD_URL = "http://%s:8000/chromedriver_win32.zip" % TEST_HOST
EDGE_DRIVER_DOWNLOAD_URL = "http://%s:8000/MicrosoftWebDriver.exe" % TEST_HOST

SELENIUM_STANDALONE_JAR_URL = "http://%s:8000/selenium-server-standalone-3.0.1.jar" % TEST_HOST

JAVA_JRE_URL = "http://%s:8000/jre-8u121-windows-i586.exe" % TEST_HOST

# JAVA_JRE_URL="http://download.oracle.com/otn-pub/java/jdk/8u121-b13/e9e7ea248e2c4826b92b3f075a80e441/jre-8u121-windows-i586.exe"
