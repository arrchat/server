from Packets import OutgoingPacket

__author__ = 'JuniorJPDJ'


class Contact(object):
    def __init__(self, provider, name, id, avatar, status, visible=True):
        self.provider, self.name, self.id = provider, name, id
        self.avatar, self.status, self.visible, self._history = avatar, status, visible, []

    def get_info(self):
        return {'name': self.name, 'id': self.id,
                'avatar': self.avatar, 'status': self.status.id, 'desc': self.status.desc}

    def get_chat_history(self, messages_amount):
        if not self._history:
            self.update_chat_history()
        return self._history[-messages_amount:]

    def update_chat_history(self):
        return True

    def send_message(self, msg):
        if self.provider.send_message(msg):
            if not self._history:
                self.update_chat_history()
            self._history.append(msg)
            return True
        return False

    def receive_message(self, msg):
        if not self._history:
            self.update_chat_history()
        self._history.append(msg)
        self.provider.client.send_outgoing_packet(OutgoingPacket.NewMessagePacket(msg))

    def get_message(self, id):
        for i in self._history:
            if i.id == id:
                return i
        raise ValueError('There is no message with that id')

    def message_in_history(self, id):
        for m in self._history:
            if m.id == id:
                return True
        return False

    def edit_message(self, msg, new_text):
        return True

    def delete_message(self, msg):
        self._history.remove(msg)
        return True
