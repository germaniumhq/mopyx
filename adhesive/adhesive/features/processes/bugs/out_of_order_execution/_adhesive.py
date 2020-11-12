import adhesive
import time


@adhesive.task("Populate Selected Builds")
def populate_selected_builds(context) -> None:
    context.data.start_times = dict()
    context.data.selected_builds = {
        "ucsj": "git://ucsj",
        "srv-core": "git://srv-core",
        "libcpprnt": "git://libcpprnt",
    }


@adhesive.task(re="^bob: (.*)$")
def bob_build(context, project_name) -> None:
    if project_name not in context.data.selected_builds:
        return

    if project_name not in context.data.start_times:
        context.data.start_times[project_name] = list()

    context.data.start_times[project_name].append(int(round(time.time() * 1000)))

    time.sleep(1)


@adhesive.task('tc: awi')
def tc_build(context) -> None:
    pass


adhesive.bpmn_build('syncfun_debug.bpmn')
