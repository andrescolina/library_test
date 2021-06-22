import graphene


class User(graphene.ObjectType):
    id = graphene.Int()
    username = graphene.String()
    is_admin = graphene.Boolean()
    is_active = graphene.Boolean()
