# Generated by Django 3.1.6 on 2021-02-18 15:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dodsbo', '0002_dodsbo_members'),
        ('main', '0010_item_dodsbo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='dodsbo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dodsbo.dodsbo'),
        ),
    ]