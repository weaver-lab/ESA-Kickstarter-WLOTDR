# -*- coding: utf-8 -*-
""""Main.py for LoPy device"""

import meshnode
import lib.lorasockets as ls
import mesh_config
config = mesh_config.config

node=meshnode.Mesh()
node.node_launch(config['id'])
