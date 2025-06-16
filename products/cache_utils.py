from django.core.cache import cache
from .models import Product

CACHE_PREFIX = 'product_'

def get_product_from_cache(product_id):
    cache_key = f'{CACHE_PREFIX}{product_id}'
    product = cache.get(cache_key)
    if not product:
        try:
            product = Product.objects.get(id=product_id)
            cache.set(cache_key, product, timeout=3600)  # Cache for 1 hour
        except Product.DoesNotExist:
            return None
    return product

def update_product_cache(product_id):
    product = Product.objects.filter(id=product_id).first()
    if product:
        cache.set(f'{CACHE_PREFIX}{product.id}', product, timeout=3600)

def invalidate_product_cache(product_id):
    cache.delete(f'{CACHE_PREFIX}{product_id}')
