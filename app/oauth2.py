from datetime import datetime, timedelta
from jose import JWSError, jwt

SECRET_KEY = "d0aa127246014c8b5181752d3b06c7ed0c55ba97a7065f025d04e70322f54d69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):

    to_encode = data.copy()
    # make a copy of data. we don't want to accidentally change the data

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # encode the payload using SECRET_KEY and algorithm

    return encoded_jwt
