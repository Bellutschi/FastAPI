from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import database, schemas, models, utils
import oauth2

router = APIRouter(tags=['Authentication'])

# user_credentials: OAuth2PasswordRequestForm = Depends()
# setzt eine Dependency bzw. gewisses Schema
@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # user_credentials.username kommt vom OAuth2PasswordRequestForm und ist wie die user.email
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    access_token = oauth2.create_access_tokens(data = {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
