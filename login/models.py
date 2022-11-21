from django.db import models
from  django.contrib.auth.models import User

# Create your models here.
class Usuario(models.Model):
    """Model definition for Usuario."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        """Unicode representation of Usuario."""
        return self.user.username
