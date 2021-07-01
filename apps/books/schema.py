from core.security import (
    valid_auth
)
from .interface import (
    InterfaceResultGet,
    InterfaceResultPost
)
from core.db import database
from .queries import (
    query_normal,
    query_relations
)
from .models import (
    book,
    authors,
    authors_book,
    category,
    category_book
)

from graphql import GraphQLError
import asyncio
import aiohttp
import graphene
import functools


def map_response(data):
    array_result = []
    for values in data:
        result = {}
        result['id'] = values.id
        result['title'] = values.title
        result['subtitle'] = values.subtitle
        result['date_publish'] = values.date_publish
        result['editor'] = values.editor
        result['description'] = values.description
        result['image'] = values.image
        result['authors'] = values.authors.split(",")
        result['categories'] = values.categories.split(",")
        result['source'] = "DB interna"
        array_result.append(result)
    return array_result


async def get(session, url, **kwargs):
    resp = await session.request('GET', url=url, **kwargs)
    data = await resp.json()
    if 'numFound' in data:
        if data['numFound']:
            elements = []
            for values in data['docs']:
                item = {}
                item['title'] = values['name']
                item['subtitle'] = values['name']
                item['date_publish'] = values['birth_date'][-4:] + '-01-01' if 'birth_date' in values else ''
                item['editor'] = ''
                item['description'] = ''
                item['image'] = values['text'][0]
                item['source'] = 'Open Library'
                item['categories'] = [values['top_work']]
                item['authors'] = []
                elements.append(item)
            return elements
    if 'totalItems' in data:
        if data['totalItems']:
            elements = []
            for values in data['items']:
                item = {}
                item['title'] = values['volumeInfo']['title']
                item['subtitle'] = ''
                item['date_publish'] = values['volumeInfo']['publishedDate'][:4] + '-01-01' if 'publishedDate' in values['volumeInfo'] else '2021-01-01'
                item['editor'] = ''
                item['description'] = values['volumeInfo']['description'] if 'description' in values['volumeInfo'] else ''
                item['image'] = (values['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in values['volumeInfo'] else '')
                item['source'] = 'Google Books'
                item['categories'] = values['volumeInfo']['categories'] if 'categories' in values['volumeInfo'] else []
                item['authors'] = values['volumeInfo']['authors'] if 'authors' in values['volumeInfo'] else []
                elements.append(item)
            return elements
    return []


async def response_all(key, element, condition):
    query = query_normal(key, element, condition)
    data = await database.fetch_all(query)
    if len(data) > 0:
        return map_response(data)
    else:
        return []


class QueryBooks(graphene.ObjectType):

    books = graphene.List(
        InterfaceResultGet,
        id=graphene.Int(),
        title=graphene.String(),
        subtitle=graphene.String(),
        date_publish=graphene.String(),
        editor=graphene.String(),
        descript=graphene.String(),
        image=graphene.String(),
        authors=graphene.String(),
        categories=graphene.String()
    )

    @valid_auth()
    async def resolve_books(self, info, **kwargs):
        for element in kwargs:
            repls = {' ': '+', "'": '"'}
            search = functools.reduce(lambda a, kv: a.replace(*kv), repls.items(), kwargs[element])
            if element in ['title', 'subtitle', 'date_publish', 'editor', 'descript', 'image']:
                element = 'description' if element == 'descript' else element
                data = await response_all(element, """'%""" + search + """%'""", 'like')
            elif element == 'id':
                query = query_normal('id', str(kwargs['id']), '=')
                all_data = await database.fetch_all(query)
                if len(all_data) > 0:
                    data = map_response(all_data)
                else:
                    raise GraphQLError('Id not found')
            elif element in ['authors', 'categories']:
                state = False if element == 'authors' else True
                search = kwargs[element].replace(' ', '+')
                query = query_relations(search, state)
                all_data = await database.fetch_all(query)
                if len(all_data) > 0:
                    data = map_response(all_data)
                else:
                    data = []
            else:
                raise GraphQLError('Miss field for filter')
        if len(data) > 0:
            return data
        async with aiohttp.ClientSession() as session:
            tasks = []
            consume = [
                f'http://openlibrary.org/search/authors.json?q={search}',
                f'https://www.googleapis.com/books/v1/volumes?q={search}'
            ]
            for c in consume:
                tasks.append(get(session=session, url=c, **{}))
            htmls = await asyncio.gather(*tasks, return_exceptions=True)
            return htmls[0] + htmls[1]


async def insert_intermediate(id_book, id_authors):
    query_autbook = authors_book.insert().values(
        book_id=int(id_book),
        authors_id=int(id_authors)
    )
    await database.execute(query_autbook)


async def insert_authors(id_book, authors_all):
    for values in authors_all:
        query = authors.select().where(authors.c.name == values)
        data = await database.fetch_all(query)
        if len(data) == 0:
            query_inser = authors.insert().values(
                name=values,
                description=''
            )
            id_insert = await database.execute(query_inser)
            await insert_intermediate(id_book, id_insert)
        else:
            await insert_intermediate(id_book, data[0].id)


async def insert_intermediate_category(id_book, id_category):
    query_autbook = category_book.insert().values(
        book_id=int(id_book),
        category_id=int(id_category)
    )
    await database.execute(query_autbook)


async def insert_categories(id_book, categories_all):
    for values in categories_all:
        query = category.select().where(category.c.name == values)
        data = await database.fetch_all(query)
        if len(data) == 0:
            query_inser = category.insert().values(
                name=values,
                description=''
            )
            id_insert = await database.execute(query_inser)
            await insert_intermediate_category(id_book, id_insert)
        else:
            await insert_intermediate_category(id_book, data[0].id)


class RegisterBook(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)
        subtitle = graphene.String(required=True)
        date_publish = graphene.String(required=True)
        editor = graphene.String(required=True)
        description = graphene.String(required=True)
        image = graphene.String(required=True)
        authors = graphene.List(graphene.String)
        categories = graphene.List(graphene.String)

    book = graphene.Field(InterfaceResultPost)


    @staticmethod
    @valid_auth()
    async def mutate(parent, info, **kwargs):
        user = info.context['user']
        if len(kwargs['authors']) == 0 or len(kwargs['categories']) == 0:
            raise GraphQLError('Field authors or authors have not items ')
        query = book.insert().values(
            title=kwargs['title'],
            subtitle=kwargs['subtitle'],
            date_publish=kwargs['date_publish'],
            editor=kwargs['editor'],
            description=kwargs['description'],
            image=kwargs['image'],
            user_created=user['id']
        )
        last_record_id = await database.execute(query)
        kwargs['id'] = last_record_id
        await insert_authors(last_record_id, kwargs['authors'])
        await insert_categories(last_record_id, kwargs['categories'])
        return RegisterBook(book=kwargs)


class DeleteBook(graphene.Mutation):

    class Arguments:
        id = graphene.Int(required=True)

    status = graphene.String()

    @staticmethod
    @valid_auth()
    async def mutate(parent, info, **kwargs):
        query = category_book.delete().where(category_book.c.book_id == int(kwargs['id']))
        await database.execute(query)
        query = authors_book.delete().where(authors_book.c.book_id == int(kwargs['id']))
        await database.execute(query)
        query = book.delete().where(book.c.id == int(kwargs['id']))
        await database.execute(query)
        return DeleteBook(status="ok")
