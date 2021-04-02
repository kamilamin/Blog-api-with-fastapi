from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models, hashing
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/createBlog', status_code=status.HTTP_201_CREATED, tags=["Blog Management"])
def create_blog(request: schemas.Blog, db: Session=Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/listOfBlogs', response_model=List[schemas.FetchBlog], tags=["Blog Management"])
def listOfBlogs(db: Session=Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blogDetails/{id}', status_code=200, response_model=schemas.FetchBlog, tags=["Blog Management"])
def getBlogById(id, response: Response, db: Session=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} is not available")
    return blog

@app.delete('/blogDelete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blog Management"])
def deleteBlogById(id, response: Response, db: Session=Depends(get_db)):
    deleteBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not deleteBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    deleteBlog.delete(synchronize_session=False)
    db.commit()
    return "Blog Deleted successfully"

@app.put('/updateBlog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blog Management"])
def updateBlogById(id, request:schemas.Blog, db: Session=Depends(get_db)):
    updateBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not updateBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    updateBlog.update({'title':request.title, 'body':request.body})
    db.commit()
    return 'Updated Blog'

@app.post('/user', response_model=schemas.ShowUser, tags=["User Management"])
def create_user(request: schemas.User, db: Session=Depends(get_db)):
    new_user = models.User(username=request.username, email=request.email, password=Hash.passwordHash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/listOfUsers/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["User Management"])
def get_user(id: int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user
