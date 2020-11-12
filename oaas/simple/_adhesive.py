import germanium_py_exe  # type: ignore


germanium_py_exe.pipeline(
    {
        "run_mypy": False,
        "repo": "git@github.com:germaniumhq/oaas-simple.git",
        "binaries": {
            "name": "Python 3.8 on Linux x64",
            "platform": "python:3.8",
            "publish_pypi": "sdist",
        },
    }
)
