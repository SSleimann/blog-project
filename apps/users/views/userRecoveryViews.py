from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import FormView, TemplateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, BadHeaderError

from apps.users.forms import userRecoveryForms

#Class views
class UserPassRecoveryView(FormView):
    ''' Send an email to the user to confirm the password change '''
    
    template_name = 'password_recovery.html'
    form_class = userRecoveryForms.RecoveryPassword
    success_url = reverse_lazy('core:users:password_recovery_ready')

    def form_valid(self, form):
        credentials = form.cleaned_data
        email = credentials.get('email')
        user = get_user_model().objects.filter(email=email)
        
        if user.exists():
            for u in user:
                email_subject = "Password Reset Requested"
                email = render_to_string('password/password_reset_email.txt', {
                    'user': u.username,
                    'domain': get_current_site(self.request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                    'token': default_token_generator.make_token(u),
                    'protocol': 'https' if self.request.is_secure() else 'http'
                    })
                
                try:
                    send_mail(email_subject, email, 'sleimanjose23@gmail.com' , [u.email], fail_silently=False)
                
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
            
        
        return super().form_valid(form)
    
class UserPassRecoveryConfirmView(FormView):
    ''' Show the form and if it is valid change the password if it is not valid, send an error '''
    
    template_name = 'password_recovery_conf.html'
    template_name_fail =  'password_recovery_failed.html'
    success_url = reverse_lazy('core:users:user_login')
    form_class = userRecoveryForms.UserSetPasswordForm
    token_generator = default_token_generator
     
    def dispatch(self, request, *args, **kwargs):
        self.user = self.get_user(kwargs['uidb64'])
        
        if self.user is not None:
            token = kwargs['token']
            
            if self.token_generator.check_token(self.user, token):
                return super().dispatch(request, *args, **kwargs)
                
        return render(self.request, self.template_name_fail)
    
    def get_user(self, uidb64):
        userModel = get_user_model()
        
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = userModel.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, userModel.DoesNotExist, ValidationError,):
            user = None
            
        return user
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        
        return kwargs
    
    def form_valid(self, form):
        saved = form.save()
        
        if saved:
            messages.success(self.request, _('You have changed your password succesful'))
            
        return super().form_valid(form)
    
class UserPassRecoveryReadyView(TemplateView):
    ''' This view is the message that the mail has been sent successfully '''
    
    template_name = 'password_recovery_ready.html'

