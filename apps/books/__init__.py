from .schema import (
    RegisterBook,
    DeleteBook
)
import graphene



class MutationBooks(graphene.ObjectType):

    create_books = RegisterBook.Field()
    delete_books = DeleteBook.Field()