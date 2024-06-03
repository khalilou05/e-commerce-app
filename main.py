from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.staticfiles import StaticFiles
from psycopg_pool import AsyncConnectionPool

from midleware.auth_midlware import Authmid
from routes import admin, article, auth
from settings import DB_NAME, DB_PASS, DB_USER


@asynccontextmanager
async def db_connect(app: FastAPI):
    app.pool = AsyncConnectionPool(
        f"host=localhost dbname={DB_NAME} user={DB_USER} password={DB_PASS} port=5432"
    )
    yield
    await app.pool.close()


app = FastAPI(
    openapi_url=None, default_response_class=ORJSONResponse, lifespan=db_connect
)


app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(Authmid)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(auth.route)
app.include_router(article.route)
app.include_router(admin.route)
