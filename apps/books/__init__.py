from .schema import (
    RegisterBook
)
import graphene



class MutationBooks(graphene.ObjectType):

    create_books = RegisterBook.Field()