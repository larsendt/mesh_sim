#!/usr/bin/env python

import device
import time
import netmesh
import base_station
import uuid

n_devs = 30
tx_dist = 30
area_size = 100

devs = map(lambda x: device.make_random_device(area_size, tx_dist), range(n_devs))
dev_ids = map(lambda d: d.id(), devs)
bs = base_station.BaseStation(uuid.uuid4().hex, (0, 0), tx_dist, dev_ids)

mesh = netmesh.NetMesh(area_size, bs)

for dev in devs:
    mesh.add_device(dev)

mesh.propagate_connections()

mesh.plot()

bs.request_identify()

while True:
    mesh.update()
    time.sleep(1.0)
