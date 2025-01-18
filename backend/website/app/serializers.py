from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
import re

allowed_user_output = ['id', 'last_login', 'is_superuser', 'username', 'first_name',
                       'last_name', 'email', 'is_staff', 'is_active', 'date_joined']


# Model Serializers
class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class UserTasksSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = allowed_user_output + ['tasks']


# Functional Serializers
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = allowed_user_output + ['password']

    def validate_username(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                "Username must be at least 5 characters long.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long.")
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
                "Password must contain at least one number.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists.")
        return value

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "New password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "New password must contain at least one number")
        return value


# Request Data Serializers
class UserTypeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(required=True, choices=[
                                   'default', 'user_tasks'])


class SortBySerializer(serializers.Serializer):
    sort_type = serializers.ChoiceField(choices=['asc', 'desc'], required=True)
    sort_by = serializers.ChoiceField(choices=[
                                      'title', 'due_date', 'completed', 'created_at', 'updated_at'], required=True)


class PaginationSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=True, min_value=1)
    page_size = serializers.IntegerField(
        required=True, min_value=1, max_value=100)
