# Generated by Django 3.1.6 on 2021-02-18 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_item_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.ImageField(blank=0, null=True, upload_to=''),
        ),
    ]
