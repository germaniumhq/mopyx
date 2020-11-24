from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="arst",
    version="0.1.master",
    description="Poor man's yo generator.",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    entry_points={"console_scripts": ["arst = arst.mainapp:main"]},
    install_requires=[
        "pybars3 >=0.9.3, < 0.10",
        "termcolor_util >= 1.2.0, <2.0",
        "colorama >= 0.4.3",
        "mdvl >=2017.7.16.7",
        "PyYAML == 5.3.1",
        "click >= 7.0, <8.0",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "arst": ["py.typed"],
    },
)
