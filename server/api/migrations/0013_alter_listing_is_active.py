# Generated by Django 4.1.7 on 2023-04-01 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_apartment_is_deleted"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="is_active",
            field=models.BooleanField(db_column="is_active", default=True),
        ),
    ]