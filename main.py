#!/usr/bin/env python

import device
from matplotlib import pyplot

devices = []
n_devs = 30
tx_dist = 30
area_size = 100

for i in range(n_devs):
    devices.append(device.make_random_device(area_size, tx_dist))

xcoords = map(lambda d: d.gps_coords()[0], devices)
ycoords = map(lambda d: d.gps_coords()[1], devices)

neighbor_edges = []

for device in devices:
    neighbor_candidates = sorted(devices, key=lambda d: device.distance_to(d))
    neighbor_candidates = filter(lambda d: d.id() != device.id(), neighbor_candidates)
    neighbor_candidates = filter(lambda d: device.is_reachable_from(d), neighbor_candidates)

    for nc in neighbor_candidates:
        start = nc.gps_coords()
        stop = device.gps_coords()
        neighbor_edges.append(((start[0], stop[0]), (start[1], stop[1])))

pyplot.plot(xcoords, ycoords, marker="o", ls="")

for x, y in neighbor_edges:
    pyplot.plot(x, y, color="r")

pyplot.xlim((-10, area_size+10))
pyplot.ylim((-10, area_size+10))
pyplot.show()

