# Generated by Django 4.2.7 on 2023-12-20 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('student_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=1500, null=True)),
                ('image_url', models.CharField(default='../static/images/base.png', max_length=50)),
                ('status', models.CharField(choices=[('0', 'Ожидает'), ('1', 'В работе'), ('2', 'Удален')], default='0', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=40)),
                ('email', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('login', models.CharField(blank=True, max_length=40, null=True, unique=True)),
                ('password', models.CharField(blank=True, max_length=30, null=True, unique=True)),
                ('role', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationForDeducation',
            fields=[
                ('application_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_application_create', models.DateField(blank=True, null=True)),
                ('date_application_accept', models.DateField(blank=True, null=True)),
                ('date_application_complete', models.DateField(blank=True, null=True)),
                ('application_status', models.CharField(choices=[('1', 'Черновик'), ('2', 'Удален'), ('3', 'Сформирован'), ('4', 'Завершен'), ('5', 'Отклонен')], default='1', max_length=30)),
                ('moderator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='moderator', to='app.user')),
                ('user', models.ForeignKey(db_column='user', on_delete=django.db.models.deletion.DO_NOTHING, to='app.user')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationsStudent',
            fields=[
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='app.applicationfordeducation')),
                ('result', models.FloatField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='app.student')),
            ],
            options={
                'unique_together': {('application', 'student')},
            },
        ),
    ]
