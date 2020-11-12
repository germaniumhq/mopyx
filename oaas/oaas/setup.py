from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="oaas",
    version="1.5.1",
    description="Operation as a Service",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "oaas": ["py.typed"],
    },
)
