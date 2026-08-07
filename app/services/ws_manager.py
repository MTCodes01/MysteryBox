"""
WebSocket connection manager.

Maintains separate sets for host and participant connections.
Broadcasts typed JSON events to the appropriate audience.
"""
import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket

logger = logging.getLogger(__name__)


class ConnectionManager:
    def __init__(self) -> None:
        # participant_id -> WebSocket
        self.participant_connections: dict[int, WebSocket] = {}
        # set of host WebSockets
        self.host_connections: set[WebSocket] = set()

    # ── Participant ───────────────────────────────────────────────────────────────
    async def connect_participant(self, participant_id: int, ws: WebSocket) -> None:
        await ws.accept()
        self.participant_connections[participant_id] = ws
        logger.info("Participant %d connected via WS", participant_id)

    def disconnect_participant(self, participant_id: int) -> None:
        self.participant_connections.pop(participant_id, None)
        logger.info("Participant %d disconnected from WS", participant_id)

    async def send_to_participant(self, participant_id: int, data: dict) -> None:
        ws = self.participant_connections.get(participant_id)
        if ws:
            try:
                await asyncio.wait_for(ws.send_text(json.dumps(data)), timeout=1.0)
            except Exception:
                self.disconnect_participant(participant_id)

    async def broadcast_participants(self, data: dict) -> None:
        dead: list[int] = []
        for pid, ws in list(self.participant_connections.items()):
            try:
                await asyncio.wait_for(ws.send_text(json.dumps(data)), timeout=1.0)
            except Exception:
                dead.append(pid)
        for pid in dead:
            self.disconnect_participant(pid)

    # ── Host ─────────────────────────────────────────────────────────────────────
    async def connect_host(self, ws: WebSocket) -> None:
        await ws.accept()
        self.host_connections.add(ws)
        logger.info("Host connected via WS")

    def disconnect_host(self, ws: WebSocket) -> None:
        self.host_connections.discard(ws)
        logger.info("Host disconnected from WS")

    async def broadcast_host(self, data: dict) -> None:
        dead: set[WebSocket] = set()
        for ws in list(self.host_connections):
            try:
                await asyncio.wait_for(ws.send_text(json.dumps(data)), timeout=1.0)
            except Exception:
                dead.add(ws)
        for ws in dead:
            self.disconnect_host(ws)

    # ── Broadcast to all ─────────────────────────────────────────────────────────
    async def broadcast_all(self, data: dict) -> None:
        await asyncio.gather(
            self.broadcast_participants(data),
            self.broadcast_host(data),
        )

    # ── Typed helpers ─────────────────────────────────────────────────────────────
    async def emit(self, event_type: str, payload: dict[str, Any], audience: str = "all") -> None:
        """
        audience: 'all' | 'participants' | 'host'
        """
        data = {"type": event_type, **payload}
        if audience == "host":
            await self.broadcast_host(data)
        elif audience == "participants":
            await self.broadcast_participants(data)
        else:
            await self.broadcast_all(data)


# Singleton instance shared across the app
manager = ConnectionManager()
