from fastapi import APIRouter, Depends, status
from blog import schemas, models, database
from sqlalchemy.orm import Session
from blog.repository import user

router = APIRouter(
    prefix="/auth",
    tags=["User Management"]
)

@router.post('/user', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session=Depends(database.get_db)):
    return user.createUser(request, db)

@router.get('/listOfUsers/{id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowUser)
def get_user(id: int, db:Session=Depends(database.get_db)):
    return user.userList(id, db)
