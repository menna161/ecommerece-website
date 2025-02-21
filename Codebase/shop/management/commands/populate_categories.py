# shop/management/commands/populate_categories.py
from django.core.management.base import BaseCommand
from shop.models import Category

class Command(BaseCommand):
    help = 'Populate the Category table with mock data'

    def handle(self, *args, **kwargs):
        categories = ['Electronics', 'Books', 'Clothing', 'Home & Kitchen', 'Sports']
        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Added category {category_name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Category {category_name} already exists'))