from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator
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