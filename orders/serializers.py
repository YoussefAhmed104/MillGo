from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
  distance_km = serializers.FloatField(write_only=True, required=False, default=0.0)
  class Meta:
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
      'status' : {'default': 'WAITING'},
      'manual_location': {'required': False, 'allow_blank': True},
      'wheat_weight_kg': {'min_value': 0.1},
    }

  def validate(self, attrs):
    service_type = attrs.get('service_type', getattr(self.instance, 'service_type', 'SELF'))
    manual_location = attrs.get('manual_location', getattr(self.instance, 'manual_location', ''))
    latitude = attrs.get('latitude', getattr(self.instance, 'latitude', None))
    distance_km = attrs.get('distance_km', 0.0)
    if service_type =='DELIVERY':
      if  not manual_location and latitude is None:
        raise serializers.ValidationError({
          "manual_location": "Either a manual location or latitude/longitude coordinates must be provided for delivery orders."
        })
      if distance_km <=0:
        raise serializers.ValidationError({
          "distance_km": "Distance must be greater than zero"
        })

    return attrs
  