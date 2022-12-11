from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Usuario(models.Model):
    """Model definition for Usuario."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, blank=True, null=True)
    
    def __str__(self):
        """Unicode representation of Usuario."""
        return self.user.username

class Follow(models.Model):
    user_id = models.ForeignKey(Usuario, related_name='following', on_delete=models.CASCADE, blank=True, null=True)
    following_user_id = models.ForeignKey(Usuario, related_name='followers', on_delete=models.CASCADE, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.user_id} follows {self.following_user_id} date: {self.created}'

