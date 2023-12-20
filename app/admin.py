from django.contrib import admin
from app.models import *


# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_management')
    list_filter = ('is_management', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'id_project', 'name_project', 'manager', 'start_date_project', 'end_date_project', 'status_project',
        'is_activate')
    list_filter = ('status_project',)
    search_fields = ('name_project',)
    ordering = ('name_project',)


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('id_process', 'name_process', 'start_date_process', 'end_date_process', 'status_process')
    list_filter = ('status_process',)
    search_fields = ('name_process',)
    ordering = ('name_process',)


class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id_task', 'name_task', 'description_task', 'create_date_task', 'start_date_task', 'end_date_task',
        'status_task',
        'is_activate')
    list_filter = ('status_task',)
    search_fields = ('name_task',)
    ordering = ('name_task',)


class AssignProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'start_date_assign_project', 'end_date_assign_project', 'role_assign')
    list_filter = ('role_assign',)
    search_fields = ('user',)
    ordering = ('user',)


class AssignProjectProcessAdmin(admin.ModelAdmin):
    list_display = ('id_assign', 'id_process', 'is_activate')
    list_filter = ('id_assign', 'id_process')
    search_fields = ('id_assign', 'id_process')
    ordering = ('id_assign',)


class DiscussAdmin(admin.ModelAdmin):
    list_display = ('id_discuss', 'create_date_discuss', 'author')
    search_fields = ('author',)
    ordering = ('author',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name_role', 'description_role', 'author', 'project')
    search_fields = ('name_role',)
    ordering = ('name_role',)


class ProjectEditableAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_project', 'is_activate')


class ProcessEditableAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_process', 'is_activate')


class TaskEditableAdmin(admin.ModelAdmin):
    list_display = ('id', 'id_user', 'id_task', 'is_activate')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectEditable, ProjectEditableAdmin)

admin.site.register(Process, ProcessAdmin)
admin.site.register(ProcessEditable, ProcessEditableAdmin)

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskEditable, TaskEditableAdmin)


admin.site.register(AssignProject, AssignProjectAdmin)
admin.site.register(AssignProjectProcess, AssignProjectProcessAdmin)
admin.site.register(Discuss, DiscussAdmin)
