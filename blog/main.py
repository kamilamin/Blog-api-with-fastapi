from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/createBlog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/listOfBlogs', response_model=List[schemas.FetchBlog])
def listOfBlogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blogDetails/{id}', status_code=200, response_model=schemas.FetchBlog)
def getBlogById(id, response: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} is not available")
    return blog

@app.delete('/blogDelete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlogById(id, response: Response, db: Session=Depends(get_db)):
    deleteBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not deleteBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    deleteBlog.delete(synchronize_session=False)
    db.commit()
    return "Blog Deleted successfully"

@app.put('/updateBlog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlogById(id, request:schemas.Blog, db: Session=Depends(get_db)):
    print(request)
    updateBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not updateBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    updateBlog.update({'title':request.title, 'body':request.body})
    db.commit()
    return 'Updated Blog'

@app.post('/user')
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password=request.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
