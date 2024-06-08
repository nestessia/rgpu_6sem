# Лабораторная работа 9. Проект на FastAPI. <b>API для сохранения фильмов</b>
Автор: Крючкова Анастасия Сергеевна ИВТ 1.2
## Описание проекта
Данная API позволяет сохранить в базу данных информацию о фильмах, указавыя название, жанр и дату выпуска
## Стек
FastAPI | docker-compose | sqlalchemy | postgres
## Развернуть проект
Находясь в директории /lr9, выполните команду (Предварительно включив впн, так как будет скачиваться образ postgres):
```
docker-compose up --build
```

## Примеры запросов
<b>POST</b>
```
curl -X POST "http://localhost:80/movies/" -H "Content-Type: application/json" -d '{
    "title": "Titanic",
    "genre": "Drama",
    "year": 1997
}'

```
<b>GET</b> Получить список всех фильмов
```
curl -X GET "http://127.0.0.1:80/movies/"

```
<b>DELETE</b> Удалить фильм по id
```
curl -X DELETE "http://127.0.0.1:80/movies/1"

```
<b>PATCH</b> Частично изменить объект
```
curl -X PATCH "http://127.0.0.1:80/movies/1" -H "Content-Type: application/json" -d '{
    "title": "Titanic (Updated)"
}'

```
<b>PUT</b> Полность изменить объект
```
curl -X PUT "http://127.0.0.1:80/movies/1" -H "Content-Type: application/json" -d '{
    "title": "Epic movie/romantic drama/disaster movie",
    "genre": "Drama",
    "year": 1997
}'

```
