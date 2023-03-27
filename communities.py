#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 11:18:22 2023

@author: tcicchini
"""

import graph_tool.all as gt
import os

PATH = ''
NET_FILE = ''
NEW_NET_FILE = NET_FILE.replace('.gml', '_COMUNIDADES.gml')

g = gt.load_graph(os.path.join(PATH,
                               NET_FILE
                               )
                  )
state = gt.minimize_blockmodel_dl(g)
community_vertex_p = state.get_blocks()
g.vertex_properties['comunidadDC'] = community_vertex_p
g.save(os.path.join(PATH,
                    NEW_NET_FILE)
       ) 
