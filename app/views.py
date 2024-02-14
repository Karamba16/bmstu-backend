from django.shortcuts import render, redirect,get_object_or_404
from django.db import connection
from django.urls import reverse
from django.db.models import Q
from datetime import date
from app.models import Student

import psycopg2


'''def detailed_operations_page(request, id):
    data_by_id = db_operations.get('operations_to_perform')[id]
    return render(request, 'operation_types_detailed.html', {
        'operations_to_perform': data_by_id
    })
'''


def detailed_service_page(request, id):
    filtered_data=list(Student.objects.filter(student_id=id))[0]
    print(filtered_data)
    return render(request, 'operation_types_detailed.html',
        {'filtered_data': filtered_data})


def service_page(request):
    query = request.GET.get('q')

    if query:
        # Фильтрую данные, при этом учитываю поле "type"
        filtered_data =  list(Student.objects.filter(status='0',last_name__icontains=query))

    else:
        filtered_data = list(Student.objects.filter(status='0'))

        query = ""
        print(filtered_data)
    return render(request, "operation_types.html", {'filtered_data': filtered_data})
# Create your views here.

def delete_operation(id):
    student=get_object_or_404(Student,pk=id)
    print(student)
    student.status='2'
    student.save()

def update_operations_page(request, id):
    student=get_object_or_404(Student,pk=id)
    print(student)
    student.status = '2'
    student.save()

    return redirect('/')


