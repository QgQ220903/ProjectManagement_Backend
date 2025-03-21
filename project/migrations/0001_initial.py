# Generated by Django 5.0.12 on 2025-02-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Tên dự án')),
                ('isDeleted', models.BooleanField(default=False, verbose_name='Đã xóa')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')),
            ],
            options={
                'verbose_name': 'Dự án',
                'verbose_name_plural': 'Các dự án',
                'db_table': 'projects',
            },
        ),
    ]
