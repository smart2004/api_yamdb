from django.db import models
from django.contrib.auth.models import AbstractUser
from reviews.validators import validate_username

# Create your models here.

class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]

    username = models.CharField(
        max_length=150, unique=True, null=True,
        validators=(validate_username,))
    email = models.EmailField(
        max_length=254, unique=True)
    first_name = models.TextField(
        max_length=150, null=True, blank=True)
    last_name = models.TextField(
        max_length=150, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        choices=ROLES, default=USER, max_length=20)
    confirmation_code = models.CharField(
        max_length=20, blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR   

    @property
    def is_admin(self):
        return self.role == self.ADMIN
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']

        constraints = [
            models.CheckConstraint(
                check=~models.Q(username__iexact="me"),
                name="username_is_not_me"
            )
        ]