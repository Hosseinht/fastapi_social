from fastapi import Depends, HTTPException, Response, status, APIRouter
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import VoteModel, PostModel
from ..schemas import VoteSchema
from ..oauth2 import get_current_user


router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: VoteSchema,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):

    post = db.query(PostModel).filter(PostModel.id == vote.post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist"
        )

    vote_query = db.query(VoteModel).filter(
        VoteModel.post_id == vote.post_id, VoteModel.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{current_user.email} has already voted on post {vote.post_id}",
            )
        new_vote = VoteModel(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"detail": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"detail": "Successfully deleted vote"}
