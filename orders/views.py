from django.http import JsonResponse
from django.db import transaction
from products.models import Product
from .models import Order

def create_order(request):
    try:
        # 假设接收到的请求数据是订单列表
        order_data = request.POST.get('order_data')  # 假设是 JSON 格式
        
        # 创建一个订单
        order = Order.objects.create(user=request.user)

        # 使用事务处理订单
        with transaction.atomic():
            for item in order_data:
                product = Product.objects.get(id=item['product_id'])
                
                if product.stock < item['quantity']:
                    return JsonResponse({'error': f"Insufficient stock for {product.name}"}, status=400)

                product.stock -= item['quantity']
                product.save()

                # 记录订单明细
                # 这里需要创建一个订单明细模型，省略了这部分的实现

            order.status = 'COMPLETED'
            order.save()

        return JsonResponse({'message': 'Order created successfully'})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
