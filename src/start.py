import streamlit as st
import pandas as pd
from st_pages import hide_pages
import numpy as np

import streamlit as st
import streamlit.components.v1 as components
import string
import random
import globals
import os 
import warnings
from collections import Counter
warnings.filterwarnings("ignore")
import pandas as pd
from scipy.stats import pearsonr


def initialize(): 


    PATH = r'/home/das432hz/sistemas_recomendacion_movies/datos/Ficheros_y_datasets'

    database_images=pd.read_csv("/home/das432hz/sistemas_recomendacion_movies/src/MovieGenre.csv",encoding='latin-1')
    genre_names = [
        'movie_id','unknown', 'Action', 'Adventure', 'Animation', 'Children\'s',
        'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
        'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
        'War', 'Western', 'movie_name']
    df_items = pd.read_csv(PATH+'/items.txt',sep="\t", encoding='latin-1',header=None, names= genre_names)
    df_genre = pd.read_csv(PATH+'/genre.txt',sep="\t", encoding='latin-1',header=None)
    df_calif=pd.read_csv(PATH+r'/u1_base.txt',sep="\t", encoding='latin-1',header=None,names=["users","movie_id","rating"])
    df_users = pd.read_csv(PATH+r'/users.txt',sep="\t", encoding='latin-1',header=None, names=["users","age","gender","ocuppation"])
    df_concat = df_users.merge(df_calif, left_on='users', right_on='users')
    df_full = df_concat.merge(df_items, left_on='movie_id', right_on='movie_id')
    df_logusers = pd.read_csv('/home/das432hz/sistemas_recomendacion_movies/src/data_loging.csv',sep=",")
    
    path_df_pref="/home/das432hz/sistemas_recomendacion_movies/src/df_pref.csv"

    if os.path.isfile(path_df_pref):
        df_pref = pd.read_csv(path_df_pref,sep=",")
    else:
        df_pref = pd.DataFrame([])
        generos_lista = ['unknown','Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
            'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

        df_pref[generos_lista] = df_full[generos_lista].mul(df_full['rating'], axis= 0 )
        df_pref['users']  = df_full["users"]
        df_pref = df_pref.groupby('users').mean()


    return df_items,df_full,df_pref,df_logusers,df_users






