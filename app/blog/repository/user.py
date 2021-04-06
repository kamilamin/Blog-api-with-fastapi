from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from blog import schemas, models
from blog.hashing import Hash

def createUser(request: schemas.Blog, db: Session):
    new_user = models.User(username=request.username, email=request.email, password=Hash.passwordHash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def userList(id: int, db: Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user
