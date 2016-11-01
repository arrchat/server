from collections import defaultdict

__author__ = 'JuniorJPDJ'


class IncomingPackets(object):
    class Packet(object):
        def __init__(self, parent, client, raw):
            self.query_id = raw.pop('query_id')
            self.parent = parent
            self.raw = raw
            self.client = client
            self.init()

        def init(self):
            pass

        def build_response(self):
            response = {}
            for i in self.parent._handlers[self.__class__]:
                handler_response = i(self)
                assert isinstance(handler_response, dict), 'bad handler response'
                response.update(handler_response)
            response['response_id'] = self.query_id
            return response

    class ConfirmationPacket(Packet):
        def build_response(self):
            pass

    class ResponsePacket(Packet):
        def __init__(self, parent, client, raw):
            self.parent = parent
            self.response_id = raw.pop('response_id')
            self.raw = raw
            self.client = client

        def build_response(self):
            pass

    class GetProvidersPacket(Packet):
        pass

    class LogInProviderPacket(Packet):
        def init(self):
            if 'provider_name' not in self.raw:
                raise ValueError('Invalid LogInProvider packet from client (doesn\'t include provider_name)')
            self.provider_name = self.raw['provider_name']
            if 'username' in self.raw and 'password' in self.raw:
                self.username, self.password = self.raw['username'], self.raw['password']
            else:
                self.username, self.password = None, None

    class LogoutProviderPacket(Packet):
        def init(self):
            if 'provider_id' not in self.raw:
                raise ValueError('Invalid LogoutProvider packet from client (doesn\'t include provider_id)')
            self.provider_id = self.raw['provider_id']


    class GetContactsPacket(Packet):
        def init(self):
            if 'provider_id' not in self.raw:
                raise ValueError('Invalid GetContacts packet from client (doesn\'t include provider_id)')
            self.provider_id = self.raw['provider_id']

    class GetChatHistoryPacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'contact_id' in self.raw):
                raise ValueError('Invalid GetChatHistory packet from client '
                                 '(doesn\'t include provider_id or contact_id)')
            self.provider_id = self.raw['provider_id']
            self.contact_id = self.raw['contact_id']
            if 'msgs_amount' in self.raw:
                self.msgs_amount = self.raw['msgs_amount']
            else:
                self.msgs_amount = None

    class SendMessagePacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'contact_id' in self.raw and 'text' in self.raw):
                raise ValueError('Invalid SendMessage packet from client '
                                 '(doesn\'t include provider_id, contact_id or text)')
            self.provider_id = self.raw['provider_id']
            self.contact_id = self.raw['contact_id']
            self.text = self.raw['text']

    class EditMessagePacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'contact_id' in self.raw and
                    'msg_id' in self.raw and 'new_text' in self.raw):
                raise ValueError('Invalid EditMessage packet from client '
                                 '(doesn\'t include provider_id, contact_id, msg_id or new_text)')
            self.provider_id = self.raw['provider_id']
            self.contact_id = self.raw['contact_id']
            self.msg_id = self.raw['msg_id']
            self.new_text = self.raw['new_text']

    class DeleteMessagePacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'contact_id' in self.raw and 'msg_id' in self.raw):
                raise ValueError('Invalid DeleteMessage packet from client '
                                 '(doesn\'t include provider_id, contact_id or msg_id)')
            self.provider_id = self.raw['provider_id']
            self.contact_id = self.raw['contact_id']
            self.msg_id = self.raw['msg_id']

    class ReadMessagePacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'contact_id' in self.raw and 'msg_id' in self.raw):
                raise ValueError('Invalid DeleteMessage packet from client '
                                 '(doesn\'t include provider_id, contact_id or msg_id)')
            self.provider_id = self.raw['provider_id']
            self.contact_id = self.raw['contact_id']
            self.msg_id = self.raw['msg_id']

    class ChangeStatusPacket(Packet):
        def init(self):
            if not ('provider_id' in self.raw and 'status_id' in self.raw and 'desc' in self.raw):
                raise ValueError('Invalid ChangeStatus packet from client '
                                 '(doesn\'t include provider_id, status_id or desc)')
            self.provider_id = self.raw['provider_id']
            self.status_id = self.raw['status_id']
            self.desc = self.raw['desc']

    _packet_types = (ConfirmationPacket, ResponsePacket, GetProvidersPacket, LogInProviderPacket, LogoutProviderPacket,
                     GetContactsPacket, GetChatHistoryPacket, SendMessagePacket, EditMessagePacket,
                     DeleteMessagePacket, ReadMessagePacket, ChangeStatusPacket)

    def __init__(self):
        self._handlers = defaultdict(lambda: [])

    def register_handler(self, packet_type, handler):
        assert callable(handler)
        packet_type = getattr(self, packet_type)
        assert packet_type in self._packet_types
        self._handlers[packet_type].append(handler)

    def make_packet(self, client, raw):
        if not (isinstance(raw, dict) and ('response_id' in raw or ('packet_type' in raw and 'query_id' in raw and isinstance(raw['packet_type'], int) and 0 <= raw['packet_type'] < len(self._packet_types)))):
            raise ValueError('Invalid packet from client')

        return self._packet_types[raw.pop('packet_type')](self, client, raw)


class OutgoingPacket(object):
    class Packet(object):
        data = {}

        def build_data(self):
            data = self.data
            data.update({'packet_type': OutgoingPacket._packet_types.index(type(self))})
            return data

    class ConfirmationPacket(Packet):
        def __init__(self, query_id):
            self.data = {'query_id': query_id}

    class ResponsePacket(Packet):
        def __init__(self, data):
            self.data = data

    class ServerInfoPacket(Packet):
        def __init__(self, protocol_version):
            self.data = {'protocol_version': protocol_version}

    class NewContactPacket(Packet):
        def __init__(self, contact):
            self.data = contact.get_info()
            self.data.update({'provider_id': contact.provider.id})

    class NewMessagePacket(Packet):
        def __init__(self, message):
            self.data = message.get_info()
            self.data.update({'provider_id': message.contact.provider.id})

    class MessageDeletedPacket(Packet):
        def __init__(self, message):
            self.data = {'provider_id': message.contact.provider.id, 'contact_id': message.contact.id,
                         'msg_id': message.id}

    class MessageEditedPacket(Packet):
        def __init__(self, message):
            self.data = {'provider_id': message.contact.provider.id, 'contact_id': message.contact.id,
                         'msg_id': message.id, 'new_text': message.text}

    class MessageReadPacket(Packet):
        def __init__(self, message):
            self.data = {'provider_id': message.contact.provider.id, 'contact_id': message.contact.id,
                         'msg_id': message.id}

    class ContactStatusChangedPacket(Packet):
        def __init__(self, contact):
            self.data = {'provider_id': contact.provider.id, 'contact_id': contact.id,
                         'status_id': contact.status.id, 'desc': contact.status.desc}

    class MemberlistChangedPacket(Packet):
        def __init__(self, contact):
            self.data = {'memberlist': map(lambda mem: mem.get_info(), contact.memberlist)}

    _packet_types = (ConfirmationPacket, ResponsePacket, ServerInfoPacket, NewContactPacket, NewMessagePacket,
                     MessageDeletedPacket, MessageEditedPacket, MessageReadPacket, ContactStatusChangedPacket,
                     MemberlistChangedPacket)
