# Generated by Django 3.1.4 on 2020-12-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodlinebot', '0007_auto_20201231_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='ans',
            field=models.JSONField(blank=True, default=[]),
        ),
    ]