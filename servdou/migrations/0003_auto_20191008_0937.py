# Generated by Django 2.1.7 on 2019-10-08 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servdou', '0002_chengyu_pos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chengyu',
            name='pos',
            field=models.IntegerField(default=130),
        ),
    ]
