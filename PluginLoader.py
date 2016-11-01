import os
import importlib
import logging

__author__ = 'JuniorJPDJ'


class PluginLoader(object):
    def __init__(self, plugins_dir='plugins', plugin_main='__plugin__', *plugin_args, **plugin_kwargs):
        self.plugins_dir, self.plugin_main, self._plugins = plugins_dir, plugin_main, {}
        self.plugin_args, self.plugin_kwargs = plugin_args, plugin_kwargs
        self.logger = logging.getLogger('WebChatSrv.Plugins.Loader')

    def load_plugins(self):
        self.logger.debug('Plugins loading started')
        for i in os.listdir(self.plugins_dir):
            location = os.path.join(self.plugins_dir, i)
            if i.startswith('!') or not (os.path.isdir(location) and '__init__.py' in os.listdir(location)):
                continue
            plugin = getattr(importlib.import_module('{}.{}'.format(self.plugins_dir, i)), self.plugin_main, None)
            if plugin is None:
                continue
            self.logger.debug('Loading plugin started: %s', plugin.name)
            if plugin.name not in self._plugins:
                self._plugins[plugin.name] = True
                self._plugins[plugin.name] = plugin(*self.plugin_args, **self.plugin_kwargs)
                self.logger.debug('Loading plugin finished: %s', plugin.name)
            else:
                self.logger.debug('Plugin with same name already loaded: %s', plugin.name)
        self.logger.debug('Plugins loading finished')

    @property
    def loaded_plugins(self):
        return list(self._plugins.keys())

    def is_plugin_loaded(self, name):
        return name in self._plugins

    def get_plugin(self, name):
        if name in self._plugins:
            return self._plugins[name]

    def get_logger(self, name):
        if self.get_plugin(name):
            return logging.getLogger('WebChatSrv.Plugins.Plugin.{}'.format(name))
