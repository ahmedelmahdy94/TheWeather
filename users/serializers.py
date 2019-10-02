from .models import *
from rest_framework import serializers
from rest_framework.serializers import (
    EmailField,
    HyperlinkedModelSerializer,
    ModelSerializer,
    ValidationError
    )
from django.contrib.auth.models import User
from django.db.models import Avg, Q
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
    )


User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'email2',
            'password'
        ]
        extra_kwargs = {"password": {"write_only":True} }

    def validate(self, data):
        # email1 = data['email']
        # email_qs = User.objects.filter(email=email1)
        # if email_qs.exists():
        #     raise ValidationError("This email has already been registered")
        return data

    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get("email2")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        email_qs = User.objects.filter(email=email1)
        if email_qs.exists():
            raise ValidationError("This email has already been registered")
        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get("email")
        email2 = value
        if email1 != email2:
            raise ValidationError("Emails must match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        user_obj = User(
            username = username,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data



class UserLoginSerializer(ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(label='Email Address', required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token'
        ]
        extra_kwargs = {"password": {"write_only":True} }

    def validate(self, data):
        user_obj = None
        email = data.get('email',None)
        username = data.get('username',None)
        password = data["password"]

        # email_qs = User.objects.filter(email=email1)
        if not email and not username:
            raise ValidationError("A username or email is required to login")

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise ValidationError("This username or email is not valid")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect Password")
        data["token"] = "SOME RANDOM TOKEN"
        return data
