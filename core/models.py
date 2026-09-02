from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    mobile = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    studio = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )
    movies_per_year = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Role(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_roles'
    )

    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='user_roles'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'role'],
                name='unique_user_role'
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"