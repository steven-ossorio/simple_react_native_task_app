# Generated by Django 3.0.5 on 2020-05-10 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_tasks_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='completed_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_date',
            field=models.DateField(null=True),
        ),
    ]
