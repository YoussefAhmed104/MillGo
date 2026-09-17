from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
  class Mete:
    model = Order
    fields = '__all__'
    read_only_fields = [
      'id',
      'grinding_cost',
      'delivery_cost',
      'total_cost',
      'estimated_wait_time_minutes',
      'created_at',
    ]
    extra_kwargs = {
      'status' : {'defult': 'WAITING'},
      'manual_location': {'required': False, 'allow_blank': True},
    }

  def validate(self, attrs):
    service_type = attrs.get('service_type', getattr(self.instance, 'service_type', 'SELF'))
    manual_location = attrs.get('manual_location', getattr(self.instance, 'manual_location', ''))
    latitude = attrs.get('latitude', getattr(self.instance, 'latitude', None))

    if service_type =='DELIVERY' and not manual_location and latitude is None:
      raise serializers.ValidationError({
        "manual_location": "Either a manual location or latitude/longitude coordinates must be provided for delivery orders."
      })
    return attrs
  