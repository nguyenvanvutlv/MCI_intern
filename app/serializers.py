from rest_framework import serializers
from app.models import CustomUser, Project, Process, AssignProject, Role, AssignProjectProcess, Discuss


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = (
            'id_project', 'name_project', 'description_project', 'start_date_project', 'end_date_project', 'manager')

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

    def update(self, instance, validated_data, *args, **kwargs):
        """
           cập nhật thêm is_activate
        """
        instance.name_project = validated_data.get('name_project', instance.name_project)
        instance.description_project = validated_data.get('description_project', instance.description_project)
        instance.start_date_project = validated_data.get('start_date_project', instance.start_date_project)
        instance.end_date_project = validated_data.get('end_date_project', instance.end_date_project)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.save()
        return instance

    def delete(self, instance, *args, **kwargs):
        instance.is_activate = False
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


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = (
            'name_process', 'description_process', 'start_date_process', 'end_date_process', 'project', 'manager', 'root_process',
            'rank_process')

    def create(self, validated_data):
        process = Process(
            name_process=validated_data['name_process'],
            description_process=validated_data['description_process'],
            start_date_process=validated_data['start_date_process'],
            end_date_process=validated_data['end_date_process'],
            project=validated_data['project'],
            manager=validated_data['manager'],
            root_process=validated_data['root_process'],
            rank_process=validated_data['rank_process']
        )
        process.save()
        return process

    def update(self, instance, validated_data):
        instance.name_process = validated_data.get('name_process', instance.name_process)
        instance.description_process = validated_data.get('description_process', instance.description_process)
        instance.start_date_process = validated_data.get('start_date_process', instance.start_date_process)
        instance.end_date_process = validated_data.get('end_date_process', instance.end_date_process)
        instance.status_process = validated_data.get('status_process', instance.status_process)
        instance.project = validated_data.get('project', instance.project)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.root_process = validated_data.get('root_process', instance.root_process)
        instance.rank_process = validated_data.get('rank_process', instance.rank_process)
        instance.save()
        return instance


class AssignProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignProject
        fields = (
            'project', 'user', 'start_date_assign_project', 'end_date_assign_project', 'role_assign')

    def create(self, validated_data):
        assign_project = AssignProject(
            project=validated_data['project'],
            user=validated_data['user'],
            start_date_assign_project=validated_data['start_date_assign_project'],
            end_date_assign_project=validated_data['end_date_assign_project'],
            role_assign=validated_data['role_assign']
        )
        assign_project.save()
        return assign_project

    def update(self, instance, validated_data):
        instance.project = validated_data.get('project', instance.project)
        instance.user = validated_data.get('user', instance.user)
        instance.start_date_assign_project = validated_data.get('start_date_assign_project',
                                                                instance.start_date_assign_project)
        instance.end_date_assign_project = validated_data.get('end_date_assign_project',
                                                              instance.end_date_assign_project)
        instance.role_assign = validated_data.get('role_assign', instance.role_assign)
        instance.save()
        return instance