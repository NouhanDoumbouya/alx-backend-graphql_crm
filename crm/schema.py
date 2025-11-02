import graphene
from graphene_django import DjangoObjectType
from crm.models import Product
from django.utils import timezone

# Define ProductType for GraphQL responses
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")


class UpdateLowStockProducts(graphene.Mutation):
    # Define what the mutation returns
    class Arguments:
        pass  # no arguments needed

    updated_products = graphene.List(ProductType)
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info):
        # Get low stock products
        low_stock_products = Product.objects.filter(stock__lt=10)

        updated_list = []
        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_list.append(product)

        return UpdateLowStockProducts(
            updated_products=updated_list,
            message=f"{len(updated_list)} products restocked at {timezone.now()}!"
        )


# Add mutation to schema
class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello from CRM GraphQL!")
    products = graphene.List(ProductType)

    def resolve_products(root, info):
        return Product.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)
