from tornado import web, ioloop
from os import getenv
import Client
import WebSocketHandler
from PacketHandlers import register_handlers
from PluginLoader import PluginLoader
from ProvidersContainer import ProvidersContainer
import logging

__author__ = 'JuniorJPDJ'


class Server(object):
    def __init__(self):
        logger = logging.getLogger('WebChatSrv')
        logger.propagate = False
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(name)s | %(message)s', '%H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        self.logger = logger

        self.clients = Client.Clients(self)
        self.providers = ProvidersContainer()
        self.plugin_loader = PluginLoader(server=self)
        register_handlers(self)

        self.app = web.Application([
            (r'/ws', WebSocketHandler.WebSocketHandler, {'clients': self.clients}),
            (r'/(.*)', web.StaticFileHandler, {'path': 'www-root/', 'default_filename': 'index.html'})
        ])

    def start(self, ip, port, **app_kwargs):
        self.plugin_loader.load_plugins()
        self.app.listen(port, ip, **app_kwargs)
        ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    server = Server()
    server.start(getenv('IP', '0.0.0.0'), int(getenv('PORT', 8080)), xheaders=True)
