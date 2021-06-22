import graphene
from core.security import (
    valid_auth
)
from .interface import (
    InterfaceResult
)
from core.db import database
from .queries import (
    query_normal,
    query_relations
)
from graphql import GraphQLError
import asyncio
import aiohttp


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
    print(data)
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
                item['category'] = [values['top_work']]
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
                item['date_publish'] = values['volumeInfo']['publishedDate'][:4] + '-01-01'
                item['editor'] = ''
                item['description'] = values['volumeInfo']['description'] if 'description' in values['volumeInfo'] else ''
                item['image'] = (values['volumeInfo']['imageLinks']['smallThumbnail'] if 'imageLinks' in values['volumeInfo'] else '')
                item['source'] = 'Google Books'
                item['category'] = values['volumeInfo']['categories'] if 'categories' in values['volumeInfo'] else []
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
        InterfaceResult,
        id=graphene.Int(),
        title=graphene.String(),
        subtitle=graphene.String(),
        date_publish=graphene.String(),
        editor=graphene.String(),
        description=graphene.String(),
        image=graphene.String(),
        authors=graphene.String(),
        categories=graphene.String()
    )

    @valid_auth()
    async def resolve_books(self, info, **kwargs):
        for element in kwargs:
            if element in ['title', 'subtitle', 'date_publish', 'editor', 'description', 'image']:
                search = kwargs[element].replace(' ', '+')
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
            print(htmls)
            return htmls[0] + htmls[1]