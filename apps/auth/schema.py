from .models import users
from core.db import database
from core.security import (
    valid_auth,
    hash_password,
    verify_password,
    create_jwt_token
)
from graphql import GraphQLError
from sqlalchemy import and_
from .interface import User
import graphene


class RegisterUser(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(User)

    @staticmethod
    @valid_auth()
    async def mutate(parent, info, **kwargs):
        user = info.context['user']
        if user['is_admin'] and user['is_active']:
            query = users.select().where(users.c.user == kwargs['username'])
            data = await database.fetch_all(query)
            if len(data) == 0:
                query_insert = users.insert().values(
                    user=kwargs['username'],
                    password=hash_password(kwargs['password']),
                    is_active=False,
                    is_admin=False
                )
                last_record_id = await database.execute(query_insert)
                query_result = users.select().where(users.c.id == last_record_id)
                user_insert = await database.fetch_all(query_result)
                result = {}
                for values in user_insert:
                    result['id'] = values.id
                    result['username'] = values.user
                    result['is_active'] = values.is_active
                    result['is_admin'] = values.is_admin
                return RegisterUser(user=result)
            else:
                raise GraphQLError('User already exists')
        else:
            raise GraphQLError('You don"t have permissions')


class LoginUser(graphene.Mutation):

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()

    @staticmethod
    async def mutate(parent, info, **kwargs):
        query = users.select().where(
            and_(users.c.user == kwargs['username'], users.c.is_active == True)
        )
        data = await database.fetch_all(query)
        if len(data) == 0:
            raise GraphQLError('User Doesn"t exists or is inactive')
        else:
            password_hash = data[0][2]
            if not verify_password(kwargs['password'], password_hash):
                raise GraphQLError('Password Incorrect')
            result = {}
            for values in data:
                result['id'] = values.id
                result['username'] = values.user
                result['is_active'] = values.is_active
                result['is_admin'] = values.is_admin
            token = create_jwt_token(data=result)
            return LoginUser(token=token)

