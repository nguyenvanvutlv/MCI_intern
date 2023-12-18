from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone


# Create your models here.


class CustomUser(AbstractUser):
    is_management = models.BooleanField(default=False)
    username_validator = UnicodeUsernameValidator()
    username_management = models.CharField(
        _("username_management"),
        max_length=150,
        null=True,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator]
    )

    def __str__(self) -> str:
        return super().__str__()


class Role(models.Model):
    id_role = models.AutoField(primary_key=True, unique=True,
                               verbose_name="ID Role", null=False, blank=False)
    name_role = models.CharField(max_length=50, verbose_name="Name Role",
                                 null=False, blank=False)
    description_role = models.TextField(null=True, blank=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="ID User", related_name="id_user_role")
    is_activate = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.name_role


class Project(models.Model):
    id_project = models.AutoField(primary_key=True, unique=True,
                                  verbose_name="ID Project", null=False, blank=False)
    name_project = models.CharField(max_length=50, verbose_name="Name Project",
                                    null=False, blank=False)
    description_project = models.TextField(null=True, blank=True)
    start_date_project = models.DateField(
        default=timezone.now, verbose_name="Start Date Project")
    end_date_project = models.DateField(
        default=timezone.now, verbose_name="End Date Project")

    choice_status = (
        ("1", "In Progress"),
        ("2", "Completed"),
        ("3", "Pending"),
        ("4", "Cancel"),
    )

    status_project = models.CharField(max_length=1, choices=choice_status, default="1")
    is_activate = models.BooleanField(default=True)

    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Manager", related_name="id_manager")

    def __str__(self) -> str:
        return self.name_project


class AssignProject(models.Model):
    id_assign_project = models.AutoField(primary_key=True, unique=True,
                                         verbose_name="ID Assign Project", null=False, blank=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Project", related_name="id_project_assign")
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Manager", related_name="id_manager_assign")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                             verbose_name="ID User", related_name="id_user_assign")
    start_date_assign_project = models.DateField(
        default=timezone.now, verbose_name="Start Date Assign Project")
    end_date_assign_project = models.DateField(
        default=timezone.now, verbose_name="End Date Assign Project")

    role_assign = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="ID Role", related_name="id_role_assign")

    # lưu ý khi mỗi lần thêm mới 1 bản ghi thì kiểm tra xem user đó có đang tham gia vào 1 project nào đó không
    # nếu có thì không cho thêm mới
    # nếu không thì cho thêm mới

    # 1 người có thể tham gia nhiều dự án

    is_activate = models.BooleanField(default=True)


class Process(models.Model):
    id_process = models.AutoField(primary_key=True, unique=True,
                                  verbose_name="ID Process", null=False, blank=False)
    name_process = models.CharField(max_length=50, verbose_name="Name Process",
                                    null=False, blank=False)
    description_process = models.TextField(null=True, blank=True)
    create_date_process = models.DateField(
        default=timezone.now, verbose_name="Create Date Process")
    start_date_process = models.DateField(
        default=timezone.now, verbose_name="Start Date Process")
    end_date_process = models.DateField(
        default=timezone.now, verbose_name="End Date Process")
    choice_status = (
        ("1", "In Progress"),
        ("2", "Completed"),
        ("3", "Pending"),
        ("4", "Cancel"),
    )
    status_process = models.CharField(max_length=1, choices=choice_status, default="1")
    is_activate = models.BooleanField(default=True)

    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Project", related_name="id_project_process")
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Manager", related_name="id_manager_process")
    root_process = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True,
                                     verbose_name="ID Root Process", related_name="id_root_process")

    rank_process = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name_process


class Discuss(models.Model):
    id_discuss = models.AutoField(primary_key=True, unique=True,
                                  verbose_name="ID Discuss", null=False, blank=False)
    content_discuss = models.TextField(null=True, blank=True)
    create_date_discuss = models.DateField(
        default=timezone.now, verbose_name="Create Date Discuss")
    is_activate = models.BooleanField(default=True)
    is_note = models.BooleanField(default=False)

    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name="ID User", related_name="id_user_discuss")
    process = models.ForeignKey(Process, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Process", related_name="id_process_discuss")
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Manager", related_name="id_manager_discuss")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="ID Project", related_name="id_project_discuss")
