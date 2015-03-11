import random
import gps
import uuid
import netpacket

class Device(object):
    def __init__(self, id, gps_coords, base_tx_dist):
        self._id = id
        self._coords = gps_coords
        self._neighbors = set()
        self._forward_queue = []

        # ring buffer of size 50, old packets fall off the end
        self._seen_packets = [None] * 50
        self._sp_idx = 0

        # allow tx dist to vary by +- 10%
        rnd = base_tx_dist / 10
        self._tx_dist = base_tx_dist + random.uniform(-rnd, rnd)

    def id(self):
        return self._id

    def tx_dist(self):
        return self._tx_dist

    def gps_coords(self):
        return self._coords

    def distance_to(self, device):
        return gps.distance(self._coords, device.gps_coords())

    def queued_packets(self):
        return self._forward_queue
    
    def known_packets(self):
        return self._seen_packets

    def is_reachable_from(self, device):
        dist = gps.distance(self._coords, device.gps_coords())

        if self._tx_dist > dist and device.tx_dist() > dist:
            return True
        else:
            return False

    def add_neighbor(self, neighbor):
        self._neighbors.add(neighbor)

    def process_command_packet(self, packet):
        if packet.msg() == "identify":
            ack_str = "ack %s %s" % (self._id, packet.id())
            new_packet = netpacket.NetPacket(ack_str)
            print "ack packet:", new_packet
            self.forward_packet(new_packet)

    def recv_packet(self, packet):
        if packet.id() in self._seen_packets:
            return True 

        if isinstance(packet, netpacket.CommandPacket):
            if packet.destination() == "global":
                self.process_command_packet(packet)
                self.forward_packet(packet)
            elif packet.destination() == self._id:
                self.process_command_packet(packet)
            else:
                self.forward_packet(packet)
        else:
            self.forward_packet(packet)

    def forward_packet(self, packet):
        new_packet = packet.clone()
        new_packet.inc_hops()
        self._forward_queue.append(new_packet) 
        self._seen_packets[self._sp_idx] = new_packet.id()
        self._sp_idx = (self._sp_idx + 1) % len(self._seen_packets)
        return True

    def forward_packets(self):
        while len(self._forward_queue) > 0:
            packet = self._forward_queue.pop(0)
            ok = True
            for n in self._neighbors:
                if not n.recv_packet(packet):
                    ok = False

            if not ok:
                self._forward_queue.append(packet)

    def update(self):
        self.forward_packets()

    def __str__(self):
        return "Device<x=%.1f y=%.1f tx=%.1f>" % (self._coords[0], self._coords[1], self._tx_dist)

    def __repr__(self):
        return "Device<x=%.1f y=%.1f tx=%.1f>" % (self._coords[0], self._coords[1], self._tx_dist)
        

def make_random_device(area_size, tx_dist):
    x = random.uniform(0, area_size)
    y = random.uniform(0, area_size)
    id = uuid.uuid4().hex
    return Device(id, (x, y), tx_dist)

