# Generated by Django 4.2.2 on 2024-06-10 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="token",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="Токен"
            ),
        ),
    ]
