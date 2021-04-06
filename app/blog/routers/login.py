from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from blog import schemas, database, models, TokenJWT
from blog.hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Login"]
)

@router.post('/login')
def login(request:OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invalid Credentials")
    if not Hash.verifyPassword(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Invalid password")
    # Generate Token and return
    access_token = TokenJWT.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
