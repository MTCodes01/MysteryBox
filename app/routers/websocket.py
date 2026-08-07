"""
WebSocket router: /ws/participant and /ws/host.
"""
import json
import logging

from fastapi import APIRouter, Cookie, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, AsyncSessionLocal
from app.models.models import Participant
from app.services.event_service import broadcast_stats, get_or_create_event
from app.services.ws_manager import manager

logger = logging.getLogger(__name__)

router = APIRouter()


# ── /ws/participant ───────────────────────────────────────────────────────────────

@router.websocket("/ws/participant")
async def participant_ws(websocket: WebSocket):
    session_id = websocket.cookies.get("session_id")
    if not session_id:
        await websocket.close(code=4001)
        return

    async with AsyncSessionLocal() as db:
        result      = await db.execute(select(Participant).where(Participant.session_id == session_id))
        participant = result.scalar_one_or_none()
        if not participant:
            await websocket.close(code=4001)
            return

        pid = participant.id

        # Mark connected
        participant.is_connected = True
        await db.commit()

    await manager.connect_participant(pid, websocket)

    async with AsyncSessionLocal() as db:
        await broadcast_stats(db)

    # Send current state to this participant
    async with AsyncSessionLocal() as db:
        event = await get_or_create_event(db)
        await manager.send_to_participant(pid, {"type": "state_sync", "phase": event.phase.value})

    try:
        while True:
            # Keep connection alive; participants don't send data via WS
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect_participant(pid)
        async with AsyncSessionLocal() as db:
            result      = await db.execute(select(Participant).where(Participant.id == pid))
            participant = result.scalar_one_or_none()
            if participant:
                participant.is_connected = False
                await db.commit()

            await manager.emit("participant_disconnected", {"participant_id": pid}, audience="host")
            await broadcast_stats(db)


# ── /ws/host ──────────────────────────────────────────────────────────────────────

@router.websocket("/ws/host")
async def host_ws(websocket: WebSocket):
    host_token = websocket.cookies.get("host_token")
    if host_token != "authenticated":
        await websocket.close(code=4001)
        return

    await manager.connect_host(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        manager.disconnect_host(websocket)
