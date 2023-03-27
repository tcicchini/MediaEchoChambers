#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:12:54 2023

@author: tcicchini
"""

import pandas as pd
import graph_tool.all as gt
from latent_ideology.latent_ideology_class import latent_ideology as li
import os

PATH = ''
NET_FILE = ''
BIPARTITE_FILE = ''
MEDIA_COL = ''
USER_COL = ''
SCORE_FILE = ''
LABEL_TAG = ''

d = pd.read_csv(os.path.join(PATH,
                             BIPARTITE_FILE
                             )
                )

d['m_count'] = d.groupby(MEDIA_COL)[MEDIA_COL].transform('count')
d.sort_values('m_count', inplace = True, ascending = False)


g = gt.load_graph(os.path.join(PATH, NET_FILE))

li_matrix = li(d) # En principio, no restringimos la base de datos
df1, df2 = li_matrix.apply_method(n = 2,
                                  targets = USER_COL,
                                  sources = MEDIA_COL
                                  )
df1.to_csv(os.paht.join(PATH, 'targets_' + SCORE_FILE), index = False)
df2.to_csv(os.paht.join(PATH, 'sources_' + SCORE_FILE), index = False)

# restringimos la base de datos a los usuarios presentes en la red
d = d[d[USER_COL] == [label for label in g.vp[LABEL_TAG]]]
li_matrix = li(d) # En principio, no restringimos la base de datos
df1, df2 = li_matrix.apply_method(n = 2,
                                  targets = USER_COL,
                                  sources = MEDIA_COL
                                  )
df1.to_csv(os.paht.join(PATH, 'RESTRINGIDAtargets_' + SCORE_FILE), index = False)
df2.to_csv(os.paht.join(PATH, 'RESTRINGIDAsources_' + SCORE_FILE), index = False)

dict_users_score = df1.set_index('targets').to_dict()
users_score = g.new_vertex_property('double') # Seteo un nuevo atributo float
for v in g.iter_vertices():
    users_score[v] = dict_users_score[v]
g.vertex_property['users_score'] = users_score
g.save(os.path.join(PATH, NET_FILE))