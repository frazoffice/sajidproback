# Generated by Django 3.0.2 on 2022-03-10 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220220_0021'),
        ('services', '0019_order_media_file_coordinator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('online_status', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, to='core.User_Profile')),
            ],
        ),
    ]