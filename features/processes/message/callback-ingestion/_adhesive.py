import adhesive
import threading
import uuid
from flask import Flask
import requests
import time
import unittest


test = unittest.TestCase()


app = Flask(__name__)
flask_thread = None


@app.route("/health")
def health_check():
    """
    Health check to use for waiting Flask to come up.
    """
    return "ok"


@adhesive.message_callback('REST: /rest/start-build')
def rest_endpoint(context, callback):
    @app.route('/rest/start-build')
    def route_root():
        callback({
            "data": "event data",
        })

        return "ok"


@adhesive.message_callback('REST: /')
def root_endpoint(context, callback):
    @app.route('/')
    def route_item():
        callback({
            "data": "event data",
        })

        return "ok"


# we need to start it async
@adhesive.task('Start Flask Server')
def run_flask_server(context):
    global flask_thread

    flask_thread = threading.Thread(name='Flask', target=app.run)
    flask_thread.setDaemon(True)
    flask_thread.start()


@adhesive.task(re='Process (.+?) Event')
def process_run_event(context, event_type):
    context.data.ran_tasks = dict()
    context.data.ran_tasks[f"Process {event_type} Event"] = { str(uuid.uuid4()) }


@adhesive.task('Generate Messages')
def generate_messages(context):
    # we wait for the server to come up
    retry_count = 6

    while retry_count > 0:
        try:
            r = requests.get("http://localhost:5000/health")

            if r.status_code != 200:
                raise Exception("problem")

            if r.text != "ok":
                raise Exception("wrong text")

            retry_count = -1
            break
        except Exception as e:
            pass

        retry_count -= 1
        time.sleep(0.4)


    requests.get("http://localhost:5000/")
    requests.get("http://localhost:5000/")
    requests.get("http://localhost:5000/")
    requests.get("http://localhost:5000/rest/start-build")


data = adhesive.bpmn_build("rest-endpoint.bpmn", wait_tasks=False)
test.assertTrue(data.ran_tasks, "We have no data back")
test.assertEqual(3, len(data.ran_tasks["Process Root Event"]))
test.assertEqual(1, len(data.ran_tasks["Process Build Event"]))

