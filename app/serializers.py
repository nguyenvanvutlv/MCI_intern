from rest_framework import serializers
from app.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_management', 'username_management')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        idm = None
        if validated_data['username_management'] is not None:
            try:
                idm = CustomUser.objects.get(username=validated_data['username_management'])
                idm = CustomUser.objects.filter(username=validated_data['username_management'])
                if idm is not None:
                    idm = idm[0].username
            except Exception as e:
                print("Error: ", e)

        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_management=validated_data['is_management'],
            username_management=validated_data['username_management']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
