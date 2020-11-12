import adhesive
from adhesive.workspace import ssh

import unittest
import random

test = unittest.TestCase()
assert_equal = unittest.TestCase().assertEqual


def find_open_port() -> int:
    # FIXME: this should find an open port on the host, not inside the
    # docker container. a bit trickier to do.
    port = random.randint(10000,60000)
    return port


@adhesive.task('Start\ SSH\ Server')
def start_ssh_server(context):
    print("starting server...")
    context.data.ssh_port = find_open_port()
    container_id = context.workspace.run(
        f"docker run -d -p {context.data.ssh_port}:22 rastasheep/ubuntu-sshd:18.04",
        capture_stdout=True)

    context.data.container_id = container_id
    print("[OK] started server")

@adhesive.task('Test running commands on ssh connections')
def run_ls_inside_server(context):
    with ssh.inside(context.workspace,
            "172.17.0.1",
            username="root",
            password="root",
            port=context.data.ssh_port) as w:
        # since the path doesn't exists on the ssh server, we first change it
        # here
        w.pwd = "/tmp"

        # we test the stderr writing
        w.run("echo text; echo error >&2")  # we write on stderr on purpose

        # we test the non-zero error codes
        got_error = True

        try:
            w.run("false")
            got_error = False
        except Exception as e:
            pass

        if not got_error:
            raise Exception("non zero error code didn't raised exception")

        # we test the capture stdout
        w.run("touch testfile.txt")
        ls_result = w.run("ls -la", capture_stdout=True)

        assert "testfile.txt" in ls_result

        # we test the pwd change
        pwd = w.run("pwd", capture_stdout=True).strip()

        assert_equal(pwd, w.pwd)


@adhesive.task('Test\ write_file\ API')
def test_write_file_api(context):
    with ssh.inside(context.workspace,
            "172.17.0.1",
            username="root",
            password="root",
            port=context.data.ssh_port) as w:
        w.pwd = "/tmp"
        w.write_file("test.txt", "yay")
        test_content = w.run("cat test.txt", capture_stdout=True)

        assert "yay" == test_content



@adhesive.task('Shutdown\ Server')
def shutdown_server(context):
    print("shutting down server...")
    context.workspace.run(f"docker rm -f {context.data.container_id}")
    print("[OK] server was shutdown")


@adhesive.task('Test\ Failed')
def test_failed(context):
    print(context.data.as_dict())
    context.data.test_failed = True



@adhesive.task('Check\ if\ test\ failed')
def check_if_test_failed(context):
    if context.data._error:
        print("Uh oh, we got an error in the ssh execution")
        print(context.data._error)

    assert not context.data.test_failed


adhesive.bpmn_build("ssh.bpmn")
