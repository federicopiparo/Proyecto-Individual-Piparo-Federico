from fastapi import FastAPI
import pandas as pd
import calendar
import numpy as np

app = FastAPI()

# Cargar el DataFrame globalmente
df = pd.read_csv('C:\\Users\\fede\\Desktop\\LABs 1\\Proyecto individual - Federico Piparo\Proyecto\\transformados.csv', low_memory=False)

# Convertir la columna 'release_date' a datetime
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

@app.get("/")
def read_root():
    return {"message": "Welcome to the Movie API"}

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    meses = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }
    
    mes_numero = meses.get(mes.lower())
    if mes_numero is None:
        return {"message": f"Mes '{mes}' no es válido. Por favor ingresa un mes válido en español."}
    
    peliculas_mes = df[df['release_date'].dt.month == mes_numero]
    cantidad = len(peliculas_mes)
    
    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    dias = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }
    
    dia_numero = dias.get(dia.lower())
    if dia_numero is None:
        return {"message": f"Día '{dia}' no es válido. Por favor ingresa un día válido en español."}
    
    peliculas_dia = df[df['release_date'].dt.dayofweek == dia_numero]
    cantidad = len(peliculas_dia)
    
    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    pelicula = df[df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"message": f"No se encontró la película con el título '{titulo_de_la_filmacion}'"}
    
    titulo = pelicula.iloc[0]['title']
    estreno = pelicula.iloc[0]['release_date'].year
    score = pelicula.iloc[0]['vote_average']
    
    return {"message": f"La película {titulo} fue estrenada en el año {estreno} con un score/popularidad de {score}"}

@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = df[df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)]
    if pelicula.empty:
        return {"message": f"No se encontró la película con el título '{titulo_de_la_filmacion}'"}
    
    titulo = pelicula.iloc[0]['title']
    estreno = pelicula.iloc[0]['release_date'].year
    votos = pelicula.iloc[0]['vote_count']
    promedio = pelicula.iloc[0]['vote_average']
    
    if votos < 2000:
        return {"message": f"La película {titulo} no cumple con el mínimo de 2000 valoraciones. Tiene {votos} valoraciones."}
    
    return {"message": f"La película {titulo} fue estrenada en el año {estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"}

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    df['cast'] = df['cast'].apply(ast.literal_eval)
    actor_films = df[df['cast'].apply(lambda x: any(d['name'].lower() == nombre_actor.lower() for d in x))]
    
    if actor_films.empty:
        return {"message": f"No se encontró al actor '{nombre_actor}' en el dataset"}
    
    total_revenue = actor_films['revenue'].sum()
    num_movies = len(actor_films)
    avg_revenue = total_revenue / num_movies
    
    return {"message": f"El actor {nombre_actor} ha participado de {num_movies} cantidad de filmaciones, el mismo ha conseguido un retorno de {total_revenue} con un promedio de {avg_revenue} por filmación"}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str):
    df['crew'] = df['crew'].apply(ast.literal_eval)
    director_films = df[df['crew'].apply(lambda x: any(d['job'].lower() == 'director' and d['name'].lower() == nombre_director.lower() for d in x))]
    
    if director_films.empty:
        return {"message": f"No se encontró al director '{nombre_director}' en el dataset"}
    
    movies_info = []
    for idx, film in director_films.iterrows():
        movie_info = {
            "title": film['title'],
            "release_date": film['release_date'],
            "revenue": film['revenue'],
            "budget": film['budget'],
            "profit": film['revenue'] - film['budget']
        }
        movies_info.append(movie_info)
    
    return {"director": nombre_director, "movies": movies_info}
