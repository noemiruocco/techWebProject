# Generated by Django 4.1.4 on 2023-01-17 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialPage', '0010_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='uploads/post_photos')),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ManyToManyField(blank=True, to='socialPage.image'),
        ),
    ]
