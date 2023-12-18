from rest_framework import serializers
from app.models import CustomUser, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id_project', 'name_project', 'description_project', 'start_date_project', 'end_date_project', 'manager')

    def create(self, validated_data):
        project = Project(
            name_project=validated_data['name_project'],
            description_project=validated_data['description_project'],
            start_date_project=validated_data['start_date_project'],
            end_date_project=validated_data['end_date_project'],
            manager=validated_data['manager']
        )
        project.save()
        return project

    def update(self, instance, validated_data):
        instance.name_project = validated_data.get('name_project', instance.name_project)
        instance.description_project = validated_data.get('description_project', instance.description_project)
        instance.start_date_project = validated_data.get('start_date_project', instance.start_date_project)
        instance.end_date_project = validated_data.get('end_date_project', instance.end_date_project)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_management', 'username_management')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        idm = None
        if validated_data['username_management'] is not None:
            try:
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
