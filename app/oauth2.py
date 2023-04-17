from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .database import get_db
from .models import UserModel
from .schemas import TokenDataSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "d0aa127246014c8b5181752d3b06c7ed0c55ba97a7065f025d04e70322f54d69"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    This function is responsible for creating access token
    """
    to_encode = data.copy()
    # make a copy of data. we don't want to accidentally change the data

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # encode the payload using SECRET_KEY and algorithm

    return encoded_jwt


def verify_access_token(token: str, credential_exception):
    """
    This function is responsible for verifying the access token and extract the user id
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id = payload.get("user_id")
        # access_token = create_access_token(data={"user_id": user.id})

        if id is None:
            raise credential_exception

        token_data = TokenDataSchema(id=id)
    except JWTError as e:
        print(e)
        raise credential_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    This function is a dependency function that is used to retrieve the current user based on the access token
    provided in the Authorization header of an HTTP request. It can be used for authenticating and authorizing users

    Input: Access token
    Once the verify_access_token returns the token_data, which is the id the get_current_user function should fetch
    the user from the database
    """

    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credential_exception)
    user = db.query(UserModel).filter(UserModel.id == token.id).first()

    return user
