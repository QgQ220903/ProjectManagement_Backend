# Generated by Django 5.0.12 on 2025-03-06 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Tên chức năng')),
                ('status', models.BooleanField(default=False, verbose_name='Trạng thái')),
            ],
            options={
                'verbose_name': 'Chức năng',
                'verbose_name_plural': 'Các chức năng',
                'db_table': 'features',
            },
        ),
    ]
