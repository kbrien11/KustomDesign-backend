# Generated by Django 4.0.6 on 2022-09-06 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0016_matchrelationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.CharField(default='default.png', max_length=300),
        ),
    ]
