import graphene
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.graphql import GraphQLApp


class Query(graphene.ObjectType):
    hello = graphene.String(name=graphene.String(default_value="stranger"))

    def resolve_hello(self, info, name):
        request = info.context["request"]
        print(request.headers.get("Authorization", ""))
        return "Hello Buena " + name


app = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_methods=["*"],
                   allow_headers=["*"]
)

app.add_route("/", GraphQLApp(schema=graphene.Schema(query=Query)))