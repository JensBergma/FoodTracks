from django.db import models
from rest_framework.exceptions import ValidationError

class Address(models.Model):
    """
    Model representing an address.
    """
    street = models.CharField(max_length=100, help_text="The street name.")
    houseNumber = models.CharField(max_length=10, help_text="The house or building number.")
    location = models.CharField(max_length=100, help_text="The city or town name.")
    postcode = models.CharField(max_length=10, help_text="The postal code or ZIP code.")

    class Meta:
        unique_together = (("street", "houseNumber", "location", "postcode"))

    def __str__(self):
        return "{} {}, {} {}".format(self.street, self.houseNumber, self.location, self.postcode)

class OpeningHours(models.Model):
    """
    Model representing the opening hours of a store.
    """
    DaysOfWeek = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday'),
    )
    dayOfWeek = models.IntegerField(choices=DaysOfWeek, help_text="The day of the week.")
    openingTime = models.TimeField(help_text="The time the store opens.")
    closingTime = models.TimeField(help_text="The time the store closes.")
    isClosed = models.BooleanField(default=False, help_text="Whether the store is closed on this day.")
    isSpecialTime = models.BooleanField(default=False, help_text="Whether this is a special opening time, such as a holiday.")

    def __str__(self):
        return "{} - {}-{} {}".format(self.dayOfWeek, self.openingTime, self.closingTime, self.isSpecialTime)

    class Meta:
        unique_together = (("dayOfWeek", "openingTime", "closingTime", "isClosed", "isSpecialTime"))

    def clean(self):
        super().clean()
        if self.closingTime <= self.openingTime:
            raise ValidationError("Closing time must be after opening time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Store(models.Model):
    """
    Model representing a store.
    """
    name = models.CharField(max_length=150, help_text="The name of the store.")
    address = models.ManyToManyField(Address, help_text="The address of the store.")
    openingHours = models.ManyToManyField(OpeningHours, help_text="The opening hours of the store.")

    def __str__(self):
        return self.name
