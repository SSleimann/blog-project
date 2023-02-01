from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.core.models import Post
from apps.blog.forms import CreatePostForm

# Create your views here.
@login_required
def index(request):
    queryset = Post.objects.all().order_by('-created_data')
    form = CreatePostForm()
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            post.save()
            messages.add_message(request, messages.SUCCESS, _('Post created!'))
            return HttpResponseRedirect(reverse_lazy('core:blog:index'))
    
    return render(request, 
                  template_name='index.html',
                  context={'posts': queryset, 'form': form}
                  )
    

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    slug_field = "title_slug"
    slug_url_kwarg = "slug"
    template_name = "post_detail.html"

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    slug_field = "title_slug"
    slug_url_kwarg = "slug"
    template_name = 'post_delete.html'
    success_url = reverse_lazy('core:blog:index')
    
    def delete(self, request, *args, **kwargs) :
        super().delete(request, *args, **kwargs)
        return messages.success(request, _('Post deleted!'))
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if obj.author != request.user:
            messages.add_message(request, messages.ERROR, _('You not are the author!'))
            return HttpResponseRedirect(reverse_lazy('core:blog:detail_post', kwargs={'slug': obj.title_slug} ))
        
        return super().dispatch(request, *args, **kwargs)
    
