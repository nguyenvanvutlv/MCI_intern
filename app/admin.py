from django.contrib import admin
from app.models import CustomUser, Project, AssignProject, Discuss, Process, Role


# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_management')
    list_filter = ('is_management', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id_project', 'name_project', 'manager', 'start_date_project', 'end_date_project', 'status_project')
    list_filter = ('status_project',)
    search_fields = ('name_project',)
    ordering = ('name_project',)


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('name_process', 'start_date_process', 'end_date_process', 'status_process')
    list_filter = ('status_process',)
    search_fields = ('name_process',)
    ordering = ('name_process',)


class AssignProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'start_date_assign_project', 'end_date_assign_project', 'role_assign')
    list_filter = ('role_assign',)
    search_fields = ('user',)
    ordering = ('user',)


class DiscussAdmin(admin.ModelAdmin):
    list_display = ('id_discuss', 'create_date_discuss', 'author')
    search_fields = ('author',)
    ordering = ('author',)


class RoleAdmin(admin.ModelAdmin):
    list_display = ('name_role', 'description_role')
    search_fields = ('name_role',)
    ordering = ('name_role',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Process, ProcessAdmin)
admin.site.register(AssignProject, AssignProjectAdmin)
admin.site.register(Discuss, DiscussAdmin)
