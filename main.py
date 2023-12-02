from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import time
from jwt_manager import create_token

#crear una instancia de FastAPI (aplicacion)
app = FastAPI()

app.title = "Mi aplicacion de peliculas"
app.version = "0.0.1"

class User(BaseModel):
    email:str
    password:str

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
        response = JSONResponse(content={"message": "Movie not found"}, status_code=404)
    return response

@app.get("/movies/", tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category:str = Query(min_length=3, max_length=12)): #Query es un parametro de consulta que se le pasa a la url 
    movie = list(filter(lambda movie: movie['category'] == category, movies))
    if len(movie) > 0:
        response = JSONResponse(content=movie, status_code=200)
    else:
        response = JSONResponse(content={"message": "Category not found"}, status_code=404)
    return response

@app.post("/movies/", tags=['movies'], response_model=dict,status_code=201)
def create_movie(movie: Movie):
    movies.append(movie)
    return JSONResponse(content={"message": "Movie created successfully"},
                        status_code=201)

@app.put("/movies/{id}", tags=['movies'], response_model=dict)
def update_movie(movie: Movie):
    for movie in movies:
        if movie['id'] == id:
            movie['title'] = movie.title
            movie['overview'] = movie.overview
            movie['year'] = movie.year
            movie['rating'] = movie.rating
            movie['category'] = movie.category
    
    return JSONResponse (content={"message": "Movie updated successfully"},
                        status_code=200)

@app.delete("/movies/{id}", tags=['movies'], response_model=dict)
def delete_movie(id: int):
    for movie in movies:
        if movie['id'] == id:
            movies.remove(movie)
    
    return JSONResponse(content={"message": "Movie deleted successfully"},
                        status_code=200)

@app.post("/login",tags=['auth'],response_model=dict,status_code=200)
def login(user:User):
    if user.email == "admin@mail.com" and user.password == "admin":
        token = create_token(data=user.model_dump())
        result = JSONResponse(content={"token":token},
                              status_code=200)
    else:
        result = JSONResponse(content={"message":"Invalid credentials"},
                              status_code=401)
    
    return result


#le escribimos a la consola: uvicorn main:app --asi inicial el servidor



