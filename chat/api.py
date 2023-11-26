from typing import List, Union
from pydantic import condecimal
from datetime import date
from fastapi import APIRouter,HTTPException
from fastapi import FastAPI, WebSocket, Depends, Request, HTTPException, Query, WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from db import database
from chat.chat_html import html


chat_router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@chat_router.get("/create/websocket/event/")
async def create_event():
    await manager.broadcast("Подпишись на наш канал в телеграмме")
    return {"message": "ok"}


@chat_router.get("/")
async def get():
    return HTMLResponse(html)



@chat_router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")