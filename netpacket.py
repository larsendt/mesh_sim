import copy
import uuid

class NetPacket(object):
    def __init__(self, msg):
        self._id = uuid.uuid4().hex
        self._msg = msg
        self._hop_count = 0

    def clone(self):
        return copy.copy(self)

    def id(self):
        return self._id

    def msg(self):
        return self._msg
    
    def hop_count(self):
        return self._hop_count

    def inc_hops(self):
        self._hop_count += 1

    def __repr__(self):
        return "%s<%s, hops=%d>" % (self.__class__.__name__, self._id, self._hop_count)

    def __str__(self):
        return "%s<%s, hops=%d>" % (self.__class__.__name__, self._id, self._hop_count)

    def __hash__(self):
        return self._id

    def __eq__(self, other):
        return self._id == other.id()


class CommandPacket(NetPacket):
    def __init__(self, msg, destination):
        super(CommandPacket, self).__init__(msg)
        self._destination = destination

    def destination(self):
        return self._destination


if __name__ == "__main__":
    p = CommandPacket("identify")
    print p.clone()
