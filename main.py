from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

# @app is path operation decortor / Base path and get function
@app.get('/blogs') 
def index(limit: int, published: bool): #Path operation function
    if published:
        return {'data': f"{limit} published blogs from the db."}
    else:
        return {'data': f"{limit} blogs from the db."}

# About path and get function 
@app.get('/blogs/{id}') #Path operation function
def fetchBlogsById(id):
    return {"data": id}

@app.get('/blogs/comments/{id}')
def getBlogComments(id):
    return {"data": {"1","2"}}

class blogModel(BaseModel):
    title: str
    body: str
    published: Optional[bool]

@app.post('/createBlogs')
def create_blog(request: blogModel):
    return {'data': f"Blog is create with title as {request.title}"}
