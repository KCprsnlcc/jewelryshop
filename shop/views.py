# shop/views.py

from django.shortcuts import render

def home(request):
    products = [
        {
            'id': 1,
            'name': 'Alicia Gold Necklace',
            'description': 'A pearl on a golden chain.',
            'price': 1899,
            'image': 'shop/images/Necklace1.png',
            'category': 'Necklace'
        },
        {
            'id': 2,
            'name': 'Macy Gold Ring',
            'description': 'Uncomplicated, matchless, open-front design.',
            'price': 1999,
            'image': 'shop/images/Ring1.png',
            'category': 'Ring'
        },
        {
            'id': 3,
            'name': 'Kyla Gold Necklace',
            'description': 'Dainty chain with minimalist pendant.',
            'price': 3899,
            'image': 'shop/images/Necklace2.png',
            'category': 'Necklace'
        },
        {
            'id': 4,
            'name': 'Andie Gold Ring',
            'description': 'Heartfelt glamor radiates love.',
            'price': 3500,
            'image': 'shop/images/Ring2.png',
            'category': 'Ring'
        }
    ]
    return render(request, 'shop/home.html', {'products': products})

def product_detail(request, product_id):
    products = [
        {
            'id': 1,
            'name': 'Alicia Gold Necklace',
            'description': 'Pearls and gold are always a classic combination. The Alicia Necklace boasts a single pearl and a delicate golden chain, easily worn with daytime attire and evening ensembles alike. You’ll definitely have this piece on a heavy rotation.',
            'price': 1899,
            'image': 'shop/images/Necklace1.png',
            'category': 'Necklace'
        },
        {
            'id': 2,
            'name': 'Macy Gold Ring',
            'description': 'Unprecedented yet uncomplicated, the matchless Macy Ring balances out simplicity and standing out. Even better, it asks you to forget worrying about sizing. It’s open-front design makes for a great fit whether you buy it for yourself or as a gift.',
            'price': 1500,
            'image': 'shop/images/Ring1.png',
            'category': 'Ring'
        },
        {
            'id': 3,
            'name': 'Kyla Gold Necklace',
            'description': 'Pre-layering a dainty beaded chain and a minimalist ring pendant, this illusion necklace understands that less is more. With the Kyla Gold Necklace, you will spend less time deciding what to wear and more time enjoying how elegant you look. ',
            'price': 3899,
            'image': 'shop/images/Necklace2.png',
            'category': 'Necklace'
        },
        {
            'id': 4,
            'name': 'Andie Gold Ring',
            'description': 'Now here’s some heartfelt glamor. Whether it serves as a reminder of self-love or a symbol of someone’s affection, the Andie Ring is all set to radiate love.',
            'price': 3500,
            'image': 'shop/images/Ring2.png',
            'category': 'Ring'
        }
    ]
    product = next((item for item in products if item["id"] == product_id), None)
    return render(request, 'shop/product_detail.html', {'product': product})
