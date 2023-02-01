from django.shortcuts import get_object_or_404, HttpResponseRedirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.core.models import Follower

# Create your views here.
@login_required
def follow(request, id):
    current_user = get_object_or_404(get_user_model(), pk=request.user.pk)
    user_to_follow = get_object_or_404(get_user_model(), pk=id)
    
    if user_to_follow != current_user:
        try:
            Follower.objects.get(current_user=current_user, following_user=user_to_follow).delete()
            messages.add_message(request, messages.SUCCESS, _('You have unfollowed @{}!'.format(user_to_follow.get_username())))
            
        except ObjectDoesNotExist:
            Follower.objects.create(current_user=current_user, following_user=user_to_follow)
            messages.add_message(request, messages.SUCCESS, _('You have followed @{}!'.format(user_to_follow.get_username())))
        
    return HttpResponseRedirect(reverse_lazy('core:me:userProfile', kwargs={'id': user_to_follow.id}))

@login_required
def me_profile(request):
    current_user = get_object_or_404(get_user_model(), pk=request.user.pk)
    
    return render(request, 'meprofile.html', context= {'user': current_user})

@login_required
def user_profile(request, id):
    current_user = get_object_or_404(get_user_model(), pk=request.user.pk)
    user = get_object_or_404(get_user_model(), pk=id)
    
    if current_user == user:
        return HttpResponseRedirect(reverse_lazy('core:me:meProfile'))
    
    return render(request, 'userprofile.html', context= {'user': user})
