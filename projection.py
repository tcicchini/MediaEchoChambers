#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 18:27:14 2023

@author: tcicchini
"""

import pandas as pd
import bicm
import networkx as nx
import os


PATH = ''
FILE = ''
US_COL = ''
NEWS_COL = ''
FILE_NEWS = ''
FILE_US = ''


d = pd.read_csv(os.path.join(PATH, FILE))
id_us = pd.DataFrame([{'i_us' : i,
                       US_COL : us} for i, us in enumerate(d[US_COL].unique())])
id_noticia = pd.DataFrame([{'i_not' : i,
                            NEWS_COL : us} for i, us in enumerate(d[NEWS_COL].unique())]
                          )

# Lista de adyacencia para buscar la proyección de noticias
edgelist_row = sorted((d.groupby([US_COL,
                           NEWS_COL]
                          ).medio.count().reset_index()
                )[[US_COL, NEWS_COL]].merge(id_us,
                                                on = US_COL
                                                ).merge(id_noticia,
                                                        on = NEWS_COL)[['i_not', 'i_us']].values.tolist())
# Lista de adyacencia para buscar proyección de usuarios
edgelist_col = sorted((d.groupby([US_COL,
                           NEWS_COL]
                          ).medio.count().reset_index()
                )[[US_COL, NEWS_COL]].merge(id_us,
                                                on = US_COL
                                                ).merge(id_noticia,
                                                        on = NEWS_COL)[['i_us', 'i_not']].values.tolist())

# Los vamos a usar para nombrar a los nodos en las redes
id_noticia = id_noticia.set_index('i_not').to_dict()[NEWS_COL]
id_us = id_us.set_index('i_us').to_dict()[US_COL]

# Proyección de noticias
alpha = 0.05
B = bicm.BipartiteGraph()
B.set_edgelist(edgelist_row)
B.get_bicm_matrix()
B.get_bicm_fitnesses()
B.compute_projection(alpha = alpha, threads_num = 1)
p1 = B.get_rows_projection(
                           method='poison',
                           fmt = 'edgelist',
                           alpha = alpha
                           )
g = nx.Graph()
g.add_edges_from([(id_noticia[i], id_noticia[j]) for i, j in p1])
nx.write_gml(g,
              os.path.join(PATH, FILE_NEWS)
              )
# Proyección de usuarios
alpha = 0.05
B = bicm.BipartiteGraph()
B.set_edgelist(edgelist_col)
B.get_bicm_matrix()
B.get_bicm_fitnesses()
B.compute_projection(alpha = alpha, threads_num = 1)
p1 = B.get_rows_projection(
                           method='poison',
                           fmt = 'edgelist',
                           alpha = alpha
                           )
g = nx.Graph()
g.add_edges_from([(id_us[i], id_us[j]) for i, j in p1])
nx.write_gml(g,
              os.path.join(PATH, FILE_US)
              )
