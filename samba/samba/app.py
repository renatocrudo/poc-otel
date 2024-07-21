import logging
from contextlib import asynccontextmanager
from datetime import datetime

import httpx
from fastapi import FastAPI
from pydantic import BaseModel


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler()) # para ele escrever no shell, o que foi enviado para Loki

@asynccontextmanager
async def lifespan(app):
    logger.info('Start Samba')
    yield
    logger.info('Stop Samba')


app = FastAPI(lifespan=lifespan)


class PessoaIn(BaseModel):
    name: str
    age: int
    email: str


class PessoaOut(PessoaIn):
    id: int
    created_at: datetime

@app.get('/')
def check():
    return "Hello World"


@app.get('/check')
def check():
    return {'status':'OK'}

@app.get('/user/{user_id}')
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'http://catedral:8002/user/{user_id}')

        return response.json()


@app.get('/user')
async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get('http://catedral:8002/user')

    return response.json()


@app.post('/user', response_model=PessoaOut)
async def create_user(user: PessoaIn):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://catedral:8002/user', json=user.model_dump()
        )

        return response.json()