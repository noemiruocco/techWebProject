# Generated by Django 4.1.4 on 2023-01-20 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialPage', '0018_items_remove_categorystorage_category_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='images',
            new_name='image',
        ),
    ]
