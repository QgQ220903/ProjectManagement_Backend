# Generated by Django 5.0.12 on 2025-03-19 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_assignment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskassignment',
            options={'verbose_name': 'Phân Công'},
        ),
        migrations.AlterModelTable(
            name='taskassignment',
            table='task_assignments',
        ),
    ]
