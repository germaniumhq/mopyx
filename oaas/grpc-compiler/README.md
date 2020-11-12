`oaas-grpc-compiler` compiles gRPC proto files, with type information
that can be verified using `mypy`, formatted with `black`, with the
possibility of custom modules where the sources to be generated in.

The `add_Type_to_server` function is moved into the Servicer type as a
static method: `Type.add_to_server`, because this is how OaaS can figure
out if this is a *gRPC* service, or a *simple* service.

Usage
=====

    Usage: oaas-grpc-compiler [OPTIONS] GRPC_FILES

    Options:
      --module TEXT  The module of the python package to generate
      --output TEXT  Output folder where to write the files
      --help         Show this message and exit.

Example
=======

Proto file `test.proto`:

    syntax = "proto3";


    message Ping {
      string text = 1;
    }

    message Pong {
      string text = 1;
      int32 len = 2;
    }

    service TestService {
      rpc ping(Ping) returns (Pong) {}
      rpc ping_copy(Ping) returns (Pong) {}
      rpc ping_exception(Ping) returns (Pong) {}
    }

Invocation:

    oaas-grpc-compiler --module some.custom.module --output some/custom/module test.proto
