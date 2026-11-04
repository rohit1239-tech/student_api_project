
from rest_framework import serializers

from .models import Student


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student

        fields = [
            "id",
            "name",
            "email",
            "age",
            "owner",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "owner",
            "created_at",
            "updated_at",
        ]

    def validate_name(self, value):

        if not value.strip():
            raise serializers.ValidationError(
                "Name cannot be empty."
            )

        return value.strip()

    def validate_age(self, value):

        if value < 1 or value > 120:
            raise serializers.ValidationError(
                "Age must be between 1 and 120."
            )

        return value
