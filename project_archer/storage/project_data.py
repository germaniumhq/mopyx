import yaml


def read_project_yml(data):
    loaded_data = yaml.safe_load(data)
    try:
        project = loaded_data.get("config") or loaded_data.get("layout")
        if not project:
            project = {"name": "<broken data>"}

        ensure_array(project, "requires")
        ensure_array(project, "layouts")
        ensure_array(project, "activate")
        ensure_array(project, "deactivate")

        if "exports" not in project:
            project["exports"] = {}
        if "commands" not in project:
            project["commands"] = {}
        if "name" not in project:
            project["name"] = "<not defined>"

        return project
    except Exception as e:
        raise Exception("Unable to read loaded data: %s" % loaded_data, e)


def ensure_array(obj, property_name):
    if property_name not in obj or not obj[property_name]:
        obj[property_name] = []
    if type(obj[property_name]) is str:
        obj[property_name] = [obj[property_name]]
