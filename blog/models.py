from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

from login.models import Usuario

from .utils import unique_slugify

# Create your models here.
class Post(models.Model):
    """Model definition for MODELNAME."""

    # TODO: Define fields here
    author = models.ForeignKey(Usuario, related_name='blog_posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    content = models.TextField(max_length=500)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        """Unicode representation of MODELNAME."""
        return f'Title: {self.title}. Author: {self.author}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_str = "%s %s %s" % (self.title, self.author.user.username, self.author.user.pk) 
            unique_slugify(self, slug_str)
        super(Post, self).save(*args, **kwargs) # Call the real save() method
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})
    
    class Meta:
        ordering = ('-created_at', )

