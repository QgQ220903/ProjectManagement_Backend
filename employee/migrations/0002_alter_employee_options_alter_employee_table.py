# Generated by Django 5.0.12 on 2025-03-19 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employee',
            options={'verbose_name': 'Nhân Viên', 'verbose_name_plural': 'Các nhân viên'},
        ),
        migrations.AlterModelTable(
            name='employee',
            table='employees',
        ),
    ]
