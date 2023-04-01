# Generated by Django 4.1.7 on 2023-04-01 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_remove_likedapartments_user_profile_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="likedapartments",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="proposal",
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name="attribute",
            name="apt",
            field=models.OneToOneField(
                db_column="apt_id",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="attributes",
                to="api.apartment",
            ),
        ),
        migrations.AddConstraint(
            model_name="likedapartments",
            constraint=models.UniqueConstraint(
                fields=("user", "apartment"), name="unique_user_liked_apartments"
            ),
        ),
        migrations.AddConstraint(
            model_name="proposal",
            constraint=models.UniqueConstraint(
                fields=("sender_user", "apartment"), name="unique_user_proposals"
            ),
        ),
        migrations.AddConstraint(
            model_name="review",
            constraint=models.UniqueConstraint(
                fields=("sender_user", "apartment"), name="unique_user_review"
            ),
        ),
    ]
