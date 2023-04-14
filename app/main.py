from fastapi import FastAPI, HTTPException, Response, status, Depends
from sqlalchemy.orm import Session

from .models import PostModel
from .schemas import PostCreate
from .database import engine, get_db, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: PostCreate, db: Session = Depends(get_db)):
    new_post = PostModel(
        title=post.title, content=post.content, published=post.published
    )
    # or we can do it like this
    # new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"post": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).get(id)
    # or
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return {"post_detail": post}


@app.delete("/posts/{id}")
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


@app.put("/posts/{id}")
def update(id: int, post: PostCreate, db: Session = Depends(get_db)):
    get_post = db.query(PostModel).filter(PostModel.id == id)

    if not get_post.first():
        raise HTTPException(status_code=404, detail=f"Post with id {id} not found")

    get_post.update(post.dict(exclude_unset=True))

    db.commit()
    return {"data": get_post.first()}
