# Generated by Django 4.1.5 on 2023-02-19 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipy', '0005_recipe_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='defaults/recipe.jpg', upload_to=''),
        ),
    ]
