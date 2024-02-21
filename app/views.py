from django.db import connection
from django.shortcuts import render, redirect

from .models import *


def get_draft_order():
    return Order.objects.filter(status=1).first()


def index(request):
    query = request.GET.get("query", "")
    students = Student.objects.filter(name__icontains=query).filter(status=1)
    draft_order = get_draft_order()

    context = {
        "query": query,
        "students": students,
        "draft_order_id": draft_order.pk if draft_order else None
    }

    return render(request, "home_page.html", context)


def student_details(request, student_id):
    context = {
        "student": Student.objects.get(id=student_id)
    }

    return render(request, "student_page.html", context)


def student_delete(request, student_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE app_student SET status = 2 WHERE id = %s", [student_id])

    return redirect("/")


def order_details(request, order_id):
    order = Order.objects.get(id=order_id)

    context = {
        "order": order,
        "students": order.students.all()
    }

    return render(request, "order_page.html", context)


def student_add_to_order(request, student_id):
    student = Student.objects.get(pk=student_id)

    order = get_draft_order()

    if order is None:
        order = Order.objects.create()

    order.students.add(student)
    order.save()

    return redirect("/")


def order_delete(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.status = 5
    order.save()
    return redirect("/")

