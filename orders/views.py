from django.shortcuts import render
from .models import *
from django.db.models import Sum
import json
from django.http import JsonResponse


# calculation functions
def calculate_cost(weight_Kg, service_type, distance_km=0):
  price_Kg = 3.0
  price_Km = 5.0
  base_delivery_fee = 15.0

  grinding_cost = weight_Kg * price_Kg
  delivery = 0.0
  if service_type == 'DELIVERY':
    delivery = distance_km * price_Km
    if delivery < base_delivery_fee:
      delivery = base_delivery_fee
    else:
      delivery = base_delivery_fee + (distance_km * price_Km)

  total_cost = grinding_cost + delivery
  return grinding_cost, delivery, total_cost

def calculate_wait_time(new_order_weight_kg):
  mill_speed_Kg_per_min = 2
  pending_orders = Order.objects.filter(status__in=['WAITING', 'PROCESSING'])
  total_existing_weight = pending_orders.aggregate(Sum('wheat_weight_kg'))['wheat_weight_kg__sum'] or 0.0
  total_queue_weight = total_existing_weight + new_order_weight_kg
  estimated_minutes = total_queue_weight / mill_speed_Kg_per_min
    
  return int(estimated_minutes)

# main Views 
def create_order_api(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    weight = float(data.get('wheat_weight_kg', 0))
    service_type = data.get('service_type', 'SELF')
    grinding, delivery, total = calculate_cost(weight, service_type)
    wait_time = calculate_wait_time(weight)
    manual_address = data.get('address')

    new_order = Order.objects.create(
      customer_name = data.get('customer_name'),
      phone_num = data.get('phone_num'),
      wheat_weight_kg = weight,
      service_type = service_type,
      manual_location = manual_address,
      grinding_cost=grinding,
      delivery_cost=delivery,
      total_cost=total,
      estimated_wait_time_minutes=wait_time,
      status='WAITING'
    )

    return JsonResponse(
      {
        'status': 'success',
        'order_id': new_order.id,
        'total_cost': total,
        'estimated_wait_time_minutes': wait_time
      }
    )