from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserManager(UserManager):
    """Custom user manager to override case-sensitive username checks."""
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

class CustomUser(AbstractUser):
    """Custom user model."""
    objects = CustomUserManager()
    email = models.EmailField(unique=True, max_length=30)
    phone = models.CharField(null=True, blank=True, max_length=20, verbose_name='Phone number')
    image = models.ImageField(default='user_images/default.jpg', upload_to="user_images")

    def __str__(self):
        return self.username