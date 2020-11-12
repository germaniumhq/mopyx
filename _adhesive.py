import adhesive
import gbs
import ge_tooling
import ge_git
import time
from adhesive import scm
from adhesive.secrets import secret
from adhesive.workspace import docker


@adhesive.task("Read Parameters")
def read_parameters(context) -> None:
    context.data.run_mypy = True
    context.data.test_integration = True


@adhesive.task(re=r"^Ensure Tooling:\s+(.+)$")
def gbs_ensure_tooling(context, tool_name) -> None:
    ge_tooling.ensure_tooling(context, tool_name)


@adhesive.task(re="Run tool: mypy")
def gbs_run_tool(context) -> None:
    image_name = gbs.test(
        context,
        platform="python:3.7",
        gbs_prefix=f"/_gbs/lin64/")

    command = f"MYPYPATH=./stubs:. " \
              f"mypy --shadow-file _adhesive.py setup.py ."

    with docker.inside(context.workspace, image_name) as w:
        w.run(command)


@adhesive.task('Run tool: version-manager')
def run_tool_version_manager(context):
    ge_tooling.run_tool(
        context,
        tool="version-manager",
        command="version-manager")


@adhesive.task("Checkout Code")
def checkout_code(context) -> None:
    scm.checkout(context.workspace)


@adhesive.task("GBS: lin64")
def gbs_build_lin64(context) -> None:
    context.data.gbs_build_image_name = \
        gbs.build(
            context,
            platform="python:3.7",
            gbs_prefix=f"/_gbs/lin64/")


@adhesive.task('GBS Test {parallel_processing}: lin64')
def gbs_test_lin64(context) -> None:
    image_name = gbs.test(
        context,
        platform="python:3.7",
        gbs_prefix=f"/_gbs/lin64/")

    command = f"ADHESIVE_PARALLEL_PROCESSING={context.data.parallel_processing} " \
              f"ADHESIVE_TEMP_FOLDER=/tmp/adhesive-test " \
              f"python -m unittest"

    with docker.inside(context.workspace, image_name) as w:
        w.run(command)


@adhesive.task('GBS Integration Test {parallel_processing}: lin64')
def gbs_integration_test_lin64(context) -> None:
    image_name = gbs.test(
        context,
        platform="python:3.7",
        gbs_prefix=f"/_gbs/lin64/")

    command = f"ADHESIVE_PARALLEL_PROCESSING={context.data.parallel_processing} " \
              f"ADHESIVE_TEMP_FOLDER=/tmp/adhesive-test " \
              f"behave -t ~@manualtest -t ~@no{context.data.parallel_processing}"

    with docker.inside(
            context.workspace,
            image_name,
            "-v /var/run/docker.sock:/var/run/docker.sock:rw") as w:
        w.run("python --version")
        w.run(command)


@adhesive.task("GBS: win32")
def gbs_build_win32(context) -> None:
    pass
    # gbs.build(workspace=context.workspace,
    #          platform="python:win32",
    #          gbs_prefix=f"/_gbs/win32/")


@adhesive.gateway('Is Release Version?')
def is_release_version(context):
    current_version = ge_tooling.run_tool(
        context,
        tool="version-manager",
        command="version-manager --tag",
        capture_stdout=True).strip()

    context.data.current_version = current_version

    if ge_git.get_tag_version(current_version):
        context.data.release_version = True
    else:
        context.data.release_version = False


@adhesive.usertask('Publish to PyPI?')
def publish_to_pypi_confirm(context, ui):
    ui.add_checkbox_group(
        "publish",
        title="Publish",
        values=(
            ("nexus", "Publish to Nexus"),
            ("pypitest", "Publish to PyPI Test"),
            ("pypi", "Publish to PyPI"),
        ),
        value=("pypitest", "pypi")
    )


@adhesive.task(re='^PyPI publish to (.+?)$')
def publish_to_pypi(context, registry):
    with docker.inside(context.workspace, context.data.gbs_build_image_name) as w:
        with secret(w, "PYPIRC_RELEASE_FILE", "/germanium/.pypirc"):
            w.run(f"python setup.py bdist_wheel upload -r {registry}")


@adhesive.task('Wait for pypi availability')
def wait_for_pypi_availability(context: adhesive.Token) -> None:
    # wait at most ~2 minutes for the package to appear
    for i in range(10):
        try:
            with docker.inside(context.workspace,
                               'germaniumhq/python:3.8') as w:
                w.run(f"""
                    pip install adhesive=={context.data.current_version}
                """)

                return
        except Exception:
            time.sleep(10)

    raise Exception(f"Timeouted waiting for adhesive=={context.data.current_version} "
                    f"to appear.")


@adhesive.task('Build Docker Image')
def build_docker_image(context):
    context.workspace.run(f"""
        docker build -t germaniumhq/adhesive \\
                     -t germaniumhq/adhesive:{context.data.current_version} \\
                     .
    """)


# FIXME: use secrets
@adhesive.task('Publish Docker Image')
def publish_docker_image(context):
    context.workspace.run(f"""
        docker push germaniumhq/adhesive:{context.data.current_version}
        docker push germaniumhq/adhesive:latest
    """)


adhesive.bpmn_build("adhesive-self.bpmn")
