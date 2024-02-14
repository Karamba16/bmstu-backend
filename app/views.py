from django.shortcuts import render

# Create your views here.
db_services = {
    'services_to_perform': [
        {
            'id': 0,
            'name': 'Ерхов М.Р.',
            'group': 'ИУ5-53Б',
            'description': 'Студент направления "Информатика и вычислительная техника", 3 курс ,1 семестр ,3 группа',
            'image_url': '../static/image/0.png'
        },
        {
            'id': 1,
            'name': 'Иванов К. Н.',
            'group': 'СМ6-42Б',
            'description': 'Студент направления "Ракетные и импульсные системы", 2 курс ,2 семестр ,2 группа',
            'image_url': '../static/image/1.png'
        },
        {
            'id': 2,
            'name': 'Сидоров М.Р.',
            'group': 'ИУ5-31Б',
            'description': 'Студент направления "Информатика и вычислительная техника", 2 курс ,1 семестр ,1 группа',
            'image_url': '../static/image/2.png'
        },
        {
            'id': 3,
            'name': 'Елисеев И.Г.',
            'group': 'ИУ6-53Б',
            'description': 'Студент направления "Компьютерные системы и сети", 3 курс ,1 семестр ,5 группа',
            'image_url': '../static/image/3.png'
        },
        {
            'id': 4,
            'name': 'Васькин И.С.',
            'group': 'ИУ5-52Б',
            'description': 'Студент направления "Информатика и вычислительная техника", 3 курс ,1 семестр ,2 группа',
            'image_url': '../static/image/4.png'
        },
        {
            'id': 5,
            'name': 'Жуков Ф.М.',
            'group': 'ИУ8-53Б',
            'description': 'Студент направления "Информационная безопасность", 3 курс ,1 семестр ,3 группа',
            'image_url': '../static/image/5.png'
        },
    ]
}


def detailed_service_page(request, id):
    data_by_id = db_services.get('services_to_perform')[id]
    return render(request, 'service_types_detailed.html', {
        'services_to_perform': data_by_id,
    })


def service_page(request):
    query = request.GET.get('q')

    if query:
        # Фильтрую данные, при этом учитываю поле "type"
        filtered_data = [item for item in db_services['services_to_perform'] if
                         query.lower() in item['name'].lower()]

    else:
        filtered_data = db_services['services_to_perform']
        query = ""

    return render(request, "services_types.html", {'filtered_data': filtered_data, 'search_value': query})