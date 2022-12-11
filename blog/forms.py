from django import forms
from .models import Post

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', )
        
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ingresa un titulo'}), 
            'content': forms.Textarea(attrs={'placeholder': 'Ingresa un contenido'}), 
        }
