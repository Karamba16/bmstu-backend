from django.db import models


class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    description = models.CharField(max_length=1500, blank=True, null=True)
    image_url = models.CharField(max_length=50, default='../static/images/base.png')
    status = models.CharField(max_length=30, choices=[('0','Ожидает'),('1', 'В работе'), ('2', 'Удален')], default='0')

    def __str__(self):
        return self.last_name + " " + self.first_name[0] +"."


class ApplicationForDeducation(models.Model):
    application_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING, db_column='user')
    date_application_create = models.DateField(blank=True, null=True)
    date_application_accept = models.DateField(blank=True, null=True)
    date_application_complete = models.DateField(blank=True, null=True)
    moderator = models.ForeignKey('User', models.DO_NOTHING, related_name='moderator',blank=True, null=True)
    application_status = models.CharField(max_length=30, choices=[('1', 'Черновик'), ('2', 'Удален'),('3', 'Сформирован')
        ,('4', 'Завершен'),('5', 'Отклонен'),], default='1')  # This field type is a guess.

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=40)
    email = models.CharField(unique=True, max_length=30, blank=True, null=True)
    login = models.CharField(unique=True, max_length=40, blank=True, null=True)
    password = models.CharField(unique=True, max_length=30, blank=True, null=True)
    role = models.BooleanField(default=False)


    """
    class Meta:
        managed = False
        db_table = 'faculty_types'
    """
class ApplicationsStudent(models.Model):
    application = models.OneToOneField(ApplicationForDeducation, models.DO_NOTHING, primary_key=True)  # The composite primary key (application_id, calculation_id) found, that is not supported. The first column is selected.
    student = models.ForeignKey('Student', models.DO_NOTHING)
    result = models.FloatField(blank=True, null=True)

    class Meta:
        unique_together = (('application', 'student'),)
