# orders/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import F
from products.cache_utils import invalidate_product_cache
from .models import Order
from products.models import Product
from django.db import IntegrityError
import logging

logger = logging.getLogger(__name__)

def process_bulk_order(order_data):
    """
    处理批量订单。每个订单项包含商品ID和数量。
    """

    with transaction.atomic():
        failed_orders = []
        for item in order_data:
            product = Product.objects.select_for_update().filter(id=item['product_id']).first()

            if not product:
                failed_orders.append(f"Product {item['product_id']} not found.")
                continue

            if product.stock < item['quantity']:
                failed_orders.append(f"Insufficient stock for product {item['product_id']}.")
                continue

            try:
                product.stock -= item['quantity']
                product.save()

                # Create the order
                order = Order.objects.create(
                    product=product,
                    quantity=item['quantity'],
                    status='Completed'
                )

                # Invalidate cache for product
                invalidate_product_cache(product.id)
            except IntegrityError as e:
                failed_orders.append(f"Error processing order for product {item['product_id']}: {e}")
                logger.error(f"Error processing order for product {item['product_id']}: {e}")

        if failed_orders:
            raise ValidationError(f"Failed orders: {', '.join(failed_orders)}")
        return "Orders processed successfully."
