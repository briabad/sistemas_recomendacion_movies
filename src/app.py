import pandas as pd

# Fetch the neccesary python modules
import streamlit as st
import pickle
import pandas as pd
import requests
import numpy  as np 

PATH = r'C:\Users\brian\OneDrive\Escritorio\PROJECTS\UPV\sistemas_recomendacion\data'
genre_names = [
    'movie_id','unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 
    'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 
    'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 
    'War', 'Western', 'movie_name']
df_items = pd.read_csv(PATH+'\items.txt',sep="	", encoding='latin-1',header=None, names= genre_names)
df_genre = pd.read_csv(PATH+'\genre.txt',sep="	", encoding='latin-1',header=None)
df_calif = pd.read_csv(PATH+r'\u1_base.txt',sep="	", encoding='latin-1',header=None,names=["users","movie_id","rating"])
df_users = pd.read_csv(PATH+r'\users.txt',sep="	", encoding='latin-1',header=None, names=["users","age","gender","ocuppation"])


df_concat = df_users.merge(df_calif, left_on='users', right_on='users')
df_concat= df_concat.merge(df_items, left_on='movie_id', right_on='movie_id')

# Agregar una imagen en la parte superior
st.image(r"C:\Users\brian\OneDrive\Escritorio\PROJECTS\UPV\sistemas_recomendacion\data\Netflix_logo.svg.png", use_column_width=True)
nombre_usuario_valido = "abad"
contrasena_valida = "abad"

sesion_iniciada = False
# Agregar una pantalla de inicio de sesión
st.title("Inicio de sesión")
boton =0 


def funcion_prueba():


    # Definir los métodos de recomendación disponibles
    metodos_recomendacion = {
        "Colaborativo": "Descripción breve del Método 1.",
        "Contendio": "Descripción breve del Método 2.",
        "Datos demograficos": "Descripción breve del Método 3."
    }

    st.text_input("Your name", key="name")

    # You can access the value at any point with:

    if 'abad' == st.session_state.name:
        ("hola briant moreno abad")

    with st.sidebar:
        # Crear un selectbox para que el usuario seleccione el método de recomendación
        metodo_seleccionado = st.selectbox("Selecciona un método de recomendación", list(metodos_recomendacion.keys()))

        # Mostrar la descripción del método seleccionado
        st.write("Descripción del método seleccionado:", metodos_recomendacion[metodo_seleccionado])

        # Dependiendo del método seleccionado, puedes mostrar parámetros adicionales o iniciar el proceso de recomendación
        if metodo_seleccionado == "Colaborativo":
            # Mostrar parámetros específicos para el Método 1
            st.write("Parámetros para el Método 1")


        elif metodo_seleccionado == "Método 2":
            # Mostrar parámetros específicos para el Método 2
            st.write("Parámetros para el Método 2")
            # Aquí puedes agregar campos para que el usuario ingrese parámetros específicos

        elif metodo_seleccionado == "Método 3":
            # Mostrar parámetros específicos para el Método 3
            st.write("Parámetros para el Método 3")
            # Aquí puedes agregar campos para que el usuario ingrese parámetros específicos

        # Una vez que el usuario haya seleccionado un método y configurado los parámetros (si es necesario),
        # puedes agregar un botón para iniciar el proceso de recomendación
        if st.button("Iniciar recomendación"):
            boton = 1 
            # Aquí puedes agregar la lógica para iniciar el proceso de recomendación con el método seleccionado
            st.write("Recomendación iniciada con el método:", metodo_seleccionado)

    # Dependiendo del método seleccionado, puedes mostrar parámetros adicionales o iniciar el proceso de recomendación
    if boton==1:
        # Mostrar parámetros específicos para el Método 1
        st.write("Parámetros para el Método 1")
        st.write(df_concat)

    left_column, right_column = st.columns(2)
    # You can use a column just like st.sidebar:
    right_column.button('Press me!')
    x = st.slider('x')

    if st.checkbox('Show dataframe'):
        chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])
        

    option = st.selectbox(
        'Which number do you like best?',
        df_concat['users'])


nombre_usuario = st.text_input("Nombre de usuario")
contrasena = st.text_input("Contraseña", type="password")



if nombre_usuario == nombre_usuario_valido and contrasena == contrasena_valida:
    # placeholder.empty()
    sesion_iniciada = True
    if sesion_iniciada:
        funcion_prueba()
        
    else:
        st.error("Nombre de usuario o contraseña incorrectos. Por favor, inténtalo de nuevo.")




