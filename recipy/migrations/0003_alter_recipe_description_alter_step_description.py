# Generated by Django 4.1.5 on 2023-01-27 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0002_alter_step_recipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='step',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
    ]
