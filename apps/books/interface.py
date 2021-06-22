import graphene


class InterfaceResult(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    subtitle = graphene.String()
    date_publish = graphene.String()
    editor = graphene.String()
    description = graphene.String()
    image = graphene.String()
    authors = graphene.List(graphene.String)
    categories = graphene.List(graphene.String)
    source = graphene.String()