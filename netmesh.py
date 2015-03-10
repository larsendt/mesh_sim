from matplotlib import pyplot

class NetMesh(object):
    def __init__(self, area_size):
        self._devices = []
        self._neighbor_edges = []
        self._area_size = area_size

    def devices(self):
        return self._devices

    def add_device(self, device):
        self._devices.append(device)

    def propagate_connections(self):
        self._neighbor_edges = []

        for device in self._devices:
            neighbor_candidates = sorted(self._devices, key=lambda d: device.distance_to(d))
            neighbor_candidates = filter(lambda d: d.id() != device.id(), neighbor_candidates)
            neighbor_candidates = filter(lambda d: device.is_reachable_from(d), neighbor_candidates)

            for nc in neighbor_candidates:
                device.add_neighbor(nc)
                start = nc.gps_coords()
                stop = device.gps_coords()
                self._neighbor_edges.append(((start[0], stop[0]), (start[1], stop[1])))

    def plot(self):
        xcoords = map(lambda d: d.gps_coords()[0], self._devices)
        ycoords = map(lambda d: d.gps_coords()[1], self._devices)
        pyplot.plot(xcoords, ycoords, marker="o", ls="")

        for x, y in self._neighbor_edges:
            pyplot.plot(x, y, color="r")

        pyplot.xlim((-10, self._area_size+10))
        pyplot.ylim((-10, self._area_size+10))
        pyplot.show()

