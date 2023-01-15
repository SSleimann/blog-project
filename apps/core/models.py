from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

from apps.core.utils import unique_slugify

import typing as t

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        
        if not email:
            raise ValueError(_("You need an email!"))
        if not username:
            raise ValueError(_("You need an username!"))
        if not password:
            raise ValueError(_("You need an password!"))
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        
        user.is_superuser = True
        user.is_staff = True
        
        user.save(using=self._db)
        
        return user

class User(PermissionsMixin, AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator]
    )
    
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    
    email = models.EmailField(_("email address"), unique=True)
    
    bio = models.CharField(_('biography'), max_length=250, blank=True)
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
    
class Follower(models.Model):
    """Model definition for Follower."""

    # TODO: Define fields here
    current_user = models.ForeignKey("User", verbose_name=_("current user"), on_delete=models.CASCADE, related_name='following')
    following_user = models.ForeignKey("User", verbose_name=_("following user"), on_delete=models.CASCADE, related_name='followers')
    
    class Meta:
        """Meta definition for Follower."""

        verbose_name = _('Follower')
        verbose_name_plural = _('Followers')

    def __str__(self):
        """Unicode representation of Follower."""
        return f'{self.current_user} following {self.following_user}'

class Post(models.Model):
    """Model definition for Post."""

    # TODO: Define fields here
    author = models.ForeignKey("User", verbose_name=_("author"), related_name='blog_posts', on_delete=models.CASCADE)
    title = models.CharField(_("title"), max_length=50)
    title_slug = models.SlugField(_("slug"), unique=True)
    content = models.TextField(_("content"), max_length=250)
    
    created_data = models.DateTimeField(_("date joined"), default=timezone.now)
    
    class Meta:
        """Meta definition for Post."""

        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return f'Title: {self.title}, creator: {self.author}'
    
    def save(self, *args, **kwargs):
        if not self.title_slug:
           slug_str = "%s %s %s" % (self.title, self.author.pk, self.author.username) 
           unique_slugify(self, slug_str, slug_field_name='title_slug')
        
        return super(Post, self).save(*args, **kwargs)
    
