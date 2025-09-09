from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Add your extra fields here

    def __str__(self):
        return self.username
