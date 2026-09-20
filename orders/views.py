from django.shortcuts import render
from .models import *
from django.db.models import Sum
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Rest 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import OrderSerializer
from rest_framework.decorators import authentication_classes, permission_classes

# calculation functions
def calculate_cost(weight_Kg, service_type, distance_km=0):
  price_Kg = 3.0
  price_Km = 5.0
  base_delivery_fee = 15.0

  grinding_cost = weight_Kg * price_Kg
  delivery = 0.0
  if service_type == 'DELIVERY':
        calculated_delivery = distance_km * price_Km
        delivery = max(base_delivery_fee, calculated_delivery)

  total_cost = grinding_cost + delivery
  return grinding_cost, delivery, total_cost

def calculate_wait_time(new_order_weight_kg):
  mill_speed_Kg_per_min = 2
  pending_orders = Order.objects.filter(status__in=['WAITING', 'PROCESSING'])
  total_existing_weight = pending_orders.aggregate(Sum('wheat_weight_kg'))['wheat_weight_kg__sum'] or 0.0
  total_queue_weight = total_existing_weight + new_order_weight_kg
  estimated_minutes = total_queue_weight / mill_speed_Kg_per_min
    
  return int(estimated_minutes)

# create new Order end point 
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_order(request):
  serializer = OrderSerializer(data=request.data)

  if serializer.is_valid():
    weight = float(serializer.validated_data.get('wheat_weight_kg', 0.0))
    service_type = serializer.validated_data.get("service_type", 'SELF')
    distance = serializer.validated_data.get('distance_km', 0.0)
    grinding, delivery, total = calculate_cost(weight, service_type, distance)
    wait_time = calculate_wait_time(weight)

    order = serializer.save(
      grinding_cost = grinding,
      delivery_cost = delivery,
      total_cost = total,
      estimated_wait_time_minutes = wait_time,
      status = 'WAITING'
    )

    return Response({
      'status' : 'success',
      'order_id' : order.id,
      'total_cost' : total,
      'estimated_wait_time_minutes' : wait_time,
      'order_details' : OrderSerializer(order).data
    }, status=status.HTTP_201_CREATED)

  return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def track_order(view_request, pk):
   if pk.isdigit() and len(pk) < 8:
      order = get_object_or_404(Order, id=pk)
      serializer = OrderSerializer(order)
      return Response(serializer.data)
   else:
      orders = Order.objects.filter(phone_number=pk)
      if not orders.exists():
         return Response({"error": "No orders found for this phone number"}, status=status.HTTP_404_NOT_FOUND)
      serializer = OrderSerializer(orders, many= True)
      return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def update_order_status(view_request, pk):
   order = get_object_or_404(Order, id=pk)
   new_status = view_request.data.get('status')
   valid_statuses = ['WAITING', 'PROCESSING', 'COMPLETED']

   if new_status not in valid_statuses:
      return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
   order.status = new_status
   order.save()

   return Response({"message": f"order status updated to {new_status}"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def order_list(request):
   order = Order.objects.all().order_by('-id')
   serializer = OrderSerializer(order, many=True)
   return Response({'status': 'SUCCESS', 'order': serializer.data})
