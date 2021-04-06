from sqlalchemy.orm import Session
from blog import models, schemas
from fastapi import status, HTTPException

def fetchAllBlogs(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs

def createBlog(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

def fetchBlogById(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not available")
    return blog

def deleteBlog(id: int, db: Session):
    deleteBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not deleteBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    deleteBlog.delete(synchronize_session=False)
    db.commit()
    return "Blog Deleted successfully"

def updateBlog(id: int, request: schemas.Blog, db: Session):
    updateBlog = db.query(models.Blog).filter(models.Blog.id == id)
    if not updateBlog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} not found")
    updateBlog.update({'title': request.title, 'body': request.body})
    db.commit()
    return 'Updated Blog'
