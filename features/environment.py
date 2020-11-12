import os
#from http.server import SimpleHTTPRequestHandler
from socketserver import ThreadingTCPServer
from threading import Thread

from germanium.static import *
from features.PostHttpRequestHandler import PostHttpRequestHandler


def before_all(context):
    ThreadingTCPServer.allow_reuse_address = True
    Handler = PostHttpRequestHandler
    context._httpServer = ThreadingTCPServer(("0.0.0.0", 8000), Handler)

    print("started server on 0.0.0.0:8000")

    t = Thread(target=context._httpServer.serve_forever)
    t.start()


def after_all(context):
    print("Shutting down HTTP server")
    context._httpServer.shutdown()

    print("Done shutting down HTTP server")
    keep_browser = 'TEST_KEEP_BROWSER' in os.environ.keys()
    reuse_browser = 'TEST_REUSE_BROWSER' in os.environ.keys()

    if keep_browser:
        print("Keeping the browser, since all is done, and TEST_KEEP_BROWSER is set.")
        return

    if reuse_browser:
        print("Closing the browser, since all is done, and TEST_REUSE_BROWSER is set.")
        if get_germanium():
            close_browser()


def after_scenario(context, scenario):
    keep_browser = 'TEST_KEEP_BROWSER' in os.environ.keys()
    reuse_browser = 'TEST_REUSE_BROWSER' in os.environ.keys()

    if keep_browser:
        print("Not closing the browser since TEST_KEEP_BROWSER is set")
    elif reuse_browser:
        print("Not closing the browser since TEST_REUSE_BROWSER is set")
    else:
        close_browser()
