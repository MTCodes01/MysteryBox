"""
Vote router: POST /vote.
"""
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.models import Participant, Phase, Upload, Vote
from app.routers.auth import get_current_participant
from app.services.event_service import broadcast_stats, get_leaderboard, get_or_create_event
from app.services.ws_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter()


class VotePayload(BaseModel):
    upload_id: int
    score:     float = Field(..., ge=1, le=5)


@router.post("/vote")
async def submit_vote(
    payload:     VotePayload,
    participant: Participant = Depends(get_current_participant),
    db:          AsyncSession = Depends(get_db),
):
    event = await get_or_create_event(db)
    if event.phase != Phase.VOTING:
        raise HTTPException(status_code=400, detail="Voting is not open right now.")

    # Fetch the upload
    upload_res = await db.execute(select(Upload).where(Upload.id == payload.upload_id))
    upload     = upload_res.scalar_one_or_none()
    if not upload:
        raise HTTPException(status_code=404, detail="Image not found.")


    # Insert vote (unique constraint prevents duplicates)
    vote = Vote(voter_id=participant.id, upload_id=payload.upload_id, score=payload.score)
    db.add(vote)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="You have already voted on this image.")

    logger.info("Participant #%d voted %d on upload %d", participant.display_number, payload.score, payload.upload_id)

    # Notify host
    await manager.emit("vote_submitted", {
        "participant_id": participant.id,
        "upload_id":      payload.upload_id,
        "score":          payload.score,
    }, audience="host")
    await broadcast_stats(db)

    # Send live leaderboard update to host
    leaderboard = await get_leaderboard(db)
    await manager.emit("leaderboard_update", {"leaderboard": leaderboard}, audience="host")

    return {"message": "Vote recorded."}
