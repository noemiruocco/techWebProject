# Generated by Django 4.1.4 on 2023-01-11 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialPage', '0007_alter_userprofile_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(blank=True, choices=[('ristoratore', 'Ristoratore'), ('cuoco amatoriale', 'Cuoco amatoriale')], max_length=30, null=True),
        ),
    ]