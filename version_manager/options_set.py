from typing import Dict, List, Optional
import yaml


def get_parameter_values(
    parameter_values: Dict[str, str], values_list: Optional[List[str]]
) -> Dict[str, str]:
    """
    Override the parameter values that are given in the list.
    It assumes each parameter is in the 'KEY=VALUE' format.
    """
    if not values_list:
        return parameter_values

    for value in values_list:
        tokens = value.split("=", 2)
        parameter_values[tokens[0]] = tokens[1]

    return parameter_values


def get_parameters_from_file(file_name: Optional[str]) -> Dict[str, str]:
    if not file_name:
        return dict()

    with open(file_name, "r", encoding="utf-8") as stream:
        result = list(yaml.safe_load_all(stream))[0]

    return result
