from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name="home"),
    path('students/<int:student_id>/', student_details),
    path('students/<int:student_id>/delete/', student_delete),
    path('students/<int:student_id>/add_to_order/', student_add_to_order),
    path('orders/<int:order_id>/', order_details),
    path('orders/<int:order_id>/delete/', order_delete),
]
