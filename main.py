import graphene
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp
from graphql.execution.executors.asyncio import AsyncioExecutor
from apps.books.schema import QueryBooks
from core.db import database
from apps.auth import Mutation


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.add_route(
    "/auth",
    GraphQLApp(
        schema=graphene.Schema(mutation=Mutation),
        executor_class=AsyncioExecutor
    ),
)

app.add_route(
    "/books",
    GraphQLApp(
        schema=graphene.Schema(query=QueryBooks),
        executor_class=AsyncioExecutor
    ),
)
