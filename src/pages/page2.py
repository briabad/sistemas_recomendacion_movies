import streamlit as st
from st_pages import hide_pages
from time import sleep
import streamlit as st
from streamlit_star_rating import st_star_rating
import random
import globals
import pandas as pd 
from start import initialize

df_items,df_full,df_pref,df_logusers,df_users=initialize()

movies = ['Action', 'Adventure', 'Animation', "Children's", 
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 
    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
    'War', 'Western', 'movie_name']
ratings = {}


def registrado():
    st.session_state["registrado"] = False
    hide_pages(["page1"])
    st.success("Registered")
    sleep(0.5)

if not st.session_state.get("registrado", False):
    hide_pages(["page1"])
    username = st.text_input("Nombre de Usuario")
    email = st.text_input("Correo Electrónico")
    password = st.text_input("Contraseña", type="password")
    ocupations= ['technician','programmer','engineer','writer','entertainment','librarian','homemaker','artist','executive','administrator','lawyer','educator','student','scientist','healthcare','doctor']
    ocupation = st.selectbox('Seleccione una opción:', ocupations)
    gender= st.text_input("Gender")
    age=st.text_input("Age")

    for movie in movies:
        st.subheader(movie)
        rating = st_star_rating(label="", maxValue=5, defaultValue=0, key=movie)
        ratings[movie] = rating

    if st.button('Registrar usuario'):
        usuarios_df=df_logusers 
        df_pref=df_pref
        new_user = {'Id':len(usuarios_df)+1,'User': username, 'Password': password}
        new_user_info = {'users':len(df_users)+1,'age': age, 'gender': gender, 'ocuppation': ocupation}
        nuevos_usuarios_demo=pd.concat([df_users, pd.DataFrame([new_user_info])], ignore_index=True)
        print(nuevos_usuarios_demo.tail(10))
        nuevo_usuarios_df= pd.concat([usuarios_df, pd.DataFrame([new_user])], ignore_index=True)
        nuevos_ratings=pd.concat([df_pref, pd.DataFrame([ratings])], ignore_index=True) 
        globals.df_logusers=nuevo_usuarios_df
        nuevo_usuarios_df.to_csv("data_loging.csv",index=False)
        nuevos_ratings.to_csv('df_pref.csv',index=False)
        nuevos_usuarios_demo.to_csv('/home/das432hz/sistemas_recomendacion_movies/datos/Ficheros_y_datasets/users.txt',sep='\t', index=False, header=False)
        st.session_state["registrado"] = True
        st.success("Logged in!")
        hide_pages(["page1"])
        sleep(0.5)
        st.switch_page("pages/page2.py")
else:
    st.write("Registered!")
    hide_pages(["page1"])
    st.button("Hecho", on_click=registrado)


print(ratings)
