from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter()

@router.post('/user', response_model=schemas.ShowUser, tags=["User Management"])
def create_user(request: schemas.User, db: Session=Depends(database.get_db)):
    new_user = models.User(username=request.username, email=request.email, password=Hash.passwordHash(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/listOfUsers/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser, tags=["User Management"])
def get_user(id: int, db:Session=Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} is not available")
    return user
