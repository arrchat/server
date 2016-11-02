from BaseProvider import BaseProvider
from Message import Message
from Status import Status
from Contact import Contact

__author__ = 'JuniorJPDJ'


class DummyProviderPlugin(object):
    name = 'dummy_provider'

    def __init__(self, server):
        self.server = server
        self.logger = server.plugin_loader.get_logger(self.name)
        self.logger.info('Dummy plugin starting')
        server.providers.register_provider(DummyProvider)
        self.logger.debug('Registered dummy provider')
        server.providers.register_provider(DummyAuthProvider)
        self.logger.debug('Registered dummy_auth provider')
        self.logger.info('Dummy plugin started')


class DummyProvider(BaseProvider):
    visible_name = 'Dummy'
    desc = 'Test provider'
    name = 'dummy'

    def __init__(self, client):
        self.contact = DummyContact(self, 'Me', 'me', "http://i.imgur.com/EwU0u0B.jpg", Status(0, 'That\'s you!'))
        BaseProvider.__init__(self, client)

    def send_message(self, message):
        if message.contact.id == 'echo':
            message.contact.receive_message(Message(message.contact, message.text, message.contact))
            return True
        else:
            return False

    def update_contacts(self):
        self._contacts = [DummyContact(self, 'Echo', 'echo', 'http://beanies.vn/wp-content/uploads/2014/05/belgian_waffle-1513470.jpg',
                                       Status(0, 'I will repeat your every message <3'))]
        return True


class DummyAuthProvider(DummyProvider):
    auth = True
    visible_name = 'Dummy auth'
    desc = 'Test provider with auth'
    name = 'dummy_auth'

    def login(self, username, password):
        return username == 'username' and password == 'password'


class DummyContact(Contact):
    def update_chat_history(self):
        self._history = [Message(self, 'chuj kurwa!', self.provider.contact), Message(self, 'zebys wiedzial kurwa!', self), Message(self, 'tak bylo', self)]
        return True


__plugin__ = DummyProviderPlugin  # main class
