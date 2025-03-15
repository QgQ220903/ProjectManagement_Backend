# Generated by Django 5.0.12 on 2025-03-07 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employeeID', models.IntegerField(verbose_name='Mã nhân viên')),
                ('departmentID', models.IntegerField(verbose_name='Mã phòng ban')),
                ('positionName', models.CharField(max_length=255, verbose_name='Tên chức vụ')),
                ('employeeName', models.CharField(max_length=255, verbose_name='Tên nhân viên')),
                ('employeePhone', models.CharField(max_length=255, verbose_name='Số điện thoại')),
                ('employeeEmail', models.CharField(max_length=255, verbose_name='Email')),
                ('status', models.BooleanField(default=True, verbose_name='Trạng thái')),
            ],
        ),
    ]
