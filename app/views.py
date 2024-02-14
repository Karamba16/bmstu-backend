from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *


def get_draft_order():
    order = Order.objects.filter(status=1).first()

    if order is None:
        return None

    return order


@api_view(["GET"])
def search_students(request):
    query = request.GET.get("query", "")

    students = Student.objects.filter(status=1).filter(name__icontains=query)

    serializer = StudentSerializer(students, many=True)

    draft_order = get_draft_order()

    resp = {
        "students": serializer.data,
        "draft_order_id": draft_order.pk if draft_order else None
    }

    return Response(resp)


@api_view(["GET"])
def get_student_by_id(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)
    serializer = StudentSerializer(student, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_student(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)
    serializer = StudentSerializer(student, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
def create_student(request):
    Student.objects.create()

    students = Student.objects.filter(status=1)
    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_student(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)
    student.status = 2
    student.save()

    students = Student.objects.filter(status=1)
    serializer = StudentSerializer(students, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_student_to_order(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)

    order = get_draft_order()

    if order is None:
        order = Order.objects.create()

    order.students.add(student)
    order.save()

    serializer = StudentSerializer(order.students, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_student_image(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)

    return HttpResponse(student.image, content_type="image/png")


@api_view(["PUT"])
def update_student_image(request, student_id):
    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    student = Student.objects.get(pk=student_id)
    serializer = StudentSerializer(student, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def search_orders(request):
    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start")
    date_end = request.GET.get("date_end")

    orders = Order.objects.all()

    if status_id != -1:
        orders = orders.filter(status=status_id)

    if date_start and parse_datetime(date_start):
        orders = orders.filter(date_formation__gte=parse_datetime(date_start))

    if date_end and parse_datetime(date_end):
        orders = orders.filter(date_formation__lte=parse_datetime(date_end))

    serializer = OrdersSerializer(orders, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_order_by_id(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    serializer = OrderSerializer(order, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    order.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 2
    order.date_formation = timezone.now()
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order = Order.objects.get(pk=order_id)

    if order.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.date_complete = timezone.now()
    order.status = request_status
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_order(request, order_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)

    if order.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    order.status = 5
    order.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete_student_from_order(request, order_id, student_id):
    if not Order.objects.filter(pk=order_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    if not Student.objects.filter(pk=student_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    order = Order.objects.get(pk=order_id)
    order.students.remove(Student.objects.get(pk=student_id))
    order.save()

    serializer = StudentSerializer(order.students, many=True)

    return Response(serializer.data)