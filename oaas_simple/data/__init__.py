import json
from typing import Union, Any

from oaas_simple.rpc import call_pb2


def create_data(data: Union[str, bytes, Any]) -> call_pb2.Data:
    if isinstance(data, str):
        return call_pb2.Data(s=data)

    if isinstance(data, bytes):
        return call_pb2.Data(b=data)

    json_data = json.dumps(data)
    return call_pb2.Data(json=json_data)


def from_data(data: call_pb2.Data) -> Union[Any, str, bytes]:
    if data.s:
        return data.s

    if data.b:
        return data.b

    return json.loads(data.json)
