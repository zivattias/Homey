# Generated by Django 4.1.7 on 2023-04-01 08:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0008_alter_listing_from_date_alter_listing_to_date"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="likedapartments",
            name="user_profile",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="liked_apartments",
        ),
    ]
