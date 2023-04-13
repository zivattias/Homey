# Generated by Django 4.1.7 on 2023-04-10 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0016_apartment_created_apartment_modified_listing_created_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="ApartmentPhoto",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("photo_url", models.URLField()),
                (
                    "apt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="photos",
                        to="api.apartment",
                    ),
                ),
            ],
            options={
                "db_table": "apartment_photos",
            },
        ),
        migrations.AddConstraint(
            model_name="apartmentphoto",
            constraint=models.UniqueConstraint(
                fields=("apt", "photo_url"), name="unique_apartment_id_photos"
            ),
        ),
    ]