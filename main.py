from fastapi import FastAPI, status, HTTPException

from database.database import SessionLocal
from typing import List

from models import models
from serializers.serializers import BlogSerializer
from utils.response import data_deleted, id_not_found

app = FastAPI()
db = SessionLocal()


@app.get('/posts/', response_model=List[BlogSerializer], status_code=status.HTTP_200_OK)
def blog_posts():
    posts = db.query(models.Blog).all()
    return posts


@app.post('/create-post/', response_model=BlogSerializer, status_code=status.HTTP_201_CREATED)
def create_blog_post(blog: BlogSerializer):
    new_post = models.Blog(
        title=blog.title,
        is_publish=blog.is_publish,
        content=blog.content
    )

    db.add(new_post)
    db.commit()
    return new_post


@app.get('/post/{id}/', response_model=BlogSerializer, status_code=status.HTTP_200_OK)
def get_single_post(id: int):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    return post


@app.put('/update-post/{id}', response_model=BlogSerializer, status_code=status.HTTP_200_OK)
def update_post(id: int, blog: BlogSerializer):
    get_post = db.query(models.Blog).filter(models.Blog.id == id).first()
    try:
        if get_post is not None:
            get_post.title = blog.title,
            # get_post.is_publish = blog.is_publish,
            get_post.content = blog.content
            db.commit()
            return get_post
    except Exception as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ex))


@app.delete('/post-delete/{id}/')
def post_delete(id: int):
    post = db.query(models.Blog).filter(models.Blog.id == id).first()
    if post is not None:
        db.delete(post)
        db.commit()
        return data_deleted()
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=id_not_found)
