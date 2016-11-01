import Message
import Status

__author__ = 'JuniorJPDJ'

handlers = {}


def reg(packet_name):
    def decor(handler):
        handlers[handler] = packet_name
        return handler
    return decor


@reg('GetProvidersPacket')
def get_providers_packet_handler(packet):
    return {'providers': map(lambda x: x.get_info(), packet.client.clients.server.providers.list_providers())}


@reg('LogInProviderPacket')
def login_provider_packet_handler(packet):
    if packet.provider_name not in packet.client.clients.server.providers.list_provider_names():
        return {'provider_id': -1}  # unknown provider name
    provider = packet.client.clients.server.providers.get_provider(packet.provider_name)(packet.client)
    if provider.auth:
        if packet.username is None or packet.password is None:
            return {'provider_id': -2}  # no auth data sent to provider requiring auth
        if not provider.login(packet.username, packet.password):
            return {'provider_id': -3}  # can't login (maybe wrong username or password)
    else:
        if not provider.login():
            return {'provider_id': -3}  # can't login
    return {'provider_id': packet.client.add_provider(provider), 'contact': provider.contact.get_info()}


@reg('LogoutProviderPacket')
def logout_provider_packet_handler(packet):
    provider = packet.client.get_provider(packet.provider_id)
    ret = provider.logout()
    packet.client.remove_provider(provider)
    return {'success': ret}


@reg('GetContactsPacket')
def get_contacts_packet_handler(packet):
    provider = packet.client.get_provider(packet.provider_id)
    if provider.update_contacts():
        return {'contacts': map(lambda x: x.get_info(), provider.contacts)}
    else:
        return {'contacts': -1}


@reg('GetChatHistoryPacket')
def get_chat_history_packet_handler(packet):
    contact = packet.client.get_provider(packet.provider_id).get_contact(packet.contact_id)
    if packet.msgs_amount is None:
        messages_amount = 15
    else:
        messages_amount = packet.msgs_amount
    return {'history': map(lambda x: x.get_info(), contact.get_chat_history(messages_amount))}


@reg('SendMessagePacket')
def send_message_packet_handler(packet):
    contact = packet.client.get_provider(packet.provider_id).get_contact(packet.contact_id)
    msg = Message.Message(contact, packet.text, contact.provider.contact)
    if contact.send_message(msg):
        return {'success': True, 'msg': msg.get_info()}
    return {'success': False}


@reg('EditMessagePacket')
def edit_message_packet_handler(packet):
    return {'success': packet.client.get_provider(packet.provider_id).get_contact(packet.contact_id).get_message(
        packet.msg_id).edit(packet.new_text)}


@reg('DeleteMessagePacket')
def delete_message_packet_handler(packet):
    contact = packet.client.get_provider(packet.provider_id).get_contact(packet.contact_id)
    return {'success': contact.delete_message(contact.get_message(packet.msg_id))}


@reg('ReadMessagePacket')
def read_message_packet_handler(packet):
    return {'success': packet.client.get_provider(packet.provider_id).get_contact(packet.contact_id).get_message(
        packet.msg_id).make_read()}


@reg('ChangeStatusPacket')
def change_status_packet_handler(packet):
    return {'success': packet.client.get_provider(packet.provider_id).send_status(
        Status.Status(packet.status_id, packet.desc))}


def register_handlers(server):
    for h in handlers:
        server.clients.ipackets.register_handler(handlers[h], h)
