# Generated by Django 4.0.5 on 2022-07-09 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_category_image_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(null=True, upload_to='maincategory'),
        ),
    ]