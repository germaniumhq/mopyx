import cgi
from http.server import SimpleHTTPRequestHandler


class PostHttpRequestHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        form = cgi.FieldStorage(
            fp = self.rfile,
            headers = self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     }
        )

        filename = form['file'].filename

        body = bytearray("<html><body>Uploaded '%s'.</body><html>" % filename, "utf-8")

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
