# Generated by Django 4.1.5 on 2023-02-19 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0006_recipe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='defaults/recipe.jpg', upload_to='uploads/'),
        ),
    ]
