__author__ = 'JuniorJPDJ'


class DisabledPlugin(object):
    name = 'debug'

    def __init__(self, server):
        self.server = server
        self.logger = server.plugin_loader.get_logger(self.name)
        self.logger.info('Disabled plugin started (should not happen until you delete "!" from start of folder name)')

__plugin__ = DisabledPlugin
