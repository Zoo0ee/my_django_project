# orders/views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .services import process_bulk_order

@api_view(['POST'])
def bulk_order(request):
    """
    批量处理订单
    """
    order_data = request.data.get('orders', [])
    try:
        result = process_bulk_order(order_data)
        return Response({"message": result}, status=status.HTTP_200_OK)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
