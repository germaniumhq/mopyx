from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="git_monorepo",
    version="1.0.0",
    description="git_monorepo",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    entry_points={
        "console_scripts": [
            "git-mono = git_monorepo.mainapp:main",
            "git-monorepo-editor = git_monorepo.editorapp:main",
        ]
    },
    install_requires=[],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "git_monorepo": ["py.typed"],
    },
)
