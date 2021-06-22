
import graphene
from .schema import (
    RegisterUser,
    LoginUser
)


class Mutation(graphene.ObjectType):

   create_user = RegisterUser.Field()
   login = LoginUser.Field()