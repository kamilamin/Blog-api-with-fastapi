from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models, OAuth2
from sqlalchemy.orm import Session
from ..repository import blog

router = APIRouter(
    prefix="/blogs",
    tags=["Blog Management"]
)

# List of Blogs Route

@router.get('/listOfBlogs', response_model=List[schemas.FetchBlog])
def listOfBlogs(db: Session = Depends(database.get_db), getCurrentUser: schemas.User=Depends(OAuth2.getCurrentUser)):
    return blog.fetchAllBlogs(db)

# Create new blog Route

@router.post('/createBlog', status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db), getCurrentUser: schemas.User=Depends(OAuth2.getCurrentUser)):
    return blog.createBlog(request, db)

# Get blog by ID Route

@router.get('/blogDetails/{id}', status_code=200, response_model=schemas.FetchBlog)
def getBlogById(id, response: Response, db: Session = Depends(database.get_db), getCurrentUser: schemas.User=Depends(OAuth2.getCurrentUser)):
    return blog.fetchBlogById(id, db)

# Delete Blog by ID Route

@router.delete('/blogDelete/{id}', status_code=status.HTTP_204_NO_CONTENT)
def deleteBlogById(id, response: Response, db: Session = Depends(database.get_db), getCurrentUser: schemas.User=Depends(OAuth2.getCurrentUser)):
    return blog.deleteBlog(id, db)

# Update Blog by ID Route

@router.put('/updateBlog/{id}', status_code=status.HTTP_202_ACCEPTED)
def updateBlogById(id, request: schemas.Blog, db: Session = Depends(database.get_db), getCurrentUser: schemas.User=Depends(OAuth2.getCurrentUser)):
    return blog.updateBlog(id, request, db)
