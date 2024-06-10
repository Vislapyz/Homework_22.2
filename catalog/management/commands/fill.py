from django.core.management import BaseCommand
from catalog.models import Category, Product
import json


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():

        with open("fixture/catalog_category.json", "r", encoding="UTF-8") as file:
            categories = json.load(file)
            return categories

    @staticmethod
    def json_read_products():

        with open("fixture/catalog_product.json", "r", encoding="UTF-8") as file:
            products = json.load(file)
            return products

    def handle(self, *args, **options):

        Product.objects.all().delete()

        Category.objects.all().delete()

        product_for_create = []
        category_for_create = []

        for category in Command.json_read_categories():
            category_for_create.append(
                Category(
                    pk=category["pk"],
                    name=category["fields"].get("name"),
                    description=category["fields"].get("description"),
                )
            )

        Category.objects.bulk_create(category_for_create)

        for product in Command.json_read_products():
            product_for_create.append(
                Product(
                    name=product["fields"].get("name"),
                    description=product["fields"].get("description"),
                    preview=product["fields"].get("preview"),
                    # получаем категорию из базы данных для корректной связки объектов
                    category=Category.objects.get(pk=product["fields"].get("category")),
                    price=product["fields"].get("price"),
                )
            )

        Product.objects.bulk_create(product_for_create)
