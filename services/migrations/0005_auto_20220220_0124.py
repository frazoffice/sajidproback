# Generated by Django 3.0.2 on 2022-02-20 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_auto_20220220_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper_type',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='services_level',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='services_type',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
