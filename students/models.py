
from django.db import models
from django.conf import settings

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)


class Student(models.Model):

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(120)
        ]
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="students",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
