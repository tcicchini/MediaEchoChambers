#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 10:02:24 2023

@author: tcicchini
"""
import os
import pandas as pd
import matplotlib.pylab as plt

PATH = '/home/tcicchini/Documentos/Post Tesis/'
FILE = 'usersMediaVector.csv'

d = pd.read_csv(os.path.join(PATH, FILE))

# Distribución de componentes
hasta = 5
d_comps = d.groupby('component').usr_id.count().sort_values(ascending = False).iloc[:hasta]
d_comps['resto'] = d.groupby('component').usr_id.count().sort_values(ascending = False).iloc[hasta:].sum()
fig, ax = plt.subplots(figsize = (10, 8), dpi = 200)
d_comps.plot(kind = 'bar',
             color = hasta * [(0.12156862745098039, 0.4666666666666667, 0.7058823529411765)] + ['grey'],
             ax = ax)
ax.set_xticklabels([f'Componente {i + 1}' for i in range(hasta)] + ['resto'],
                   rotation = 45)
ax.grid(linestyle = 'dashed')
ax.set_xlabel('Componentes de la red usuarios')
ax.set_ylabel('Cantidad de Usuarios')
plt.show()

# Distribución medios primeras dos componentes

medios = ['Clarin',
          'Todo Noticias',
          'La Nacion',
          'Infobae',
          'Perfil',
          'El Cronista',
          'Radio Mitre',
          'El Litoral',
          'Contexto',
          'Radio Dos',
          'Jornada',
          'TYC Sports',
          'El Dia',
          'La Izquierda Diario',
          'Ambito Financiero',
          'Minuto Uno',
          'Pagina 12',
          'El Destape']

d_medios = d.set_index('usr_id').groupby('component').mean().iloc[:2, ].T.loc[medios,:]
fig, ax = plt.subplots(figsize = (6, 10), dpi = 200)
ax.set_title('Distribución de los vectores de consumo promedio de las Camponentes más grandes')
d_medios.plot(kind = 'barh', ax = ax, stacked = True)
ax.grid(linestyle = 'dashed')
plt.show()