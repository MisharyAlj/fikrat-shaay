from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import CustomUser


##### Testing this code #####
class UserLoginSerializer(serializers.Serializer):
    nationality_id = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id', 'nationality_id', 'first_name', 'last_name', 'phone', 'email',
            'occupation', 'salary', 'password',
            'is_superuser', 'is_staff', 'is_active',
            'groups', 'user_permissions',
            'last_login', 'date_joined']
        read_only_fields = ('last_login', 'date_joined', 'groups', 'user_permissions',
                            'is_superuser', 'is_staff', 'is_active')

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_superuser:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this Action."})

        user = CustomUser(first_name=validated_data['first_name'],
                          last_name=validated_data['last_name'],
                          email=validated_data['email'],
                          nationality_id=validated_data['nationality_id'],
                          phone=validated_data['phone'],
                          occupation=validated_data['occupation'],
                          salary=validated_data['salary'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        # MANIPULATE DATA HERE BEFORE INSERTION
        user = self.context['request'].user
        if user.nationality_id != instance.nationality_id and not user.is_superuser:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.nationality_id = validated_data['nationality_id']
        instance.email = validated_data['email']
        instance.phone = validated_data['phone']
        instance.occupation = validated_data['occupation']
        instance.salary = validated_data['salary']
        instance.set_password(validated_data['password'])
        instance.save()
        # ADD CODE HERE THAT YOU WANT TO VIEW
        return instance


class EmptySerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                'Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value
