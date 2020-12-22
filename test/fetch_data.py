from typing import Any

import jenkins
import json


def dump_data(file_name: str, data: Any) -> None:
    print(f"Writing: {file_name}")

    with open(file_name, "wt", encoding="utf-8") as f:
        f.write(json.dumps(data,
                           sort_keys=True,
                           indent=3,
                           separators=(',', ': ')))


server = jenkins.Jenkins("http://jenkins:30000",
                         username="admin",
                         password="admin")


result = server.get_job_info("felixbm", depth="5")
# result = server.get_all_jobs()

dump_data("model/remote/jenkins/felixbm.json", result)
