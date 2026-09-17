from django.urls import path
from . import views

urlpatterns = [
  path('create-order/', views.create_order_api, name = 'create_order_api')
]