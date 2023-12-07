from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import UniqueConstraint


class Profile(AbstractUser):
    registered_at = models.DateTimeField(auto_now_add=True)
    agreement_accept = models.BooleanField(default=False)
    phone = models.CharField(max_length=14, unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    cart = models.IntegerField(null=True, blank=True)
    archived = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    # Заменяем поле имени пользователя на электронную почту для аутентификации
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # 'username' требуется по умолчанию

    # обеспечиваем уникальность электронной почты.
    # class Meta:
    #     UniqueConstraint(fields=['email', 'username'], name='unique_fields')
