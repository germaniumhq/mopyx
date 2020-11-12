import shlex
import uuid
from typing import Optional, Any, Union, Dict, List, cast

import yaml

from adhesive.workspace.Workspace import Workspace
from yamldict import YamlDict, YamlList
from yamldict.YamlNavigator import YamlNavigator


class KubeApi():
    ALL: str = ":all:"

    def __init__(self,
                 workspace: Workspace,
                 namespace: Optional[str] = None) -> None:
        self._workspace = workspace
        self._namespace = namespace

    def get(self,
            *args,
            kind: str,
            name: str,
            namespace: Optional[str] = None) -> Any:
        """
        Gets an object from the kubernetes API
        :param args:
        :param kind:
        :param name:
        :param namespace:
        :return:
        """
        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl get {kind} {name} -o yaml"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        object_data = self._workspace.run(
            command,
            capture_stdout=True)

        assert object_data

        return YamlDict(
            property_name=f"{{kind:{kind}}}",
            content=yaml.safe_load(object_data))

    def yaml(self, content: str) -> YamlDict:
        return YamlDict(content=yaml.safe_load(content))

    def getall(self,
               *args,
               kind: str,
               filter: Optional[str] = None,
               namespace: Optional[str] = None) -> YamlList:
        """
        Gets an object from the kubernetes API
        :param args:
        :param kind:
        :param filter:
        :param namespace:
        :return:
        """
        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl get {kind} -o yaml"

        if filter:
            command += f" -l {shlex.quote(filter)}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        object_data = self._workspace.run(
            command,
            capture_stdout=True)

        assert object_data

        content = YamlDict(content=yaml.safe_load(object_data))

        if content.kind == "List" and content.apiVersion == "v1":
            return YamlList(
                property_name=f"{{kind:List[{kind}]}}",
                content=content.items._raw)

        return YamlList(property_name=f"{{kind:List[{kind}]}}",
                        content=[content._raw])

    def exists(self,
               *args,
               kind: str,
               name: str,
               namespace: Optional[str] = None) -> bool:
        """
        Checks if an object exists
        :param args:
        :param kind:
        :param name:
        :param namespace:
        :return:
        """
        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl get {kind} {name}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        try:
            self._workspace.run(command)
            return True
        except Exception:
            return False

    def delete(self,
               *args,
               kind: str,
               name: str,
               namespace: Optional[str] = None) -> None:
        """
        Delete an object
        :param args:
        :param kind:
        :param name:
        :param namespace:
        :return:
        """

        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl delete {kind} {name}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        self._workspace.run(command)

    def create(self,
               *args,
               kind: str,
               name: str,
               namespace: Optional[str] = None) -> None:
        """
        Delete an object
        :param args:
        :param kind:
        :param name:
        :param namespace:
        :return:
        """

        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl create {kind} {name}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        self._workspace.run(command)

    def scale(self,
              *args,
              kind: str,
              name: str,
              replicas: int,
              namespace: Optional[str] = None) -> None:
        """
        Delete an object
        :param args:
        :param kind:
        :param name:
        :param namespace:
        :return:
        """

        if args:
            raise Exception("You need to use named arguments.")

        command = f"kubectl scale {kind} {name} --replicas={replicas}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        self._workspace.run(command)

    def apply(self,
              content: Union[str, YamlDict, Dict, YamlList, List],
              namespace: Optional[str] = None) -> None:
        """
        Apply the content
        :param content:
        :return:
        """
        file_name = f"/tmp/{str(uuid.uuid4())}.yml"
        command = f"kubectl apply -f {file_name}"

        namespace = namespace if namespace is not None else self._namespace

        if namespace == KubeApi.ALL:
            command += f" --all-namespaces"
        elif namespace:
            command += f" --namespace={namespace}"

        if isinstance(content, YamlNavigator):
            content = content._raw

        if isinstance(content, dict):
            content = yaml.safe_dump(content)

        if isinstance(content, list):
            content = yaml.safe_dump_all(content)

        try:
            self._workspace.write_file(file_name, cast(str, content))
            self._workspace.run(command)
        finally:
            self._workspace.rm(file_name)
