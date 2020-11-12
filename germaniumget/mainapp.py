import colorama
from germaniumget.styles import title, text, question, read_option, warning, block, logo, read_string
from germaniumget.detectors import is_edge_detected, is_chrome_detected, is_firefox_detected, is_java8_installed
from germaniumget.download import download, extract_zip
from germaniumget.templates import template_run_node, template_configuration_file, write_file
import re
from germaniumget.execute_program import execute_program
from germaniumget.file_operations import \
    create_temp_folder, \
    get_germanium_folder, \
    mkdir_p, \
    rm_rf, \
    create_desktop_link

from germaniumget.download_urls import \
    IE_DRIVER_DOWNLOAD_URL, \
    GECKO_DRIVER_DOWNLOAD_URL, \
    CHROME_DRIVER_DOWNLOAD_URL, \
    EDGE_DRIVER_DOWNLOAD_URL, \
    SELENIUM_STANDALONE_JAR_URL, \
    JAVA_JRE_URL


def parse_tags(tags):
    values = []

    for tag in tags.split(","):
        items = tag.split("=", 1)
        values.append({
            "key": items[0],
            "value": items[1]
        })

    return values


def main():
    install_ie = False
    install_edge = False
    install_firefox = False
    install_chrome = False
    install_java = False
    edge_tags = ""
    chrome_tags = ""
    firefox_tags = ""
    ie_tags = ""

    germanium_home = r'C:\Germanium'
    java_home = r'C:\Germanium\Java'

    # =====================================================
    # Actual program starts here
    # =====================================================
    colorama.init()
    print(logo("""
                                           _
      __ _  ___ _ __ _ __ ___   __ _ _ __ (_)_   _ _ __ ___
     / _` |/ _ \ '__| '_ ` _ \ / _` | '_ \| | | | | '_ ` _ \\
    | (_| |  __/ |  | | | | | | (_| | | | | | |_| | | | | | |
     \__, |\___|_|  |_| |_| |_|\__,_|_| |_|_|\__,_|_| |_| |_|
     |___/  2.0.5

    """))

    print(title("GET.germanium"))
    print(text("""
    This tool can be used to provision Windows Hosts with all
    the necessary environment.
    """))

    print(title("Selenium Node"))

    # =====================================================
    # Internet Explorer
    # =====================================================
    print('')
    print(question("Should IE support be enabled?"))
    option = read_option("[Y]es", "[N]o", "[C]ancel")

    if option == "cancel":
        exit(1)

    if option == "yes":
        install_ie = 1

        print(question("IE tags for the Selenium node"))
        print(block("""
            You can pass multiple tags in name=value format, comma
            separated.
        """))
        ie_tags = read_string("Tags")

    # =====================================================
    # Edge
    # =====================================================
    print('')
    if is_edge_detected():
        def check_edge_and_license():
            print(question("Should Edge support be enabled?"))
            option = read_option("[Y]es", "[N]o", "[C]ancel")

            if option == "cancel":
                exit(1)

            if option == "no":
                return False

            print(question("Do you agree to the Microsoft Edge WebDriver EULA?"))
            print(text("""
                       You can find the license at:
                       https://az813057.vo.msecnd.net/eulas/webdriver-eula.pdf
            """))
            option = read_option("[Y]es", "[N]o", "[C]ancel")

            if option == "cancel":
                exit(1)

            if option == "no":
                return False

            print(question("Edge tags for the Selenium node"))
            print(block("""
                You can pass multiple tags in name=value format, comma
                separated.
            """))
            edge_tags = read_string("Tags")  # NOQA - flake8 screws up in edge_tags scope analysis

            return True

        if check_edge_and_license():
            install_edge = 1
    else:
        print(warning("No Edge Support"))
        print(block(
            """
            Edge was not detected on this system, so no binary
            drivers will be downloaded, nor any configuration
            will be generated for the Selenium Node.
            """
        ))

    # =====================================================
    # Chrome
    # =====================================================
    print('')
    if is_chrome_detected():
        print(question("Should Chrome support be enabled?"))
        option = read_option("[Y]es", "[N]o", "[C]ancel")

        if option == "cancel":
            exit(1)

        if option == "yes":
            install_chrome = 1

            print(question("Chrome tags for the Selenium node"))
            print(block("""
                You can pass multiple tags in name=value format, comma
                separated.
            """))
            chrome_tags = read_string("Tags")
    else:
        print(warning("No Chrome Support"))
        print(block(
            """
            Chrome was not detected on this system, so no binary
            drivers will be downloaded, nor any configuration
            will be generated for the Selenium Node.
            """
        ))

    # =====================================================
    # Firefox
    # =====================================================
    print('')
    if is_firefox_detected():
        print(question("Should Firefox support be enabled?"))
        option = read_option("[Y]es", "[N]o", "[C]ancel")

        if option == "cancel":
            exit(1)

        if option == "yes":
            install_firefox = 1

            print(question("Firefox tags for the Selenium node"))
            print(block("""
                You can pass multiple tags in name=value format, comma
                separated.
            """))
            firefox_tags = read_string("Tags")
    else:
        print(warning("No Firefox Support"))
        print(block(
            """
            Firefox was not detected on this system, so no binary
            drivers will be downloaded, nor any configuration
            will be generated for the Selenium Node.
            """
        ))

    # =====================================================
    # Java
    # =====================================================
    if not is_java8_installed():
        def check_java_and_license():
            print('')
            print(question("Install Java 8?"))
            print(warning("This is required for the Selenium Node to work."))

            option = read_option("[Y]es", "[N]o", "[C]ancel")

            if option == "cancel":
                exit(1)

            if option == "no":
                print(warning("Without a Java 8 installation the Selenium Node will "
                              "not function. Make sure you will install it before attempting to "
                              "run the node."))
                return False

            print(question("Do you agree with the Oracle Java License?"))
            print(text("You can find the license at: "
                       "http://www.oracle.com/technetwork/java/javase/terms/license/index.html"))
            option = read_option("[Y]es", "[N]o", "[C]ancel")

            if option == "cancel":
                exit(1)

            if option == "no":
                print(warning("Without a Java 8 installation the Selenium Node will "
                              "not function. Make sure you will install it before attempting to "
                              "run the node."))
                return False

            return True

        if check_java_and_license():
            install_java = 1

    # =====================================================
    # Selenium Hub location.
    # =====================================================
    print(question("Selenium Hub URL?"))
    print(text("""
    To what hub should this node connect to. Only the IP,
    and the port if it's different from 4444, are required.
    """))

    selenium_hub = read_string("Hub", default="localhost")

    # if there is no port specified in the host
    if not re.compile(r"^.*?\:\d+$").match(selenium_hub):
        selenium_hub += ":4444"

    # =====================================================
    # Now that the configuration is done, let's ask the user
    # one more time, and be done with it.
    # =====================================================
    print('')
    print(title("Planned steps:"))

    if install_ie:
        print("  Install IE support.")

    if install_edge:
        print("  Install Edge support.")

    if install_chrome:
        print("  Install Chrome support.")

    if install_firefox:
        print("  Install Firefox support.")

    if install_java:
        print("  Install Java.")

    print("  Hub: %s" % selenium_hub)

    print(question("Start downloading and installation?"))
    option = read_option("[Y]es", "[N]o")

    if option == "no":
        exit(1)

    # =====================================================
    # Ok, now we need to start fetching files.
    # We will create first an empty folder for the downloads,
    # then we will fetch stuff.
    # =====================================================
    temp = create_temp_folder()
    ge_folder = get_germanium_folder(germanium_home)

    rm_rf(ge_folder('germanium-node.conf'),
          ge_folder('run-node.bat'),
          ge_folder('lib'))

    mkdir_p(ge_folder("lib"))

    browsers_enabled = []

    if install_ie:
        browsers_enabled.append({
            'browserName': 'internet explorer',
            'maxInstances': '1',
            'seleniumProtocol': 'WebDriver',
            'extraTags': parse_tags(ie_tags)
        })

    if install_firefox:
        browsers_enabled.append({
            'browserName': 'firefox',
            'maxInstances': '10',
            'seleniumProtocol': 'WebDriver',
            'extraTags': parse_tags(firefox_tags)
        })

    if install_chrome:
        browsers_enabled.append({
            'browserName': 'chrome',
            'maxInstances': '10',
            'seleniumProtocol': 'WebDriver',
            'extraTags': parse_tags(chrome_tags)
        })

    if install_edge:
        browsers_enabled.append({
            'browserName': 'MicrosoftEdge',
            'maxInstances': '10',
            'seleniumProtocol': 'WebDriver',
            'extraTags': parse_tags(edge_tags)
        })

    # =====================================================
    # If Java needs to be downloaded, let's start with
    # the elephant in the room.
    # =====================================================

    if install_java:
        download(JAVA_JRE_URL,
                 temp("jre-8u121-windows-i586.exe"))

        print(execute_program(temp("jre-8u121-windows-i586.exe"),
                              r'INSTALLDIR=%s' % java_home,
                              'INSTALL_SILENT=Enable',
                              'WEB_JAVA=0',
                              'SPONSORS=0'))

    # =====================================================
    # Download and unzip the drivers that are needed.
    # =====================================================
    if install_ie:
        download(IE_DRIVER_DOWNLOAD_URL,
                 temp("IEDriverServer.zip"))
        extract_zip(temp("IEDriverServer.zip"), ge_folder("lib"))

    if install_firefox:
        download(GECKO_DRIVER_DOWNLOAD_URL,
                 temp("GeckoDriver.zip"))

        extract_zip(temp("GeckoDriver.zip"), ge_folder("lib"))

    if install_chrome:
        download(CHROME_DRIVER_DOWNLOAD_URL,
                 temp("ChromeDriver.zip"))

        extract_zip(temp("ChromeDriver.zip"), ge_folder("lib"))

    if install_edge:
        download(EDGE_DRIVER_DOWNLOAD_URL,
                 ge_folder("lib/MicrosoftWebDriver.exe"))

    download(SELENIUM_STANDALONE_JAR_URL,
             ge_folder("lib/selenium-standalone.jar"))

    write_file(ge_folder("run-node.bat"),
               template_run_node(**{
                                 'hub_address': selenium_hub,
                                 'java_home': java_home,
                                 'germanium_home': germanium_home,
                                 'install_java': install_java
                                 }))

    write_file(ge_folder("germanium-node.conf"),
               template_configuration_file(**{
                                           'browsers': browsers_enabled
                                           }))

    print('')
    print(title("Create a desktop link?"))
    if read_option("[Y]es", "[N]o") == "yes":
        create_desktop_link(
            "Run Germanium Node",
            ge_folder("run-node.bat"))

    print('')
    print(title("Done"))
    print(text(r"Run the node by calling %s\run-node.bat" % germanium_home))

    print('')
    read_string("Press ENTER to continue")

    rm_rf(temp())

    colorama.deinit()

