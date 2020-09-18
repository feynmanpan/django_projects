import graphene
import mainsite.schema


class Query(mainsite.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
