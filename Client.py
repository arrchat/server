import traceback
import msgpack
import WebSocketHandler
import Packets
from datetime import datetime
import logging
import json

logger = logging.getLogger('WebChatSrv.Networking')

__author__ = 'JuniorJPDJ'


class Clients(object):
    def __init__(self, server):
        self.logger = logging.getLogger('WebChatSrv.Networking.Clients')
        self._clients = []
        self._id = 0
        self.ipackets = Packets.IncomingPackets()
        self.server = server

    def __contains__(self, item):
        if isinstance(item, Clients.Client):
            return item in self._clients
        elif isinstance(item, int):
            return not self.get_client(item) is None
        else:
            return False

    def get_client(self, id):
        if not isinstance(id, int):
            raise ValueError('id is not instance of int')
        for c in self._clients:
            if c.id == id:
                return c
        return None

    def new_client(self, socket):
        if not isinstance(socket, WebSocketHandler.WebSocketHandler):
            raise ValueError('socket is not instance of WebSocketHandler')
        if socket not in self:
            cl = self.Client(self._id, socket, self)
            self._id += 1
            self._clients.append(cl)
            return cl
        else:
            raise ValueError('socket already has client')

    def remove_client(self, client):
        client.logger.info('Disconnected')
        if client in self._clients:
            self._clients.remove(client)
        else:
            raise ValueError('There is no client like that')

    class Client(object):
        # TODO: resend missing packets
        def __init__(self, id_, socket, clients):
            if not isinstance(socket, WebSocketHandler.WebSocketHandler):
                raise ValueError('socket is not instance of WebSocketHandler')
            if not isinstance(id_, int):
                raise ValueError('id is not instance of int')
            self.logger = logging.getLogger('WebChatSrv.Networking.Client.{}'.format(id_))
            self.id = id_
            self.socket = socket
            self._providers_list = []
            self._outgoing_packet_id = 0
            self._sync_time = datetime.now()
            self.logger.info('Connected ({})'.format(self.socket.request.remote_ip))
            self.send_outgoing_packet(Packets.OutgoingPacket.ServerInfoPacket(0.1))
            self.clients = clients

        def process_incoming_data(self, data):
            try:
                raw_packet = msgpack.unpackb(data)
                self.logger.debug('Incoming: %s', json.dumps(raw_packet))
                packet = self.clients.ipackets.make_packet(self, raw_packet)
                if isinstance(packet, Packets.IncomingPackets.ConfirmationPacket):
                    pass
                elif isinstance(packet, Packets.IncomingPackets.ResponsePacket):
                    self.send_outgoing_packet(Packets.OutgoingPacket.ConfirmationPacket(packet.response_id))
                else:
                    self.send_outgoing_packet(Packets.OutgoingPacket.ConfirmationPacket(packet.query_id))
                    self.send_outgoing_packet(Packets.OutgoingPacket.ResponsePacket(packet.build_response()))

            except Exception as e:
                print('{}: {}'.format(type(e).__name__, e.message))
                print(traceback.format_exc())

        def send_outgoing_packet(self, packet):
            data = packet.build_data()
            if not isinstance(packet, (Packets.OutgoingPacket.ResponsePacket, Packets.OutgoingPacket.ConfirmationPacket)):
                data.update({'query_id': self._outgoing_packet_id})
                self._outgoing_packet_id += 1
            self.logger.debug('Outgoing: %s', json.dumps(data))
            raw = msgpack.packb(data)
            self.socket.sync_write_message(raw)

        def is_provider_id(self, provider_id):
            return 0 <= provider_id < len(self._providers_list) and self._providers_list[provider_id] is not None

        def add_provider(self, provider):
            self._providers_list.append(provider)
            return self.get_provider_id(provider)

        def get_provider_id(self, provider):
            if provider not in self._providers_list:
                raise ValueError('There is no provider like that')
            return self._providers_list.index(provider)

        def get_provider(self, provider_id):
            if not self.is_provider_id(provider_id):
                raise ValueError('There is no provider with this id')
            return self._providers_list[provider_id]

        def remove_provider(self, provider):
            if provider not in self._providers_list:
                raise ValueError('There is no provider like that')
            self._providers_list[self.get_provider_id(provider)] = None

        def seconds_since_sync(self, time):
            return int((time - self._sync_time).total_seconds())
