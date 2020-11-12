import adhesive
from flask import Flask, escape, request
from addict import Dict

app = Flask(__name__)


@adhesive.task('Run Flask Server')
def run_flask_server(context):
    app.run()


@adhesive.task('Create Resource')
def create_resource(context):
    pass


@adhesive.task('Update Resource')
def update_resource(context):
    pass


@adhesive.message_callback('REST: /rest/process-resource')
def message_rest_rest_process_resource(context, callback):
    @app.route("/rest/resource/create")
    def create_resource():
        callback(Dict({
            "type": "CREATE"
        }))

        return "Create event fired"

    @app.route("/rest/resource/process")
    def process_resource():
        callback(Dict({
            "type": "PROCESS"
        }))

        return "Process event fired"



adhesive.bpmn_build("rest-endpoint.bpmn")
