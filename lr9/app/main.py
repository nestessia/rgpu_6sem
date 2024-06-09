from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Movie, Base
from schemas import MovieCreate, MovieUpdate, Movie as MovieSchema
from database import SessionLocal, engine

app = FastAPI()

# Создание таблиц в базе данных
try:
    Base.metadata.create_all(bind=engine)
except:
    pass

# Функция для получения соединения с базой данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Роут для создания записи о фильме
@app.post("/movies/")
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

# Роут для получения списка всех фильмов
@app.get("/movies/", response_model=list[MovieSchema])  # Исправлено на MovieSchema
def read_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies

# Роут для удаления записи о фильме
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie:
        db.delete(db_movie)
        db.commit()
        return {"message": "Movie deleted successfully"}
    raise HTTPException(status_code=404, detail="Movie not found")

# Роут для обновления записи о фильме
@app.put("/movies/{movie_id}")
def update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie:
        for var, value in vars(movie_update).items():
            if value is not None:
                setattr(db_movie, var, value)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    raise HTTPException(status_code=404, detail="Movie not found")

# Роут для частичного обновления записи о фильме
@app.patch("/movies/{movie_id}")
def partial_update_movie(movie_id: int, movie_update: MovieUpdate, db: Session = Depends(get_db)):
    db_movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if db_movie:
        for var, value in vars(movie_update).items():
            if value is not None:
                setattr(db_movie, var, value)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    raise HTTPException(status_code=404, detail="Movie not found")
