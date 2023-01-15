from django.forms import ModelForm

from apps.core.models import Post

class CreatePostForm(ModelForm):
    """Form definition for CreatePost.
        Form for create a post"""

    class Meta:
        """Meta definition for CreatePostform."""

        model = Post
        fields = ('title', 'content')
    
