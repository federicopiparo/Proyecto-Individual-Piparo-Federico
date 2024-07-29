from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import os
import uvicorn

app = FastAPI()

# Configuración de templates y static files
templates = Jinja2Templates(directory="web/templates")
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Cargar los DataFrames globalmente
df = pd.read_parquet('Transformaciones/transformados.parquet')
df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')
df['Nombre_Director'] = df['Nombre_Director'].fillna('')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/cantidad_filmaciones_mes")
def cantidad_filmaciones_mes(parameter: str):
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
    
    mes_numero = meses.get(parameter.lower())
    if mes_numero is None:
        raise HTTPException(status_code=400, detail=f"Mes '{parameter}' no es válido. Por favor ingresa un mes válido en español.")
    
    peliculas_mes = df[df['release_date'].dt.month == mes_numero]
    cantidad = len(peliculas_mes)
    
    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en el mes de {parameter}"}


@app.get("/api/cantidad_filmaciones_dia")
def cantidad_filmaciones_dia(parameter: str):
    dias = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }
    
    dia_numero = dias.get(parameter.lower())
    if dia_numero is None:
        return {"message": f"Día '{parameter}' no es válido. Por favor ingresa un día válido en español."}
    
    peliculas_dia = df[df['release_date'].dt.dayofweek == dia_numero]
    cantidad = len(peliculas_dia)
    
    return {"message": f"{cantidad} cantidad de películas fueron estrenadas en los días {parameter}"}

@app.get("/api/score_titulo")
def score_titulo(parameter: str):
    pelicula = df[df['title'].str.contains(parameter, case=False, na=False)]
    if pelicula.empty:
        return {"message": f"No se encontró la película con el título '{parameter}'"}
    
    titulo = pelicula.iloc[0]['title']
    estreno = pelicula.iloc[0]['release_date'].year
    score = pelicula.iloc[0]['vote_average']
    
    return {"message": f"La película {titulo} fue estrenada en el año {estreno} con un score/popularidad de {score}"}

@app.get("/api/votos_titulo")
def votos_titulo(parameter: str):
    pelicula = df[df['title'].str.contains(parameter, case=False, na=False)]
    if pelicula.empty:
        return {"message": f"No se encontró la película con el título '{parameter}'"}
    
    titulo = pelicula.iloc[0]['title']
    estreno = pelicula.iloc[0]['release_date'].year
    votos = pelicula.iloc[0]['vote_count']
    promedio = pelicula.iloc[0]['vote_average']
    
    if votos < 2000:
        return {"message": f"La película {titulo} no cumple con el mínimo de 2000 valoraciones. Tiene {votos} valoraciones."}
    
    return {"message": f"La película {titulo} fue estrenada en el año {estreno}. La misma cuenta con un total de {votos} valoraciones, con un promedio de {promedio}"}

@app.get("/api/get_actor")
def get_actor(parameter):
    # Filtrar las filas donde el actor está en alguna de las columnas 'nombre_'
    actor_df = df[df.filter(like='nombre_').apply(lambda x: parameter in x.values, axis=1)]
    
    # Contar la cantidad de películas en las que ha participado
    cantidad_peliculas = actor_df.shape[0]
    if cantidad_peliculas == 0:
        return {"message": f"No se encontró al actor '{parameter}'"}
    
    # Calcular el éxito total (suma de los retornos)
    éxito_total = actor_df['return'].sum()
    
    # Calcular el promedio de retorno
    promedio_retorno = actor_df['return'].mean()
    
    return {
        'nombre_actor': parameter,
        'éxito_total': éxito_total,
        'cantidad_películas': cantidad_peliculas,
        'promedio_retorno': promedio_retorno
    }

@app.get("/api/get_director")
def get_director(parameter):

    director_df = df[df['Nombre_Director'].apply(lambda x: parameter in x)]
    
    lista_peliculas = director_df[['title', 'release_year', 'return', 'budget', 'revenue']].to_dict(orient='records')
     
    # Calcular el éxito total (suma de los retornos)
    éxito_total = director_df['return'].sum()
    
    return {
        'nombre_dicrector': parameter,
        'éxito_total': éxito_total,
        'lista_peliculas': lista_peliculas

    }
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
