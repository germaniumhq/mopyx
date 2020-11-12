from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="project_archer",
    version="0.3.0",
    description="Switch projects with ease.",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    entry_points={"console_scripts": ["archer = project_archer.mainapp:main"]},
    install_requires=[
        "termcolor-util",
        "click",
        "PyYAML >=5.1, <5.2",
    ],
    packages=packages,
    package_data={"": ["*.txt", "*.rst"]},
)
