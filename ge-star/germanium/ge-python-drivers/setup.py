from setuptools import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='germaniumdrivers',
    version='master',
    description='The germanium project: Selenium WebDriver testing API that doesn\'t disappoint. (tested WebDrivers package)',
    long_description = readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='BSD',

    install_requires=[],
    packages=[
        'germaniumdrivers',
        'germaniumdrivers.binary.chrome.linux.64',
        'germaniumdrivers.binary.chrome.mac.64',
        'germaniumdrivers.binary.chrome.win.32',
        'germaniumdrivers.binary.firefox.linux.64',
        'germaniumdrivers.binary.firefox.mac.32',
        'germaniumdrivers.binary.firefox.win.64',
        'germaniumdrivers.binary.ie.win.32',
        'germaniumdrivers.binary.ie.win.64',
    ],
    package_data={
        'germaniumdrivers.binary.chrome.linux.64' : ['chromedriver'],
        'germaniumdrivers.binary.chrome.mac.64' : ['chromedriver'],
        'germaniumdrivers.binary.chrome.win.32' : ['chromedriver.exe'],
        'germaniumdrivers.binary.firefox.linux.64' : ['geckodriver'],
        'germaniumdrivers.binary.firefox.mac.32' : ['geckodriver'],
        'germaniumdrivers.binary.firefox.win.64' : ['geckodriver.exe'],
        'germaniumdrivers.binary.ie.win.32' : ['IEDriverServer.exe'],
        'germaniumdrivers.binary.ie.win.64' : ['IEDriverServer.exe']
    }
)

