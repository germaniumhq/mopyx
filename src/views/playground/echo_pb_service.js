// package: 
// file: echo.proto

var echo_pb = require("./echo_pb");
var grpc = require("@improbable-eng/grpc-web").grpc;

var Echo = (function () {
  function Echo() {}
  Echo.serviceName = "Echo";
  return Echo;
}());

Echo.echo = {
  methodName: "echo",
  service: Echo,
  requestStream: false,
  responseStream: false,
  requestType: echo_pb.EchoMessage,
  responseType: echo_pb.EchoMessage
};

Echo.repeat = {
  methodName: "repeat",
  service: Echo,
  requestStream: false,
  responseStream: true,
  requestType: echo_pb.EchoMessage,
  responseType: echo_pb.EchoMessage
};

exports.Echo = Echo;

function EchoClient(serviceHost, options) {
  this.serviceHost = serviceHost;
  this.options = options || {};
}

EchoClient.prototype.echo = function echo(requestMessage, metadata, callback) {
  if (arguments.length === 2) {
    callback = arguments[1];
  }
  var client = grpc.unary(Echo.echo, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onEnd: function (response) {
      if (callback) {
        if (response.status !== grpc.Code.OK) {
          var err = new Error(response.statusMessage);
          err.code = response.status;
          err.metadata = response.trailers;
          callback(err, null);
        } else {
          callback(null, response.message);
        }
      }
    }
  });
  return {
    cancel: function () {
      callback = null;
      client.close();
    }
  };
};

EchoClient.prototype.repeat = function repeat(requestMessage, metadata) {
  var listeners = {
    data: [],
    end: [],
    status: []
  };
  var client = grpc.invoke(Echo.repeat, {
    request: requestMessage,
    host: this.serviceHost,
    metadata: metadata,
    transport: this.options.transport,
    debug: this.options.debug,
    onMessage: function (responseMessage) {
      listeners.data.forEach(function (handler) {
        handler(responseMessage);
      });
    },
    onEnd: function (status, statusMessage, trailers) {
      listeners.status.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners.end.forEach(function (handler) {
        handler({ code: status, details: statusMessage, metadata: trailers });
      });
      listeners = null;
    }
  });
  return {
    on: function (type, handler) {
      listeners[type].push(handler);
      return this;
    },
    cancel: function () {
      listeners = null;
      client.close();
    }
  };
};

exports.EchoClient = EchoClient;

