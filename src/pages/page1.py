import streamlit as st
import pandas as pd
from st_pages import hide_pages
import numpy as np

import streamlit as st
import streamlit.components.v1 as components
import string
import random
import globals
import warnings
from collections import Counter

# Ignorar las advertencias
warnings.filterwarnings("ignore")
import pandas as pd
from scipy.stats import pearsonr

from start import initialize


df_items,df_full,df_pref,df_logusers,df_users=initialize()


#Carrusel para mostrar las recomendaciones 

def carrusel(recomendaciones):

    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

    imageUrls = recomendaciones
    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

    if selectedImageUrl is not None:
        st.image(selectedImageUrl)

#Cargo dataframe de las imagenes 

PATH = r'/home/das432hz/sistemas_recomendacion_movies/datos/Ficheros_y_datasets'
database_images=pd.read_csv("/home/das432hz/sistemas_recomendacion_movies/src/MovieGenre.csv",encoding='latin-1')
genre_names = [
    'movie_id','unknown', 'Action', 'Adventure', 'Animation', 'Children\'s',
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir',
    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller',
    'War', 'Western', 'movie_name']


left_column, right_column = st.columns(2)


#Función de la recomendación basada en contenido 
def basado_contenido(df_full,df_items,df_pref):
    movies=[]
    for elements in range(len(df_pref)): 
        elements=elements+1
        movies_todelete=df_full[df_full['users']==elements]['movie_id'].to_list()
        movies_torecomend = df_items[~df_items['movie_id'].isin(movies_todelete)]
        best_genders_names=list(pd.DataFrame(df_pref.iloc[(elements-1),:].sort_values(ascending=False)).index)[0:5]
        best_genders_values=list(df_pref.iloc[(elements-1),:].sort_values(ascending=False))[0:5]
        best_genders = {best_genders_names[i]: best_genders_values[i] for i in range(len(best_genders_names))}
        for key,value in best_genders.items():
            movies_torecomend[str(key)]=movies_torecomend.loc[:,str(key)]*value
        data_drop=['movie_id', 'movie_name']
        movies_torecomend['Ratio'] = movies_torecomend.drop(data_drop, axis=1).sum(axis=1)
        movies_torecomend=movies_torecomend.sort_values(by='Ratio',ascending=False)
        movies_torecomend_names=list(movies_torecomend.loc[:,'movie_name'])[0:5]
        movies.append(movies_torecomend_names)

    return movies

#Funciones de la recomendación colaborativa 

generos_lista =[ 'Action', 'Adventure', 'Animation', "Children's", 'Comedy',
       'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
       'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War',
       'Western']
df_pref=df_pref[generos_lista]
def top_10_correlations(movie_a, df):
    correlations = {}
    for idx, row in df.iterrows():
        movie_b = row.tolist()
        correlation, _ = pearsonr(movie_a.to_list(), movie_b)
        correlations[idx] = abs(correlation)

    top_10 = sorted(correlations.items(), key=lambda x: x[1], reverse=True)[:40]
    
    return top_10


def movies_user(id_b,df,movie_a):
    df_user = df[df['users']==id_b]
    df_user = df_user[df_user["rating"]>4]

    print(df_user.tail(5))
    print(movie_a)

    df_user['sum'] = (df_user*movie_a).sum(axis=1)
    df_user = df_user.sort_values('sum',ascending=False)
    movie_user_list = df_user["movie_name"].values.tolist()

    
    return movie_user_list[:10]


def elementos_mas_comunes(lista):
    contador = Counter(lista)
    elementos_ordenados = contador.most_common()
    return elementos_ordenados




def recomendacion_coolaborativo(movie_a):

    top_correlations = top_10_correlations(movie_a, df_pref)
    # print("Top 10 correlations with movie_a:")
    # for idx, correlation in top_correlations:
    #     print(f"Movie {idx}: {correlation}")
    movie_recomendation = []
    for i in range(39):
        movie_recomendation.extend(movies_user(top_correlations[i+1][0], df_full,movie_a))
    # Obtener los elementos más comunes
    elementos_comunes = elementos_mas_comunes(movie_recomendation)
    # Imprimir los elementos más comunes en orden ascendente
    # print("Elementos más comunes en la lista:")
    # for elemento, frecuencia in sorted(elementos_comunes, key=lambda x: x[1],reverse=True):
    #     print(f"{elemento}: {frecuencia} veces")
    elmentos_ordenados =  sorted(elementos_comunes, key=lambda x: x[1],reverse=True)
    recomendacion = [i[0] for i in elmentos_ordenados] 
    return recomendacion



#Definicion de la recomendación demografica 
label_dem = []
for i in range(len(df_users)):
    #infantes
    row = df_users.iloc[i]
    if row['age'] < 13:
        label_dem.append(1)
    #adolescentes
    if (row['age'] < 21) and (row['age']>=13):
        if row['gender'] == 'M':
            label_dem.append(2)
        else:
            label_dem.append(3)
    #adultos
    if row["age"]>=21:
        if row['ocuppation'] in ['technician', 'programmer', 'engineer', 'scientist']:
            label_dem.append(4)
        elif row['ocuppation'] in ['writer', 'artist', 'entertainment']:
            label_dem.append(5)
        elif row['ocuppation'] in ['executive', 'administrator','lawyer', 'marketing', 'salesman']:
            label_dem.append(6)
        elif row['ocuppation'] in ['student', 'educator','librarian']:
            label_dem.append(7)
        elif row['ocuppation'] in ['doctor','healthcare']:
            label_dem.append(8)
        elif row['ocuppation'] in ['homemaker', 'retired', 'none']:
            label_dem.append(9)
        else:
            label_dem.append(10)

