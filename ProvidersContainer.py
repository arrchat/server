__author__ = 'JuniorJPDJ'


class ProvidersContainer(object):
    def __init__(self):
        self._providers = {}

    def register_provider(self, provider):
        if provider.name not in self._providers:
            self._providers[provider.name] = provider

    def list_provider_names(self):
        return list(self._providers.keys())

    def list_providers(self):
        return list(self._providers.values())

    def get_provider(self, name):
        if name in self._providers:
            return self._providers[name]
        else:
            return False
