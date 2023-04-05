#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 16:40:43 2023

@author: tcicchini
"""

import pandas as pd
import graph_tool.all as gt
import os
import numpy as np

PATH = ''
NET_FILE = ''
BIP_FILE = ''
SAVE_FILE = ''


def matrizUsuariosMediosCorrected(d, user_col = 'usr_id', media_col = 'medio', tweet_id = 'component'):
    matriz_usuario_medio = d.groupby([user_col,media_col])[tweet_id].count().unstack().fillna(0)
    medio_frec = matriz_usuario_medio.apply(sum, axis = 0)
    medio_frec = medio_frec / medio_frec.sum()
    medio_frec = - medio_frec.apply(np.log2)
    for c in matriz_usuario_medio.columns:
        matriz_usuario_medio[c] = matriz_usuario_medio[c] * medio_frec[c]
    matriz_usuario_medio = matriz_usuario_medio.apply(lambda x : x / x.sum(), axis = 1)
    matriz_usuario_medio = matriz_usuario_medio.reset_index()
    return matriz_usuario_medio

g = gt.load_graph(os.path.join(PATH, NET_FILE))
d = pd.read_csv(os.path.join(PATH, BIP_FILE))

# buscamos las componentes de la red
comp, hist = gt.label_components(g, )
dic_Labelnodo_componente = pd.Series({l : c for l, c in zip(g.vp['label'], comp)}).reset_index().rename({'index' : 'usr_id',
                                                                                                         0 : 'component'},
                                                                                                        axis = 1)

d.usr_id = d.usr_id.astype(str)
d = dic_Labelnodo_componente.merge(d, on = 'usr_id')
matriz_usuario_medio = matrizUsuariosMediosCorrected(d)
matriz_usuario_medio = matriz_usuario_medio.merge(d[['usr_id', 'component']].drop_duplicates(), on = 'usr_id').set_index('usr_id')

matriz_usuario_medio.to_csv(os.path.join(PATH, SAVE_FILE))