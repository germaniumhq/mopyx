from adhesive.graph.Process import Process


def write_dot_file(file_name: str,
                   process: Process) -> None:
    with open(file_name, "wt") as f:
        f.write("digraph {\n")

        for task_id, task in process.tasks.items():
            f.write(f"{getid(task_id)} [label=\"{task.name}\"];\n")

        for edge_id, edge in process.edges.items():
            f.write(f"{getid(edge.source_id)} -> {getid(edge.target_id)};\n")

        f.write("}\n")


def getid(id: str) -> str:
    return "n" + id.replace('-', '')
