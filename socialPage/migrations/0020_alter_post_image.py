# Generated by Django 4.1.4 on 2023-01-20 15:43

from django.db import migrations, models
import socialPage.models


class Migration(migrations.Migration):

    dependencies = [
        ('socialPage', '0019_rename_images_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/post_photos'),
        ),
    ]