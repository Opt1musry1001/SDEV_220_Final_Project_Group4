# Generated by Django 3.2.21 on 2023-10-10 22:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('groceryshop', '0010_auto_20231009_1943'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedcart',
            name='created_at',
            field=models.DateTimeField(verbose_name=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='savedcart',
            name='items',
            field=models.ManyToManyField(to='groceryshop.Food'),
        ),
        migrations.AlterField(
            model_name='savedcart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]