from Status import Status
from copy import copy

__author__ = 'JuniorJPDJ'


class BaseProvider(object):
    auth = False
    visible_name = ''
    name = ''
    logo = 'http://svg2stl.com/api/preview/567908aa9f2e1c6c3904b58c'
    color = 'ce4847'
    features = ()

    def __init__(self, client):
        self.client = client
        self._contacts = []
        self.send_status(Status())
        self.update_contacts()

    @classmethod
    def get_info(cls):
        return {'visibleName': cls.visible_name, 'name': cls.name, 'logo': cls.logo, 'auth': cls.auth, 'features': cls.features, 'color': int(cls.color, 16)}

    @property
    def id(self):
        return self.client.get_provider_id(self)

    @property
    def contacts(self):
        '''returns list with Contact() objects'''
        return copy(self._contacts)

    def update_contacts(self):
        '''downloads contacts from provider's server'''
        return True

    def send_status(self, status):
        self.status = status
        return True

    def send_message(self, msg):
        '''sends message'''
        return True

    def login(self):
        return True

    def logout(self):
        return True

    def get_contact(self, id):
        for i in self._contacts:
            if i.id == id:
                return i
        raise ValueError('There is no contact with that id')

__provider__ = BaseProvider  # main class
