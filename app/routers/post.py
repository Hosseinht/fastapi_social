from typing import List, Optional

from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import PostModel
from ..schemas import PostCreateSchema, PostOutSchema
from ..oauth2 import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostOutSchema])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(PostModel)
        .filter(func.lower(PostModel.title).contains(f"%{search.lower()}%"))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostOutSchema)
def create_posts(
    post: PostCreateSchema,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    new_post = PostModel(
        title=post.title,
        content=post.content,
        published=post.published,
        user_id=current_user.id,
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=PostOutSchema)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post = db.query(PostModel).get(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


@router.delete("/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(PostModel).filter(PostModel.id == id)
    post = post_query.first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found",
        )

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorize to perform requested action",
        )
    post_query.delete()

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=PostOutSchema)
def update_post(
    id: int,
    post: PostCreateSchema,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    post_query = db.query(PostModel).filter(PostModel.id == id)
    get_post = post_query.first()

    if not get_post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    if get_post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorize to perform requested action",
        )

    post_query.update(post.dict(exclude_unset=True), synchronize_session=False)

    db.commit()

    return get_post
