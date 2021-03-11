import re
from threading import Thread
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
from tests.contansts import *


class HttpMockHandler(BaseHTTPRequestHandler):
    @staticmethod
    def get_port():
        socket_obj = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
        socket_obj.bind((host, 0))
        address, port = socket_obj.getsockname()
        socket_obj.close()
        return port

    def do_GET(self):
        if re.search(re.compile(r'_complete'), self.path):
            self.send_response(requests.codes.ok)
            self.send_header(content_type,type_parm)
            self.end_headers()
            self.wfile.write(content)
            return
        elif re.search(re.compile(r'_none'), self.path):
            self.send_response(requests.codes.not_found)
            self.send_header(content_type, type_parm)
            self.end_headers()
            self.wfile.write(b'')
            return

    @staticmethod
    def mocked_server(port):
        server=Thread(target=HTTPServer((host, port), HttpMockHandler).serve_forever)
        server.setDaemon(True)
        server.start()
        pass
    pass
