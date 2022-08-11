import datetime
from jose import JWTError, jwt
import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# secret key = verifys the server authentification (access to server)
# to get a string like this run in bash:
# openssl rand -hex 32
SECRET_KEY = "852f23d149f26f1f2ac7b81421996c28c34cee1edb33c613983b22b33023c3f0"

# Algorithm
ALGORITHM = "HS256"

# expiration time to logout
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_tokens(data: dict):
    to_encode = data.copy()

    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)