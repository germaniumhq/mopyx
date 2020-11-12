def read_stdout(process) -> str:
    result = process.stdout

    if result:
        print(f"out: '{result}'")

    return result


def read_stderr(process) -> str:
    result = process.stderr

    if result:
        print(f"err: '{result}'")

    return result
