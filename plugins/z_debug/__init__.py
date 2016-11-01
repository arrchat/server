__author__ = 'JuniorJPDJ'


class DebugPlugin(object):
    name = 'debug'

    def __init__(self, server):
        self.server = server
        self.logger = server.plugin_loader.get_logger(self.name)
        self.logger.debug('Debug plugin starting')

__plugin__ = DebugPlugin
