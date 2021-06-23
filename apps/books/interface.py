import graphene


class InterfaceResultPost(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    subtitle = graphene.String()
    date_publish = graphene.String()
    editor = graphene.String()
    description = graphene.String()
    image = graphene.String()
    authors = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)


class InterfaceResultGet(InterfaceResultPost):
    source = graphene.String()