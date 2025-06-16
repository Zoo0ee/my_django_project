from django.shortcuts import render
from django.http import JsonResponse
from products.models import Product

def search_products(request):
    query = request.GET.get('query', '')
    if query:
        products = Product.objects.filter(name__icontains=query)
        product_list = [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]
        return JsonResponse({'products': product_list})
    else:
        return JsonResponse({'error': 'No query provided'}, status=400)