import random
import gps
import uuid
import netpacket
import device
import time
from collections import defaultdict

class BaseStation(device.Device):
    def __init__(self, id, gps_coords, base_tx_dist, device_ids):
        super(BaseStation, self).__init__(id, gps_coords, base_tx_dist)

        self._captured_packets = []
        self._device_ids = set(device_ids)
        self._bad_devices = defaultdict(int)
        self._pending_identify = None
        self._network_is_complete = False
        self._identify_acks = set()


    def update(self):
        for packet in self.queued_packets():
            self._captured_packets.append(packet)

        self.forward_packets()


    def display_packet_stats(self):
        print "***************************************************************"
        print "            Base Station Statistics - %d" % time.time()
        
        for packet in self._captured_packets:
            print packet.__class__.__name__, packet.msg()
            if packet.msg().startswith("ack "):
                self._identify_acks.add(packet.msg().split()[1])

        if self._pending_identify != None:
            print "\nDevices not yet responding to identify request %s" % self._pending_identify
            diff = self._device_ids.difference(self._identify_acks)
            intersect = self._device_ids.intersection(self._identify_acks)
            
            if len(diff) > 0:
                for _id in diff:
                    self._bad_devices[_id] += 1
                    age = self._bad_devices[_id]
                    print "%s: ticks since id requested = %d" % (_id, self._bad_devices[_id]), 
                    if age > 10:
                        print "LIKELY DISCONNECTED!"
                    else:
                        print ""
            else:
                print "All devices responded to identify request %s" % self._pending_identify
                self._network_is_complete = True
                self._pending_identify = None

        print "***************************************************************"


    def request_identify(self):
        packet = netpacket.CommandPacket("identify", "global")
        self._pending_identify = packet.id()
        self.forward_packet(packet)
