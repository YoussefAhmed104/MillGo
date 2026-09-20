from django.urls import path
from . import views

urlpatterns = [
  path('create-order/', views.create_order, name = 'create_order'),
  path('track-order/<str:pk>/', views.track_order, name = 'track_order'),
  path('update-status/<int:pk>/', views.update_order_status, name = 'update_order_status'),
  path('orders/', views.order_list, name= 'order_list')
]