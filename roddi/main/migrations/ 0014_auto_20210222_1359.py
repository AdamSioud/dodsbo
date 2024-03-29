# Generated by Django 3.1.6 on 2021-02-22 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0013_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='item_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='main.item'),
        ),
        migrations.AddField(
            model_name='choice',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterModelTable(
            name='choice',
            table='item_choice',
        ),
    ]
