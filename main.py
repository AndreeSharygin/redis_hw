# pip install fastapi[all] redis
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from typing import List
import json
from workers import write_log
from redis_client import redis_client

# Создаем экземпляр FastAPI
app = FastAPI()



# Модель данных
class Article(BaseModel):
    id: int
    title: str
    content: str

# Хранилище статей
articles: List[Article] = []

# Эндпоинт для получения статей
@app.get("/articles", response_model=List[Article])
async def get_articles():
    # Проверка кеша
    cached_articles = redis_client.get("articles_cache")

    if cached_articles:
        return json.loads(cached_articles)

    # Если кеша нет, возвращаем статьи и пишем в кеш
    articles_response = articles
    redis_client.setex("articles_cache", 60, json.dumps([article.dict() for article in articles_response]))
    return articles_response


# Эндпоинт для добавления статьи
@app.post("/articles", response_model=Article)
async def create_article(article: Article, background_tasks: BackgroundTasks):
    articles.append(article)
    # Очищаем кеш
    redis_client.delete("articles_cache")

    # Запускаем фоновую задачу
    background_tasks.add_task(write_log, article.id)

    return article


# Эндпоинт для очистки кеша
@app.delete("/cache")
async def clear_cache():
    redis_client.delete("articles_cache")
    return {"message": "Cache cleared"}

