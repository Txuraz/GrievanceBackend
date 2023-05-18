from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'last_login': {'write_only': True},
            'is_superuser': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'is_staff': {'write_only': True},
            'is_active': {'write_only': True},
            'date_joined': {'write_only': True},
            'groups': {'write_only': True},
            'password': {'write_only': True},
            'user_permissions': {'write_only': True},

        }

    # Password is Converted into Hash
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
