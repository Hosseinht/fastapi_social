from fastapi import Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import UserModel
from ..schemas import UserCreateSchema, UserOutSchema
from ..utils import hash

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    # hash the password
    hash_password = hash(user.password)
    user.password = hash_password

    new_user = UserModel(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/{id}", status_code=status.HTTP_201_CREATED, response_model=UserOutSchema)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    return user
