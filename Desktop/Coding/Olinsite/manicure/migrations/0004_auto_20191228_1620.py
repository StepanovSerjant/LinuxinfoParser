# Generated by Django 2.2.7 on 2019-12-28 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manicure', '0003_aboutmaster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aboutmaster',
            name='image',
            field=models.ImageField(upload_to='media', verbose_name='Фото'),
        ),
    ]
