from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError

from .utils.consts import IL_ZIPCODE_REGEX

# Create your models here.

# Backend models:
# Apartment, Listing, Proposal, Attribute, LikedApartment, Review


class Apartment(models.Model):
    user = models.ForeignKey(
        db_column="user_id",
        to=User,
        on_delete=models.RESTRICT,
        verbose_name="User ID",
    )
    street = models.CharField(
        db_column="street",
        max_length=128,
        validators=[MinLengthValidator(5)],
        verbose_name="Street Name",
    )
    street_num = models.IntegerField(
        db_column="street_num", verbose_name="Street Number"
    )
    apt_num = models.IntegerField(db_column="apt_num", verbose_name="Apartment Number")
    zip_code = models.CharField(
        db_column="zip_code",
        max_length=7,
        validators=[
            RegexValidator(
                regex=IL_ZIPCODE_REGEX,
                message="Zip code must be 7 digits and match the pattern of an Israeli zip code.",
            )
        ],
        verbose_name="Zip Code",
    )
    square_meter = models.IntegerField(
        db_column="square_meter", verbose_name="Square Meter"
    )

    def has_active_listing(self):
        return self.listings.filter(is_active=True).exists()

    class Meta:
        db_table = "apartments"


class Listing(models.Model):
    apt = models.ForeignKey(
        db_column="apt_id",
        to=Apartment,
        on_delete=models.CASCADE,
        related_name="listings",
    )
    title = models.CharField(db_column="title", max_length=128)
    description = models.TextField(db_column="description")
    price = models.DecimalField(db_column="price", max_digits=5, decimal_places=0)
    from_date = models.DateField(db_column="from_date")
    to_date = models.DateField(db_column="to_date")
    duration = models.PositiveIntegerField(
        db_column="duration", null=True, blank=True, default=0
    )
    is_active = models.BooleanField(db_column="is_active", default=False)

    class Meta:
        db_table = "listings"

    def activate(self):
        if self.is_active:
            return
        Listing.objects.filter(pk=self.pk).update(is_active=True)
        self.is_active = True

    def save(self, *args, **kwargs):
        # Convert from_date and to_date to "YYYY-MM-DD" format, which is saveable in DB and Django
        if "/" in self.from_date:
            self.from_date = datetime.strptime(self.from_date, "%d/%m/%Y").strftime(
                "%Y-%m-%d"
            )
        if "/" in self.to_date:
            self.to_date = datetime.strptime(self.to_date, "%d/%m/%Y").strftime(
                "%Y-%m-%d"
            )
        if not self.duration:
            self.duration = (
                datetime.strptime(self.to_date, "%Y-%m-%d")
                - datetime.strptime(self.from_date, "%Y-%m-%d")
            ).days
        # Check if a Listing instance with the same Apartment instance and dates is already present
        if Listing.objects.filter(
            apt=self.apt, from_date=self.from_date, to_date=self.to_date
        ).exists():
            raise ValidationError(
                "You're trying to save an already existant listing object."
            )

        super().save(*args, **kwargs)