df_users["label_demografico"] = label_dem

#crear vector de preferencias
df_pref_dem = pd.DataFrame([])
df_full_dem = pd.merge(df_full, df_users, on='users')
df_pref_dem[generos_lista] = df_full_dem[generos_lista].mul(df_full_dem['rating'], axis= 0 )
df_pref_dem['label_demografico']  = df_full_dem["label_demografico"]
df_pref_dem = df_pref_dem.groupby('label_demografico').mean()
df_group_movie = df_full.groupby("movie_id")[generos_lista].mean()


def recomendacion_demografica(vector_pref_infantil,df_group_movie):
    df_group_movie['suma'] = (df_group_movie*vector_pref_infantil).sum(axis=1)
    df_group_movie = df_group_movie.sort_values('suma',ascending=False)
    df_recomendacion = pd.merge(df_group_movie, df_full_dem[['movie_name','movie_id']].drop_duplicates(), on='movie_id')
    return df_recomendacion["movie_name"].values.tolist()

#Funciones método hibrido 

def repeated_elements(arr):
    counter = Counter(arr)
    max_count = max(counter.values())
    most_common_elements = [elem for elem, count in counter.items() if count == max_count]
    return most_common_elements, max_count


#Definición de lo que se mostrará en pantalla 

def colaborativo_method():
    movie_a = df_pref.iloc[globals.user]
    recomendacion_col = recomendacion_coolaborativo(movie_a)
    recomendacion_col=recomendacion_col[:5]
    print(recomendacion_col)
    link=[]
    for elementos in recomendacion_col:
        try:
            print(elementos)
            link.append(str(database_images[database_images['Title']==str(elementos)]['Poster'].iloc[0]))
        except: 
            link.append("https://qph.cf2.quoracdn.net/main-qimg-fd839aed3acf60248a0d77e02b017248-lq")
    
    right_column.button('Press me!')
    carrusel(link)

def contenido_method():
    movies = basado_contenido(df_full, df_items, df_pref)
    link=[]
    for elementos in range(len(movies[globals.user])):
        try: 
            link.append(str(database_images[database_images['Title']==movies[int(globals.user)][elementos]]['Poster'].iloc[0]))
        except: 
            link.append("https://qph.cf2.quoracdn.net/main-qimg-fd839aed3acf60248a0d77e02b017248-lq")

    right_column.write(str(movies[int(globals.user)]))
    right_column.button('Press me!')
    right_column.write(str(link))
    carrusel(link)


def demografico_method():
    vector_pref_infantil = df_full_dem.iloc[globals.user]
    movies=recomendacion_demografica(vector_pref_infantil,df_group_movie)
    movies=movies[:5]
    link=[]
    for elementos in movies:
        try:
            print(elementos)
            link.append(str(database_images[database_images['Title']==str(elementos)]['Poster'].iloc[0]))
        except: 
            link.append("https://qph.cf2.quoracdn.net/main-qimg-fd839aed3acf60248a0d77e02b017248-lq")
    
    right_column.button('Press me!')
    carrusel(link)

def hybrid_method():

    movie_a = df_pref.iloc[globals.user]
    recomendacion_col = recomendacion_coolaborativo(movie_a)
    recomendacion_col=recomendacion_col[0:50]
    
    vector_pref_infantil = df_full_dem.iloc[globals.user]
    movies=recomendacion_demografica(vector_pref_infantil,df_group_movie)
    movies=movies[0:50]

    total_movies = recomendacion_col + movies
    most_repeated=repeated_elements(total_movies)
    print(most_repeated[0])
    link=[]
    for elementos in most_repeated[0]:
        try:
            print(elementos)
            link.append(str(database_images[database_images['Title']==str(elementos)]['Poster'].iloc[0]))
        except: 
            link.append("https://qph.cf2.quoracdn.net/main-qimg-fd839aed3acf60248a0d77e02b017248-lq")
    
    carrusel(link)




def main():
    # Definir los métodos de recomendación disponibles
    metodos_recomendacion = {
        "Colaborativo": colaborativo_method,
        "Contenido": contenido_method,
        "Demográfico": demografico_method,
        "Hibrido": hybrid_method
    }

    with st.sidebar:
        # Crear un selectbox para que el usuario seleccione el método de recomendación
        metodo_seleccionado = st.selectbox("Selecciona un método de recomendación", list(metodos_recomendacion.keys()))

        # Mostrar la descripción del método seleccionado
        st.write("Descripción del método seleccionado:", metodos_recomendacion[metodo_seleccionado].__doc__)

        # Dependiendo del método seleccionado, puedes mostrar parámetros adicionales o iniciar el proceso de recomendación
        if st.button("Iniciar recomendación"):
            # Aquí puedes agregar la lógica para iniciar el proceso de recomendación con el método seleccionado
            st.write("Recomendación iniciada con el método:", metodo_seleccionado)

    # Call the selected method to display its specific parameters and logic
    metodos_recomendacion[metodo_seleccionado]()


if __name__ == "__main__":
    main()