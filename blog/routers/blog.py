from typing import List
from fastapi import APIRouter, Depends, status, Response, HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

# List of Blogs Route
@router.get('/listOfBlogs', response_model=List[schemas.FetchBlog], tags=["Blog Management"])
def listOfBlogs(db: Session=Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

# Create new blog Route
@router.post('/createBlog', status_code=status.HTTP_201_CREATED, tags=["Blog Management"])
def create_blog(request: schemas.Blog, db: Session=Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

# Get blog by ID Route
@router.get('/blogDetails/{id}', status_code=200, response_model=schemas.FetchBlog, tags=["Blog Management"])
def getBlogById(id, response: Response, db: Session=Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Blog with id {id} is not available")
    return blog

# Delete Blog by ID Route
@router.delete('/blogDelete/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=["Blog Management"])
def deleteBlogById(id, response: Response, db: Session=Depends(database.get_db)):
    deleteBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not deleteBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    deleteBlog.delete(synchronize_session=False)
    db.commit()
    return "Blog Deleted successfully"

# Update Blog by ID Route
@router.put('/updateBlog/{id}', status_code=status.HTTP_202_ACCEPTED, tags=["Blog Management"])
def updateBlogById(id, request:schemas.Blog, db: Session=Depends(database.get_db)):
    updateBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not updateBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    updateBlog.update({'title':request.title, 'body':request.body})
    db.commit()
    return 'Updated Blog'
