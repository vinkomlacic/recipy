# Generated by Django 4.1.7 on 2023-02-20 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0007_alter_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
