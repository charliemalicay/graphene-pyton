# cookbook/ingredients/schema.py
import graphene
from graphql import GraphQLError

from graphene_django.types import DjangoObjectType

from ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    all_categories = graphene.List(CategoryType)
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()


# Add New Category Mutation
class AddCategory(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        categoryName = graphene.String(required=True)

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    def mutate(self, info, categoryName):
        _category = Category.objects.create(name=categoryName)

        if not _category:
            raise GraphQLError("An error occurred while adding category")

        # Notice we return an instance of this mutation
        return AddCategory(category=_category)


class Mutation(object):
    add_category = AddCategory.Field()
