# shop/management/commands/populate_products.py
import random
from django.core.management.base import BaseCommand
from shop.models import Product, Category

class Command(BaseCommand):
    help = 'Populate the Products table with mock data'

    def handle(self, *args, **kwargs):
        categories = Category.objects.all()
        if not categories:
            self.stdout.write(self.style.ERROR('No categories found. Please add categories first.'))
            return

        for i in range(10):  # Adjust the range for the number of products you want to add
            product = Product(
                name=f'Product {i+1}',
                description=f'Description for product {i+1}',
                price=round(random.uniform(10.0, 100.0), 2),
                stock_quantity=random.randint(1, 100),
                category=random.choice(categories),
                image=None  # Adjust this if you have images to add
            )
            product.save()
            self.stdout.write(self.style.SUCCESS(f'Added {product.name}'))