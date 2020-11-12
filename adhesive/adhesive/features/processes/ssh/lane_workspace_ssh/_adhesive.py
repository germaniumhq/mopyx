import random

import adhesive
from adhesive.workspace import ssh


def find_open_port() -> int:
    # FIXME: this should find an open port on the host, not inside the
    # docker container. a bit trickier to do.
    port = random.randint(10000,60000)
    return port


@adhesive.lane("ssh")
def lane_ssh(context):
    with ssh.inside(context.workspace,
            "172.17.0.1",
            username="root",
            password="root",
            port=context.data.ssh_port) as w:
        yield w


@adhesive.task('Start SSH Server')
def start_ssh_server(context):
    print("starting server...")
    context.data.ssh_port = find_open_port()
    container_id = context.workspace.run(
        f"docker run -d -p {context.data.ssh_port}:22 rastasheep/ubuntu-sshd:18.04",
        capture_stdout=True)

    context.data.container_id = container_id
    print("[OK] started server")


@adhesive.task('Task', lane="ssh", loop="items")
def run_ls_in_ssh(context):
    print(context.workspace)
    context.workspace.run(f"""
        whoami
        ls -la
    """)

@adhesive.task('Shutdown Server')
def shutdown_server(context):
    print("shutting down server...")
    context.workspace.run(f"docker rm -f {context.data.container_id}")
    print("[OK] server was shutdown")

# We need to create more than the number of available channels, to see if we leak
# channels with executions. Another limit is the amount of parallel connections.
# For that we configure the pool_size in the `.adhesive/config.yml` in this folder.
adhesive.build(initial_data={
    "items": range(40),
})
