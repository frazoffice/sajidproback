# Generated by Django 3.0.2 on 2022-02-22 11:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0009_auto_20220220_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_pages',
            field=models.CharField(default='1', max_length=255),
        ),
        migrations.AlterField(
            model_name='order',
            name='pricing',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='pricing', to='services.Pricing'),
        ),
    ]
