# Generated by Django 5.0.6 on 2024-06-16 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(max_length=1000),
        ),
    ]
