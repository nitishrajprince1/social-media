# Generated by Django 3.2.9 on 2021-12-12 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('welcome', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ('Not Specified', 'not specified')], max_length=50, null=True),
        ),
    ]
