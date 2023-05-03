from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User


class UserSerializer(serializers.ModelSerializer):
    model = User
    fields = [
        "id",
        "username",
        "email",
        "password",
        "first_name",
        "last_name",
        "is_seller",
        "is_superuser",
    ]
    read_only_fields = ["id", "is_superuser"]
    write_only_fields = ["password"]
    extra_kwargs = {
        "username": {
            "validators": [
                UniqueValidator(
                    queryset=User.objects.all(),
                    message="A user with that username already exists."
                )
            ]
        },
        "email": {"validators": [
            UniqueValidator(
                queryset=User.objects.all(),
                message="A user with that email already exists."
                )
            ]
        }
    }

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)
    
    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            setattr(instance, key, value)
        password = validated_data.pop("password", None)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
