# Generated by Django 4.2.5 on 2023-09-25 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='robot',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
