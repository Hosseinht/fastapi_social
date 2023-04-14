from typing import List

from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import PostModel
from ..schemas import PostCreate, PostOut

router = APIRouter()


@router.get("/posts", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts


@router.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostModel(
        title=post.title, content=post.content, published=post.published
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}")
def update(id: int, post: PostCreate, db: Session = Depends(get_db)):
    get_post = db.query(PostModel).filter(PostModel.id == id)

    if not get_post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    get_post.update(post.dict(exclude_unset=True))

    db.commit()

    return get_post.first()
