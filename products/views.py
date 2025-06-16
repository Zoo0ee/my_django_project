# products/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Product
from .cache_utils import get_product_from_cache

@api_view(['GET'])
def search_products(request):
    """
    商品搜索接口
    """
    query = request.query_params.get('query', '')
    if not query:
        return Response({"error": "Query parameter is required."}, status=400)

    products = Product.objects.filter(name__icontains=query)
    product_list = [
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "stock": p.stock
        }
        for p in products
    ]
    return Response({"products": product_list})
