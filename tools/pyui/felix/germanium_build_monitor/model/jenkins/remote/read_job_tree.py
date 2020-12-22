from typing import Dict, Set, Any

from germanium_build_monitor.model.JenkinsFolder import JenkinsFolder
from germanium_build_monitor.model.JenkinsJob import JenkinsJob


def process(folder: JenkinsFolder, result: Any):
    found_urls: Set[str] = set()

    def process_entry(folder: JenkinsFolder, entry: Dict):

        def process_folder(folder: JenkinsFolder, entry: Dict):
            f = JenkinsFolder(parent=folder,
                              name=entry['name'])
            folder.folders.append(f)

            for job in entry['jobs']:
                process_entry(f, job)

        def process_job(folder: JenkinsFolder, entry: Dict):
            url: str = entry['url']

            if url in found_urls:
                return

            found_urls.add(url)

            job = JenkinsJob(parent=folder,
                             name=entry['name'],
                             full_name=entry['fullname'],
                             url=url)
            folder.jobs.append(job)

        def process_workflow_job(folder: JenkinsFolder, entry: Dict):
            if "/" not in entry["fullname"] or folder.parent:
                process_job(folder, entry)

        if entry["_class"] == "com.cloudbees.hudson.plugins.folder.Folder":
            process_folder(folder, entry)
        elif entry["_class"] == "org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject":
            process_job(folder, entry)
        elif entry["_class"] == "org.jenkinsci.plugins.workflow.job.WorkflowJob":
            process_workflow_job(folder, entry)
        else:
            print(f"Unprocessed: {entry['_class']}")

    for entry in result:
        process_entry(folder, entry)

