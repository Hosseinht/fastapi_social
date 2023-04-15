from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import UserModel
from ..schemas import UserLogin
from ..utils import verify

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == user_credentials.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials"
        )

    return {"token": "yakhchi"}
