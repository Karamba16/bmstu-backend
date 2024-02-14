from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/students/search/', search_students),  # GET
    path('api/students/<int:student_id>/', get_student_by_id),  # GET
    path('api/students/<int:student_id>/image/', get_student_image),  # GET
    path('api/students/<int:student_id>/update/', update_student),  # PUT
    path('api/students/<int:student_id>/update_image/', update_student_image),  # PUT
    path('api/students/<int:student_id>/delete/', delete_student),  # DELETE
    path('api/students/create/', create_student),  # POST
    path('api/students/<int:student_id>/add_to_order/', add_student_to_order),  # POST

    # Набор методов для заявок
    path('api/orders//search/', search_orders),  # GET
    path('api/orders/<int:order_id>/', get_order_by_id),  # GET
    path('api/orders/<int:order_id>/update/', update_order),  # PUT
    path('api/orders/<int:order_id>/update_status_user/', update_status_user),  # PUT
    path('api/orders/<int:order_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/orders/<int:order_id>/delete/', delete_order),  # DELETE
    path('api/orders/<int:order_id>/delete_student/<int:student_id>/', delete_student_from_order)  # DELETE
]
