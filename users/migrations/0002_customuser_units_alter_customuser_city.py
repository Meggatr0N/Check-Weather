# Generated by Django 4.0.3 on 2022-05-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='units',
            field=models.CharField(default='celsius', max_length=150),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(max_length=150),
        ),
    ]
