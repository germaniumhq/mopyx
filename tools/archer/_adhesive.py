import germanium_py_exe  # type: ignore


germanium_py_exe.pipeline(
    {
        "run_mypy": False,
        "run_flake8": False,
        "repo": "git@github.com:bmustiata/archer-py.git",
        "binaries": {
            "name": "Python 3.7 on Linux x64",
            "platform": "python:3.7",
            "publish_pypi": "sdist",
        },
    }
)
