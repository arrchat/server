import utils
from datetime import datetime
import Contact

__author__ = 'JuniorJPDJ'


class Message(object):
    def __init__(self, contact, text, author=None, time=None, read=False, id=None):
        # system messages have author=None
        self.id, self.text, self.author, self.contact = utils.random_string(10) if not id else id, text, author, contact
        self.time, self.read = time if time is not None else datetime.now(), read

    def edit(self, new_text):
        if self.contact.edit_message(self, new_text):
            self.text = new_text
            return True
        return False

    def make_read(self):
        if self.read:
            return False
        else:
            self.read = True
            return True

    def get_info(self):
        return {'id': self.id, 'contact_id': self.contact.id, 'text': self.text, 'author': self.author.id if isinstance(self.author, Contact.Contact) else None, 'time': self.contact.provider.client.seconds_since_sync(self.time), 'read': self.read}
