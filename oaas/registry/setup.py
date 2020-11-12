from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="oaas_registry",
    version="1.1.1",
    description="oaas_registry",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[
        "oaas",
        "grpc-stubs==1.24.2",
        "readerwriterlock==1.0.7",
        "oaas_grpc",
        "oaas_simple",
        "oaas_registry_api",
        "countertype",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "oaas_registry": ["py.typed"],
    },
)
