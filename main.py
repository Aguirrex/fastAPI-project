from fastapi import FastAPI, Body, Path
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import time

#crear una instancia de FastAPI (aplicacion)
app = FastAPI()

app.title = "Mi aplicacion de peliculas"
app.version = "0.0.1"

class Movie(BaseModel):
    id : Optional[int] = None
    title : str = Field(min_length=1, max_length=50)
    overview : str = Field(min_length=20, max_length=300)
    year : int = Field(ge=0, le=time.localtime().tm_year)
    rating : float = Field(ge=0.0, le=10.0)
    category : str = Field(min_length=3, max_length=12)

movies = [
    {
        'id': 1,
        'title': 'pene',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 2,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Acción'    
    },
    {
        'id': 3,
        'title': 'Cars',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': 2009,
        'rating': 7.8,
        'category': 'Comedia'
    }
]

@app.get("/") #punto a donde nos vamos a conectar: "/" es la raiz
def message():
    return HTMLResponse(content="<h1>Maduro mamaguevooooo lider !!!!</h1>") #le vamos a pasar un contenido html 

@app.get("/movies", tags=['movies'], response_model = List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)

@app.get("/movies/{id}", tags=['movies'], response_model = Movie, status_code=200 )
def get_movie(id:int = Path(ge=1, le=2000)):
    movie = list(filter(lambda movie: movie['id'] == id, movies))
    if len(movie) > 0:
        response = JSONResponse(content=movie, status_code=200)
    else:
        response = JSONResponse(content=("message: Movie not found"), status_code=404)
    return response

@app.get("/movies/", tags=['movies'])
def get_movies_by_category(category:str):
    movie = list(filter(lambda movie: movie['category'] == category, movies))
    return movie

@app.post("/movies/", tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movie = {
        'id': id,
        'title': title,
        'overview': overview,
        'year': year,
        'rating': rating,
        'category': category
    }
    movies.append(movie)
    return movies

@app.put("/movies/{id}", tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = title
            movie['overview'] = overview
            movie['year'] = year
            movie['rating'] = rating
            movie['category'] = category
    
    return movies

@app.delete("/movies/{id}", tags=['movies'])
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return movies


#le escribimos a la consola: uvicorn main:app --asi inicial el servidor



