import datetime
from jose import JWTError, jwt

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

    expire = datetime.datetime.now() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt