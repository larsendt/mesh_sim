#!/usr/bin/env python

import device
import time
import netmesh

n_devs = 30
tx_dist = 30
area_size = 100

mesh = netmesh.NetMesh(area_size)

for i in range(n_devs):
    mesh.add_device(device.make_random_device(area_size, tx_dist))

mesh.propagate_connections()

mesh.plot()
