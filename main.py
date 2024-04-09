from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from psycopg_pool import AsyncConnectionPool

from midleware.auth_midlware import Authmid
from routes import admin, article, auth


@asynccontextmanager
async def db_connect(app: FastAPI):
    # todo use env variable                  ↓              ↓               ↓
    app.pool = AsyncConnectionPool("dbname=djamel user=postgres password=khalil")
    yield
    await app.pool.close()


app = FastAPI(
    openapi_url=None, default_response_class=ORJSONResponse, lifespan=db_connect
)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(Authmid)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.route)
app.include_router(article.route)
app.include_router(admin.route)
