from rest_framework import serializers
from app.models import (
    CustomUser, Project, Process, AssignProject, Role, AssignProjectProcess, Discuss,
    ProcessEditable, TaskEditable, Task, ProjectEditable
)


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
        fields = ('username', 'password', 'email', 'first_name', 'last_name', 'is_management')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_management=validated_data['is_management']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = (
            'id_process','name_process', 'description_process', 'start_date_process', 'end_date_process', 'project', 'manager',
            'root_process',
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


class AssignProjectProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignProjectProcess
        fields = (
            'id_assign', 'id_process')

    def create(self, validated_data):
        assign_project_process = AssignProjectProcess(
            id_assign=validated_data['id_assign'],
            id_process=validated_data['id_process']
        )
        assign_project_process.save()
        return assign_project_process

    def update(self, instance, validated_data):
        instance.id_assign = validated_data.get('id_assign', instance.id_assign)
        instance.id_process = validated_data.get('id_process', instance.id_process)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = (
            'id_role', 'name_role', 'description_role', 'author', 'project', 'is_activate')

    def create(self, validated_data):
        role = Role(
            name_role=validated_data['name_role'],
            description_role=validated_data['description_role'],
            author=validated_data['author'],
            project=validated_data['project']
        )
        role.save()
        return role

    def update(self, instance, validated_data):
        instance.name_role = validated_data.get('name_role', instance.name_role)
        instance.description_role = validated_data.get('description_role', instance.description_role)
        instance.is_activate = validated_data.get('is_activate', instance.is_activate)
        instance.save()
        return instance

    def delete(self, instance, *args, **kwargs):
        instance.is_activate = False
        instance.save()
        return instance


class ProjectEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectEditable
        fields = (
            'id', 'id_user', 'id_project', 'is_activate')

    def create(self, validated_data):
        project_edit = ProjectEditable(
            id_user=validated_data['id_user'],
            id_project=validated_data['id_project']
        )
        project_edit.save()
        return project_edit

    def update(self, instance, validated_data):
        instance.id_user = validated_data.get('id_user', instance.id_user)
        instance.id_project = validated_data.get('id_project', instance.id_project)
        instance.save()
        return instance

    def delete(self, instance, *args, **kwargs):
        instance.is_activate = False
        instance.save()
        return instance


class ProcessEditableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessEditable
        fields = ( 'id', 'id_user', 'id_process')

    def create(self, validated_data):
        process_editable = ProcessEditable(
            id_user=validated_data['id_user'],
            id_process=validated_data['id_process']
        )
        process_editable.save()
        return process_editable

    def update(self, instance, validated_data):
        instance.id_user = validated_data.get('id_user', instance.id_user)
        instance.id_process = validated_data.get('id_process', instance.id_process)
        instance.save()
        return instance

    def delete(self, instance, *args, **kwargs):
        instance.is_activate = False
        instance.save()
        return instance


class TaskEditableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskEditable
        fields = (
            'id', 'id_user', 'id_task', 'is_activate')

    def create(self, validated_data):
        task_editable = TaskEditable(
            id_user=validated_data['id_user'],
            id_task=validated_data['id_task']
        )
        task_editable.save()
        return task_editable

    def update(self, instance, validated_data):
        instance.id_user = validated_data.get('id_user', instance.id_user)
        instance.id_task = validated_data.get('id_task', instance.id_task)
        instance.save()
        return instance

    def delete(self, instance, *args, **kwargs):
        instance.is_activate = False
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id_task', 'name_task', 'description_task', 'create_date_task', 'status_task',
            'start_date_task', 'end_date_task', 'project', 'manager', 'process', 'rank_task')

    def create(self, validated_data):
        task = Task(
            name_task=validated_data['name_task'],
            description_task=validated_data['description_task'],
            create_date_task=validated_data['create_date_task'],
            start_date_task=validated_data['start_date_task'],
            end_date_task=validated_data['end_date_task'],
            project=validated_data['project'],
            process=validated_data['process'],
            manager=validated_data['manager'],
            rank_task=validated_data['rank_task']
        )
        task.save()
        return task

    def update(self, instance, validated_data):
        instance.name_task = validated_data.get('name_task', instance.name_task)
        instance.description_task = validated_data.get('description_task', instance.description_task)
        instance.create_date_task = validated_data.get('create_date_task', instance.create_date_task)
        instance.status_task = validated_data.get('status_task', instance.status_task)
        instance.start_date_task = validated_data.get('start_date_task', instance.start_date_task)
        instance.end_date_task = validated_data.get('end_date_task', instance.end_date_task)
        instance.project = validated_data.get('project', instance.project)
        instance.process = validated_data.get('process', instance.process)
        instance.manager = validated_data.get('manager', instance.manager)
        instance.rank_task = validated_data.get('rank_task', instance.rank_task)
        instance.save()
        return instance
