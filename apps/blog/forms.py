from django.forms import ModelForm
from django import forms
from apps.core.models import Post

class CreatePostForm(ModelForm):
    """Form definition for CreatePost.
        Form for create a post"""

    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Título de la publicación'})) 

    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': '¡Deja fluir pensamientos aquí!'})) 

    class Meta:
        """Meta definition for CreatePostform."""

        model = Post
        fields = ('title', 'content')
    
