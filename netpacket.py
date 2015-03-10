
class NetPacket(object):
    def __init__(self, id, msg):
        self._id = id
        self._msg = msg

    def id(self):
        return self._id

    def msg(self):
        return self._msg

    def __repr__(self):
        return "Packet<%s>" % self._id

    def __str__(self):
        return "Packet<%s>" % self._id


_PACKET_ID = 0

def make_packet():
    global _PACKET_ID
    p = NetPacket(_PACKET_ID, "packet %s" % _PACKET_ID)
    _PACKET_ID += 1
    return p
