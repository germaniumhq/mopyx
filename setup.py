from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name='felixbm',
    version='master',
    description='Felix Build Monitor - a Jenkins monitoring tool.',
    long_description=readme,
    author='Bogdan Mustiata',
    author_email='bogdan.mustiata@gmail.com',
    license='BSD',
    entry_points={
        "console_scripts": [
            "felixbm = germanium_build_monitor.mainapp:main"
        ]
    },
    install_requires=[
        "PySide2",
        "mopyx >= 1.1.0, < 1.2.0",
        "python-jenkins",
        "PyYAML >=3.12, <3.13",
        "arrow >= 0.12.1, < 0.13"],
    packages=packages,
    url="https://germaniumhq.com/felix-build-monitor/",
    package_data={
        '': ['*.txt', '*.rst']
    })
