from tornado import websocket
from multiprocessing.pool import ThreadPool
from tornado import ioloop

_workers = ThreadPool(20)

__author__ = 'JuniorJPDJ'


class WebSocketHandler(websocket.WebSocketHandler):
    def __init__(self, app, request, clients, **kwargs):
        websocket.WebSocketHandler.__init__(self, app, request, **kwargs)
        self.clients = clients
        self.client = None

    def check_origin(self, origin):
        return True

    def open(self):
        self.client = self.clients.new_client(self)

    def on_message(self, message):
        _workers.apply_async(self.client.process_incoming_data, (message,))

    def sync_write_message(self, message):
        ioloop.IOLoop.instance().add_callback(lambda: self.write_message(message, binary=True))

    def on_connection_close(self):
        self.clients.remove_client(self.client)
        self.client = None
