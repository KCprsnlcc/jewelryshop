# shop/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from shop.models import Category, Product
from django.shortcuts import render

class Command(BaseCommand):
    help = 'Populates the database with initial product data'

    def handle(self, request, *args, **kwargs):
        # Clear existing data
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        necklace_category = Category.objects.create(name='Necklace')
        ring_category = Category.objects.create(name='Ring')

        # Create Products
        products = [
            {
                'name': 'Alicia Gold Necklace',
                'short_description': 'A pearl on a golden chain.',
                'detailed_description': 'Pearls and gold are always a classic combination. The Alicia Necklace boasts a single pearl and a delicate golden chain, easily worn with daytime attire and evening ensembles alike. You’ll definitely have this piece on a heavy rotation.',
                'price': 1899,
                'image': 'shop/images/Necklace1.png',
                'category': necklace_category,
                'stock': 10,
            },
            {
                'name': 'Macy Gold Ring',
                'short_description': 'Uncomplicated, matchless, open-front design.',
                'detailed_description': 'Unprecedented yet uncomplicated, the matchless Macy Ring balances out simplicity and standing out. Even better, it asks you to forget worrying about sizing. It’s open-front design makes for a great fit whether you buy it for yourself or as a gift.',
                'price': 1999,
                'image': 'shop/images/Ring1.png',
                'category': ring_category,
                'stock': 15,
            },
            {
                'name': 'Kyla Gold Necklace',
                'short_description': 'Dainty chain with minimalist pendant.',
                'detailed_description': 'Pre-layering a dainty beaded chain and a minimalist ring pendant, this illusion necklace understands that less is more. With the Kyla Gold Necklace, you will spend less time deciding what to wear and more time enjoying how elegant you look.',
                'price': 3899,
                'image': 'shop/images/Necklace2.png',
                'category': necklace_category,
                'stock': 5,
            },
            {
                'name': 'Andie Gold Ring',
                'short_description': 'Heartfelt glamor radiates love.',
                'detailed_description': 'Now here’s some heartfelt glamor. Whether it serves as a reminder of self-love or a symbol of someone’s affection, the Andie Ring is all set to radiate love.',
                'price': 3500,
                'image': 'shop/images/Ring2.png',
                'category': ring_category,
                'stock': 8,
            }
        ]

        for product_data in products:
            Product.objects.create(**product_data)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
