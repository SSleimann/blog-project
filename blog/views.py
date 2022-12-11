from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from login.models import Usuario

from .forms import PostCreationForm
from .models import Post

# Create your views here.
class CreatePost(LoginRequiredMixin, CreateView):
    template_name = 'createpost.html'
    form_class = PostCreationForm
    
    def form_valid(self, form):
        user = get_object_or_404(Usuario, user=self.request.user)
        
        form.instance.author = user
        return super(CreatePost, self).form_valid(form)
    
class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name='detailview.html'
    
@login_required
def post_detail(request, slug):
     return render(request, 'index2.html')

@login_required
def delete_post(request, slug):
    user = get_object_or_404(Usuario, user=request.user)
    
    try:
        Post.objects.get(slug=slug, author=user).delete()
    except Post.DoesNotExist:
        messages.error(request, 'Este Post no existe.')
    
    return redirect('profile')
